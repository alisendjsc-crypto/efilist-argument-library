#!/usr/bin/env python3
"""anthropocentrism_ledger_validator v0.1

Validates anthropocentrism_grading_ledger.json (v0.1.6+). Checks, per cell:
  1. band-true      : stored grade letter == band(recomputed unrounded geomean)
  2. display        : stored rsi_pct       == round(geomean*100, 1)
  3. boundary       : stored `boundary`    == (dist_to_nearest_band_line <= policy.epsilon)
Plus ledger-level:
  4. manifest       : boundary_policy.flagged_cells == recomputed boundary set
  5. counts         : count_boundary_cells / count_total_cells correct
  6. policy shape    : epsilon, band_lines, register, scope_note present

Epsilon and band lines are read FROM boundary_policy (validates against the
declared policy, not a hardcode). Depth modifiers are the flagship inheritance.

Usage:  python3 anthropocentrism_ledger_validator_v0_1.py [path-to-ledger.json]
Exit 0 = PASS, non-zero = FAIL.
"""
import json, sys

MODS = {"long": (0.0, 0.0), "medium": (-0.05, -0.03), "short": (-0.12, -0.06)}
DEPTHS = ("short", "medium", "long")


def geomean(ax):
    p = 1.0
    for k in ("v", "s", "c", "r", "a"):
        p *= ax[k]
    return p ** 0.2


def depth_axes(ax, depth):
    dc, dr = MODS[depth]
    a = dict(ax)
    a["c"] = round(a["c"] + dc, 10)
    a["r"] = round(a["r"] + dr, 10)
    return a


def band(gm):
    return "A" if gm >= 0.88 else "B" if gm >= 0.82 else "C" if gm >= 0.76 else "D"


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "anthropocentrism_grading_ledger.json"
    d = json.load(open(path))
    fails = []

    pol = d.get("boundary_policy")
    if not pol:
        print("FAIL: no boundary_policy block"); sys.exit(2)
    eps = pol["epsilon"]
    lines = pol["band_lines"]
    for k in ("register", "scope_note", "epsilon", "band_lines"):
        if k not in pol:
            fails.append(f"policy: missing `{k}`")

    def nearest(gm):
        L = min(lines, key=lambda x: abs(gm - x))
        return L, abs(gm - L)

    recomputed = []
    for nid, g in d["grades"].items():
        for depth in DEPTHS:
            cell = g[depth]
            gm = geomean(depth_axes(g["axes"], depth))
            # 1 band-true
            if band(gm) != cell["grade"]:
                fails.append(f"band-true {nid}/{depth}: stored {cell['grade']} != {band(gm)} (gm={gm:.6f})")
            # 2 display
            disp = round(gm * 100, 1)
            if abs(disp - cell["rsi_pct"]) > 1e-9:
                fails.append(f"display {nid}/{depth}: stored {cell['rsi_pct']} != {disp}")
            # 3 boundary
            _, dist = nearest(gm)
            want = dist <= eps
            if "boundary" not in cell:
                fails.append(f"boundary {nid}/{depth}: field absent")
            elif cell["boundary"] != want:
                fails.append(f"boundary {nid}/{depth}: stored {cell['boundary']} != {want} (dist={dist:.6f}, eps={eps})")
            if want:
                recomputed.append((nid, depth))

    # 4 manifest matches recomputed set
    man = {(m["objection"], m["depth"]) for m in pol.get("flagged_cells", [])}
    if man != set(recomputed):
        fails.append(f"manifest mismatch: policy={sorted(man)} recomputed={sorted(recomputed)}")

    # 5 counts
    total = len(d["grades"]) * 3
    if pol.get("count_total_cells") != total:
        fails.append(f"count_total_cells {pol.get('count_total_cells')} != {total}")
    if pol.get("count_boundary_cells") != len(recomputed):
        fails.append(f"count_boundary_cells {pol.get('count_boundary_cells')} != {len(recomputed)}")

    if fails:
        print(f"FAIL ({len(fails)}):")
        for f in fails:
            print("  -", f)
        sys.exit(1)
    print(f"PASS  ledger v{d['version']}  |  {len(recomputed)}/{total} boundary cells @ eps={eps}  |  band-true + display + boundary + manifest + counts OK")


main()

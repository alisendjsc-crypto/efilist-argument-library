#!/usr/bin/env python3
"""anthropocentrism_ledger_validator v0.2

Supersedes v0.1 (4a555ce8). Validates anthropocentrism_grading_ledger.json
(v0.1.7+). Inherits every v0.1 grading/boundary check, unchanged:

  per cell   1. band-true : stored grade == band(recomputed unrounded geomean)
             2. display   : stored rsi_pct == round(geomean*100, 1)
             3. boundary  : stored `boundary` == (dist_to_nearest_band_line <= eps)
  ledger     4. manifest  : boundary_policy.flagged_cells == recomputed boundary set
             5. counts    : count_boundary_cells / count_total_cells correct
             6. policy    : epsilon, band_lines, register, scope_note present

NEW in v0.2 (routing lattice, node-level — K193):
  per node   7. routes_to shape : `routes_to` is a list; each edge has str `horn`,
                                   and `to` is str|null. Non-null `to` resolves to a
                                   real node id and is not a self-edge. Null `to`
                                   carries `terminus_kind` in the allowed set;
                                   non-null `to` carries no `terminus_kind`.
             8. terminus bool    : `terminus_contested` is a bool.
             9. consistency gate : terminus_contested ==
                                    any(edge.terminus_kind == 'contested'
                                        for edge in routes_to if edge.to is None)
                                    -- the bool cannot drift from the edge set.

Rationale for the gate (K193 design call): terminus_contested is derivable from
the edge set's terminus_kinds, so it is stored AND gated rather than dropped --
the game may consume the bool directly with a guarantee it agrees with the edges.
It is NOT derivable from cell-level `boundary` (grading-proximity): the sets do
not coincide (privilege-tracks-a-capacity is a boundary node yet not a contested
terminus), so the two fields are stored independently and respond to different
mutations (regrade vs re-author).

Usage:  python3 anthropocentrism_ledger_validator_v0_2.py [path-to-ledger.json]
Exit 0 = PASS, non-zero = FAIL.
"""
import json, sys

MODS = {"long": (0.0, 0.0), "medium": (-0.05, -0.03), "short": (-0.12, -0.06)}
DEPTHS = ("short", "medium", "long")
TERMINUS_KINDS = ("contested", "clean_dissolve", "firebreak_out_of_scope")


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

    node_ids = set(d["grades"].keys())
    recomputed = []

    for nid, g in d["grades"].items():
        # ---- v0.1 grading + boundary (per cell) --------------------------
        for depth in DEPTHS:
            cell = g[depth]
            gm = geomean(depth_axes(g["axes"], depth))
            if band(gm) != cell["grade"]:
                fails.append(f"band-true {nid}/{depth}: stored {cell['grade']} != {band(gm)} (gm={gm:.6f})")
            disp = round(gm * 100, 1)
            if abs(disp - cell["rsi_pct"]) > 1e-9:
                fails.append(f"display {nid}/{depth}: stored {cell['rsi_pct']} != {disp}")
            _, dist = nearest(gm)
            want = dist <= eps
            if "boundary" not in cell:
                fails.append(f"boundary {nid}/{depth}: field absent")
            elif cell["boundary"] != want:
                fails.append(f"boundary {nid}/{depth}: stored {cell['boundary']} != {want} (dist={dist:.6f}, eps={eps})")
            if want:
                recomputed.append((nid, depth))

        # ---- v0.2 routing lattice (per node) -----------------------------
        if "routes_to" not in g:
            fails.append(f"routing {nid}: `routes_to` absent"); continue
        edges = g["routes_to"]
        if not isinstance(edges, list):
            fails.append(f"routing {nid}: `routes_to` not a list"); continue
        if "terminus_contested" not in g:
            fails.append(f"routing {nid}: `terminus_contested` absent")
        elif not isinstance(g["terminus_contested"], bool):
            fails.append(f"routing {nid}: `terminus_contested` not a bool")

        contested_seen = False
        for i, e in enumerate(edges):
            tag = f"{nid}/edge[{i}]"
            if not isinstance(e.get("horn"), str) or not e["horn"].strip():
                fails.append(f"routing {tag}: missing/empty `horn`")
            to = e.get("to", "__missing__")
            if to == "__missing__":
                fails.append(f"routing {tag}: `to` absent"); continue
            if to is None:
                tk = e.get("terminus_kind")
                if tk not in TERMINUS_KINDS:
                    fails.append(f"routing {tag}: null `to` needs terminus_kind in {TERMINUS_KINDS}, got {tk!r}")
                if tk == "contested":
                    contested_seen = True
            else:
                if not isinstance(to, str) or to not in node_ids:
                    fails.append(f"routing {tag}: `to`={to!r} does not resolve to a node id")
                if to == nid:
                    fails.append(f"routing {tag}: self-edge (`to`==`{nid}`) not permitted")
                if "terminus_kind" in e:
                    fails.append(f"routing {tag}: non-null `to` must not carry terminus_kind")

        # consistency gate
        tc = g.get("terminus_contested")
        if isinstance(tc, bool) and tc != contested_seen:
            fails.append(f"routing {nid}: terminus_contested={tc} != derived {contested_seen} (contested-edge presence)")

    # ---- v0.1 ledger-level -----------------------------------------------
    man = {(m["objection"], m["depth"]) for m in pol.get("flagged_cells", [])}
    if man != set(recomputed):
        fails.append(f"manifest mismatch: policy={sorted(man)} recomputed={sorted(recomputed)}")
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

    n_edges = sum(len(g["routes_to"]) for g in d["grades"].values())
    n_term = sum(1 for g in d["grades"].values() if g.get("terminus_contested"))
    print(f"PASS  ledger v{d['version']}  |  {len(recomputed)}/{total} boundary cells @ eps={eps}  "
          f"|  {n_edges} routing edges / {n_term} contested termini  "
          f"|  band-true + display + boundary + manifest + counts + routing + consistency OK")


main()

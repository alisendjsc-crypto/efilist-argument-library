#!/usr/bin/env python3
"""sp_redraft_reading.py -- gate2's reading instrument for its second judgment of L6's safety pass: the correction row
SD-10 (gate2, 2026-09-26, R0210).

Every figure SP_redrafts_judgments.json states as measured, recomputed from the judged artifacts at their pinned md5s:

  new_rows     the rows the drafts record gained after the bytes gate2's first judgment read (050d240f)
  diff         each new row against the row it supersedes: which fields moved, and the replacement's one change
  patch        the patch for every current row (SD-10 in place of SD-02): gate2's X-032 patterns after it; which rows,
               if any, bring the other em-dash style into their slot
  knock_on     L6's knock-on record v0_2 against the v0_1 gate2 confirmed: the same rows

  python3 sp_redraft_reading.py [--emit | --check]
Repo-relative. Writes nothing unless --emit is given. Deterministic.
"""
import json, os, sys, types

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import pinned  # noqa: E402

RECORD = "adversarial_map_staging/r1/sp_redraft_reading_v0_1.json"
DRAFTS = ("adversarial_map_staging/r1/SP_drafts_L6.json", "8742b882b6055761207c7dc1618b645b")
DRAFTS_FIRST = "050d240fe08f5ea69b883fb4b199c959"
PATCH = ("tools/pin_patch_l6.py", "4686278407b961c3aefa00ac1b08c11a")
FIRST_INSTRUMENT = ("adversarial_map_staging/r1/sp_judgment_reading.py", "4b8ba90b57aeced8557a5468fb955aeb")
PQ_INSTRUMENT = ("adversarial_map_staging/r1/pq_judgment_reading.py", "d11cfbc7182e8fba0f549467b654b1bd")
KNOCK1 = ("adversarial_map_staging/r1/SP_knock_on_L6_v0_1.json", "feff44032200e5617bd420b6f7440bd9")
KNOCK2 = ("adversarial_map_staging/r1/SP_knock_on_L6_v0_2.json", "013319b88335e3b6ce6bc8dd9ac709a4")
CORPUS = "efilist_argument_library_v4_0_0.json"


def module_at(rel, want, name):
    m = types.ModuleType(name)
    m.__file__ = os.path.join(REPO, rel)
    exec(compile(pinned.bytes_at(REPO, rel, want).decode("utf-8"), m.__file__, "exec"), m.__dict__)
    return m


def load(rel, want):
    return json.loads(pinned.bytes_at(REPO, rel, want).decode("utf-8"))


def measure():
    R1 = module_at(PQ_INSTRUMENT[0], PQ_INSTRUMENT[1], "pq_reading_pinned")
    SP = module_at(FIRST_INSTRUMENT[0], FIRST_INSTRUMENT[1], "sp_reading_pinned")
    P = module_at(PATCH[0], PATCH[1], "pin_patch_l6_pinned")
    rec = load(*DRAFTS)
    first = load(DRAFTS[0], DRAFTS_FIRST)
    assert rec["rows"][:len(first["rows"])] == first["rows"], "the drafts record did not merely grow"
    first_ids = {r["id"] for r in first["rows"]}
    by = {r["id"]: r for r in rec["rows"]}
    new = [r for r in rec["rows"] if r["id"] not in first_ids]
    diff = []
    for r in new:
        old = by.get(r.get("supersedes"), {})
        a, b = old.get("replacement", ""), r.get("replacement", "")
        i = 0
        while i < min(len(a), len(b)) and a[i] == b[i]:
            i += 1
        j = 0
        while j < min(len(a), len(b)) - i and a[len(a) - 1 - j] == b[len(b) - 1 - j]:
            j += 1
        diff.append({"row": r["id"], "supersedes": r.get("supersedes"),
                     "fields_moved": sorted(k for k in set(old) | set(r) if old.get(k) != r.get(k)),
                     "current_unchanged": old.get("current") == r.get("current"),
                     "replacement_change": {"from": a[i:len(a) - j], "to": b[i:len(b) - j]}})
    rows = P.select(rec, "all")
    out, _ = P.build(rec, rows, repo=REPO)
    pre_c = json.loads(pinned.bytes_at(REPO, CORPUS, rec["pinned"]["surfaces"][CORPUS]).decode("utf-8"))
    pre, post = R1.text_map(pre_c), R1.text_map(json.loads(out[CORPUS]))
    ex_post = R1.sweep(post, R1.EXIT)
    mixed = []
    for r in rows:
        rest = pre[r["locus"]].replace(r["current"], "")
        s_rest, s_new = SP.style(rest), SP.style(r["replacement"])
        if (s_new["spaced"] and s_rest["unspaced"] and not s_rest["spaced"]) or \
                (s_new["unspaced"] and s_rest["spaced"] and not s_rest["unspaced"]):
            mixed.append(r["id"])
    k1 = load(*KNOCK1)
    k2 = load(*KNOCK2)
    return {
        "artifact": os.path.basename(RECORD),
        "instrument": "adversarial_map_staging/r1/sp_redraft_reading.py",
        "reads": {"drafts": DRAFTS[1], "drafts_first_judged": DRAFTS_FIRST, "patch_tool": PATCH[1],
                  "knock_on_v0_1": KNOCK1[1], "knock_on_v0_2": KNOCK2[1],
                  "set": "all: %d rows (%s)" % (len(rows), ", ".join(r["id"] for r in rows))},
        "new_rows": [r["id"] for r in new],
        "diff": diff,
        "patch": {"x032_hits_after_every_row": len(ex_post), "rows_mixing_dash_styles": mixed},
        "knock_on": {"v0_2_rows_equal_v0_1": k2.get("rows") == k1.get("rows"), "rows": len(k1.get("rows", []))},
    }


def main():
    fresh = (json.dumps(measure(), indent=1, ensure_ascii=False) + "\n").encode("utf-8")
    path = os.path.join(REPO, RECORD)
    if "--emit" in sys.argv:
        open(path, "wb").write(fresh)
        print("wrote %s  %s / %d" % (RECORD, pinned.md5(fresh), len(fresh)))
    elif "--check" in sys.argv:
        same = os.path.exists(path) and open(path, "rb").read() == fresh
        print("READING RECORD: %s" % ("matches the committed record" if same else "DIFFERS from the committed record"))
        sys.exit(0 if same else 1)
    else:
        sys.stdout.write(fresh.decode("utf-8"))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""pq_redraft_reading.py -- gate2's reading instrument for its second judgment of the pin session's repairs, the
correction rows (gate2, 2026-09-26, R0179).

Every figure PQ_repair_redrafts_judgments.json states as measured, recomputed from the judged artifacts at the md5s
they are pinned to, never from the working tree:

  new_rows            the rows the drafts record gained after the bytes gate2's first judgment read, and what each
                      supersedes
  owed_changes        for each correction, the phrases its owed change removes and adds, as plain string facts
  patch_equivalence   the judged patch tool (pin_patch_l5.py) and its phase-5 successor (pin_patch_l5_v0_2.py), each at
                      its pinned bytes, build the same three surfaces for the same rows (the declared set and all)
  confinement         the corrected patch differs from the pre-pin corpus at exactly the repaired loci, and at each only
                      by the rows' replacements
  knock_on            the entries anchored inside a repaired sentence that move with it, and the (a) entries whose
                      answer routes to a repaired locus, for the corrected set; compared as sets with the first
                      reading's and with the drafts' knock-on record v0_2
  holds               the five HOLDS: each supporting sentence the first judgment named still stands
  exit_framing        the corrections add or remove no survival-as-barrier framing (pre-pin sweep == post-pin sweep)

  python3 pq_redraft_reading.py            # print the record
  python3 pq_redraft_reading.py --emit     # write the record beside this file
  python3 pq_redraft_reading.py --check    # compare with the committed record; exit 1 on any difference

Repo-relative. Writes nothing unless --emit is given. Deterministic.
"""
import json, os, sys, types

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import pinned  # noqa: E402

RECORD = "adversarial_map_staging/r1/pq_redraft_reading_v0_1.json"
DRAFTS = ("adversarial_map_staging/r1/PQ_repair_drafts_L5.json", "496c3a5c63541d8657e7d7e949e43648")
DRAFTS_FIRST = "0819125d28c58561bcda42570181e105"
FIRST_READING = ("adversarial_map_staging/r1/pq_judgment_reading_v0_1.json", "16e8bd96b7c3f81e2cea356af59b0f26")
FIRST_INSTRUMENT = ("adversarial_map_staging/r1/pq_judgment_reading.py", "d11cfbc7182e8fba0f549467b654b1bd")
KNOCK2 = ("adversarial_map_staging/r1/PQ_knock_on_L5_v0_2.json", "2cde775ee82cd16b0e5cdb88820bd130")
PATCH1 = ("tools/pin_patch_l5.py", "092b9adc7cfbac33ed0f99d2b6170bb5")
PATCH2 = ("tools/pin_patch_l5_v0_2.py", "6b810494885853aec7f43b12a51cb3f9")
CORPUS = "efilist_argument_library_v4_0_0.json"

# What each owed change removes and adds (X-002, X-003, X-008; X-034's safe wording), as literal phrases.
OWED = {
    "PD-19": {"answers": "X-002", "gone": ["every life carries"],
              "present": ["The floor the typical life carries",
                          "only if the person-affecting view that prevails keeps the weight against non-consensual imposition"]},
    "PD-20": {"answers": "X-003", "gone": ["does not depend on the act it forbids"],
              "present": ["the view does not will, as its means, the act it forbids",
                          "whatever that path owes to the births others choose"]},
    "PD-21": {"answers": "X-008", "gone": ["Some efilists", "Its core was"],
              "present": ["Efilism itself goes further", "Its core is", "its own burden", "painlessly and all at once"]},
    "PC-06": {"answers": "X-034", "gone": ["Bradley"], "present": ["the person-affecting re-explanation"]},
}


def load(pin):
    return json.loads(pinned.bytes_at(REPO, pin[0], pin[1]).decode("utf-8"))


def module_at(rel, want, name):
    """A committed file at its pinned bytes, run as a module (never the working copy)."""
    m = types.ModuleType(name)
    m.__file__ = os.path.join(REPO, rel)
    exec(compile(pinned.bytes_at(REPO, rel, want).decode("utf-8"), m.__file__, "exec"), m.__dict__)
    return m


def measure():
    R1 = module_at(FIRST_INSTRUMENT[0], FIRST_INSTRUMENT[1], "pq_judgment_reading_pinned")
    rec = load(DRAFTS)
    first_ids = [r["id"] for r in json.loads(pinned.bytes_at(REPO, DRAFTS[0], DRAFTS_FIRST).decode("utf-8"))["rows"]]
    assert rec["rows"][:len(first_ids)] == json.loads(pinned.bytes_at(REPO, DRAFTS[0], DRAFTS_FIRST).decode("utf-8"))["rows"]
    new_rows = [{"id": r["id"], "kind": r["kind"], "supersedes": r.get("supersedes"), "locus": r.get("locus")}
                for r in rec["rows"] if r["id"] not in first_ids]
    by_id = {r["id"]: r for r in rec["rows"]}
    owed = {}
    for rid, spec in OWED.items():
        t = by_id[rid]["replacement"]
        owed[rid] = {"answers": spec["answers"], "supersedes": by_id[rid].get("supersedes"),
                     "gone": {p: p not in t for p in spec["gone"]}, "present": {p: p in t for p in spec["present"]},
                     "current_text_unchanged": by_id[rid]["current"] == by_id[by_id[rid]["supersedes"]]["current"]}

    P1 = module_at(PATCH1[0], PATCH1[1], "pin_patch_l5_pinned")
    P2 = module_at(PATCH2[0], PATCH2[1], "pin_patch_l5_v0_2_pinned")
    equiv = {}
    for which in ("declared", "all"):
        rows1, rows2 = P1.select(rec, which), P2.select(rec, which)
        o1, _ = P1.build(rec, rows1, repo=REPO)
        o2, _ = P2.build(rec, rows2, repo=REPO)
        equiv[which] = {"rows": [r["id"] for r in rows1], "same_rows": [r["id"] for r in rows1] == [r["id"] for r in rows2],
                        "surfaces": {f: pinned.md5(o1[f].encode("utf-8")) for f in sorted(o1)},
                        "byte_identical": sorted(o1) == sorted(o2) and all(o1[f] == o2[f] for f in o1)}

    rows = P1.select(rec, "all")
    pre_corpus = json.loads(pinned.bytes_at(REPO, CORPUS, rec["pinned"]["surfaces"][CORPUS]).decode("utf-8"))
    out, _ = P1.build(rec, rows, repo=REPO)
    pre, post = R1.text_map(pre_corpus), R1.text_map(json.loads(out[CORPUS]))
    by_locus = {}
    for r in rows:
        by_locus.setdefault(r["locus"], []).append(r)
    changed = sorted(k for k in pre if pre[k] != post.get(k))
    conf_ok = True
    for locus, rs in by_locus.items():
        want = pre[locus]
        for r in rs:
            conf_ok &= pre[locus].count(r["current"]) == 1
            want = want.replace(r["current"], r["replacement"], 1)
        conf_ok &= post[locus] == want
    confinement = {"repaired_loci": len(by_locus), "rows": len(rows), "changed_loci_are_the_repaired_loci":
                   changed == sorted(by_locus), "each_locus_is_pre_with_the_replacements": conf_ok,
                   "loci_added_or_removed": sorted(set(pre) ^ set(post))}

    m = load(R1.MAP)
    ev = {(e["target_id"], e["target_locus"], e["target_anchor"]): e["n"] for e in load(R1.EVID)["entries"]}
    rr = load(R1.RULINGS)["rows"]
    sup = {r["supersedes"] for r in rr if r.get("supersedes")}
    verdict = {r["n"]: r["verdict"] for r in rr if r["row"] not in sup}
    moved, routes = [], []
    for e in m["entries"]:
        key = "%s#%s" % (e["target_id"], e["target_locus"])
        rs = by_locus.get(key, [])
        if any(e["target_anchor"] in r["current"] for r in rs):
            if pre[key].count(e["target_anchor"]) == sum(r["current"].count(e["target_anchor"]) for r in rs):
                moved.append((key, e["target_anchor"]))
        if e["class"] == "a":
            for loc in e.get("routing", {}).get("answered_by", []):
                if loc in by_locus:
                    n = ev.get((e["target_id"], e["target_locus"], e["target_anchor"]))
                    routes.append((loc, key, e["target_anchor"], n, verdict.get(n)))
    first = load(FIRST_READING)["knock_on_independent"]
    k2 = load(KNOCK2)
    rec_in = sorted((r["locus"], r["anchor"]) for r in k2["rows"] if r["kind"] == "anchor_inside")
    rec_rt = sorted((r["locus"], r["target"], r["anchor"]) for r in k2["rows"] if r["kind"] == "answer_routes_here")
    knock = {"anchor_inside": len(moved), "answer_routes_here": len(routes),
             "holds": sorted({x[3] for x in routes if x[4] == "HOLDS"}),
             "fails": sorted({x[3] for x in routes if x[4] == "FAILS"}),
             "same_as_first_reading": sorted(moved) == sorted((x["locus"], x["anchor"]) for x in first["inside"]
                                                              if x["moves_with_the_repair"])
             and sorted(x[:3] for x in routes) == sorted((x["routed_to"], x["target"], x["anchor"]) for x in first["routes"]),
             "matches_knock_on_v0_2": sorted(moved) == rec_in and sorted(x[:3] for x in routes) == rec_rt}

    holds = []
    for n, locus, sentence in R1.HOLDS:
        x = {"n": n, "rests_on": locus, "locus_repaired": locus in by_locus}
        if sentence is not None:
            x.update(sentence=sentence, stands_after_the_pin=post[locus].count(sentence) == 1)
        holds.append(x)
    ex_pre, ex_post = R1.sweep(pre, R1.EXIT), R1.sweep(post, R1.EXIT)

    return {
        "artifact": os.path.basename(RECORD),
        "instrument": "adversarial_map_staging/r1/pq_redraft_reading.py",
        "reads": {"drafts": DRAFTS[1], "drafts_first_judged": DRAFTS_FIRST, "first_reading": FIRST_READING[1],
                  "first_instrument": FIRST_INSTRUMENT[1], "knock_on_v0_2": KNOCK2[1], "patch_v0_1": PATCH1[1],
                  "patch_v0_2": PATCH2[1], "corpus": rec["pinned"]["surfaces"][CORPUS]},
        "new_rows": new_rows,
        "owed_changes": owed,
        "patch_equivalence": equiv,
        "confinement": confinement,
        "knock_on": knock,
        "holds": holds,
        "exit_framing": {"pre_equals_post": ex_pre == ex_post, "loci": sorted({h["locus"] for h in ex_post})},
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

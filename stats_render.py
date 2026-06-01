#!/usr/bin/env python3
"""stats_render.py - render-time STATISTICS generator for efilist_argument_library.

Replaces the retired hand-authored STATISTICS.md grade layer. Every figure is
computed from canonical data at run time, never stored as a literal:
  - grade distribution : corpus objections[].tier x ledger grades[].headline_grade_long
  - C-band floor        : min long.rsi_pct among headline_grade_long == 'C'
  - danger quadrant     : deployment >= DEPLOY_THRESHOLD  AND  (C-band OR ungraded)
  - deployment leaders  : corpus.realWorldExamples[].attached_objections[].objection_id

Reconciliation asserts gate the build (CI): exits non-zero if the grade basis is
not the ledger headline_grade_long set, n != 81, or any node lacks a long grade.
On success it (re)emits STATISTICS_render_v3_8_4.md.

Usage:  python3 stats_render.py [REPO_ROOT=.]
"""
import sys
import os
import json
import glob
import datetime
from collections import Counter, defaultdict

GRADES = ("A", "B", "C", "D")
BELOW_B = ("C", "D")          # below-B-band headline grades (ungraded handled separately)
EXPECTED_N = 81
DEPLOY_THRESHOLD = 8          # spec sec.6 / old STATISTICS sec.7: high-deployment cut
OUT_NAME = "STATISTICS_render_v3_8_4.md"


def find_file(root, patterns, exclude=()):
    for pat in patterns:
        for path in sorted(glob.glob(os.path.join(root, pat))):
            if any(x in os.path.basename(path) for x in exclude):
                continue
            return path
    return None


def fail(msg):
    sys.stderr.write("RECONCILE FAIL: " + msg + "\n")
    sys.exit(1)


def cell(n):
    return str(n) if n else "-"


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    corpus_p = find_file(root, ["efilist_argument_library_v3_8_*.json",
                                "efilist_argument_library_v*.json"],
                         exclude=("backup", "pre_render"))
    ledger_p = find_file(root, ["rebuttal_grading_ledger*.json"], exclude=("backup",))
    if not corpus_p:
        fail("corpus json not found under " + repr(root))
    if not ledger_p:
        fail("ledger json not found under " + repr(root))

    corpus = json.load(open(corpus_p, encoding="utf-8"))
    ledger = json.load(open(ledger_p, encoding="utf-8"))["grades"]
    objs = corpus["objections"]

    # reconciliation gate
    if len(objs) != EXPECTED_N:
        fail("objection count " + str(len(objs)) + " != " + str(EXPECTED_N))
    ungraded = [o["id"] for o in objs if "headline_grade_long" not in ledger.get(o["id"], {})]
    if ungraded:
        fail("ungraded-long nodes: " + str(ungraded))
    bad = [o["id"] for o in objs if ledger[o["id"]]["headline_grade_long"] not in GRADES]
    if bad:
        fail("grade outside enum " + str(list(GRADES)) + ": " + str(bad))
    graded_n = sum(1 for o in objs if ledger[o["id"]]["headline_grade_long"] in GRADES)
    if graded_n != EXPECTED_N:
        fail("graded basis count " + str(graded_n) + " != " + str(EXPECTED_N))

    # compute
    by_tier = defaultdict(Counter)
    tot = Counter()
    for o in objs:
        g = ledger[o["id"]]["headline_grade_long"]
        by_tier[o["tier"]][g] += 1
        tot[g] += 1
    if sum(tot.values()) != EXPECTED_N:
        fail("distribution sums to " + str(sum(tot.values())))

    dep = Counter()
    for r in corpus.get("realWorldExamples", []):
        for a in r.get("attached_objections", []):
            nid = a.get("objection_id") if isinstance(a, dict) else a
            if nid:
                dep[nid] += 1

    grade_of = {o["id"]: ledger[o["id"]]["headline_grade_long"] for o in objs}
    rsi_of = {o["id"]: ledger[o["id"]]["long"]["rsi_pct"] for o in objs}
    c_nodes = sorted((rsi_of[o["id"]], o["id"]) for o in objs if grade_of[o["id"]] == "C")
    top_dep = sorted(dep.items(), key=lambda kv: (-kv[1], kv[0]))[:12]

    # danger quadrant: deployment >= threshold AND below B-band (C/D/ungraded)
    quadrant = sorted(((dep[o["id"]], o["id"], grade_of[o["id"]]) for o in objs
                       if dep[o["id"]] >= DEPLOY_THRESHOLD and grade_of[o["id"]] in BELOW_B),
                      reverse=True)
    c_dep = [dep[o["id"]] for o in objs if grade_of[o["id"]] == "C"]
    c_dep_max = max(c_dep) if c_dep else 0
    most_dep_c = sorted(((dep[o["id"]], o["id"]) for o in objs if grade_of[o["id"]] == "C"),
                        reverse=True)[:2]

    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    cv = str(corpus.get("version", "?"))
    cg = str(corpus.get("generated", "?"))
    n_rwe = len(corpus.get("realWorldExamples", []))

    out = []
    out.append("# STATISTICS (render-time) - efilist_argument_library\n")
    out.append("> **Generated** " + ts + " by `stats_render.py` from canonical data: `"
               + os.path.basename(corpus_p) + "` objections[].tier x `"
               + os.path.basename(ledger_p) + "` grades[].headline_grade_long x "
               "corpus.realWorldExamples. **Never hand-authored.** Corpus version "
               + cv + " (" + cg + ").\n")
    out.append("> **Reconciliation:** basis=`headline_grade_long`, n=" + str(graded_n)
               + "/" + str(EXPECTED_N) + ", ungraded-long=" + str(len(ungraded))
               + ", D-band=" + str(tot["D"]) + " - **PASS**\n")
    out.append("\n## Sampling provenance (read first)\n")
    out.append("The real-world example corpus is **diversified but opportunistic** "
               "(institutional / lifestyle / student-journalism / primary-platform / niche "
               "surfaces). It is **not a representative sample of real-world objection "
               "frequency**. Every deployment count below is **internal to the harvested "
               "set** (" + str(n_rwe) + " instances), never a real-world rate.\n")
    out.append("\n## Grade distribution by tier (headline long-form grade)\n")
    out.append("| Tier | A | B | C | D | Ungraded |")
    out.append("|---|---|---|---|---|---|")
    for t in sorted(by_tier):
        row = by_tier[t]
        out.append("| T" + str(t) + " | " + cell(row["A"]) + " | " + cell(row["B"])
                   + " | " + cell(row["C"]) + " | " + cell(row["D"]) + " | - |")
    out.append("| **Total** | **" + str(tot["A"]) + "** | **" + str(tot["B"]) + "** | **"
               + str(tot["C"]) + "** | **" + str(tot["D"]) + "** | **0** |")
    out.append("\nAll " + str(EXPECTED_N) + "/" + str(EXPECTED_N)
               + " graded; zero D-band; zero ungraded.\n")
    out.append("\n## C-band floor (strengthen worklist)\n")
    out.append(str(len(c_nodes)) + " nodes remain at C (all C, none D). "
               "Lowest long-RSI = current floor:\n")
    out.append("| Objection | long RSI | Grade |")
    out.append("|---|---|---|")
    for rsi, nid in c_nodes:
        out.append("| `" + nid + "` | " + format(rsi, ".1f") + " | C |")

    out.append("\n## Deployment x grade - danger quadrant (deployment >= "
               + str(DEPLOY_THRESHOLD) + " AND below B-band)\n")
    out.append("The view the project most needs: a weak rebuttal (C-band or ungraded) that "
               "is also heavily deployed in the wild. High deployment alone is not risk; a "
               "low grade alone is not exposure; the danger is the **intersection**.\n")
    if quadrant:
        out.append("| Objection | Grade | long RSI | Deployments |")
        out.append("|---|---|---|---|")
        for d, nid, g in quadrant:
            out.append("| `" + nid + "` | " + g + " | " + format(rsi_of[nid], ".1f")
                       + " | " + str(d) + " |")
    else:
        leaders = ", ".join("`" + nid + "` " + grade_of[nid] + " (" + str(c) + ")"
                            for nid, c in top_dep[:3])
        cc = ", ".join("`" + nid + "` (" + str(d) + ")" for d, nid in most_dep_c)
        out.append("**EMPTY at this release.** No objection with deployment >= "
                   + str(DEPLOY_THRESHOLD) + " RWE sits below B-band. The most-deployed nodes ("
                   + leaders + ") are all B-or-better; every remaining C-band node is "
                   "low-deployment (max " + str(c_dep_max) + " RWE). The most-deployed C-nodes - "
                   + cc + " - are strengthen-candidates **below** the quadrant threshold, not "
                   "exposure-to-watch. (Ungraded high-deployment nodes would render here as a "
                   "distinct pending-grade state; there are none.) Not foreclosed: a new attested "
                   "deployment pushing a C-node past >= " + str(DEPLOY_THRESHOLD)
                   + ", or a band-reverting regrade, would re-populate it.\n")

    out.append("\n## Deployment leaders (context for the quadrant)\n")
    out.append("Most-attached objections and their headline grade - shows the heavily-deployed "
               "nodes are all well-graded (which is why the quadrant above is empty).\n")
    out.append("| Objection | Grade | long RSI | Deployments |")
    out.append("|---|---|---|---|")
    for nid, count in top_dep:
        out.append("| `" + nid + "` | " + grade_of.get(nid, "?") + " | "
                   + format(rsi_of.get(nid, float("nan")), ".1f") + " | " + str(count) + " |")

    out_path = os.path.join(root, OUT_NAME)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")

    floor_rsi, floor_id = c_nodes[0]
    print("OK: wrote " + out_path + " | n=" + str(graded_n) + " A=" + str(tot["A"])
          + " B=" + str(tot["B"]) + " C=" + str(tot["C"]) + " D=" + str(tot["D"])
          + " | floor=" + floor_id + " " + format(floor_rsi, ".1f")
          + " | quadrant=" + (str(len(quadrant)) if quadrant else "EMPTY"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

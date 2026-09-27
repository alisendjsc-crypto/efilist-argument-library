#!/usr/bin/env python3
"""l7_dossiers.py -- the reading instrument for the successor map's drafting (L7, 2026-09-26, R0223 order 2).

One markdown dossier per node the successor has to read, for the drafter and for the judge:
  - every locus of the node that either cut moved, as the map found it (04bf6482) and as it reads now (7b6e65e5),
    with each landed row's current text and replacement;
  - every v1_6 entry at the node, with l7_measure's status for it (unchanged / moved / gone, and whether an
    unchanged anchor sits at a moved locus), its fields, its current R1 row where it has one, and, for a (d), the
    register v0_7 tributary it is filed under;
  - every (a) anywhere whose answer routes into the node, with the answering locus as it reads now;
  - every finding (PF-, X-, Z-, SF-) that names the node.

Which nodes: every node l7_measure's record lists (a moved locus, an anchor that moved or went, a routed answer, a
quoting passage), the nodes of the six waiting (a)s (v1_6 (a)s whose current R1 row is FAILS), and the nodes the
findings name for filing. Nothing is inferred: the findings table below is each finding's own locus list.

Reads at a pin (pinned.py): l7_measure's record, the map v1_6, the two corpora, R1_rulings, the R1 evidence,
register v0_7, both drafts records and both judgment records the findings live in.

  python3 l7_dossiers.py --out <dir>             # every node
  python3 l7_dossiers.py --out <dir> --node X Y  # named nodes
  python3 l7_dossiers.py --list                  # the node list and why each is on it; writes nothing

Repo-relative. Writes only under --out. Deterministic.
"""
import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import pinned  # noqa: E402

S, R = "adversarial_map_staging", "adversarial_map_staging/r1"
CORPUS = "efilist_argument_library_v4_0_0.json"
PIN = {
    "measure": (R + "/l7_measure_v0_1.json", "4d98b4a3b5c3a57ef62543001ba7ff64"),
    "map": (S + "/adversarial_map_v1_6.json", "7a69bc9fd197047c3cf7cecdb37a44ed"),
    "pre": (CORPUS, "04bf6482aa0374ee92a81c1d55ec41f8"),
    "post": (CORPUS, "7b6e65e531018fecb37baf2a4fedd6d1"),
    "rulings": (R + "/R1_rulings.json", "d829437e938a8b9dded5cb8cbaa26b74"),
    "evidence": (R + "/R1_evidence_2026-09-19.json", "719b5ddb27680f32181a8a953c84b6c2"),
    "register": (S + "/honest_residuals_register_v0_7.json", "bcbff23113f3fb0135d5fd5b3e2630d5"),
    "drafts_L5": (R + "/PQ_repair_drafts_L5.json", "8c57223e8f9170cb8303bcc4b9d982c4"),
    "drafts_L6": (R + "/SP_drafts_L6.json", "e493f8cdcf74aa3ad7982e1e906cffde"),
    "judged_L5": (R + "/PQ_repair_drafts_judgments.json", "2ed68a7cf7f83b8d61a977f0aad0b08e"),
    "judged_L6": (R + "/SP_drafts_judgments.json", "437013204cfafc4c740a763e1fb79349"),
}
# The findings the successor files, each with the loci its own text names (R0223: "To file as (b)s").
FILINGS = {
    "PF-01": ["just-depressed#archetypeVariants.defender"],
    "PF-02": ["slippery-slope-eugenics#long"],
    "PF-03": ["bitter-childhood#archetypeVariants.defender"],
    "X-033": ["violence-as-reductio#long", "why-not-suicide#long", "ai-fear#archetypeVariants.defender",
              "slippery-slope-eugenics#long", "slippery-slope-eugenics#archetypeVariants.defender",
              "slippery-slope-eugenics#archetypeVariants.sophisticate", "bitter-childhood#archetypeVariants.defender",
              "just-depressed#long"],
    "X-034": ["bradley-no-subject#long"],
    "Z-033": ["boonin-critique#long"],
}


def load():
    return {k: json.loads(pinned.bytes_at(REPO, rel, m).decode("utf-8")) for k, (rel, m) in PIN.items()}


def locus_text(o, loc):
    if loc in ("diagnosis", "note"):
        return o.get(loc) or ""
    if loc.startswith("archetypeVariants."):
        return (o["responses"].get("archetypeVariants") or {}).get(loc.split(".", 1)[1], "")
    return o["responses"].get(loc, "")


def world(d):
    w = {"d": d}
    w["pre"] = {o["id"]: o for o in d["pre"]["objections"]}
    w["post"] = {o["id"]: o for o in d["post"]["objections"]}
    w["ev"] = {(e["target_id"], e["target_locus"], e["target_anchor"]): e["n"] for e in d["evidence"]["entries"]}
    rr = d["rulings"]["rows"]
    sup = {r["supersedes"] for r in rr if r.get("supersedes")}
    w["ruling"] = {r["n"]: r for r in rr if r["row"] not in sup}
    w["status"] = {x["i"]: x for x in d["measure"]["entries"]}
    w["trib"] = {}
    for b in d["register"]["bedrocks"]:
        for f in b["facets"]:
            for t in f["tributaries"]:
                w["trib"][(t["node"], t["locus"], t["anchor"])] = (b["bedrock_id"], b["name"], f["facet_id"])
    w["rows"] = {}
    for k in ("drafts_L5", "drafts_L6"):
        rat = [r for r in d[k]["rows"] if r["kind"] == "ratification"][0]["rows"]
        for r in d[k]["rows"]:
            if r["id"] in rat:
                w["rows"].setdefault(r["locus"], []).append((k[-2:], r))
    w["findings"] = []
    for k in ("drafts_L5", "drafts_L6"):
        for r in d[k]["rows"]:
            if r["kind"] == "finding":
                w["findings"].append((r["id"], r["title"], r["finding"], r.get("lean", "")))
    for k in ("judged_L5", "judged_L6"):
        for r in d[k]["rows"]:
            if r.get("kind") == "finding":
                w["findings"].append((r["id"], r["title"], r["finding"], r.get("recommendation", "")))
            elif r.get("carries"):
                w["findings"].append((r["id"], "carries (%s %s)" % (r.get("row_id", ""), r.get("verdict", "")),
                                      " | ".join(r["carries"]), ""))
    # the six waiting (a)s: v1_6 (a)s whose current R1 row is FAILS
    w["waiting"] = []
    for i, e in enumerate(d["map"]["entries"]):
        n = w["ev"].get((e["target_id"], e["target_locus"], e["target_anchor"]))
        if e["class"] == "a" and n in w["ruling"] and w["ruling"][n]["verdict"] == "FAILS":
            w["waiting"].append((i, n))
    return w


def nodes_to_read(w):
    why = {}
    m = w["d"]["measure"]
    for x in m["entries"]:
        if x["status"] != "unchanged" or x.get("survives_outside"):
            why.setdefault(x["target"].split("#")[0], []).append("entry %d %s" % (x["i"], x["status"] +
                                                                              (" (at a moved locus)" if x.get("survives_outside") else "")))
    for x in m["routes"]:
        why.setdefault(x["target"].split("#")[0], []).append("entry %d routes to %s" % (x["i"], x["answered_by"]))
    for x in m["quotes"]:
        why.setdefault(x["target"].split("#")[0], []).append("entry %d quotes %s" % (x["i"], x["quotes_from"]))
    for i, n in w["waiting"]:
        e = w["d"]["map"]["entries"][i]
        why.setdefault(e["target_id"], []).append("entry %d is waiting (a) #%d" % (i, n))
    for f, loci in FILINGS.items():
        for l in loci:
            why.setdefault(l.split("#")[0], []).append("%s names %s" % (f, l))
    for l in m["changed_loci"]:
        why.setdefault(l.split("#")[0], []).append("locus %s moved" % l)
    return {k: sorted(set(v)) for k, v in sorted(why.items())}


def dossier(w, node):
    d = w["d"]
    out = ["# %s" % node, ""]
    pre, post = w["pre"][node], w["post"][node]
    out.append("tier %s | trigger: %s" % (post.get("tier"), (post.get("trigger") or post.get("objection") or "")[:300]))
    out.append("")
    for locus in [l for l in d["measure"]["changed_loci"] if l.split("#")[0] == node]:
        loc = locus.split("#")[1]
        out += ["## MOVED LOCUS %s" % locus, ""]
        for cut, r in w["rows"].get(locus, []):
            out += ["- %s %s (%s): CURRENT: %s" % (cut, r["id"], r["kind"], r["current"]),
                    "  REPLACEMENT: %s" % r["replacement"], ""]
        out += ["NOW (7b6e65e5):", "", locus_text(post, loc), ""]
    entries = [(i, e) for i, e in enumerate(d["map"]["entries"]) if e["target_id"] == node]
    out += ["## ENTRIES AT THIS NODE (%d)" % len(entries), ""]
    for i, e in entries:
        st = w["status"][i]
        n = w["ev"].get((e["target_id"], e["target_locus"], e["target_anchor"]))
        out.append("### entry %d%s  (%s) at %s -- %s%s" % (i, " #%d" % n if n else "", e["class"], e["target_locus"],
                                                          st["status"], " (anchor outside the repair, locus moved)"
                                                          if st.get("survives_outside") else ""))
        out += ["- anchor: %s" % e["target_anchor"], "- move: %s" % e["adversarial_move"], "- grounds: %s" % e["grounds"],
                "- routing: %s" % json.dumps(e["routing"], ensure_ascii=False),
                "- provenance: %s" % json.dumps({k: v for k, v in e["provenance"].items() if k in ("phase", "date", "seat")})]
        am = e["provenance"].get("amended") or e["provenance"].get("redrafted")
        if am:
            out.append("- amended: %s" % json.dumps({k: am.get(k) for k in ("at", "r1_row", "shape", "disposition")}))
        if n in w["ruling"]:
            r = w["ruling"][n]
            out.append("- R1 %s %s: %s | stronger: %s" % (r["row"], r["verdict"], r["reason"], r.get("stronger_continuation", "")))
        if e["class"] == "d":
            t = w["trib"].get((e["target_id"], e["target_locus"], e["target_anchor"]))
            out.append("- register v0_7: %s" % (" / ".join(t) if t else "NOT FILED under this (node, locus, anchor)"))
        if e["target_locus"] and "#%s" % e["target_locus"] and st["status"] == "unchanged" and not st.get("survives_outside"):
            pass
        out.append("")
    # loci that host entries but did not move: text now, for context
    hosted = sorted({e["target_locus"] for _i, e in entries} - {l.split("#")[1] for l in d["measure"]["changed_loci"]
                                                                 if l.split("#")[0] == node})
    for loc in hosted:
        out += ["## UNMOVED LOCUS %s#%s (hosts an entry)" % (node, loc), "", locus_text(post, loc), ""]
    routed = [x for x in d["map"]["entries"] if x["class"] == "a"
              and any(ref.split("#")[0] == node for ref in x["routing"]["answered_by"])]
    if routed:
        out += ["## (a)s ANYWHERE THAT ROUTE INTO THIS NODE", ""]
        for x in routed:
            i = d["map"]["entries"].index(x)
            n = w["ev"].get((x["target_id"], x["target_locus"], x["target_anchor"]))
            r = w["ruling"].get(n)
            out.append("- entry %d%s %s#%s -> %s | R1 %s | anchor: %s | move: %s" % (
                i, " #%d" % n if n else "", x["target_id"], x["target_locus"], x["routing"]["answered_by"],
                ("%s %s" % (r["row"], r["verdict"])) if r else "-", x["target_anchor"], x["adversarial_move"]))
        out.append("")
    fs = [f for f in w["findings"] if node in f[2] or node in f[1]]
    if fs:
        out += ["## FINDINGS NAMING THIS NODE", ""]
        for fid, title, text, lean in fs:
            out.append("- %s | %s | %s%s" % (fid, title, text, (" | LEAN: " + lean) if lean else ""))
        out.append("")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--node", nargs="*")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    w = world(load())
    todo = nodes_to_read(w)
    if a.list or not a.out:
        for k, v in todo.items():
            print("%-40s %s" % (k, "; ".join(v)))
        print("%d nodes; waiting (a)s: %s" % (len(todo), ", ".join("#%d (entry %d)" % (n, i) for i, n in w["waiting"])))
        return 0
    os.makedirs(a.out, exist_ok=True)
    for node in (a.node or list(todo)):
        open(os.path.join(a.out, "%s.md" % node), "w", encoding="utf-8").write(dossier(w, node))
    print("wrote %d dossier(s) under %s" % (len(a.node or todo), a.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())

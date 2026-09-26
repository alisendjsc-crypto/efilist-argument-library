#!/usr/bin/env python3
"""r1_draft_dossiers.py -- the reading instrument gate2 judged L4's drafts with (2026-09-25).

One markdown dossier per draft in R1_drafts_L4.json, holding what a judge needs to rule a draft
under R1_standard_ruling_L2, drawn from the committed files and nothing else:

  - the entry's current R1 row, and canon's R1_drafting_pass_L4 row for it;
  - the draft as authored (dispositions, move edits, quotes, the drafter's note to the judge);
  - the entry in v1_3 (what R1 ruled) and in v1_4 (what the draft made of it);
  - the target locus in full, every answering locus in full, and every v1_3 entry on the target
    node and on each answering node, all slots and all classes;
  - for a (d): the registered (d) the bedrock name is copied from, and the register bedrock with
    its gloss, relations and facets; for a wait: the pin-move queue rows it waits on.

r1_dossiers.py (L3) reads the 69 R1 entries; this reads the 45 drafts. It judges nothing and drafts
nothing (K258).

  python3 r1_draft_dossiers.py --out <dir>             # all 45
  python3 r1_draft_dossiers.py --out <dir> --n 14 58   # named drafts

Repo-relative. Writes only under --out. Deterministic: every listing is in file order.
"""
import argparse, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
M3 = "adversarial_map_staging/adversarial_map_v1_3.json"
M4 = "adversarial_map_staging/adversarial_map_v1_4.json"
DRAFTS = "adversarial_map_staging/r1/R1_drafts_L4.json"
EVID = "adversarial_map_staging/r1/R1_evidence_2026-09-19.json"
RULINGS = "adversarial_map_staging/r1/R1_rulings.json"
REGISTER = "adversarial_map_staging/honest_residuals_register_v0_5.json"
CORPUS = "efilist_argument_library_v4_0_0.json"


def load(rel):
    return json.load(open(os.path.join(REPO, rel), encoding="utf-8"))


def locus_text(obj, locus):
    if locus in ("short", "medium", "long"):
        return obj["responses"].get(locus)
    if locus.startswith("archetypeVariants."):
        return obj["responses"].get("archetypeVariants", {}).get(locus.split(".", 1)[1])
    return obj.get(locus)


def dumps(o):
    return json.dumps(o, indent=1, ensure_ascii=False)


def listing(entries):
    return "\n".join("- [%s] %s#%s :: %s\n   MOVE: %s\n   GROUNDS: %s\n   ROUTING: %s"
                     % (y["class"], y["target_id"], y["target_locus"], y["target_anchor"], y["adversarial_move"],
                        y["grounds"], json.dumps(y["routing"], ensure_ascii=False)) for y in entries)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, nargs="*")
    a = ap.parse_args()
    m3, m4, drafts_doc = load(M3), load(M4), load(DRAFTS)
    ev = {e["n"]: e for e in load(EVID)["entries"]}
    rows = load(RULINGS)["rows"]
    superseded = {r["supersedes"] for r in rows if r.get("supersedes")}
    current = {r["n"]: r for r in rows if r["row"] not in superseded}
    canon_rows = {}
    for p in sorted(f for f in os.listdir(REPO) if f.startswith("project_canon_v38_") and f.endswith(".json")):
        c = load(p)
        canon_rows = {x["n"]: x for x in c["adversarial_map"].get("R1_drafting_pass_L4", {}).get("rows", [])}
    hr = {b["bedrock_id"]: b for b in load(REGISTER)["bedrocks"]}
    queue = {p["id"]: p for p in drafts_doc["pin_move_queue"]}
    nodes = {o["id"]: o for o in load(CORPUS)["objections"]}

    def at(m, node, locus=None, klass=None):
        return [e for e in m["entries"] if e["target_id"] == node and (locus is None or e["target_locus"] == locus)
                and (klass is None or e["class"] == klass)]

    os.makedirs(a.out, exist_ok=True)
    wrote = 0
    for x in drafts_doc["drafts"]:
        n = x["n"]
        if a.n and n not in a.n:
            continue
        e, r = ev[n], current[n]
        node, _, loc = r["target"].partition("#")
        key = lambda y: y["target_id"] == e["target_id"] and y["target_anchor"] == e["target_anchor"]
        e3, e4 = [y for y in m3["entries"] if key(y)], [y for y in m4["entries"] if key(y)]
        L = ["# #%d  %s  (%s)  disposition=%s" % (n, r["target"], x["row"], x["disposition"]),
             "\n## R1 row (current)\n" + dumps({k: r[k] for k in r if k not in ("ruled_by", "seat", "date",
                                                                                  "evidence_md5")}),
             "\n## canon row\n" + dumps(canon_rows.get(n)),
             "\n## draft\n" + dumps(x),
             "\n## v1_3 entry\n" + dumps(e3[0]),
             "\n## v1_4 entry (move words %d)\n" % len(e4[0]["adversarial_move"].split())
             + dumps({k: v for k, v in e4[0].items() if k != "provenance"}),
             "\n## target locus text: %s\n%s" % (r["target"], locus_text(nodes[node], loc))]
        for ref in e.get("answered_by", []):
            an, _, al = ref.partition("#")
            L.append("\n## answering locus text: %s\n%s" % (ref, locus_text(nodes[an], al)))
            L.append("\n## v1_3 entries at answering node %s\n%s" % (an, listing(at(m3, an))))
        L.append("\n## v1_3 entries on target node %s (all slots)\n%s" % (node, listing(at(m3, node))))
        if x.get("bedrock_from"):
            bn, _, bl = x["bedrock_from"].partition("#")
            L.append("\n## bedrock_from %s (v1_3)\n%s" % (x["bedrock_from"],
                                                        "\n".join(dumps(y) for y in at(m3, bn, bl, "d"))))
        if x.get("hr"):
            b = hr[x["hr"]]
            L.append("\n## register %s: %s\nGLOSS: %s\nRELATIONS: %s\nFACETS: %s"
                     % (b["bedrock_id"], b["name"], b["gloss"], json.dumps(b["relations"], ensure_ascii=False),
                        [f["facet_id"] for f in b["facets"]]))
        for p in x.get("waits_on") or []:
            L.append("\n## waits_on %s\n%s" % (p, dumps(queue.get(p))))
        open(os.path.join(a.out, "n%02d.md" % n), "w", encoding="utf-8").write("\n".join(L) + "\n")
        wrote += 1
    print("wrote %d dossiers under %s" % (wrote, a.out))


if __name__ == "__main__":
    main()

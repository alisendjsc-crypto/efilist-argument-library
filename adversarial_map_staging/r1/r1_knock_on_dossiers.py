#!/usr/bin/env python3
"""r1_knock_on_dossiers.py -- the reading instrument for the knock-on HOLDS (gate2, 2026-09-26).

R1 ruled its HOLDS against adversarial_map_v1_3.json. L4's drafts, and L4b's redrafts, put new (b)s
and (d)s on the nodes those HOLDS answer through (l4_knock_on_v0_1.json; canon
knock_on_collisions_v1_5). The collision rule says each such HOLDS is read again before its card
ships. One markdown dossier per HOLDS, from the committed files and nothing else:

  - the R1 row that ruled it HOLDS, and the knock-on record's line for it;
  - the (a) entry as it stands in v1_5 (asserted unchanged since v1_3);
  - the target locus and every answering locus, in full;
  - every v1_5 entry on the target node and on each answering node, all slots and classes, with
    each entry the drafting pass or the redrafts changed marked NEW and its v1_3 class shown;
  - the register bedrocks those NEW entries name.

It judges nothing (K258).

  python3 r1_knock_on_dossiers.py --out <dir>           # all HOLDS the knock-on record lists
  python3 r1_knock_on_dossiers.py --out <dir> --n 3 53

Repo-relative. Writes only under --out. Deterministic: every listing is in file order.
"""
import argparse, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
M3 = "adversarial_map_staging/adversarial_map_v1_3.json"
M5 = "adversarial_map_staging/adversarial_map_v1_5.json"
EVID = "adversarial_map_staging/r1/R1_evidence_2026-09-19.json"
RULINGS = "adversarial_map_staging/r1/R1_rulings.json"
KNOCK = "adversarial_map_staging/r1/l4_knock_on_v0_1.json"
REGISTER = "adversarial_map_staging/honest_residuals_register_v0_6.json"
CORPUS = "efilist_argument_library_v4_0_0.json"


def load(rel):
    return json.load(open(os.path.join(REPO, rel), encoding="utf-8"))


def locus_text(obj, locus):
    if locus in ("short", "medium", "long"):
        return obj["responses"].get(locus)
    if locus.startswith("archetypeVariants."):
        return obj["responses"].get("archetypeVariants", {}).get(locus.split(".", 1)[1])
    return obj.get(locus)


def key(e):
    return (e["target_id"], e["target_locus"], e["target_anchor"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, nargs="*")
    a = ap.parse_args()
    m3, m5 = load(M3)["entries"], load(M5)["entries"]
    was = {key(e): e for e in m3}
    ev = {e["n"]: e for e in load(EVID)["entries"]}
    rows = load(RULINGS)["rows"]
    superseded = {r["supersedes"] for r in rows if r.get("supersedes")}
    current = {r["n"]: r for r in rows if r["row"] not in superseded}
    knock = {r["n"]: r for r in load(KNOCK)["rows"]}
    holds = [n for n in load(KNOCK)["holds_newly_collided"] if not a.n or n in a.n]
    nodes = {o["id"]: o for o in load(CORPUS)["objections"]}
    reg = load(REGISTER)["bedrocks"]
    trib = {}
    for b in reg:
        for f in b["facets"]:
            for t in f["tributaries"]:
                trib[(t["node"], t["locus"], t["anchor"])] = (b["bedrock_id"], b["name"], f["facet_id"], b["gloss"])

    def new(e):
        p = e.get("provenance", {})
        return "amended" in p or "redrafted" in p

    def listing(node):
        out = []
        for y in m5:
            if y["target_id"] != node:
                continue
            tag = ""
            if new(y):
                old = was.get(key(y))
                tag = " NEW (v1_3 class %s)" % (old["class"] if old else "none")
            out.append("- [%s]%s %s#%s :: %s\n   MOVE: %s\n   GROUNDS: %s\n   ROUTING: %s"
                       % (y["class"], tag, y["target_id"], y["target_locus"], y["target_anchor"],
                          y["adversarial_move"], y["grounds"], json.dumps(y["routing"], ensure_ascii=False)))
        return "\n".join(out)

    os.makedirs(a.out, exist_ok=True)
    for n in holds:
        e, r = ev[n], current[n]
        assert r["verdict"] == "HOLDS", "#%d is not a current HOLDS" % n
        mine = [y for y in m5 if y["target_id"] == e["target_id"] and y["target_anchor"] == e["target_anchor"]]
        assert len(mine) == 1 and mine[0] == was[key(mine[0])], "#%d moved since v1_3" % n
        node, _, loc = r["target"].partition("#")
        L = ["# #%d  %s  (%s, HOLDS)" % (n, r["target"], r["row"]),
             "\n## R1 row (current)\n" + json.dumps({k: r[k] for k in r if k not in ("seat", "evidence_md5")},
                                                     indent=1, ensure_ascii=False),
             "\n## knock-on record\n" + json.dumps(knock.get(n), indent=1, ensure_ascii=False),
             "\n## the (a) in v1_5 (unchanged since v1_3)\n" + json.dumps(mine[0], indent=1, ensure_ascii=False),
             "\n## target locus text: %s\n%s" % (r["target"], locus_text(nodes[node], loc))]
        seen = [node]
        for ref in mine[0]["routing"].get("answered_by", []):
            an, _, al = ref.partition("#")
            L.append("\n## answering locus text: %s\n%s" % (ref, locus_text(nodes[an], al)))
            if an not in seen:
                seen.append(an)
        for nd in seen:
            L.append("\n## v1_5 entries on node %s (all slots)\n%s" % (nd, listing(nd)))
        named = []
        for nd in seen:
            for y in m5:
                if y["target_id"] == nd and new(y) and y["class"] == "d":
                    t = trib.get(key(y))
                    if t and t not in named:
                        named.append(t)
        for t in named:
            L.append("\n## register %s: %s (facet %s)\nGLOSS: %s" % t)
        open(os.path.join(a.out, "k%02d.md" % n), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("wrote %d knock-on dossiers under %s" % (len(holds), a.out))


if __name__ == "__main__":
    main()

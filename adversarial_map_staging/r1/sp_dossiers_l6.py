#!/usr/bin/env python3
"""sp_dossiers_l6.py -- the reading instrument for the X-032 safety pass's drafts (L6, 2026-09-26, R0193 order 2).

One dossier per locus a current row of SP_drafts_L6.json patches (the six declared, and the proposed companions and
widening rows), for the drafter's own reading and for the judge's:
  - the locus as a reader meets it now, with each row's span marked, and as it would read with every row applied;
  - each row's cuts, keeps and how;
  - every entry of the ruled map (v1_6) at that locus, and where its anchor lies: inside a replaced span, inside a
    touched sentence (W-007: a repair moves every anchor inside its sentence), or outside; and whether the anchor
    string survives the repair;
  - every (a) entry of v1_6 whose answer routes to the locus, with its current R1 verdict;
  - the node's other slots, with what the reading record classes each of them.

knock_on() returns the same facts as data (the gate writes them as SP_knock_on_L6_v0_1.json), plus every v1_6 entry,
anywhere, whose move or grounds quote six or more consecutive words of a replaced span.

Reads everything at a pin: the corpus the record pins (f3d88311, the v4.1.3 cut served in v4.1.4); map v1_6 and
R1_rulings.json at the md5s the record pins; the R1 evidence (#n for (a) entries); the reading record at its pin. The
map pins the pre-v4.1.3 corpus, so an anchor is looked for in the text as it stands now, not where the map found it.

  python3 sp_dossiers_l6.py --out <dir>      # one markdown dossier per locus, and knock_on.json
  python3 sp_dossiers_l6.py --knock-on       # print the knock-on data, write nothing
Repo-relative. Writes only under --out. Deterministic: every listing is in file order.
"""
import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import pinned  # noqa: E402

RECORD = "adversarial_map_staging/r1/SP_drafts_L6.json"
EVID = ("adversarial_map_staging/r1/R1_evidence_2026-09-19.json", "719b5ddb27680f32181a8a953c84b6c2")
CORPUS = "efilist_argument_library_v4_0_0.json"
KINDS = ("draft", "companion", "widening")


def load(rel, md5):
    return json.loads(pinned.bytes_at(REPO, rel, md5).decode("utf-8"))


def locus_text(corpus_by_id, locus):
    oid, loc = locus.split("#")
    o = corpus_by_id[oid]
    r = o["responses"]
    if loc.startswith("archetypeVariants."):
        return r["archetypeVariants"][loc.split(".", 1)[1]]
    return r[loc] if loc in r else o[loc]


def slots(o):
    r = o["responses"]
    for k in ("short", "medium", "long"):
        yield k, r[k]
    for s, t in (r.get("archetypeVariants") or {}).items():
        yield "archetypeVariants." + s, t
    for k in ("diagnosis", "note"):
        if isinstance(o.get(k), str):
            yield k, o[k]


def sentence_bounds(t, i0, i1):
    """The smallest run of whole sentences containing [i0, i1). A sentence ends at '. ', '? ', '! ' or the text's end;
    a replaced span that starts or ends mid-sentence widens to the sentence around it."""
    ends = [m.end() - 1 for m in re.finditer(r"[.?!](?= )", t)]
    starts = [0] + [e + 2 for e in ends]
    s0 = max(s for s in starts if s <= i0)
    later = [e + 1 for e in ends if e + 1 >= i1]
    return s0, (min(later) if later else len(t))


def shingles(s, n=6):
    ws = s.split()
    return {" ".join(ws[i:i + n]) for i in range(max(0, len(ws) - n + 1))}


class World:
    def __init__(self, record=None):
        self.record = record or json.load(open(os.path.join(REPO, RECORD), encoding="utf-8"))
        p = self.record["pinned"]
        self.corpus_md5 = p["surfaces"][CORPUS]
        self.corpus = {o["id"]: o for o in load(CORPUS, self.corpus_md5)["objections"]}
        self.map = load(p["map"]["file"], p["map"]["md5"])
        rr = load(p["rulings"]["file"], p["rulings"]["md5"])["rows"]
        sup = {r["supersedes"] for r in rr if r.get("supersedes")}
        self.ruling = {r["n"]: r for r in rr if r["row"] not in sup}
        self.by_triple = {(e["target_id"], e["target_locus"], e["target_anchor"]): e["n"] for e in load(*EVID)["entries"]}
        q = self.record["queue"]["reading"]
        self.reading = load(q["file"], q["md5"])
        self.cls = {}
        for c, keys in self.reading["classes"].items():
            for k in keys:
                self.cls[k] = c
        sup = {r["supersedes"] for r in self.record["rows"] if r.get("supersedes")}
        self.rows = [r for r in self.record["rows"] if r["id"] not in sup and r["kind"] in KINDS
                     and (r["status"] == "declared" or r["status"].startswith("proposed"))]
        self.loci = []
        for r in self.rows:
            if r["locus"] not in self.loci:
                self.loci.append(r["locus"])

    def n_of(self, e):
        return self.by_triple.get((e["target_id"], e["target_locus"], e["target_anchor"]))

    def text(self, locus):
        return locus_text(self.corpus, locus)

    def rows_at(self, locus):
        return [r for r in self.rows if r["locus"] == locus]

    def patched(self, locus):
        t = self.text(locus)
        spans = sorted(((t.index(r["current"]), r) for r in self.rows_at(locus)), key=lambda x: x[0])
        for i, r in reversed(spans):
            t = t[:i] + r["replacement"] + t[i + len(r["current"]):]
        return t

    def anchors(self, locus):
        node, loc = locus.split("#")
        t, new = self.text(locus), self.patched(locus)
        out = []
        for e in self.map["entries"]:
            if (e["target_id"], e["target_locus"]) != (node, loc):
                continue
            a = e["target_anchor"]
            x = {"n": self.n_of(e), "class": e["class"], "anchor": a, "occurrences_now": t.count(a),
                 "survives_the_repair": new.count(a) == 1}
            if t.count(a) == 1:
                i = t.index(a)
                x["inside_span"], x["inside_sentence"] = [], []
                for r in self.rows_at(locus):
                    s0 = t.index(r["current"]); s1 = s0 + len(r["current"])
                    b0, b1 = sentence_bounds(t, s0, s1)
                    if i < s1 and i + len(a) > s0:
                        x["inside_span"].append(r["id"])
                    elif i < b1 and i + len(a) > b0:
                        x["inside_sentence"].append(r["id"])
            out.append((e, x))
        return out

    def routed_here(self, locus):
        out = []
        for e in self.map["entries"]:
            if e["class"] == "a" and locus in e.get("routing", {}).get("answered_by", []):
                n = self.n_of(e)
                ru = self.ruling.get(n)
                out.append((e, {"n": n, "target": "%s#%s" % (e["target_id"], e["target_locus"]),
                                "anchor": e["target_anchor"], "ruling_row": ru["row"] if ru else None,
                                "verdict": ru["verdict"] if ru else None}))
        return out


def knock_on(w):
    rows = []
    for locus in w.loci:
        for e, x in w.anchors(locus):
            if x.get("inside_span") or x.get("inside_sentence") or x["occurrences_now"] != 1:
                rows.append(dict({"kind": "anchor_meets_repair", "locus": locus}, **x))
        for e, x in w.routed_here(locus):
            rows.append(dict({"kind": "answer_routes_here", "locus": locus}, **x))
    for r in w.rows:
        sh = shingles(r["current"])
        for e in w.map["entries"]:
            for fld in ("adversarial_move", "grounds"):
                hit = sorted(s for s in sh if s in e[fld])
                if hit:
                    rows.append({"kind": "quoted_in_map", "row": r["id"], "locus": r["locus"], "n": w.n_of(e),
                                 "target": "%s#%s" % (e["target_id"], e["target_locus"]), "class": e["class"],
                                 "field": fld, "shingle": hit[0]})
    return {"map": w.record["pinned"]["map"], "rulings": w.record["pinned"]["rulings"], "corpus_md5": w.corpus_md5,
            "rows": rows}


def dossier(w, locus):
    node, loc = locus.split("#")
    t = w.text(locus)
    marked = t
    for r in sorted(w.rows_at(locus), key=lambda r: -t.index(r["current"])):
        i = t.index(r["current"])
        marked = marked[:i] + "⟦" + r["id"] + ": " + marked[i:i + len(r["current"])] + "⟧" + marked[i + len(r["current"]):]
    L = ["# `%s` · %s" % (locus, ", ".join("%s (%s)" % (r["id"], r["kind"]) for r in w.rows_at(locus))), "",
         "Corpus `%s` (%s); map `%s` `%s`; rulings `%s`." % (
             CORPUS, w.corpus_md5[:8], os.path.basename(w.record["pinned"]["map"]["file"]),
             w.record["pinned"]["map"]["md5"][:8], w.record["pinned"]["rulings"]["md5"][:8]), "",
         "## As a reader meets it now (%d words); each row's span in ⟦ ⟧" % len(t.split()), "",
         "> " + marked, "", "## With every row here applied (%d words)" % len(w.patched(locus).split()), "",
         "> " + w.patched(locus), ""]
    for r in w.rows_at(locus):
        L += ["## %s · %s · %s" % (r["id"], r["kind"], r["status"]), "",
              "- **replaces (%d words):** %s" % (r["words"]["current"], r["current"]),
              "- **with (%d words):** %s" % (r["words"]["replacement"], r["replacement"]),
              "- **cuts:** %s" % r["cuts"], "- **keeps:** %s" % r["keeps"], "- **how:** %s" % r["how"],
              "- **answers:** %s" % "; ".join(r["answers"]), ""]
    L += ["## Map v1_6 entries at this locus", ""]
    got = w.anchors(locus)
    if not got:
        L += ["None.", ""]
    for e, x in got:
        where = ("INSIDE %s's replaced span" % ", ".join(x["inside_span"]) if x.get("inside_span") else
                 "inside %s's sentence" % ", ".join(x["inside_sentence"]) if x.get("inside_sentence") else
                 "outside every repaired sentence" if x["occurrences_now"] == 1 else
                 "anchor occurs %d times now" % x["occurrences_now"])
        L += ["### (%s) #%s · \"%s\" · %s · %s" % (e["class"], x["n"] or "-", e["target_anchor"], where,
                                                  "survives" if x["survives_the_repair"] else "MOVES"),
              "", "- **move:** %s" % e["adversarial_move"], "- **grounds:** %s" % e["grounds"],
              "- **routing:** `%s`" % json.dumps(e["routing"], ensure_ascii=False), ""]
    L += ["## (a) entries of v1_6 answered here", ""]
    rh = w.routed_here(locus)
    if not rh:
        L += ["None.", ""]
    for e, x in rh:
        ru = w.ruling.get(x["n"])
        L += ["### #%s · `%s` · %s" % (x["n"], x["target"], x["verdict"]), "",
              "- **anchor:** \"%s\"" % e["target_anchor"], "- **move:** %s" % e["adversarial_move"],
              "- **grounds:** %s" % e["grounds"]]
        if ru:
            L.append("- **R1 %s:** %s" % (ru["row"], ru["reason"]))
        L.append("")
    L += ["## The node's other slots", ""]
    for s, txt in slots(w.corpus[node]):
        if s == loc:
            continue
        key = "flagship:%s#%s" % (node, s)
        rs = [r["id"] for r in w.rows_at("%s#%s" % (node, s))]
        L.append("- `%s` (%d words): reading class **%s**%s" % (
            s, len(txt.split()), w.cls.get(key, "no hit"), "; rows %s" % ", ".join(rs) if rs else ""))
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--knock-on", action="store_true")
    a = ap.parse_args()
    w = World()
    if a.knock_on:
        sys.stdout.write(json.dumps(knock_on(w), indent=1, ensure_ascii=False) + "\n")
        return
    if not a.out:
        sys.exit("--out <dir> or --knock-on")
    os.makedirs(a.out, exist_ok=True)
    for i, locus in enumerate(w.loci):
        name = "%02d_%s.md" % (i + 1, locus.replace("#", "__").replace(".", "_"))
        open(os.path.join(a.out, name), "w", encoding="utf-8").write(dossier(w, locus))
    open(os.path.join(a.out, "knock_on.json"), "w", encoding="utf-8").write(
        json.dumps(knock_on(w), indent=1, ensure_ascii=False) + "\n")
    print("wrote %d dossier(s) and knock_on.json under %s" % (len(w.loci), a.out))


if __name__ == "__main__":
    main()

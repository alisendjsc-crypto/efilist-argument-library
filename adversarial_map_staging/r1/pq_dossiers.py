#!/usr/bin/env python3
"""pq_dossiers.py -- the reading instrument for the pin-move queue's repairs (L5, 2026-09-26, R0150 phase 2).

One dossier per row of the newest pin_move_queue block in canon:
  - the locus as a reader meets it, in the pre-pin corpus, with the queued sentence(s) marked;
  - every entry of the ruled map (v1_6) at that locus, of any class, and whether its anchor lies inside a
    queued sentence (W-007, ruled at R0164: a repair moves every anchor inside its sentence);
  - the entry the row serves, as v1_6 holds it, with its current R1 row;
  - every (a) entry of v1_6 whose answer routes to the locus, with its current R1 verdict (R0150's knock-on
    list: a repair changes what those answers say; the lesson that reopened #46).
Also writes knock_on.json: the W-007 anchors and the knock-on (a)s as data, which the drafts gate recomputes.

Reads: the one canon; the corpus at the md5 map v1_6 pins (pinned.py, so it still reads after the pin);
map v1_6 at its md5; R1_rulings.json (current rows, supersessions applied); the R1 evidence ((a) entries).

  python3 pq_dossiers.py --out <dir>                  # every row
  python3 pq_dossiers.py --out <dir> --id PQ-17 PQ-08  # named rows
  python3 pq_dossiers.py --knock-on                    # print knock_on.json to stdout, write nothing

Repo-relative. Writes only under --out. Deterministic: every listing is in file order.
"""
import argparse, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import pinned  # noqa: E402

MAP = ("adversarial_map_staging/adversarial_map_v1_6.json", "7a69bc9fd197047c3cf7cecdb37a44ed")
RULINGS = "adversarial_map_staging/r1/R1_rulings.json"
EVID = "adversarial_map_staging/r1/R1_evidence_2026-09-19.json"
CORPUS = "efilist_argument_library_v4_0_0.json"


def load_json(b):
    return json.loads(b.decode("utf-8"))


def words(s):
    return len(s.split())


def locus_text(obj, locus):
    r = obj["responses"]
    if locus.startswith("archetypeVariants."):
        return r.get("archetypeVariants", {}).get(locus.split(".", 1)[1])
    if locus in r:
        return r[locus]
    return obj.get(locus)


class World:
    def __init__(self):
        canons = sorted(glob.glob(os.path.join(REPO, "project_canon_v38_*.json")))
        if len(canons) != 1:
            sys.exit("REFUSED: expected exactly one project_canon_v38_*.json, found %d" % len(canons))
        self.canon_rel = os.path.basename(canons[0])
        am = json.load(open(canons[0], encoding="utf-8"))["adversarial_map"]
        self.queue_key = [k for k in am if k.startswith("pin_move_queue_")][-1]
        self.rows = am[self.queue_key]["rows"]
        self.map = load_json(pinned.bytes_at(REPO, MAP[0], MAP[1]))
        self.corpus_md5 = self.map["meta"]["source_corpus_md5"]
        self.corpus = {o["id"]: o for o in load_json(pinned.bytes_at(REPO, CORPUS, self.corpus_md5))["objections"]}
        rows = json.load(open(os.path.join(REPO, RULINGS), encoding="utf-8"))["rows"]
        sup = {r["supersedes"] for r in rows if r.get("supersedes")}
        self.ruling = {r["n"]: r for r in rows if r["row"] not in sup}
        self.ev = {e["n"]: e for e in json.load(open(os.path.join(REPO, EVID), encoding="utf-8"))["entries"]}
        self.by_triple = {(e["target_id"], e["target_locus"], e["target_anchor"]): n for n, e in self.ev.items()}

    def n_of(self, e):
        return self.by_triple.get((e["target_id"], e["target_locus"], e["target_anchor"]))

    def text(self, locus):
        node, loc = locus.split("#")
        return locus_text(self.corpus[node], loc)

    def spans(self, row):
        t = self.text(row["locus"])
        out = []
        for s in row["sentences"]:
            assert t.count(s) == 1, "%s: a queued sentence is not once in its locus" % row["id"]
            out.append((t.index(s), t.index(s) + len(s)))
        return out

    def anchors_inside(self, row):
        """Every v1_6 entry at the row's locus whose anchor overlaps a queued sentence."""
        node, loc = row["locus"].split("#")
        t, sp = self.text(row["locus"]), self.spans(row)
        out = []
        for e in self.map["entries"]:
            if (e["target_id"], e["target_locus"]) != (node, loc):
                continue
            a = e["target_anchor"]
            if t.count(a) != 1:
                out.append({"entry": e, "inside": None, "why": "anchor occurs %d times in the locus" % t.count(a)})
                continue
            i = t.index(a)
            hit = [k for k, (s0, s1) in enumerate(sp) if i < s1 and i + len(a) > s0]
            whole = [k for k in hit if sp[k][0] <= i and i + len(a) <= sp[k][1]]
            out.append({"entry": e, "inside": hit, "whole": bool(hit) and len(whole) == len(hit)})
        return out

    def routed_here(self, row):
        """Every v1_6 (a) whose answered_by names the row's locus, with its #n and current R1 verdict."""
        out = []
        for e in self.map["entries"]:
            if e["class"] == "a" and row["locus"] in e["routing"].get("answered_by", []):
                n = self.n_of(e)
                out.append({"entry": e, "n": n, "ruling": self.ruling.get(n)})
        return out


def shingles(s, n=6):
    ws = s.split()
    return {" ".join(ws[i:i + n]) for i in range(max(0, len(ws) - n + 1))}


def knock_on(w, rows_in=None):
    """rows_in: queue-shaped rows ({id, locus, sentences}); default the canon queue's. A caller adding rows (the
    drafts gate's proposed companions) gets the same three lists for them."""
    rows = []
    for r in (rows_in if rows_in is not None else w.rows):
        sents = r["sentences"]
        for x in w.anchors_inside(r):
            if x["inside"]:
                e = x["entry"]
                rows.append({"kind": "anchor_inside", "pq": r["id"], "locus": r["locus"],
                             "sentences": ["%s%s" % (r["id"], "" if k == 0 else "." + str(k + 1)) for k in x["inside"]],
                             "n": w.n_of(e), "class": e["class"], "status": e.get("status"),
                             "anchor": e["target_anchor"], "anchor_wholly_inside": x["whole"]})
        for x in w.routed_here(r):
            e, n, ru = x["entry"], x["n"], x["ruling"]
            rows.append({"kind": "answer_routes_here", "pq": r["id"], "locus": r["locus"],
                         "n": n, "target": "%s#%s" % (e["target_id"], e["target_locus"]),
                         "anchor": e["target_anchor"], "verdict": ru["verdict"] if ru else None,
                         "ruling_row": ru["row"] if ru else None})
        # map text, anywhere in v1_6, that quotes six or more consecutive words of a repaired sentence: the
        # successor map re-reads these too (the frozen maps keep quoting the pinned corpus, which is correct)
        for k, s in enumerate(sents):
            sh = shingles(s)
            for e in w.map["entries"]:
                for fld in ("adversarial_move", "grounds"):
                    hit = sorted(x for x in sh if x in e[fld])
                    if hit:
                        rows.append({"kind": "quoted_in_map", "pq": r["id"],
                                     "sentence": "%s%s" % (r["id"], "" if k == 0 else "." + str(k + 1)),
                                     "n": w.n_of(e), "target": "%s#%s" % (e["target_id"], e["target_locus"]),
                                     "class": e["class"], "field": fld, "shingle": hit[0]})
    return {"queue_block": w.queue_key, "map": {"file": MAP[0], "md5": MAP[1]},
            "corpus_md5": w.corpus_md5, "rows": rows}


def dossier(w, r):
    L = []
    t = w.text(r["locus"])
    sp = w.spans(r)
    marked = t
    for k, (s0, s1) in sorted(enumerate(sp), key=lambda z: -z[1][0]):
        tag = r["id"] + ("" if k == 0 else "." + str(k + 1))
        marked = marked[:s0] + "⟦" + tag + ": " + marked[s0:s1] + "⟧" + marked[s1:]
    L.append("# %s · `%s` · serves %s" % (r["id"], r["locus"], ", ".join(r["serves"])))
    L.append("")
    L.append("Sources: queue `%s` in `%s`; corpus `%s` (%s); map `%s` `%s`; `%s`."
             % (w.queue_key, w.canon_rel, CORPUS, w.corpus_md5[:8], os.path.basename(MAP[0]), MAP[1][:8],
                os.path.basename(RULINGS)))
    L.append("")
    for k in ("section", "answers", "repair", "also", "note", "corrected"):
        if r.get(k):
            L.append("- **%s:** %s" % (k, r[k]))
    L.append("")
    L.append("## The locus as a reader meets it (%d words); the queued sentence(s) in ⟦ ⟧" % words(t))
    L.append("")
    L.append("> " + marked.replace("\n", "\n> "))
    L.append("")
    for k, s in enumerate(r["sentences"]):
        L.append("- %s%s: %d words" % (r["id"], "" if k == 0 else "." + str(k + 1), words(s)))
    L.append("")
    L.append("## Map v1_6 entries at this locus (W-007)")
    L.append("")
    for x in w.anchors_inside(r):
        e = x["entry"]
        where = ("INSIDE %s%s" % (", ".join("%s%s" % (r["id"], "" if k == 0 else "." + str(k + 1)) for k in x["inside"]),
                                  "" if x.get("whole") else " (overlaps the edge)")) if x["inside"] else \
                ("outside the queued sentence(s)" if x["inside"] == [] else x["why"])
        L.append("### (%s) #%s · anchor: \"%s\" · %s" % (e["class"], w.n_of(e) or "-", e["target_anchor"], where))
        L.append("")
        L.append("- **move:** %s" % e["adversarial_move"])
        L.append("- **grounds:** %s" % e["grounds"])
        L.append("- **routing:** `%s`" % json.dumps(e["routing"], ensure_ascii=False))
        L.append("- **status:** %s" % e.get("status"))
        L.append("")
    L.append("## What the row serves")
    L.append("")
    for tag in r["serves"]:
        n = int(tag.lstrip("#"))
        ev = w.ev.get(n)
        ru = w.ruling.get(n)
        cur = [e for e in w.map["entries"] if ev and w.n_of(e) == n]
        L.append("### #%d · evidence target `%s#%s`" % (n, ev["target_id"], ev["target_locus"]) if ev else "### #%d" % n)
        L.append("")
        for e in cur:
            L.append("- **v1_6 (%s)** anchor \"%s\"" % (e["class"], e["target_anchor"]))
            L.append("- **move:** %s" % e["adversarial_move"])
            L.append("- **grounds:** %s" % e["grounds"])
            L.append("- **routing:** `%s`" % json.dumps(e["routing"], ensure_ascii=False))
        if ru:
            L.append("- **R1 %s, %s:** %s" % (ru["row"], ru["verdict"], ru["reason"]))
            if ru.get("stronger_continuation"):
                L.append("- **stronger continuation:** %s" % ru["stronger_continuation"])
            for mr in ru.get("map_record") or []:
                L.append("- **map record** `%s`: \"%s\"" % (mr["at"], mr["quote"]))
        L.append("")
    L.append("## Knock-on: (a) entries of v1_6 answered at this locus")
    L.append("")
    rh = w.routed_here(r)
    if not rh:
        L.append("None.")
    for x in rh:
        e, n, ru = x["entry"], x["n"], x["ruling"]
        L.append("### #%s · `%s#%s` · %s" % (n, e["target_id"], e["target_locus"], ru["verdict"] if ru else "no R1 row"))
        L.append("")
        L.append("- **anchor:** \"%s\"" % e["target_anchor"])
        L.append("- **move:** %s" % e["adversarial_move"])
        L.append("- **grounds:** %s" % e["grounds"])
        if ru:
            L.append("- **R1 %s:** %s" % (ru["row"], ru["reason"]))
        L.append("")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--id", nargs="*")
    ap.add_argument("--knock-on", action="store_true")
    a = ap.parse_args()
    w = World()
    if a.knock_on:
        sys.stdout.write(json.dumps(knock_on(w), indent=1, ensure_ascii=False) + "\n")
        return
    if not a.out:
        sys.exit("--out <dir> or --knock-on")
    os.makedirs(a.out, exist_ok=True)
    n = 0
    for r in w.rows:
        if a.id and r["id"] not in a.id:
            continue
        open(os.path.join(a.out, "%s.md" % r["id"]), "w", encoding="utf-8").write(dossier(w, r))
        n += 1
    open(os.path.join(a.out, "knock_on.json"), "w", encoding="utf-8").write(
        json.dumps(knock_on(w), indent=1, ensure_ascii=False) + "\n")
    print("wrote %d dossier(s) and knock_on.json under %s" % (n, a.out))


if __name__ == "__main__":
    main()

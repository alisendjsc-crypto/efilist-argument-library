#!/usr/bin/env python3
"""pin_ratify_l5.py -- append his word to the repair record as one ratification row (L5, 2026-09-26, R0150 phase 4).

The row names EXACTLY the rows his word ratifies. They are copied from gate2's list in canon
(adversarial_map.pin_repair_redrafts_judgment_gate2.the_text_his_word_would_ratify), never typed: --set all takes its
drafts and companions, --set drafts only the drafts (if he admits no companion). His words go in verbatim, with the
relay that carried them; the judgment the row answers is the newest one, with the first beside it.

The record is append-only; this adds one row and changes no other byte of meaning. Then run
adversarial_map_staging/r1/pin_repair_drafts_gate_v0_2.py (G10 checks the row) before anything is applied.

  python3 tools/pin_ratify_l5.py --words "<his words>" --said "<when, where>" --relay R0nnn --set all
"""
import argparse, glob, hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
RECORD = "adversarial_map_staging/r1/PQ_repair_drafts_L5.json"
INDEX = os.path.expanduser("~/Downloads/Claude Code/relays/RELAY_INDEX.tsv")
JUDGMENTS = [("adversarial_map_staging/r1/PQ_repair_redrafts_judgments.json", "612ab672"),
             ("adversarial_map_staging/r1/PQ_repair_drafts_judgments.json", "2ed68a7c")]


def md5(rel):
    return hashlib.md5(open(os.path.join(REPO, rel), "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--words", required=True)
    ap.add_argument("--said", required=True)
    ap.add_argument("--relay", required=True)
    ap.add_argument("--relay-md5")
    ap.add_argument("--set", default="all", choices=["all", "drafts"])
    a = ap.parse_args()
    canons = glob.glob(os.path.join(REPO, "project_canon_v38_*.json"))
    assert len(canons) == 1, canons
    lst = json.load(open(canons[0], encoding="utf-8"))["adversarial_map"]["pin_repair_redrafts_judgment_gate2"][
        "the_text_his_word_would_ratify"]
    assert lst["drafts_record"]["md5"] == "496c3a5c63541d8657e7d7e949e43648"
    rows = lst["drafts"] + (lst["companions"] if a.set == "all" else [])
    relay_md5 = a.relay_md5
    if not relay_md5 and os.path.exists(INDEX):
        for line in open(INDEX, encoding="utf-8"):
            p = line.rstrip("\n").split("\t")
            if len(p) > 8 and p[1] == "SENT" and p[2] == a.relay:
                relay_md5 = p[8]
    assert relay_md5 and len(relay_md5) == 32, "the relay's md5 is not in the index; pass --relay-md5"
    for rel, pre in JUDGMENTS:
        assert md5(rel).startswith(pre), "%s moved" % rel
    rec = json.load(open(os.path.join(REPO, RECORD), encoding="utf-8"))
    assert not any(r["kind"] == "ratification" for r in rec["rows"]), "a ratification row already exists"
    by = {r["id"]: r for r in rec["rows"]}
    sup = {r["supersedes"] for r in rec["rows"] if r.get("supersedes")}
    for x in rows:
        assert x in by and x not in sup, "%s is not a current row" % x
    seat = by[rows[0]]["seat"]
    rec["rows"].append({
        "id": "PR-01", "kind": "ratification", "rows": rows, "his_words_verbatim": a.words, "said": a.said,
        "relay": {"relay": a.relay, "md5": relay_md5},
        "judgment": {"file": JUDGMENTS[0][0], "md5": md5(JUDGMENTS[0][0]),
                     "first": {"file": JUDGMENTS[1][0], "md5": md5(JUDGMENTS[1][0])}},
        "seat": seat, "date": "2026-09-26", "supersedes": None})
    open(os.path.join(REPO, RECORD), "wb").write((json.dumps(rec, indent=1, ensure_ascii=False) + "\n").encode("utf-8"))
    print("PR-01 appended: %d rows (%d drafts, %d companions); relay %s %s" % (
        len(rows), len(lst["drafts"]), len(rows) - len(lst["drafts"]), a.relay, relay_md5[:8]))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""pin_ratify_l6.py -- append his word to the safety pass's record as one ratification row (L6, 2026-09-26, R0193 order 4).

The row names EXACTLY the rows his word ratifies. They are copied from gate2's list in canon
(adversarial_map.safety_pass_redraft_judgment_gate2.the_text_his_word_ratifies), never typed, and must be current rows
of the record. His words go in verbatim, with the relay whose asks they answer; the judgment the row answers is the
newest (the one-row judgment of SD-10), with the first beside it.

The record is append-only; this adds one row and changes no other byte of meaning. Then run
adversarial_map_staging/r1/sp_drafts_gate_l6_v0_2.py (G11 checks the row) before anything is applied.

  python3 tools/pin_ratify_l6.py --words "<his words>" --said "<when, where>" --relay R0nnn
"""
import argparse, glob, hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
RECORD = "adversarial_map_staging/r1/SP_drafts_L6.json"
RECORD_MD5 = "8742b882b6055761207c7dc1618b645b"   # the record gate2's list names
INDEX = os.path.expanduser("~/Downloads/Claude Code/relays/RELAY_INDEX.tsv")
JUDGMENTS = [("adversarial_map_staging/r1/SP_redrafts_judgments.json", "3cd8dbb92a034351fb28c63dbb3a74ad"),
             ("adversarial_map_staging/r1/SP_drafts_judgments.json", "437013204cfafc4c740a763e1fb79349")]


def md5(rel):
    return hashlib.md5(open(os.path.join(REPO, rel), "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--words", required=True)
    ap.add_argument("--said", required=True)
    ap.add_argument("--relay", required=True)
    a = ap.parse_args()
    canons = glob.glob(os.path.join(REPO, "project_canon_v38_*.json"))
    assert len(canons) == 1, canons
    block = json.load(open(canons[0], encoding="utf-8"))["adversarial_map"]["safety_pass_redraft_judgment_gate2"]
    lst = block["the_text_his_word_ratifies"]
    assert lst["drafts_record"]["md5"] == RECORD_MD5 == md5(RECORD), "the record is not the one gate2's list names"
    assert block["his_word"]["verbatim"] == a.words, "the words differ from the words gate2 recorded"
    rows = lst["drafts"] + lst["companions_and_widening"]
    relay_md5 = None
    for line in open(INDEX, encoding="utf-8"):
        p = line.rstrip("\n").split("\t")
        if len(p) > 8 and p[1] == "SENT" and p[2] == a.relay:
            relay_md5 = p[8]
    assert relay_md5 and len(relay_md5) == 32, "the relay's md5 is not in the index"
    assert relay_md5 == block["his_word"]["asks"]["md5"], "the relay is not the one his word answers"
    for rel, m in JUDGMENTS:
        assert md5(rel) == m, "%s moved" % rel
    rec = json.load(open(os.path.join(REPO, RECORD), encoding="utf-8"))
    assert not any(r["kind"] == "ratification" for r in rec["rows"]), "a ratification row already exists"
    by = {r["id"]: r for r in rec["rows"]}
    sup = {r["supersedes"] for r in rec["rows"] if r.get("supersedes")}
    for x in rows:
        assert x in by and x not in sup and by[x]["kind"] in ("draft", "companion", "widening"), \
            "%s is not a current row of a patching kind" % x
    current = [r["id"] for r in rec["rows"] if r["id"] not in sup and r["kind"] in ("draft", "companion", "widening")]
    assert sorted(current) == sorted(rows), "his word ratifies every current row; the lists differ"
    rec["rows"].append({
        "id": "SR-01", "kind": "ratification", "rows": rows, "his_words_verbatim": a.words, "said": a.said,
        "relay": {"relay": a.relay, "md5": relay_md5},
        "judgment": {"file": JUDGMENTS[0][0], "md5": JUDGMENTS[0][1],
                     "first": {"file": JUDGMENTS[1][0], "md5": JUDGMENTS[1][1]}},
        "seat": by[rows[0]]["seat"], "date": "2026-09-26", "supersedes": None})
    open(os.path.join(REPO, RECORD), "wb").write((json.dumps(rec, indent=1, ensure_ascii=False) + "\n").encode("utf-8"))
    print("SR-01 appended: %d rows (%d drafts, %d companions and widening); relay %s %s" % (
        len(rows), len(lst["drafts"]), len(lst["companions_and_widening"]), a.relay, relay_md5[:8]))


if __name__ == "__main__":
    main()

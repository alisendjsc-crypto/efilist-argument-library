#!/usr/bin/env python3
"""tools/v38_52_his_words.json -- his word owed to canon v38.52, cut byte-exact from the user turn where he said it.

Read at the user turn, never at a search hit (gate2's law; R0309): the excerpt is an exact, unique substring of one human
turn in seat l's V2b transcript (f5e10266-5519-4820-8d43-cd27cfcfdcf0), located by its own words, and the turn is pinned
by the md5 of its text. The excerpt also names the seat's message it answers (the last assistant text before the turn),
by line and md5.

His word answers R0314 (gate2 -> josiah, the three asks of V3b's round-two judgment); R0315 (V2b -> l, this session's
kickoff) carries it. Both relays are read at the md5 the relay index gives them; R0315 must carry the word verbatim and
name the turn. Relays are named by id and md5 only: a relay's filename carries its topic.

The transcript and the relays live outside the repository and may be cleaned up or moved; this tool then cannot run,
and the committed output stands as the record. canon v38.52's builder reads the output at its md5 and never needs them.

  python3 tools/extract_his_words_v38_52.py [--check]
"""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "tools", "v38_52_his_words.json")
SID = "f5e10266-5519-4820-8d43-cd27cfcfdcf0"
TRANSCRIPT = os.path.join(os.path.expanduser("~/.claude/projects"), "-home-josiahscooper-Projects-efilist-argument-library",
                          SID + ".jsonl")
DESK = os.path.expanduser("~/Downloads/Claude Code/relays")
INDEX = os.path.join(DESK, "RELAY_INDEX.tsv")
# (key, turn md5, relays, the unique public substring of the turn)
SPEC = [("R0314_word", "2d211155785a303e9ac638b4c17edfaa", {"answers": "R0314", "recorded_by": "R0315"},
         "Proceed with your recommendations")]
RELAYS = ["R0314", "R0315"]
CARRIES_WORD = {"R0315": "R0314_word"}


def md5(s):
    return hashlib.md5(s.encode("utf-8")).hexdigest()


def turns(path):
    """Every human user turn (not a tool result, not meta, not a side chain, origin kind human), and for each the last
    assistant text before it."""
    last = None
    for i, line in enumerate(open(path, encoding="utf-8")):
        o = json.loads(line)
        c = (o.get("message") or {}).get("content")
        if o.get("type") == "assistant" and isinstance(c, list):
            t = "\n".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
            if t.strip():
                last = {"line": i + 1, "utc": o.get("timestamp"), "text_md5": md5(t)}
            continue
        if o.get("type") != "user" or o.get("isMeta") or o.get("isSidechain"):
            continue
        if (o.get("origin") or {}).get("kind") != "human":
            continue
        if isinstance(c, list):
            if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in c):
                continue
            c = "\n".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
        if c and c.strip():
            yield i + 1, o.get("timestamp"), c, last


def relays():
    """Each relay's SENT row from the append-only index, its body read at that md5."""
    got = {}
    for line in open(INDEX, encoding="utf-8"):
        f = line.rstrip("\n").split("\t")
        if len(f) > 8 and f[1] == "SENT":
            got[f[2]] = (f[7], f[8], f[3], f[4])
    out = {}
    for rid in RELAYS:
        name, m, frm, to = got[rid]
        raw = open(os.path.join(DESK, name), "rb").read()
        assert hashlib.md5(raw).hexdigest() == m, "%s: the drop dir file moved from the index's md5" % rid
        out[rid] = (m, frm, to, raw.decode("utf-8"))
    return out


def build():
    T = {}
    for line, ts, text, prev in turns(TRANSCRIPT):
        T[md5(text)] = {"line": line, "utc": ts, "text": text, "answers_message": prev}
    rec = {"what": "his word owed to canon v38.52, cut byte-exact from the user turn (V5, seat l, 2026-10-04)",
           "tool": "tools/extract_his_words_v38_52.py", "transcript": {"V2b": SID}, "excerpts": {}}
    for key, tmd5, rel, s in SPEC:
        t = T.get(tmd5)
        assert t, "%s: turn %s not found as a human turn" % (key, tmd5)
        text = t["text"]
        i = text.find(s)
        assert i >= 0 and text.find(s, i + 1) < 0, "%s: the words are not in the turn exactly once" % key
        ex = text[i:i + len(s)]
        rec["excerpts"][key] = dict(rel, turn={"transcript": "V2b", "line": t["line"], "utc": t["utc"], "turn_md5": tmd5},
                                    answers_message={"seat": "l (V2b)", **t["answers_message"]}, offsets=[i, i + len(s)],
                                    md5=md5(ex), words=len(ex.split()), whole_turn=(text == s), text=ex)
    R = relays()
    rec["relays"] = {}
    for rid, (m, frm, to, body) in R.items():
        row = {"md5": m, "from": frm, "to": to}  # no filename: a relay's topic slug can summarise its content
        if rid in CARRIES_WORD:
            e = rec["excerpts"][CARRIES_WORD[rid]]
            assert e["text"] in body, "%s: does not carry %r" % (rid, e["text"])
            assert e["turn"]["turn_md5"] in body and ("line %d" % e["turn"]["line"]) in body, "%s: names another turn" % rid
            assert e["answers_message"]["text_md5"] in body, "%s: names another message" % rid
            row["carries"] = CARRIES_WORD[rid]
            row["names_the_turn"] = True
        rec["relays"][rid] = row
    return (json.dumps(rec, indent=1, ensure_ascii=False) + "\n").encode("utf-8")


def main():
    out = build()
    if "--check" in sys.argv:
        same = open(OUT, "rb").read() == out
        print("HIS WORDS v38.52: %s" % ("matches the committed record" if same else "DIFFERS"))
        sys.exit(0 if same else 1)
    open(OUT, "wb").write(out)
    print("tools/v38_52_his_words.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))


if __name__ == "__main__":
    main()

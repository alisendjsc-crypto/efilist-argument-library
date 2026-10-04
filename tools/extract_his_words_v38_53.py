#!/usr/bin/env python3
"""tools/v38_53_his_words.json -- his word owed to canon v38.53, cut byte-exact from the user turn where he said it.

Read at the user turn, never at a search hit (gate2's law; R0309): the excerpt is an exact, unique substring of one human
turn in seat l's V5 transcript (e013cfb0-df3e-4174-b2ea-e9c65822debb), located by its own words, and the turn is pinned
by the md5 of its text. The excerpt also names the seat's message it answers (the last assistant text before the turn),
by line and md5.

His word answers R0316 (V5 -> josiah, the eight rulings RV-1..RV-8 of the responseVariants design, with leans); R0318
(V5 -> l, V6's kickoff) carries it. Both relays are read at the md5 the relay index gives them; R0318 must carry the word
verbatim and name the turn. Relays are named by id and md5 only: a relay's filename carries its topic.

The turn has two sentences of instruction. The first is the word (it adopts RV-1..RV-8 as leaned); the whole turn is
recorded too, as said with it (V6's kickoff, R0318: "The rest of the turn is public too"). Both excerpts are public.

The transcript and the relays live outside the repository and may be cleaned up or moved; this tool then cannot run,
and the committed output stands as the record. canon v38.53's builder reads the output at its md5 and never needs them.

  python3 tools/extract_his_words_v38_53.py [--check]
"""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "tools", "v38_53_his_words.json")
SID = "e013cfb0-df3e-4174-b2ea-e9c65822debb"
TRANSCRIPT = os.path.join(os.path.expanduser("~/.claude/projects"), "-home-josiahscooper-Projects-efilist-argument-library",
                          SID + ".jsonl")
DESK = os.path.expanduser("~/Downloads/Claude Code/relays")
INDEX = os.path.join(DESK, "RELAY_INDEX.tsv")
# (key, turn md5, relays, the unique public substring of the turn)
TURN = "4dace677153a5e04d76bd77caa032ca1"
SPEC = [("R0316_word", TURN, {"answers": "R0316", "recorded_by": "R0318"},
         "Proceed with your recommendations on all of the above."),
        ("R0316_whole_turn", TURN, {"answers": "R0316", "recorded_by": "R0318"}, None)]
RELAYS = ["R0316", "R0318"]
CARRIES_WORD = {"R0318": "R0316_whole_turn"}


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
    rec = {"what": "his word owed to canon v38.53, cut byte-exact from the user turn (V6, seat l, 2026-10-04)",
           "tool": "tools/extract_his_words_v38_53.py", "transcript": {"V5": SID}, "excerpts": {}}
    for key, tmd5, rel, s in SPEC:
        t = T.get(tmd5)
        assert t, "%s: turn %s not found as a human turn" % (key, tmd5)
        text = t["text"]
        s = text if s is None else s
        i = text.find(s)
        assert i >= 0 and text.find(s, i + 1) < 0, "%s: the words are not in the turn exactly once" % key
        ex = text[i:i + len(s)]
        rec["excerpts"][key] = dict(rel, turn={"transcript": "V5", "line": t["line"], "utc": t["utc"], "turn_md5": tmd5},
                                    answers_message={"seat": "l (V5)", **t["answers_message"]}, offsets=[i, i + len(s)],
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
        print("HIS WORDS v38.53: %s" % ("matches the committed record" if same else "DIFFERS"))
        sys.exit(0 if same else 1)
    open(OUT, "wb").write(out)
    print("tools/v38_53_his_words.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""tools/v38_50_his_words.json -- his words owed to canon v38.50, cut byte-exact from the user turns where he said them.

Read at the user turn, never at a search hit (gate2's law; R0309): each public excerpt is an exact, unique substring of
one human turn in seat l's V2 transcript (b664995c-43f2-4ec1-877b-d18b71cb68d8), located by its own words, and each turn
is pinned by the md5 of its text. Each excerpt also names the seat's message it answers (the last assistant text before
the turn), by line and md5.

His private statements (R0300, R0302, R0304, and the rest of his 22:51 MST turn that R0309 quotes) are recorded by turn,
md5 and offsets only, never as text, and this tool carries none of their words: a private excerpt is a whole turn, or the
part of a turn before a public word, located by that word's offset. This repository is public; the texts live in the
relays named, on the operator's desk (R0309's law). Each relay is read at the md5 the relay index gives it, and its
first quotation is asserted equal to the turn, so the relay is shown to carry the exact text. Relays are named by id and
md5 only: a relay's filename carries its topic, which can summarise a private statement.

The July line R0300 adds to the R-V6 batch (vault raw/facebook/2026/fb-2026-07.md, body line 25 by the vault's
grep_sources numbering) is located through R0300's own quotation and recorded by md5 and offsets only.

The transcript, the relays and the vault live outside the repository and may be cleaned up or moved; this tool then
cannot run, and the committed output stands as the record. canon v38.50's builder reads the output at its md5 and never
needs them.

  python3 tools/extract_his_words_v38_50.py [--check]
"""
import hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "tools", "v38_50_his_words.json")
SID = "b664995c-43f2-4ec1-877b-d18b71cb68d8"
TRANSCRIPT = os.path.join(os.path.expanduser("~/.claude/projects"), "-home-josiahscooper-Projects-efilist-argument-library",
                          SID + ".jsonl")
DESK = os.path.expanduser("~/Downloads/Claude Code/relays")
INDEX = os.path.join(DESK, "RELAY_INDEX.tsv")
VAULT_REL = "raw/facebook/2026/fb-2026-07.md"
VAULT = (os.path.join(os.path.expanduser("~/Documents/Obsidian Vault"), VAULT_REL), "01ccc618713a165585a5acc5f51b4cb8")
WITHHELD = ("recorded by turn, md5 and offsets only: this repository is public, and his private statements stay in the "
            "relays named (R0309's law)")
# (key, turn md5, relays, how it is cut, how it is recorded)
#   ("words", s):       the unique substring s of the turn (public)
#   ("whole", None):    the whole turn (private)
#   ("before", s):      the turn up to the unique public substring s, trailing whitespace stripped (private)
SPEC = [
    ("R0298_word", "d80c299aa385b0ae56b6b9c5e3f5f339", {"answers": "R0298", "recorded_by": "R0299"},
     ("words", "Go with your recommendations on all of the above."), "text"),
    ("R0300_gloss", "69964e34acdf2687f06e659fc863ee4f", {"recorded_by": "R0300"}, ("whole", None), "md5_only"),
    ("R0302_followup", "798ed6c18977308f7d3b5385d0a8460c", {"recorded_by": "R0302"}, ("whole", None), "md5_only"),
    ("R0304_third_followup", "545fdc8cd255c4abf05e0bc39eb609c5", {"recorded_by": "R0304"}, ("whole", None), "md5_only"),
    ("R0308_word", "327c7ceb3a68bfe317a55f44f87c17f7", {"answers": "R0308", "recorded_by": "R0309"},
     ("words", "Go with your recommendations on the rest."), "text"),
    ("R0309_statement_2251", "327c7ceb3a68bfe317a55f44f87c17f7", {"recorded_by": "R0309"},
     ("before", "Go with your recommendations on the rest."), "md5_only"),
]
# relays whose first quotation must equal a whole turn, and relays that must carry a public word
QUOTE_EQUALS_TURN = {"R0300": "69964e34acdf2687f06e659fc863ee4f", "R0302": "798ed6c18977308f7d3b5385d0a8460c",
                     "R0304": "545fdc8cd255c4abf05e0bc39eb609c5", "R0309": "327c7ceb3a68bfe317a55f44f87c17f7"}
CARRIES_WORD = {"R0299": "R0298_word", "R0309": "R0308_word"}


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
            got[f[2]] = (f[7], f[8])
    out = {}
    for rid in sorted(set(QUOTE_EQUALS_TURN) | set(CARRIES_WORD)):
        name, m = got[rid]
        raw = open(os.path.join(DESK, name), "rb").read()
        assert hashlib.md5(raw).hexdigest() == m, "%s: the drop dir file moved from the index's md5" % rid
        out[rid] = (name, m, raw.decode("utf-8"))
    return out


def first_quote(body):
    q, started = [], False
    for ln in body.splitlines():
        if ln.startswith(">"):
            q.append(ln[2:] if ln.startswith("> ") else ln[1:])
            started = True
        elif started:
            break
    return "\n".join(q)


def build():
    T = {}
    for line, ts, text, prev in turns(TRANSCRIPT):
        T[md5(text)] = {"line": line, "utc": ts, "text": text, "answers_message": prev}
    rec = {"what": ("his words owed to canon v38.50, cut byte-exact from the user turns (V2b, seat l, 2026-10-03); his "
                    "private statements by turn, md5 and offsets only"),
           "tool": "tools/extract_his_words_v38_50.py", "transcript": {"V2": SID}, "excerpts": {}}
    for key, tmd5, rel, (how, s), rec_as in SPEC:
        t = T.get(tmd5)
        assert t, "%s: turn %s not found as a human turn" % (key, tmd5)
        text = t["text"]
        if how == "whole":
            a, b = 0, len(text)
        else:
            i = text.find(s)
            assert i >= 0 and text.find(s, i + 1) < 0, "%s: the words are not in the turn exactly once" % key
            a, b = (i, i + len(s)) if how == "words" else (0, len(text[:i].rstrip()))
            if how == "before":
                assert text[i:].strip() == s, "%s: the public word does not close the turn" % key
        ex = text[a:b]
        item = dict(rel, turn={"transcript": "V2", "line": t["line"], "utc": t["utc"], "turn_md5": tmd5},
                    answers_message={"seat": "l (V2)", **t["answers_message"]}, offsets=[a, b], md5=md5(ex),
                    words=len(ex.split()))
        if rec_as == "text":
            item["text"] = ex
        else:
            item["text_withheld"] = WITHHELD
            if how == "whole":
                item["whole_turn"] = True
        rec["excerpts"][key] = item

    R = relays()
    rec["relays"] = {}
    for rid, (name, m, body) in R.items():
        row = {"md5": m}  # no filename: a relay's topic slug can summarise a private statement
        if rid in QUOTE_EQUALS_TURN:
            row["first_quote_equals_turn"] = first_quote(body) == T[QUOTE_EQUALS_TURN[rid]]["text"]
            assert row["first_quote_equals_turn"], "%s: its quotation is not the turn" % rid
            row["turn_md5"] = QUOTE_EQUALS_TURN[rid]
        if rid in CARRIES_WORD:
            w = rec["excerpts"][CARRIES_WORD[rid]]["text"]
            assert w in body, "%s: does not carry %r" % (rid, w)
            row["carries"] = CARRIES_WORD[rid]
        rec["relays"][rid] = row
    # R0304 printed its turn md5 as a placeholder; the turn above is pinned by the md5 measured at the turn
    r0304 = R["R0304"][2]
    assert "turn md5 `md5`" in r0304 and SPEC[3][1] not in r0304
    rec["relays"]["R0304"]["turn_md5_as_printed"] = "md5 (a placeholder; measured at the turn: see excerpts)"

    # the July line, located through R0300's own quotation; md5 and offsets only
    raw = open(VAULT[0], "rb").read()
    assert hashlib.md5(raw).hexdigest() == VAULT[1], "the vault file moved"
    vt = raw.decode("utf-8")
    m = re.search(r"\(vault `fb-2026-07` L25, authorship josiah\): \"(.*?)\" That quote stops", R["R0300"][2])
    ex = m.group(1)
    lines = vt.split("\n")
    assert lines[0] == "---"
    close = lines.index("---", 1)
    body = lines[close + 1:]
    hits = [(n + 1, ln.find(ex)) for n, ln in enumerate(lines) if ex in ln]
    assert vt.count(ex) == len(hits) == 2 and body[24].find(ex) == 0, hits
    line = close + 1 + 25
    assert hits[0] == (line, 0)
    rec["july_line"] = {
        "file": "~/Documents/Obsidian Vault/" + VAULT_REL, "file_md5": VAULT[1],
        "line": line, "body_line": 25, "numbering": "body_line counts from the line after the front matter, as the "
        "vault's claude/tools/grep_sources.py does; R0300's 'L25'",
        "line_md5": md5(lines[line - 1]), "line_words": len(lines[line - 1].split()),
        "excerpt": {"as_quoted_by": "R0300", "offsets": [0, len(ex)], "md5": md5(ex), "words": len(ex.split())},
        "also_at": [{"line": n, "offset": o} for n, o in hits[1:]],
        "authorship": "josiah (the vault's label)",
        "text_withheld": ("recorded by md5 and offsets only, as R0300 asks: the line reaches the adversarial side only "
                          "when the R-V6 intake drafts it, with his 2026-10-03 gloss beside it")}
    return (json.dumps(rec, indent=1, ensure_ascii=False) + "\n").encode("utf-8")


def main():
    out = build()
    if "--check" in sys.argv:
        same = open(OUT, "rb").read() == out
        print("HIS WORDS v38.50: %s" % ("matches the committed record" if same else "DIFFERS"))
        sys.exit(0 if same else 1)
    open(OUT, "wb").write(out)
    print("tools/v38_50_his_words.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))


if __name__ == "__main__":
    main()

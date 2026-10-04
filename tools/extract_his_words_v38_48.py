#!/usr/bin/env python3
"""tools/v38_48_his_words.json -- his words owed to canon v38.48, cut byte-exact from the user turns where he said them.

Read at the user turn, never at a search hit (gate2's law; R0295): each excerpt is an exact, unique substring of one
human turn in a Claude Code transcript, located by its opening and closing words, and each turn is pinned by the md5 of
its text. Two transcripts:
  vault V2   038df8e5-141f-4cb5-babe-d1c4caa5aaed   his word on R0272 (relayed as R0274), 2026-10-02
  L8         87cc1d8f-fbf4-44dc-981f-9b205c311dbf   his answers behind R0290, R0292, R0294, R0295 and R0296, 2026-10-03

One sentence is recorded by md5 and offsets only, never as text: the resentment line R0292 item 3 adopts as an R-V6
candidate. This repository is public, and that line goes to the adversarial side only with his framing beside it, when
the intake drafts it (V2's choice, reversible on his word).

The transcripts live outside the repository and may be cleaned up; this tool then cannot run, and the committed output
stands as the record. canon v38.48's builder reads the output at its md5 and never needs the transcripts.

  python3 tools/extract_his_words_v38_48.py [--check]
"""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "tools", "v38_48_his_words.json")
PROJ = os.path.expanduser("~/.claude/projects")
NOTES = (os.path.expanduser("~/Documents/Obsidian Vault/claude/analyses/library-crossref-notes-2026-10-02.md"),
         "71f31df9ad4e1b41da40922e62f21669")
TRANSCRIPTS = {
    "vault_V2": ("-home-josiahscooper-Documents-Obsidian-Vault", "038df8e5-141f-4cb5-babe-d1c4caa5aaed"),
    "L8": ("-home-josiahscooper-Projects-efilist-argument-library", "87cc1d8f-fbf4-44dc-981f-9b205c311dbf"),
}
# (key, transcript, turn md5, relay it stands behind, opening words, closing words, how it is recorded)
SPEC = [
    ("R0274_word", "vault_V2", "1c3d23785b363272ee12d6eafbf56342", "R0274",
     "Go with your recommendations on all of the above.", None, "text"),
    ("R0274_pleasure_account", "vault_V2", "1c3d23785b363272ee12d6eafbf56342", "R0274",
     "The library believed granted", "it does not completely defeat them.", "text"),
    ("R0290_not_a_mirror", "L8", "c7692763fa1f1ac503908f079e277530", "R0290",
     "The library is not meant to be", "description of antinatalists.", "text"),
    ("R0290_numbers_game", "L8", "c7692763fa1f1ac503908f079e277530", "R0290",
     "For me, it's more of a numbers game.", "almost entirely.", "text"),
    ("R0290_resentment_line", "L8", "c7692763fa1f1ac503908f079e277530", "R0290",
     "I don't like people,", "throughout history and today.", "md5_only"),
    ("R0290_relief_account", "L8", "c7692763fa1f1ac503908f079e277530", "R0290",
     "On the pleasure being merely illusory", "regardless.", "text"),
    ("R0290_proceed_line", "L8", "c7692763fa1f1ac503908f079e277530", "R0290",
     "Proceed on the previous", "if you can now.", "text"),
    ("R0292_argument", "L8", "61cea7813b9998589cd38f63deff7ed5", "R0292",
     "\"Needing a condition isn't the same", "than the adversarial take.", "text"),
    ("R0292_word", "L8", "61cea7813b9998589cd38f63deff7ed5", "R0292",
     "Go with your recommendations on the rest.", None, "text"),
    ("R0292_keep_to_it", "L8", "61cea7813b9998589cd38f63deff7ed5", "R0292",
     "Note I don't want you to agree", "keep to it.", "text"),
    ("R0292_open_disagreement", "L8", "61cea7813b9998589cd38f63deff7ed5", "R0292",
     "Some things I admit we won't come to an agreement on", "agree on ultimately.", "text"),
    ("R0294_account", "L8", "00b7dda99e83710ebcd568f9c12375d7", "R0294",
     "What is the state before liking?", "not a staunch adversarial.", "text"),
    ("R0294_alternative", "L8", "00b7dda99e83710ebcd568f9c12375d7", "R0294",
     "On \"alternative\":", "unless you have a better idea.", "text"),
    ("R0294_relief_thesis_noted", "L8", "00b7dda99e83710ebcd568f9c12375d7", "R0294",
     "Noted on the", "regardless of what I believe here.", "text"),
    ("R0294_word", "L8", "00b7dda99e83710ebcd568f9c12375d7", "R0294",
     "\"Go with your recommendations on the rest\"", None, "text"),
    ("R0295_parsimony_and_deprivation_test", "L8", "728eacfe3c84a830a26e93e4d9a35c14", "R0295",
     "\"Parsimony now cuts against you\"", "(deficit to relief).", "text"),
    ("R0295_word", "L8", "728eacfe3c84a830a26e93e4d9a35c14", "R0295",
     "Generate next session's prompt as you recommend.", None, "text"),
    ("R0296_concession", "L8", "83e32a25c4ca95260519240a703fa8db", "R0296",
     "I concede that i reliability", "and has for many years.", "text"),
    ("R0296_pointer", "L8", "83e32a25c4ca95260519240a703fa8db", "R0296",
     "I am not sure if the Obsidian Vault relayed to you this section where I argue for life, in an obscure "
     "anecdote I forgot about", None, "text"),
]


def md5(s):
    return hashlib.md5(s.encode("utf-8")).hexdigest()


def human_turns(path):
    """Every human user turn: not a tool result, not meta, not a side chain, origin kind human."""
    for i, line in enumerate(open(path, encoding="utf-8")):
        o = json.loads(line)
        if o.get("type") != "user" or o.get("isMeta") or o.get("isSidechain"):
            continue
        if (o.get("origin") or {}).get("kind") != "human":
            continue
        c = (o.get("message") or {}).get("content")
        if isinstance(c, list):
            if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in c):
                continue
            c = "\n".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
        if c and c.strip():
            yield i + 1, o.get("timestamp"), c


def build():
    turns = {}
    for key, (proj, sid) in TRANSCRIPTS.items():
        path = os.path.join(PROJ, proj, sid + ".jsonl")
        for line, ts, text in human_turns(path):
            turns[md5(text)] = {"transcript": key, "session": sid, "line": line, "utc": ts, "text": text}
    rec = {"what": "his words owed to canon v38.48, cut byte-exact from the user turns (V2, seat l, 2026-10-03)",
           "tool": "tools/extract_his_words_v38_48.py", "transcripts": {k: v[1] for k, v in TRANSCRIPTS.items()},
           "excerpts": {}}
    for key, tkey, tmd5, relay, start, end, how in SPEC:
        t = turns.get(tmd5)
        assert t and t["transcript"] == tkey, "%s: turn %s not found as a human turn in %s" % (key, tmd5, tkey)
        text = t["text"]
        a = text.find(start)
        assert a >= 0 and text.find(start, a + 1) < 0, "%s: opening words not found exactly once" % key
        b = a + len(start) if end is None else text.find(end, a) + len(end)
        assert b > a and (end is None or text.find(end, a) >= 0), "%s: closing words not found" % key
        ex = text[a:b]
        item = {"relay": relay, "turn": {"transcript": tkey, "line": t["line"], "utc": t["utc"], "turn_md5": tmd5},
                "offsets": [a, b], "md5": md5(ex), "words": len(ex.split())}
        if how == "text":
            item["text"] = ex
        else:
            item["text_withheld"] = ("recorded by md5 and offsets only: this repository is public, and the line "
                                     "reaches the adversarial side only with his framing beside it (R0292 item 3)")
        rec["excerpts"][key] = item
    # the six recommendations his R0274 word adopted, verbatim from the vault seat's notes at their md5 (seat's words)
    raw = open(NOTES[0], "rb").read()
    assert hashlib.md5(raw).hexdigest() == NOTES[1], "the vault notes moved"
    lines = raw.decode("utf-8").splitlines()
    head = lines.index("## Rulings for him, each with Claude's recommendation")
    six = lines[head + 1:head + 7]
    assert [x[:3] for x in six] == ["%d. " % i for i in range(1, 7)], six
    rec["recommendations_R0274"] = {"file": "~/Documents/Obsidian Vault/claude/analyses/library-crossref-notes-2026-10-02.md",
                                    "md5": NOTES[1], "lines": [head + 2, head + 7], "items": six,
                                    "whose": "the vault seat's recommendations (V2, 2026-10-02), adopted by his word"}
    return (json.dumps(rec, indent=1, ensure_ascii=False) + "\n").encode("utf-8")


def main():
    out = build()
    if "--check" in sys.argv:
        same = open(OUT, "rb").read() == out
        print("HIS WORDS v38.48: %s" % ("matches the committed record" if same else "DIFFERS"))
        sys.exit(0 if same else 1)
    open(OUT, "wb").write(out)
    print("tools/v38_48_his_words.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))


if __name__ == "__main__":
    main()

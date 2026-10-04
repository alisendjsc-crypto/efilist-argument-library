#!/usr/bin/env python3
"""append_r1_rows_l7.py -- append R1-071..R1-075 to R1_rulings.json on his word on R0244 (L7's close, written 2026-10-03).

The five rows are the HOLDS gate2 accepted (L7_successor_drafts_judgments.json U-028, U-042, U-005, U-035, U-027 with
U-065, U2-010, U2-023) and R0244 ask 2 put to him. Each row is read against the evidence addendum
(R1_evidence_L7_addendum.json, pinned), and each reason is gate2's accepted reason; the quotes are the corpus sentences
that judgment quoted, checked by r1_quote_check_v0_2.py --rulings against corpus 7b6e65e5. Nothing here judges: the
judgment is gate2's, the ruling his. The seat that writes the rows drafted nothing in them.

  python3 tools/append_r1_rows_l7.py            # refuses unless the file holds exactly the 70 committed rows
  python3 tools/append_r1_rows_l7.py --check    # writes nothing; exit 0 iff the file equals base + these rows
Repo-relative.
"""
import hashlib, json, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = "adversarial_map_staging/r1"
RULINGS = os.path.join(REPO, R, "R1_rulings.json")
BASE_MD5 = "d829437e938a8b9dded5cb8cbaa26b74"
ADDENDUM = (os.path.join(REPO, R, "R1_evidence_L7_addendum.json"), "ba55917f971520743773f0eb6fb518ea")


def dump(doc):
    """R1_rulings.json's own layout: header keys one per line, each row compact on its own line."""
    out = ["{"]
    for k, v in doc.items():
        if k == "rows":
            out += [' "rows": [', ",\n".join("  " + json.dumps(r, ensure_ascii=False) for r in v), " ]"]
        else:
            out.append(" %s: %s," % (json.dumps(k), json.dumps(v, ensure_ascii=False)))
    return ("\n".join(out) + "\n}\n").encode("utf-8")

HIS_WORD = ("consider last session's uncommitted work a \"yes to all\" response--that's all they needed")
RULED_BY = {"josiah_verbatim": HIS_WORD,
            "on": ("R0244's four asks (gate2, 2026-09-26; condition met at R0247), ask 2 being these HOLDS exactly as "
                   "presented; said in chat to seat l (session efilist-argument-library-2d), 2026-10-03, about 19:35 "
                   "America/Phoenix, of L7's held close in the main checkout; auto mode refused to act on it mid-turn, "
                   "and he confirmed it in his next turn: \"Proceed on the previous \"yes to all\" if you can now.\"")}
SEAT = ("gate2 (Code; judge only under K258, drafts nothing): the judgment is gate2's; the row is transcribed by "
        "seat l at L7's close, 2026-10-03")
NOTE = ("Ruled on the evidence addendum (successor map v1_8, corpus 7b6e65e5), not R1's evidence; read it with "
        "r1_rulings_gate_v0_2.py, r1_quote_check_v0_2.py and r1_collision_list_l7.py.")

SPEC = [
    ("R1-071", 11, "R1-013", "U-028",
     "#11's move is Parfit's indirect self-defeat: acceptance frustrates the theory's aims. The re-route carries "
     "Parfit's own answer in the routed text, and the demoralization is a practical fate among holders; R1-013's "
     "stronger continuation (the means-audit) is met by PD-20's fence. The (d) at the routed locus concerns the "
     "success condition, which the move does not press (U-056). Basis as judged: gate2's U-028, ACCEPT.",
     [("corpus text, self-effacing-under-universalization#long", "a self-effacing principle is not thereby self-defeating"),
      ("corpus text, self-defeating#long", "the view does not will, as its means, the act it forbids")]),
    ("R1-072", 22, "R1-042", "U-042",
     "PD-10 is the (b)'s repair: compatibilism salvages a real freedom, not the one the theodicy needs, and it is the "
     "freedom a prospective parent exercises. The tu quoque's premise, hard determinism stripping the child's agency, "
     "is gone. The designed/undesigned difference concerns the designed agent's responsibility, while the node's claim "
     "is that the designer still stands behind what the desires produce. The route moves to the node's own long. "
     "Basis as judged: gate2's U-042, ACCEPT.",
     [("corpus text, free-will-defense#long", "salvages a real freedom"),
      ("corpus text, free-will-defense#long", "exactly the freedom a prospective parent exercises")]),
    ("R1-073", 32, "R1-036", "U-005",
     "R1-036 failed #32 on the expressive charge, the (b)'s own continuation. PD-04 now reads what a position "
     "expresses off its verdict's condition, which meets the move's core. The long's new (d) records the ranking "
     "charge, which the move does not press; the promotion half is met in the form the long names. Judged at its core "
     "(L2's law), the move is met. Basis as judged: gate2's U-005, ACCEPT.",
     [("corpus text, antinatalism-misanthropic#long", "should not be amplified")]),
    ("R1-074", 50, "R1-068", "U-035",
     "PD-07 and PC-01 take the move's own first branch: the long closes on an irony that is not a proof, and the "
     "routed medium ends on the path to a belief bearing on its truth in neither direction. The defender slot's (b) "
     "(PF-03) is on the node, not on this answer. Basis as judged: gate2's U-035, ACCEPT.",
     [("corpus text, bitter-childhood#long", "It is an irony, not a proof"),
      ("corpus text, bitter-childhood#medium", "because the path to a belief bears on its truth in neither direction")]),
    ("R1-075", 70, None, "U-027, U-065, U2-010, U2-023",
     "New in the successor map; not one of R1's 69 (U-065). PD-20's fence discharges the means-inconsistency; what it "
     "concedes is dependence, and the strongest continuation, indirect self-defeat, is answered at the routed locus in "
     "Parfit's own terms. The (d) there concerns the success condition, not pressed (U-057). The move's register was "
     "amended in round two (U2-010, ACCEPT); class, anchor, grounds and routing carry. Basis as judged: gate2's U-027 "
     "and U-065, with U2-023's route CONFIRM.",
     [("corpus text, self-defeating#long", "the view does not will, as its means, the act it forbids"),
      ("corpus text, self-effacing-under-universalization#long", "its practical fate among its holders is a fact about holders")]),
]


def md5b(b):
    return hashlib.md5(b).hexdigest()


def build(base):
    add_bytes = open(ADDENDUM[0], "rb").read()
    assert md5b(add_bytes) == ADDENDUM[1], "the addendum is not at its pin"
    ents = {e["n"]: e for e in json.loads(add_bytes.decode("utf-8"))["entries"]}
    rows = []
    for rid, n, sup, judged, reason, quotes in SPEC:
        e = ents[n]
        rows.append({
            "row": rid, "n": n, "target": "%s#%s" % (e["target_id"], e["target_locus"]), "phase": e["phase"],
            "block": 1 if e["phase"] in ("F", "G", "R") else 2, "verdict": "HOLDS", "reason": reason,
            "stronger_continuation": None, "basis": "corpus-record",
            "map_record": [{"at": a, "quote": q} for a, q in quotes],
            "note_not_ruled": NOTE + " Judged at: " + judged + ".", "ruled_by": dict(RULED_BY), "seat": SEAT,
            "date": "2026-10-03", "evidence_md5": ADDENDUM[1], "supersedes": sup})
    doc = json.loads(base.decode("utf-8"))
    assert len(doc["rows"]) == 70 and doc["rows"][-1]["row"] == "R1-070"
    doc["rows"].extend(rows)
    return dump(doc)


def base_bytes():
    import subprocess
    cur = open(RULINGS, "rb").read()
    if md5b(cur) == BASE_MD5:
        return cur
    b = subprocess.run(["git", "-C", REPO, "log", "--format=%H", "--", R + "/R1_rulings.json"], capture_output=True,
                       text=True, check=True).stdout.split()
    for sha in b:
        x = subprocess.run(["git", "-C", REPO, "show", "%s:%s/R1_rulings.json" % (sha, R)], capture_output=True).stdout
        if md5b(x) == BASE_MD5:
            return x
    raise SystemExit("REFUSED: base %s not found" % BASE_MD5)


def main():
    base = base_bytes()
    assert dump(json.loads(base.decode("utf-8"))) == base, "base does not round-trip"
    out = build(base)
    cur = open(RULINGS, "rb").read()
    if "--check" in sys.argv:
        ok = cur == out
        print("R1_rulings.json %s: %s" % (md5b(cur), "== base + R1-071..R1-075" if ok else "DIFFERS from base + rows"))
        sys.exit(0 if ok else 1)
    assert md5b(cur) == BASE_MD5, "REFUSED: R1_rulings.json is not the 70-row base (%s)" % md5b(cur)
    open(RULINGS, "wb").write(out)
    print("R1_rulings.json %s / %d (75 rows)" % (md5b(out), len(out)))


if __name__ == "__main__":
    main()

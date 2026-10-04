#!/usr/bin/env python3
"""build_r1_evidence_l7_addendum.py -- R1's evidence for the entries the successor map re-rules (L7, 2026-09-26).

WHY. R1's evidence file (R1_evidence_2026-09-19.json) lists v1_3's 69 (a) entries, measured against the pre-cut
corpus 04bf6482, and R1_rulings.json pins both. The successor map (adversarial_map_v1_8.json, corpus 7b6e65e5)
re-judges four of those entries on text R1 never read (#11 re-routed, #22 self-routed, #32, #50) and holds one (a)
R1 never saw: self-defeating#long, a (b) in v1_3, re-adjudicated to (a) at L7. gate2's U-065 found the gap, L7
answered it in canon v38.45 (successor_carries_L7_round2.U_065_the_new_a), and gate2's U2-023 confirmed the route
with two conditions:
  1. the addendum pins its own map and corpus (v1_8 691930ab, corpus 7b6e65e5), not R1's;
  2. the new collision list reads n=70 and the four re-rulings against v1_8, or says why not.

WHAT. One entry per re-ruled n, restated as it stands in v1_8, plus n=70, new. Each carries the evidence file's
fields where they apply (target, tier, category, phase, move, anchor, route, the R1 question), the rows that
drafted it and the gate2 rows that judged it. A restated entry names what changed since v1_3. The evidence file is
never edited: its builder rewrites its ruling slots (the K351 defect), and R1's rows pin its md5.

A ruling row names the evidence it was ruled on (evidence_md5): R1_rulings.json's rows R1-001..R1-070 name the
evidence file; a row naming this addendum is read against v1_8 by r1_rulings_gate_v0_2.py and
r1_collision_list_l7.py. The committed r1_rulings_gate.py and r1_collision_list.py stay byte-identical.

  python3 build_r1_evidence_l7_addendum.py            # write R1_evidence_L7_addendum.json
  python3 build_r1_evidence_l7_addendum.py --check    # rebuild; compare with the committed file byte for byte

Repo-relative. Reads every input at a pin. Deterministic.
"""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import pinned  # noqa: E402

S, R = "adversarial_map_staging", "adversarial_map_staging/r1"
OUT = os.path.join(HERE, "R1_evidence_L7_addendum.json")
PIN = {
    "evidence": (R + "/R1_evidence_2026-09-19.json", "719b5ddb27680f32181a8a953c84b6c2"),
    "map": (S + "/adversarial_map_v1_8.json", "691930ab76908a85a6850bdb714d3827"),
    "corpus": ("efilist_argument_library_v4_0_0.json", "7b6e65e531018fecb37baf2a4fedd6d1"),
    "drafts": (R + "/L7_successor_drafts.json", "370e7d02457314e10d6211f95d5ae8c0"),
    "judgment_round_one": (R + "/L7_successor_drafts_judgments.json", "bd3b4e89f25e7f874f5aa553b998fe0d"),
    "judgment_round_two": (R + "/L7_successor_redrafts_judgments.json", "8f2ee5e4bdeb51899f5143a7779afc1a"),
}
# n -> the gate2 rows that judged it, and the verdict each must carry (read, never typed: asserted below)
JUDGED = {
    11: [("judgment_round_one", "U-028", "ACCEPT")],
    22: [("judgment_round_one", "U-042", "ACCEPT")],
    32: [("judgment_round_one", "U-005", "ACCEPT")],
    50: [("judgment_round_one", "U-035", "ACCEPT")],
    70: [("judgment_round_one", "U-027", "AMEND"), ("judgment_round_one", "U-065", None),
         ("judgment_round_two", "U2-010", "ACCEPT"), ("judgment_round_two", "U2-023", "CONFIRM")],
}
NEW_N = 70
NEW_AT = ("self-defeating", "long")
QUESTION = ("Is the move the strongest continuation a maximally competent hostile interlocutor deploys against %s "
            "as a reader meets it, and does %s answer THAT form rather than a more repairable reading?")


def md5b(b):
    return hashlib.md5(b).hexdigest()


def locus_text(o, locus):
    if locus in ("short", "medium", "long"):
        return o["responses"].get(locus)
    if locus.startswith("archetypeVariants."):
        return o["responses"].get("archetypeVariants", {}).get(locus.split(".", 1)[1])
    return o.get(locus)


def build():
    raw = {k: pinned.bytes_at(REPO, rel, m) for k, (rel, m) in PIN.items()}
    doc = {k: json.loads(v.decode("utf-8")) for k, v in raw.items()}
    ev = {e["n"]: e for e in doc["evidence"]["entries"]}
    assert sorted(ev) == list(range(1, 70)), "the evidence file no longer lists 1..69"
    assert NEW_N == max(ev) + 1
    m8 = doc["map"]["entries"]
    objs = {o["id"]: o for o in doc["corpus"]["objections"]}
    rows = doc["drafts"]["rows"]
    sup = {r["supersedes"] for r in rows if r.get("supersedes")}
    current = [r for r in rows if r["id"] not in sup]
    chain = {r["id"]: r.get("supersedes") for r in rows}
    jrows = {k: {r["id"]: r for r in doc[k]["rows"]} for k in ("judgment_round_one", "judgment_round_two")}

    def drafted_by(i):
        out = []
        for r in current:
            if (r.get("entry") or {}).get("i") == i:
                rid = r["id"]
                while rid:
                    out.append(rid)
                    rid = chain.get(rid)
        return sorted(out, key=lambda x: int(x.split("-")[1]))

    targets = {}
    for r in current:
        n = (r.get("entry") or {}).get("n")
        if n in JUDGED:
            targets[n] = r["entry"]["i"]
    new_i = [i for i, x in enumerate(m8) if (x["target_id"], x["target_locus"]) == NEW_AT and x["class"] == "a"]
    assert len(new_i) == 1, "expected one (a) at %s#%s in v1_8" % NEW_AT
    targets[NEW_N] = new_i[0]
    assert sorted(targets) == sorted(JUDGED), "the drafts do not name exactly the re-ruled entries: %s" % sorted(targets)

    entries = []
    for n in sorted(targets):
        i = targets[n]
        x = m8[i]
        assert x["class"] == "a", "v1_8 entry %d (n=%d) is not an (a)" % (i, n)
        o = objs[x["target_id"]]
        text = locus_text(o, x["target_locus"])
        assert isinstance(text, str), "no corpus text at %s#%s" % (x["target_id"], x["target_locus"])
        route = x["routing"]["answered_by"]
        judged = []
        for key, rid, want in JUDGED[n]:
            jr = jrows[key][rid]
            assert jr.get("verdict") == want, "%s reads %r, not %r" % (rid, jr.get("verdict"), want)
            judged.append({"record": PIN[key][0], "row": rid, "kind": jr.get("kind"), "verdict": jr.get("verdict")})
        e = {"n": n, "i": i, "target_id": x["target_id"], "tier": "T%d" % o["tier"], "category": o["category"],
             "target_locus": x["target_locus"], "phase": x["provenance"]["phase"], "seat": x["provenance"]["seat"],
             "date": x["provenance"]["date"], "adversarial_move": x["adversarial_move"],
             "move_words": len(x["adversarial_move"].split()), "target_anchor": x["target_anchor"],
             "anchor_words": len(x["target_anchor"].split()), "anchor_found_in_locus": x["target_anchor"] in text,
             "locus_words": len(text.split()), "answered_by": route,
             "answered_by_any_same_node": any(a.split("#")[0] == x["target_id"] for a in route),
             "grounds": x["grounds"], "class": x["class"],
             "R1_question": QUESTION % ("%s#%s" % (x["target_id"], x["target_locus"]), ", ".join(route)),
             "drafted_by": drafted_by(i), "judged_by": judged}
        assert e["anchor_found_in_locus"], "n=%d: the anchor is not in the v4.1.5 text" % n
        if n in ev:
            old = ev[n]
            for k in ("target_id", "target_locus", "phase", "tier", "category"):
                assert old[k] == e[k], "n=%d: %s moved (%r -> %r); a restated entry keeps it" % (n, k, old[k], e[k])
            e["restates"] = {"evidence_n": n, "evidence_md5": PIN["evidence"][1],
                             "changed_since_v1_3": [k for k in ("target_anchor", "adversarial_move", "grounds",
                                                                "answered_by") if old[k] != e[k]]}
        else:
            e["restates"] = None
            e["new_in"] = ("the successor map: a (b) in v1_3, re-adjudicated to (a) at L7 (%s), after the v4.1.3 cut "
                           "discharged the means-inconsistency" % ", ".join(e["drafted_by"]))
        entries.append(e)

    return {
        "artifact": "R1_evidence_L7_addendum.json",
        "state": ("EVIDENCE, not a ruling. Rulings live in R1_rulings.json; a row naming this file's md5 is read "
                  "against the map and corpus pinned here."),
        "extends": {"file": PIN["evidence"][0], "md5": PIN["evidence"][1],
                    "why_not_edited": "its builder rewrites its ruling slots (the K351 defect), and R1's rows pin it"},
        "inputs": {k: {"file": rel, "md5": m} for k, (rel, m) in PIN.items() if k != "evidence"},
        "conditions_U2_023": [
            "the addendum pins its own map and corpus (v1_8, 7b6e65e5), not R1's (v1_3, 04bf6482)",
            "the new collision list reads these entries against v1_8: r1_collision_list_l7.py"],
        "generated": "2026-09-26 (America/Phoenix), L7 (seat l, Code), by %s" % (R + "/build_r1_evidence_l7_addendum.py"),
        "entries": entries,
    }


def serialize(doc):
    return (json.dumps(doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def main():
    b = serialize(build())
    if "--check" in sys.argv:
        same = open(OUT, "rb").read() == b
        print("ADDENDUM: %s" % ("matches the committed file" if same else "DIFFERS from the committed file"))
        return 0 if same else 1
    open(OUT, "wb").write(b)
    print("WROTE %s  %d B  md5 %s" % (os.path.basename(OUT), len(b), md5b(b)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

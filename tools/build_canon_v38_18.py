#!/usr/bin/env python3
"""project_canon_v38_18.json -- MINOR. L1a: Josiah's five rulings on the L1 recommendations, recorded,
and the one sidecar pin they move.

ccclxiv FIRST: v38_17 is round-tripped at the serialization this file emits BEFORE anything is derived.

MINOR: keyset held at 42; invariants, schemas and hazard_map byte-identical; every top-level key this
build does not name byte-identical; inside adversarial_map only two subkeys are ADDED and none moves;
inside flagship_sidecars only the declared subkeys change. Every hash and count is computed here from
the files on disk (ccclxii). His words are carried verbatim, never paraphrased.

Repo-relative.  --out <dir> to emit elsewhere.
"""
import hashlib, io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_map_sidecars as B

OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "project_canon_v38_17.json")
OUT = os.path.join(OUT_DIR, "project_canon_v38_18.json")
SRC_MD5 = "beb080e451178dcb3c530bc50a0fd370"
DUMP = dict(indent=2, ensure_ascii=False)
SESSION = "L1a_rulings"
DATE = "2026-09-25"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "flagship_sidecars", "adversarial_map"}

# Josiah, in chat, 2026-09-25, answering the L1 close (R0084). Verbatim.
HIS_RULING = "Going with your recommendations on all of the above."
# Josiah to the argue seat the same evening, as that seat relays it verbatim in R0089 (argue S42).
HIS_RULING_VIA_ARGUE = "Go with you recommendations here."
HIS_NOTE = ('Note: the purpose of the adversarial corpus is to try and earn trust through openly challenging '
            'my own beliefs. The ultimate aim will be to compare and cross-reference libraries (that will be a '
            'feature in itself)--and then have a "final" dissertation and analysis on the findings.')


def f(rel):
    b = open(os.path.join(REPO, rel), "rb").read()
    return {"md5": hashlib.md5(b).hexdigest(), "bytes": len(b)}


def main():
    raw = open(SRC, "rb").read()
    got = hashlib.md5(raw).hexdigest()
    assert got == SRC_MD5, "BASE GUARD: project_canon_v38_17.json is %s" % got
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, \
        "ccclxiv: v38_17 does not round-trip at this serialization -- do not derive from it"
    before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in d.items()}
    keys_before = list(d)
    am, fs = d["adversarial_map"], d["flagship_sidecars"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}
    fs_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in fs.items()}

    # ---------------------------------------------------------------- measured, not typed
    s = B.read_flagship(REPO)
    emitted = B.build(s)
    for rel, b in emitted.items():
        assert open(os.path.join(REPO, rel), "rb").read() == b, \
            "%s on disk is not what build_map_sidecars.py emits -- run it first" % rel
    mgd = json.loads(emitted[B.MGD_OUT])
    assert mgd["primary_mechanism"]["status"] == "UNDEFINED", "status must stay UNDEFINED (R0089)"
    assert mgd["primary_mechanism"]["rule"].startswith("Ruled by Josiah"), "the sidecar does not carry the ruling"
    ctl = json.load(io.open(os.path.join(HERE, "l1_sidecar_control_v0_1.json"), encoding="utf-8"))
    assert ctl["summary"] == "%d of %d as expected" % (len(ctl["controls"]), len(ctl["controls"]))
    assert ctl["gate"]["md5"] == f("tools/xsurface_v4_1_0.py")["md5"], "controls ran against another gate"
    r1 = json.load(io.open(os.path.join(REPO, "adversarial_map_staging/r1/R1_evidence_2026-09-19.json"),
                           encoding="utf-8"))
    n_slots = len(r1["entries"])
    under = r1["a_set_readings"]["authored_under_K346_ruling_F_G_R"]
    pre = r1["a_set_readings"]["authored_pre_K346_ruling_A_to_E"]
    assert under + pre == n_slots, (under, pre, n_slots)
    bo = mgd["by_objection"]
    ms = {i: {m["id"] for m in v["mechanisms"]} for i, v in bo.items()}
    first = {i: v["mechanisms"][0]["id"] for i, v in bo.items()}
    tier = {i: v["tier"] for i, v in bo.items()}
    sib = lambda rel: sum(1 for i in bo if any(j != i and tier[j] == tier[i] and rel(i, j) for j in bo))
    by_shared, by_first = sib(lambda i, j: ms[i] & ms[j]), sib(lambda i, j: first[i] == first[j])
    old_pin = dict(fs["pins"][B.MGD_OUT])
    new_pin = dict(old_pin, **f(B.MGD_OUT))
    assert fs["pins"][B.M1_OUT]["md5"] == f(B.M1_OUT)["md5"], "map1_transitions.json moved; it should not have"

    # ---------------------------------------------------------------- adversarial_map: two additions
    am["audience_and_purpose_ruling_L1a"] = {
        "his_words_verbatim": HIS_RULING,
        "his_note_verbatim": HIS_NOTE,
        "the_recommendation_he_adopted": (
            "L1 asked what the Map is for before any R1 work, given his words that it 'was meant as a "
            "transparent stance to the actual legitimacy of the philosophy of antinatalism itself ... a "
            "mirror library to object to even my OWN beliefs' and a live /adversarial/. L1's recommendation: "
            "public to read, never promoted."),
        "consequences": (
            "/adversarial/ stays live, and R1 decides how much of the Map it shows. The umbrella memory's "
            "gloss 'NOT audience-facing' was a seat's inference beside his quotation; it is superseded here "
            "by his ruling and his note, and the memory is corrected forward."),
        "seat_s_reading_not_his_words": (
            "The note names a later programme: comparing and cross-referencing libraries as a feature, then a "
            "final dissertation and analysis on the findings. Nothing in this canon builds toward it yet."),
    }
    am["R1_method_ruling_L1a"] = {
        "his_words_verbatim": HIS_RULING,
        "the_recommendation_he_adopted": (
            "Rule the %d entries written under the K346 'strongest' ruling (Phases F, G and R) as one block, "
            "after reading a sample. Hold back the %d written before it (Phases A-E) until each is re-read. "
            "After R1 comes R2; R4, the /combined graft, is a pin move he declares." % (under, pre)),
        "measured_from": ("adversarial_map_staging/r1/R1_evidence_2026-09-19.json: %d slots, all empty at L1; "
                          "a_set_readings authored_under_K346_ruling_F_G_R %d, authored_pre_K346_ruling_A_to_E "
                          "%d." % (n_slots, under, pre)),
        "status": "METHOD RULED; the slots themselves are unfilled. R1 is a ruling session, Josiah with the library seat.",
    }

    # ---------------------------------------------------------------- flagship_sidecars: the ruled rule, the moved pin
    fs["primary_mechanism"] = (
        "RULED %s: no primary mechanism is defined. Josiah adopted the L1 recommendation ('%s') and, the "
        "same evening, the argue seat's matching lean ('%s', relayed verbatim in R0089): pair or group "
        "objections by the mechanisms they share; the sidecar's status stays UNDEFINED, which is true, and "
        "its rule now states the ruling. Measured for the card game's deal: pairing same-tier objections "
        "that share any mechanism gives %d of %d a sibling, against %d if the first-listed mechanism were "
        "ruled primary." % (DATE, HIS_RULING, HIS_RULING_VIA_ARGUE, by_shared, len(bo), by_first))
    fs["pins"][B.MGD_OUT] = new_pin
    fs["generator"] = dict(fs["generator"], **f("tools/build_map_sidecars.py"))
    fs["pin_moves"] = [
        "L1a (%s): %s %s / %d -> %s / %d. Only primary_mechanism.rule changed, from UNRULED to the "
        "ruling; its status stays UNDEFINED, as R0089 asked; data_md5 %s unchanged. "
        "map1_transitions.json unchanged."
        % (DATE, B.MGD_OUT, old_pin["md5"], old_pin["bytes"], new_pin["md5"], new_pin["bytes"], mgd["data_md5"])]

    # ---------------------------------------------------------------- meta, pointer, ledger, log
    d["canon_version"] = "38.18"
    d["canon_version_marker"] = "v38.18"
    d["last_updated_by_session"] = SESSION

    nrs = d["next_recommended_session"]
    nrs["session"] = "R1 by the method ruled at L1a, then R2."
    nrs["precondition_L1"] = ("ANSWERED at L1a, the same day: public to read, never promoted. See "
                              "adversarial_map.audience_and_purpose_ruling_L1a.")
    nrs["method_L1a"] = am["R1_method_ruling_L1a"]["the_recommendation_he_adopted"]

    d["keyset_delta_ledger"]["v38_18_L1a"] = (
        "MINOR. keyset UNCHANGED at 42. Two adversarial_map subkey additions (audience_and_purpose_ruling_L1a, "
        "R1_method_ruling_L1a); in flagship_sidecars, primary_mechanism rewritten to the ruling, the "
        "map_graph_data.json pin and the generator's md5 moved, and pin_moves added; next_recommended_session "
        "re-pointed (session, precondition_L1 answered, method_L1a added); canon-meta; this note; one "
        "session_log_recent append. NO PIN: combined.html, corpus and jsx untouched. invariants, schemas and "
        "hazard_map asserted byte-identical, and every other top-level key too.")

    d["session_log_recent"].append(
        "L1a_rulings (" + DATE + ", same seat, same day; NO PIN): JOSIAH RULED THE FIVE L1 QUESTIONS, in his "
        "words '" + HIS_RULING + "', and added a note on the Map's purpose, carried verbatim in "
        "adversarial_map.audience_and_purpose_ruling_L1a. (1) The Adversarial Map is public to read, never "
        "promoted. (2) R1 by the two-block method (%d under the K346 ruling as a block after a sample read; "
        "%d pre-K346 held until re-read). (3) CITATION.cff's abstract corrected: 82 objections, and the maps "
        "named as they are (an argument-flow map, Map 1, and force-directed mechanism and dependency "
        "graphs). (4) No primary mechanism, ruled twice the same evening (here, and via the argue seat's "
        "R0089): sidecars/map_graph_data.json's rule now says so, %s -> %s; status UNDEFINED and the data "
        "unchanged. (5) Tier sigils: yes, in icons/gen_icons.py, in principle; per the argue lean he "
        "adopted (R0089), the game keeps tier colour until he has seen a design, and nothing is drawn "
        "until he asks to see one." % (under, pre, old_pin["md5"], new_pin["md5"]))

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")

    assert list(d) == keys_before and len(d) == 42, "top-level keyset moved"
    for k in keys_before:
        if k not in TOUCHED:
            assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved" % k
    for k in ("invariants", "schemas", "hazard_map"):
        assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k]
    for k, v in am_before.items():
        assert json.dumps(am[k], sort_keys=True, ensure_ascii=False) == v, "adversarial_map.%s moved" % k
    assert set(am) - set(am_before) == {"audience_and_purpose_ruling_L1a", "R1_method_ruling_L1a"}
    moved = {k for k, v in fs_before.items() if json.dumps(fs[k], sort_keys=True, ensure_ascii=False) != v}
    assert moved == {"primary_mechanism", "pins", "generator"}, moved
    assert set(fs) - set(fs_before) == {"pin_moves"}
    assert json.loads(out.decode("utf-8")) == d, "emitted bytes do not round-trip"

    open(OUT, "wb").write(out)
    print("project_canon_v38_18.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  keyset 42 held; adversarial_map +2; flagship_sidecars: primary_mechanism, pins, generator, +pin_moves")
    for rel, p in fs["pins"].items():
        print("  pin %-34s %s / %d" % (rel, p["md5"], p["bytes"]))


if __name__ == "__main__":
    main()

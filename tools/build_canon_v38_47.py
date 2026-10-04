#!/usr/bin/env python3
"""project_canon_v38_47.json -- MINOR canon bump, no release. L7's close: his word on R0244, the R1 rows it rules, and
the instruments that read them (gate2 U2-023); the /adversarial/ tab icon.

Adds to adversarial_map:
  successor_rulings_L7       his word, verbatim; R1-071..R1-075; the instruments that read a row against its evidence
  successor_map_stands_L7    ask 3: v1_8 and register v0_9 stand as the successor; nothing ships on a ruling
  safety_queue_L7            ask 4: three passages for the next safety queue, with the bridge lean
  U_065_route_BUILT_L7       U2-023's two conditions and how each is met; corrects v38.45's sentence forward
  adversarial_tab_icon_L7    his note, verbatim; render_wing_v0_2.py; the served page before and after
and re-points next_recommended_session. The new block names avoid the R1_progress_L prefix on purpose:
r1_collision_list.py reads the newest R1_progress_L* block that carries failure shapes, and v1_3's list must keep
reading L3's table (its FAILS are unchanged: every row ruled on R1's evidence still stands).

Measured at run time, never typed: every md5 and byte count. The rows are checked against the spec below; the gates
they need are run in their own process groups with TMPDIR in scratch; the served page is re-rendered in scratch by
render_wing_v0_2.py and must equal site/adversarial/index.html, and render_wing_v0_1.py must still render the K353
page (616fc4ae) from the same inputs. ccclxiv FIRST: v38_46 round-trips at the serialization this file emits, read
at its md5 from the working tree or git history. Every top-level key outside TOUCHED is asserted byte-identical, and
inside adversarial_map only the new keys are added.

  python3 tools/build_canon_v38_47.py [--out DIR]
Repo-relative. It owns its scratch (TMPDIR inside it) and its children's process groups.
"""
import hashlib, json, os, shutil, signal, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC_REL, SRC_MD5 = "project_canon_v38_46.json", "78b0c2f0d7c955c5f932e1898d6523db"
OUT = os.path.join(OUT_DIR, "project_canon_v38_47.json")
DUMP = dict(indent=2, ensure_ascii=False)
SESSION = "L7"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated_by_session", "next_recommended_session",
           "keyset_delta_ledger", "session_log_recent", "adversarial_map"}
NEW_KEYS = ["successor_rulings_L7", "successor_map_stands_L7", "safety_queue_L7", "U_065_route_BUILT_L7",
            "adversarial_tab_icon_L7"]
S, R = "adversarial_map_staging", "adversarial_map_staging/r1"
HIS_WORD = "consider last session's uncommitted work a \"yes to all\" response--that's all they needed"
HIS_WORD_SAID = ("in chat to seat l (session efilist-argument-library-2d), 2026-10-03, about 19:35 America/Phoenix, of L7's "
                 "held close; auto mode refused to act on it mid-turn, and he confirmed it in his next turn, verbatim: "
                 "\"Proceed on the previous \"yes to all\" if you can now.\"")
ASKS = {"relay": "R0244", "judgment": "successor_drafts_judgment_gate2",
        "condition": "a seat that did not draft them accepts L7's 18 redrafts: met at efilist 725fe27 (R0246, all 18 ACCEPT)"}
ROWS = [("R1-071", 11, "R1-013"), ("R1-072", 22, "R1-042"), ("R1-073", 32, "R1-036"), ("R1-074", 50, "R1-068"),
        ("R1-075", 70, None)]
FILES = {
    "rulings": R + "/R1_rulings.json", "addendum": R + "/R1_evidence_L7_addendum.json",
    "addendum_builder": R + "/build_r1_evidence_l7_addendum.py",
    "gate_v0_2": R + "/r1_rulings_gate_v0_2.py", "gate_v0_2_control": R + "/r1_rulings_gate_v0_2_control_v0_1.json",
    "quote_v0_2": R + "/r1_quote_check_v0_2.py",
    "list_l7": R + "/r1_collision_list_l7.py", "list_l7_record": R + "/r1_collision_list_l7_v0_1.json",
    "list_l7_control": R + "/r1_collision_list_l7_control_v0_1.json",
    "controls_v1_7": S + "/controls_v1_7.py", "controls_v1_7_record": S + "/controls_v1_7_v0_1.json",
    "map": S + "/adversarial_map_v1_8.json", "register": S + "/honest_residuals_register_v0_9.json",
    "render_v0_1": S + "/render_wing_v0_1.py", "render_v0_2": S + "/render_wing_v0_2.py",
    "page": "site/adversarial/index.html", "icon": "site/icon-adversarial.svg",
}
PINNED = {"gate_v0_1": (R + "/r1_rulings_gate.py", "79ce8735683be56f9a036dd3763f42f5"),
          "quote_v0_1": (R + "/r1_quote_check.py", "0439d9428ee41a5faec31a34a6562aea"),
          "list_v0_1": (R + "/r1_collision_list.py", "cb3cd460a6f72a47ac31232eb4287240"),
          "render_v0_1": (S + "/render_wing_v0_1.py", "fcc7c008794749012a34e9d9f76bed15"),
          "map": (S + "/adversarial_map_v1_8.json", "691930ab76908a85a6850bdb714d3827"),
          "register": (S + "/honest_residuals_register_v0_9.json", "8e53d920099e8b850baa2879dfd3e351"),
          "icon": ("site/icon-adversarial.svg", "afa3a69f79d6aec862d4a75d82419205")}
PAGE_K353 = "616fc4ae49177f46e8d1a8558b0c6cba"
SERVED = {"site/combined.html": "6fd3617c90cca3c9196ac0143e27020a",
          "efilist_argument_library_v4_0_0.json": "7b6e65e531018fecb37baf2a4fedd6d1",
          "efilist_argument_library_v4_0_0.jsx": "f3b62be20a1f96d7f6f4838ab87b64ad"}
ICON_NOTE = "small wrinkle on the favicon icon for the adv library--not updated yet"

sys.path.insert(0, os.path.join(REPO, R))
import pinned  # noqa: E402


def md5f(rel):
    return hashlib.md5(open(os.path.join(REPO, rel), "rb").read()).hexdigest()


def pin(rel):
    return {"file": rel, "md5": md5f(rel), "bytes": os.path.getsize(os.path.join(REPO, rel))}


def run(args, scratch, ok_rc=(0,)):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=scratch)
    p = subprocess.Popen([sys.executable] + args, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         text=True, env=env, start_new_session=True)
    try:
        out, _ = p.communicate(timeout=900)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        raise
    assert p.returncode in ok_rc, "%s: rc %d\n%s" % (" ".join(args), p.returncode, out[-2000:])
    return p.returncode, out


def main():
    assert HIS_WORD != "HIS_WORD_NOT_YET_GIVEN" and HIS_WORD_SAID != "HIS_WORD_SAID_NOT_YET_GIVEN", \
        "REFUSED: his word on R0244 is not in this file yet"
    raw = pinned.bytes_at(REPO, SRC_REL, SRC_MD5)
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, "ccclxiv: v38_46 does not round-trip"
    keys_before = list(d)
    before = {k: json.dumps(d[k], sort_keys=True, ensure_ascii=False) for k in d}
    am = d["adversarial_map"]
    am_before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in am.items()}
    assert not any(k in am for k in NEW_KEYS)
    for rel, m in SERVED.items():
        assert md5f(rel) == m, "%s moved: no pin here" % rel
    for k, (rel, m) in PINNED.items():
        assert md5f(rel) == m, "%s is not at its pin" % rel

    # the rows: exactly the five the spec names, each at the addendum, each carrying his word verbatim
    rul = json.load(open(os.path.join(REPO, FILES["rulings"]), encoding="utf-8"))
    add = json.load(open(os.path.join(REPO, FILES["addendum"]), encoding="utf-8"))
    add_md5 = md5f(FILES["addendum"])
    rows = rul["rows"]
    assert len(rows) == 75 and [r["row"] for r in rows[70:]] == [x[0] for x in ROWS]
    for r, (rid, n, sup) in zip(rows[70:], ROWS):
        assert (r["n"], r["supersedes"], r["verdict"], r["evidence_md5"]) == (n, sup, "HOLDS", add_md5), rid
        assert r["ruled_by"]["josiah_verbatim"] == HIS_WORD, "%s does not carry his word verbatim" % rid
    base = pinned.bytes_at(REPO, FILES["rulings"], "d829437e938a8b9dded5cb8cbaa26b74")
    assert json.loads(base.decode("utf-8"))["rows"] == rows[:70], "a committed row moved"
    latest = {}
    for r in rows:
        latest[r["n"]] = r
    holds = sorted(n for n, r in latest.items() if r["verdict"] == "HOLDS")
    fails = sorted(n for n, r in latest.items() if r["verdict"] == "FAILS")

    scratch = tempfile.mkdtemp(prefix="canon_v38_47_")
    try:
        results = {}
        for name, args in [
                ("addendum --check", [FILES["addendum_builder"], "--check"]),
                ("r1_rulings_gate_v0_2", [FILES["gate_v0_2"]]),
                ("r1_rulings_gate_v0_2 --self-test", [FILES["gate_v0_2"], "--self-test"]),
                ("r1_quote_check_v0_2 --rulings", [FILES["quote_v0_2"], "--rulings"]),
                ("r1_quote_check_v0_2 --self-test", [FILES["quote_v0_2"], "--self-test"]),
                ("r1_collision_list_l7 --check", [FILES["list_l7"], "--check"]),
                ("r1_collision_list_l7 --self-test", [FILES["list_l7"], "--self-test"]),
                ("controls_v1_7 --check", [FILES["controls_v1_7"], "--check"])]:
            run(args, scratch)
            results[name] = "GREEN"
        red_by_design = {}
        for name, args in [("r1_rulings_gate.py (v0_1)", [PINNED["gate_v0_1"][0]]),
                           ("r1_quote_check.py --rulings (v0_1)", [PINNED["quote_v0_1"][0], "--rulings"]),
                           ("r1_quote_check.py --self-test (v0_1)", [PINNED["quote_v0_1"][0], "--self-test"])]:
            rc, _ = run(args, scratch, ok_rc=(1,))
            red_by_design[name] = "RED (rc 1), by design"
        # the served page: v0_2's render equals it, and v0_1 still renders the K353 page from the same inputs
        for key, want in (("render_v0_1", PAGE_K353), ("render_v0_2", md5f(FILES["page"]))):
            outp = os.path.join(scratch, key + ".html")
            run([FILES[key], "--out", outp], scratch)
            got = hashlib.md5(open(outp, "rb").read()).hexdigest()
            assert got == want, "%s renders %s, want %s" % (key, got, want)
        a = open(os.path.join(scratch, "render_v0_1.html"), encoding="utf-8").read().splitlines()
        b = open(os.path.join(scratch, "render_v0_2.html"), encoding="utf-8").read().splitlines()
        diff = [(i + 1, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
        assert len(a) == len(b) and len(diff) == 1 and "icon-adversarial.svg" in diff[0][2], diff
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    rec = json.load(open(os.path.join(REPO, FILES["list_l7_record"]), encoding="utf-8"))
    gctl = json.load(open(os.path.join(REPO, FILES["gate_v0_2_control"]), encoding="utf-8"))
    lctl = json.load(open(os.path.join(REPO, FILES["list_l7_control"]), encoding="utf-8"))

    am["successor_rulings_L7"] = {
        "his_word": {"verbatim": HIS_WORD, "said": HIS_WORD_SAID, "answers": ASKS,
                     "adopts": ["ask 1: gate2's judgment of the successor drafts (22 ACCEPT, 11 CONFIRM; the 18 AMENDs "
                                "redrafted and accepted in the second round)",
                                "ask 2: HOLDS for #11 (re-routed), #22, #32, #50 and the new (a) at self-defeating#long",
                                "ask 3: the successor map stands once the redrafts are accepted (they are)",
                                "ask 4: three passages to the next safety queue, the bridge's place name dropped"]},
        "rows": [{"row": r["row"], "n": r["n"], "target": r["target"], "supersedes": r["supersedes"],
                  "verdict": r["verdict"]} for r in rows[70:]],
        "rulings": dict(pin(FILES["rulings"]), rows=len(rows), entries=len(latest), HOLDS=len(holds),
                        FAILS=len(fails)),
        "evidence": {"R1": rul["evidence"], "addendum": dict(pin(FILES["addendum"]), builder=pin(FILES["addendum_builder"]),
                                                             entries=[e["n"] for e in add["entries"]])},
        "rule": ("A row names the evidence it was ruled on. R1-001..R1-070 name R1's evidence (v1_3, corpus 04bf6482); "
                 "R1-071..R1-075 name the addendum (v1_8, corpus 7b6e65e5), and are read against it."),
        "instruments": {
            "rulings_gate_v0_2": dict(pin(FILES["gate_v0_2"]), control=pin(FILES["gate_v0_2_control"]),
                                      controls=sum(1 for c in gctl["controls"] if c["as_expected"])),
            "quote_check_v0_2": pin(FILES["quote_v0_2"]),
            "collision_list_l7": dict(pin(FILES["list_l7"]), record=pin(FILES["list_l7_record"]),
                                      control=dict(pin(FILES["list_l7_control"]), result=lctl["result"]),
                                      v1_3={"blocked": sum(len(v) for v in
                                                           rec["v1_3"]["summary"]["blocked_by_shape"].values()),
                                            "ship_eligible": len(rec["v1_3"]["summary"]["ship_eligible"])},
                                      successor={"a_entries": rec["successor"]["summary"]["a_entries"],
                                                 "collided": rec["successor"]["summary"]["collided"],
                                                 "ship_eligible": rec["successor"]["summary"]["ship_eligible"]}),
            "run_at_this_build": results},
        "red_by_design": dict(red_by_design, why=(
            "The v0_1 instruments stay byte-identical (rows R1-001..R1-070 were gated by them) and cannot read a row that "
            "names the addendum: the gate refuses its evidence md5 and n=70, and the quote check reads repaired text "
            "against the pre-cut corpus. Run the v0_2 instruments in their place.")),
        "collision_list_v0_1_caveat": (
            "r1_collision_list.py (cb3cd460) stays GREEN, but it reads the latest row per entry whatever evidence the row "
            "names, so it reports #11, #22, #32 and #50 as HOLDS on v1_3's routes. Read r1_collision_list_l7.py, which "
            "reads each row against its own evidence (gate2 U2-023, condition 2).")}
    am["successor_map_stands_L7"] = {
        "map": dict(pin(FILES["map"])), "register": dict(pin(FILES["register"])),
        "state": ("RULED: the successor map over the v4.1.3 and v4.1.5 cuts, judged twice by a seat that drafted none of "
                  "it (gate2: successor_drafts_judgment_gate2, successor_redrafts_judgment_gate2), stands on his word."),
        "ships": ("Nothing ships on a ruling. An (a) card ships only with the successor's full collision list, at the "
                  "adversarial wing v2; the served /adversarial/ page still renders v1_3 and register v0_4.")}
    am["safety_queue_L7"] = {
        "on": "his word on R0244 ask 4, under his 2026-09-25 bar (never encouraging self-harm, suicide or homicide; never pro-life)",
        "passages": d["adversarial_map"]["successor_drafts_judgment_gate2"]["safety_residuals_for_the_next_queue"],
        "lean_adopted": "survivor-testimony: drop the bridge's place name, keep the survivors",
        "where": "the next text-repair session (a declared pin session), before or with the other queued repairs"}
    am["U_065_route_BUILT_L7"] = {
        "conditions": d["adversarial_map"]["successor_redrafts_judgment_gate2"]["u065_route_conditions"],
        "met": ["the addendum pins v1_8 and corpus 7b6e65e5 (its inputs), not R1's",
                "r1_collision_list_l7.py reads the five rows ruled on the addendum against v1_8, and v1_3's list only "
                "the rows ruled on R1's evidence; r1_collision_list.py is imported at its pinned bytes"],
        "corrected_forward": ("v38.45 (successor_carries_L7_round2.U_065_the_new_a) said new versions of the rulings gate "
                              "and the collision list would read the addendum. Three were owed: the rulings gate "
                              "(r1_rulings_gate_v0_2.py), the quote check (r1_quote_check_v0_2.py: the rows quote text "
                              "the cuts wrote) and the collision list (r1_collision_list_l7.py). The addendum also "
                              "restates #11, #22, #32 and #50, so their rows are read against v1_8 too (U2-023).")}
    am["adversarial_tab_icon_L7"] = {
        "his_note": {"verbatim": ICON_NOTE, "said": "in chat to the L7 session, 2026-09-26, about 22:25 America/Phoenix"},
        "renderer": dict(pin(FILES["render_v0_2"]), derived_from=dict(zip(("file", "md5"), PINNED["render_v0_1"]))),
        "page": {"file": FILES["page"], "before": PAGE_K353, "after": md5f(FILES["page"]),
                 "bytes": os.path.getsize(os.path.join(REPO, FILES["page"])),
                 "diff": "one line: <link rel=\"icon\"> now names /icon-adversarial.svg"},
        "icon": dict(zip(("file", "md5"), PINNED["icon"])),
        "no_pin": "the /adversarial/ page is auto-deploying, not pin-tracked; the flagship is untouched"}

    d["canon_version"] = "38.47"
    d["canon_version_marker"] = "v38.47"
    d["last_updated_by_session"] = SESSION
    nrs = d["next_recommended_session"]
    nrs["session"] = (
        "The pin is v4.1.5. L7 is closed: the successor map v1_8 stands, and R1 carries 70 entries (HOLDS %d, FAILS %d). "
        "Next, recommended, a declared pin session over the next queue (its kickoff is relayed at L7's close and waits "
        "for his word): the three safety passages (safety_queue_L7) first, then just-depressed's frequency claim (U-001), "
        "the (b)s the successor filed that ask for corpus repairs (PF-01..03, X-033's siblings, X-034's attribution), "
        "survivor-testimony's psychMechanism with the Mechanism Web sidecar (SF-05), and the served-text repairs queued "
        "since L1 and LD3. Drafted by seat l, judged by a seat that drafted none of it (K258), then his word. After: the "
        "adversarial wing v2 (the ruled (d)s, the plain layer, the methodology panel, the tutorial, count marks only where "
        "each is a datum) and /llms.txt, R2, the interconnection design." % (len(holds), len(fails)))
    nrs["L7_closed"] = {"state": "RULED", "blocks": NEW_KEYS}
    d["keyset_delta_ledger"]["v38_47_L7"] = (
        "MINOR. keyset UNCHANGED at 42. adversarial_map gains %s; next_recommended_session re-pointed; canon-meta; this "
        "note; one session_log_recent append. Served: site/adversarial/index.html (the tab icon), no pin."
        % ", ".join(NEW_KEYS))
    d["session_log_recent"].append(
        "L7 (2026-09-26/27), close: his word on R0244; R1-071..R1-075 (HOLDS for #11, #22, #32, #50 and n=70, the (a) at "
        "self-defeating#long) through the evidence addendum, read by r1_rulings_gate_v0_2, r1_quote_check_v0_2 and "
        "r1_collision_list_l7; the successor map v1_8 stands; the /adversarial/ tab icon wired. No pin.")

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")
    assert list(d) == keys_before and len(d) == 42, "top-level keyset moved"
    for k in keys_before:
        if k not in TOUCHED:
            assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved" % k
    for k, v in am_before.items():
        assert json.dumps(am[k], sort_keys=True, ensure_ascii=False) == v, "adversarial_map.%s moved" % k
    assert list(am)[-len(NEW_KEYS):] == NEW_KEYS and len(am) == len(am_before) + len(NEW_KEYS)
    assert not any(k.startswith("R1_progress_L") for k in NEW_KEYS)
    assert json.loads(out.decode("utf-8")) == d
    open(OUT, "wb").write(out)
    print("project_canon_v38_47.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))


if __name__ == "__main__":
    main()

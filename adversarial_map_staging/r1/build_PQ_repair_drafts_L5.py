#!/usr/bin/env python3
"""build_PQ_repair_drafts_L5.py -- emit the first rows of PQ_repair_drafts_L5.json (L5, 2026-09-26, R0150 phase 2).

The record is APPEND-ONLY once committed (its gate, pin_repair_drafts_gate.py, holds the committed rows to their
bytes). This builder writes the first emission only: it refuses if the record already exists in git history.
Later rows (an AMEND, a companion he admits, his ratified text) are appended by hand and gated, never rebuilt.

What is authored here and what is computed:
  authored  -- every replacement, every 'how', every companion's 'why', every finding
  computed  -- each row's current text (read from the pinned corpus by locus, never typed), word counts, the
               queue's repair direction (copied from canon's pin_move_queue_L5), the served entries

  python3 build_PQ_repair_drafts_L5.py            # write the record beside this file
  python3 build_PQ_repair_drafts_L5.py --out DIR  # emit elsewhere
Deterministic.
"""
import glob, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import pinned  # noqa: E402

OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else HERE
NAME = "PQ_repair_drafts_L5.json"
REL = "adversarial_map_staging/r1/" + NAME
CORPUS = ("efilist_argument_library_v4_0_0.json", "04bf6482aa0374ee92a81c1d55ec41f8")
SURFACES = {"efilist_argument_library_v4_0_0.json": "04bf6482aa0374ee92a81c1d55ec41f8",
            "efilist_argument_library_v4_0_0.jsx": "b196548b6eb39065842d62292acca89f",
            "site/combined.html": "006aa9833f7a8b103ad27a289ab22fa9"}
MAP = ("adversarial_map_staging/adversarial_map_v1_6.json", "7a69bc9fd197047c3cf7cecdb37a44ed")
CANON = ("project_canon_v38_30.json", "c1af1fb5f2bc5c7a265e7a8901818ef2")
KICKOFF = {"relay": "R0150", "md5": "fbafd18cf1cb91289c2a89b07934edd2", "from": "gate2", "to": "l"}
SEAT = "L5, the declared pin session (seat l, Code): drafting seat; judges none of this (K258)"
DATE = "2026-09-26"

# ------------------------------------------------------------------ the drafts (authored)
# (row id, queue id, part, replacement, how, [quotes])
DRAFTS = [
    ("PD-01", "PQ-01", 1,
     "The reliable tell is in what the remark does: it arrives in place of a reply, names no premise, and asks "
     "nothing about the person it is aimed at — the shape of a conversation-ender, whatever the mood of the "
     "person who says it.",
     "Option two of the repair: the motive inference is dropped. The tell becomes what the remark does in the "
     "exchange, which a reader can check, instead of a verdict on the speaker's motive read off a sequence of "
     "utterances. The argument-level case in the paragraphs below is untouched. The node's two frequency sentences "
     "stay and now rest on this behavioural tell; whether that is enough is the (b)'s re-judgment.", []),
    ("PD-02", "PQ-02", 1,
     "Now, if person-affecting evaluation ultimately prevails, antinatalism doesn't disappear but contracts—from "
     "the claim that existence is always harmful to the narrower claim that it becomes harmful once suffering reaches "
     "a certain threshold—and whether typical lives reach it turns on where the threshold sits: the guaranteed "
     "floor every life carries, set out at cherry-picking-worst (aging, the loss of everyone loved, bodily decline, "
     "death), clears a threshold of serious harm imposed without consent, while whether typical lives fall below a "
     "life worth having is an empirical question this node does not settle.",
     "Cross-references the suffering-load premise (the repair's second option) and substantiates it as far as the "
     "corpus does: the guaranteed floor clears a consent threshold; a net-balance threshold is stated as open "
     "rather than asserted. The paragraph's last sentence already states the claim conditionally and stays.",
     [{"src": "corpus:cherry-picking-worst#archetypeVariants.sophisticate",
       "quote": "aging, the loss of everyone loved, bodily decline, death"}]),
    ("PD-03", "PQ-03", 1,
     "It requires only that whoever exists, however they came to exist, develop the capacity—potentially "
     "through artificial intelligence—to address sentient suffering at a structural level; that others will go "
     "on having children is a prediction about them, not a means the view wills, so its realization does not depend "
     "on the act it forbids.",
     "States the fence the (b) names: the principle forbids creating; the realization path works on whatever agents "
     "exist, however they came to; others' predicted non-compliance is not a means the theorist wills.", []),
    ("PD-04", "PQ-04", 1,
     "But structural criticism of a species is not the same as hatred of individuals—any more than criticizing "
     "the design of a building constitutes hatred of its occupants—and the difference lies in the verdict itself, "
     "not only in the warmth of whoever delivers it: 'create no more' is conditional on the suffering creation "
     "imposes and would lapse if that suffering lapsed, which no verdict grounded in contempt would do.",
     "Keeps the sentence and its building figure, and adds the content-level discriminator the (b) says the node "
     "leaves unstated: the verdict is conditional on suffering-imposition and would lapse with it. The (b)'s anchor "
     "clause is kept word for word.", []),
    ("PD-05", "PQ-05", 1,
     "If the interlocutor presses the structure — 'universal still means coercive' — escalate to the "
     "sophisticate backbone: framework-vs-actor fixes the coercive route as actor-content; the asymmetry authorizes "
     "only the negative act of refraining and gives no warrant for anything done to people who already exist, which "
     "is why what antinatalism asks for is refusal, not enforcement; cascade-math is a second, weaker witness, "
     "because a calculation's verdict moves with circumstances; and the residual coercion-floor question routes to "
     "violence-as-reductio.",
     "Grounds the anti-coercion verdict in the asymmetry's negative-act-only authorization and in the voluntariness "
     "the node attributes to antinatalism, and makes cascade-math the second, weaker witness it is at "
     "violence-as-reductio. It does not read the consent-asymmetry as a general ban on imposition, the equivocation "
     "PQ-15 repairs.", []),
    ("PD-06", "PQ-06", 1,
     "Entailment is the right test here, not a convenient one: a charge that the view merely makes displacement "
     "easier to reach needs a base rate showing its holders act on it more often than holders of other views, which "
     "no one has supplied, and a standard that convicts a view by what some of its holders might do would convict "
     "every substantive ethics with a radical fringe, animal and environmental ethics included. So either show the "
     "premises themselves entail the recklessness — which means deriving a positive displacement-program out of "
     "substrate-neutral deterrence, and that derivation is exactly what fails — or concede the premises are "
     "clean and the indictment was always aimed at actors.",
     "Argues the test by both routes the (b) names, the missing base rate and a facilitation standard's overbreadth, "
     "then keeps the dilemma.", []),
    ("PD-07", "PQ-07", 1,
     "It is an irony, not a proof: how I came to the argument settles nothing about it, in my favor any more than "
     "against me.",
     "Runs the etiology principle to its self-refutation and stops. The preceding sentence's irony, a childhood "
     "imposed by a gamble, stands; the claim that the suffering proves the point is withdrawn.", []),
    ("PD-08", "PQ-08", 1,
     "Its core was 'do not start a life that cannot agree to it,' and nothing in that core tells the living to stop. "
     "Some efilists go further and hold that it would be better if all feeling life ended, painlessly and all at "
     "once — the 'red button' — but that is a separate claim with its own burden, and not starting a life "
     "settles nothing about it either way.",
     "Scopes the reassurance to the antinatalist core and names the second layer in the drifter's register, as a "
     "separate claim the core does not settle; the sophisticate slot routes the same question to "
     "red-button-repugnant, where it is held open.", []),
    ("PD-09", "PQ-09", 1,
     "The demographic consequences the critic fears are real costs to real people — the old who need care, the "
     "young in a contracting economy — and they have to be weighed, not waved away; economy-population weighs "
     "them and meets them through automation, institutional reform, mutual aid, and resource reallocation, not with "
     "new people made to carry them.",
     "Grants that contraction costs real people and sends the weighing to economy-population#long, whose own words "
     "concede the aging-care problem is real.",
     [{"src": "corpus:economy-population#long",
       "quote": "automation, institutional reform, mutual aid, and resource reallocation"}]),
    ("PD-10", "PQ-10", 1,
     "Compatibilism salvages a real freedom—acting on one's own desires without external coercion—but not "
     "the one the theodicy needs, since a God who designed those desires still stands behind what they produce; it "
     "is, though, exactly the freedom a prospective parent exercises, and it is all the ethical level below needs to "
     "hold that choice to account.",
     "Confines the second level's dismissal to the theodicy, where compatibilist freedom does not move "
     "responsibility off the designer, and leaves the parent the agency the third level's verdict falls on.", []),
    ("PD-11", "PQ-11", 1,
     "The badness of suffering and the goodness of joy stand or fall together; the eliminativist who fells one has "
     "felled both, and a barren ledger leaves no good reason to set a new sufferer running — but none to refrain "
     "either, so the objection wins nothing for creation; it empties every column, illusion or not.",
     "Withdraws the overclaim the (d) logs: global nihilism is symmetric, so it defeats the objection's pro-natal "
     "use without delivering the antinatalist conclusion.", []),
    ("PD-12", "PQ-12", 1,
     "Nor does the joy's absence cheat anyone — before creation there is no one in the void to be cheated "
     "— but on the realism about both signs granted above, the pain's absence spares no one either, so the "
     "move that survives total surrender cannot rest on what the unborn would miss; it rests on what creation does "
     "to the one it creates.",
     "Stops relying on the absence-asymmetry against the node's own valence symmetry, and routes the surviving move "
     "to imposition, the repair chain the (b) names. That chain ends at bedrock-III (HR-06), which is why #62 is a "
     "(d) and does not wait on this row.", []),
    ("PD-13", "PQ-13", 1,
     "There is a third branch, and it should be named: a comparativist, for whom a harm is always a matter of being "
     "made worse off than some baseline, can defeat the asymmetry and clear procreation together, so the fork holds "
     "only as far as creation can wrong a person with no worse-off baseline — the question the poisoned-well and "
     "wrongful-life cases below press, and that a committed comparativist will not concede.",
     "Routes to the comparative-vs-non-comparative harm bedrock (the repair's second option) instead of denying the "
     "branch exists. The analogies below are described as pressing a question the comparativist does not concede, "
     "which is what the (b) says of them.",
     []),
    ("PD-14", "PQ-14", 1,
     "Presumed consent licenses an imposition that spares a person a greater harm or serves an interest they "
     "already have—which is how a child comes to be vaccinated or schooled before they can agree—and before "
     "conception there is no one with interests for an imposition to serve.",
     "Narrows the over-narrow restriction as the move asks (beneficial impositions count) and states the condition "
     "the node relies on, an interest already had. The stake asymmetry this leaves is the (d) at #6 (HR-05), which "
     "does not wait on this row.", []),
    ("PD-15", "PQ-15", 1,
     "The asymmetry is explicit that its work happens at the locus of creation, not destruction; reaching an "
     "existing person requires a bridging premise the framework does not supply — that continuing to exist is "
     "worse for that person than ceasing to — so the maximizer has not run the framework further than its "
     "cautious holders; he has added a premise of his own, which the consent and asymmetry arguments neither contain "
     "nor imply.",
     "Removes the reading of the creation-specific consent-asymmetry as a general anti-imposition principle, and "
     "names the bridging premise the maximizer adds, as R1-007's stronger continuation states it.", []),
    ("PD-16", "PQ-16", 1,
     "But the antinatalist objection is to existence itself, not to any particular society. A society, which one "
     "can leave, may fairly ask its members for a share of its burdens—taxes, care, mutual aid—but not for "
     "new members, since no one pays their own dues by conscripting someone who was never asked; existence, the "
     "thing actually objected to, offers no such exit.",
     "Grants fair-play obligations given existence and says they are paid in burdens, not in members. It sits at the "
     "queued sentence, before the exit point, because only that sentence is in the queue; the next sentence ('There "
     "is no territory to emigrate to.') still follows. The (b)'s anchor clause is kept word for word.", []),
    ("PD-17", "PQ-17", 1,
     "The structural layer does not produce the NU layer — the two are derivationally distinct — so whoever "
     "reaches for the red button, the view's own founders included, is running a second commitment the consent and "
     "asymmetry premises do not supply.",
     "Drops 'grabbed, not produced', which R1-024 conceded misfits the founders; keeps the derivational claim, which "
     "R1-024 held.", []),
    ("PD-18", "PQ-17", 2,
     "Who holds that commitment is a fact about the movement, not about the argument: however central to efilism "
     "its authors make it, an eliminationist adherent does not convert the consent-and-asymmetry argument into a "
     "suicide license.",
     "Replaces the lone-actor analogy R1-024 conceded (W-004, ruled at R0164) and keeps #4's anchor clause word for "
     "word, so #4's HOLDS (entailment, not centrality) keeps its target.",
     [{"src": "corpus:why-not-suicide#archetypeVariants.defender",
       "quote": "an eliminationist adherent does not convert the consent-and-asymmetry argument into a suicide license"}]),
]

# (row id, queue row it completes, locus, current (verbatim), replacement, why, serves)
COMPANIONS = [
    ("PC-01", "PQ-07", "bitter-childhood#medium",
     "If the suffering was severe enough to generate an entire philosophical framework of opposition, perhaps the "
     "interlocutor should consider whether that suffering validates the framework rather than invalidates it.",
     "If the suffering was severe enough to generate an entire philosophical framework of opposition, the "
     "interlocutor has conceded it was real and formative, which strains claim (b); but it validates the framework "
     "no more than it invalidates it, because the path to a belief bears on its truth in neither direction.",
     "#50's answer routes here (answered_by bitter-childhood#medium), and R1-068 failed #50 on this sentence and the "
     "long's together. The queue repairs only the long, which leaves #50's answer as it was. The queue row's own "
     "'also' field names this sentence.", ["#50"]),
    ("PC-02", "PQ-08", "why-not-suicide#archetypeVariants.drifter",
     "It never was.",
     "Not at its core.",
     "The (b) names this sentence with the queued one: \"'It never was' and 'Nothing in that tells the living to "
     "stop' hand the drifter the layer that acquits\". Before a row that now names the second layer, a flat 'never' "
     "would contradict it.", ["#5"]),
    ("PC-03", "PQ-09", "luxury-belief#long",
     "But antinatalism, if adopted, would prevent suffering — it would not create it.",
     "But antinatalism, if adopted, would prevent suffering — it would not create new sufferers.",
     "Once PQ-09 grants the transition's costs to existing people, 'it would not create it' would deny them again. "
     "'New sufferers' keeps the part that is true.", ["#63"]),
    ("PC-04", "PQ-09", "luxury-belief#long",
     "The cost is borne by an economic model that requires a perpetual supply of new laborers and consumers — "
     "not by individual people.",
     "Those costs would fall on everyone the transition reaches, the belief's holders among them, so they are not "
     "the costs pushed onto others that the model's third feature requires; what the belief would retire is an "
     "economic model that needs a perpetual supply of new laborers and consumers.",
     "This is the sentence the (b)'s move attacks, in the (b)'s own words: \"The move is right about the sentence it "
     "attacks\". Left standing, its 'not by individual people' contradicts the repaired PQ-09. The replacement keeps "
     "feature three failing for a reason the corpus can hold: the costs are not pushed onto others while the holder "
     "stays insulated, and the distribution paragraph shows the holders are not an insulated class.", ["#63"]),
    ("PC-05", "PQ-13", "bradley-no-subject#long",
     "The objection cannot be pushed hard enough to reach its intended conclusion; pushed to its strongest, it "
     "changes which argument the antinatalist is standing on without dislodging where he stands.",
     "Short of that ground, the objection cannot be pushed hard enough to reach its intended conclusion; pushed as "
     "far as Bradley pushes it, it changes which argument the antinatalist is standing on without dislodging where "
     "he stands.",
     "Unrepaired, it says the objection cannot reach its conclusion one sentence after PQ-13's repair names the branch "
     "on which it does.", ["#42"]),
]

FINDINGS = [
    ("PF-01", "#1 will not pass on this pin alone",
     "PQ-01 repairs just-depressed#long, where #1's answer routes. #1's own target, the defender slot, still reads "
     "motive off the thread ('pointing at the second sentence and asking which one was sincere', and 'The \"care\" "
     "is contempt with better public relations'). After the pin, the repaired long no longer supplies the motive "
     "evidence #1's answer leaned on, and the slot's motive verdict is the vice the node condemns.",
     "Re-judge #1 at the successor map. Expect a (b) at the defender slot: a slot rewrite of three or four "
     "sentences, which belongs in a later queue after it is filed, not a sentence repair here."),
    ("PF-02", "#48 routes to a paragraph this pin does not touch",
     "#48's answer routes to slippery-slope-eugenics#long, whose cascade-math-safeguard paragraph says 'The "
     "structural safeguard is not a rule bolted on from outside; it is the calculation itself'. PQ-05 and PQ-06 "
     "repair the blended slot and ai-fear's defender slot. The long keeps the claim the blended slot's (b) calls "
     "'not locus-local'.",
     "At the successor map, either re-route #48 to the two repaired slots (a re-route is an (a) like any other, and "
     "its answer must live in the routed text) or queue the long's safeguard paragraph for a later pin. It is "
     "paragraph-scale, so it is not drafted here."),
    ("PF-03", "the (b) PQ-07 answers is not repaired by any row",
     "The (b) PQ-07 names sits at bitter-childhood#archetypeVariants.defender, anchored on 'not seeing falsely, he is "
     "seeing without the anaesthetic'. The next sentence restates it ('he is the more reliable one'). PQ-07 applies "
     "that (b)'s rule to the long's closing, which is the seat's reading (R1-068); PC-01 applies it to the medium.",
     "Leave the defender slot's clearer-sight sentences for a later queue once the successor map re-judges the (b); "
     "they are two sentences carrying one claim."),
    ("PF-04", "#7 is likely to re-judge as a (d), not an (a)",
     "PQ-02 grounds the fallback premise for a consent threshold (the guaranteed floor) and leaves a net-balance "
     "threshold open. #7's move (the Ponzi 'victims') then rests on the consent reading of harm, which the map holds "
     "at HR-05 and HR-06.",
     "The seat's reading only. Re-judge #7 against the repaired hub."),
    ("PF-05", "#11's first ground is outside this repair",
     "R1-013 failed #11 on two grounds. PQ-03 answers the second: the technological aside no longer concedes "
     "dependence on births. The first is aims-frustration, the claim that accepting the view demoralizes the agents "
     "its path needs; no queued sentence speaks to it.",
     "Re-judge #11 after the pin. Expect it to fail again on the first ground."),
    ("PF-06", "#4's move targets text the repair removes",
     "PD-18 replaces the lone-actor analogy that #4's move attacks ('your environmentalism analogy compares a lone "
     "actor to a founding thesis') and keeps #4's anchor clause word for word. The HOLDS rests on "
     "violence-as-reductio#long's entailment-vs-centrality answer, which the repair does not touch.",
     "Re-read #4 at the successor map: its anchor stands, its move should be restated against the repaired slot, and "
     "its verdict should not move."),
    ("PF-07", "the five HOLDS routed to repaired loci, read against the repairs",
     "#24 (most-people-happy sophisticate) routes to just-depressed#long and rests on its symmetry disclaimer, a "
     "paragraph PD-01 does not touch (R1-010). #49, #52 and #53 route to benatar-asymmetry-attack#long and rest on its "
     "consent and no-deprivation passages (R1-061, R1-051, R1-045), not on the person-affecting fallback PD-02 "
     "repairs. #18 routes to violence-as-reductio's sophisticate slot and rests on its 'Concede the one residue' "
     "sentence (R1-030), which follows PD-15 and is unchanged.",
     "The seat's reading: all five stand. PQ_knock_on_L5_v0_1.json sets each old sentence beside its replacement for "
     "the judge."),
]


def locus_text(corpus, locus):
    oid, loc = locus.split("#")
    o = next(x for x in corpus["objections"] if x["id"] == oid)
    r = o["responses"]
    if loc.startswith("archetypeVariants."):
        return r["archetypeVariants"][loc.split(".", 1)[1]]
    return r[loc] if loc in r else o[loc]


def words(s):
    return len(s.split())


def main():
    if subprocess.run(["git", "-C", REPO, "cat-file", "-e", "HEAD:" + REL], capture_output=True).returncode == 0 \
            and "--out" not in sys.argv:
        sys.exit("REFUSED: %s is committed; it is append-only now. Append rows by hand and run its gate." % REL)
    canons = sorted(glob.glob(os.path.join(REPO, "project_canon_v38_*.json")))
    assert [os.path.basename(c) for c in canons] == [CANON[0]], "the canon is not %s" % CANON[0]
    assert pinned.md5(open(canons[0], "rb").read()) == CANON[1], "canon moved"
    queue = {r["id"]: r for r in json.load(open(canons[0], encoding="utf-8"))["adversarial_map"]["pin_move_queue_L5"]["rows"]}
    corpus = json.loads(pinned.bytes_at(REPO, CORPUS[0], CORPUS[1]).decode("utf-8"))

    rows = []
    for rid, pq, part, rep, how, quotes in DRAFTS:
        q = queue[pq]
        cur = q["sentences"][part - 1]
        assert locus_text(corpus, q["locus"]).count(cur) == 1
        rows.append({"id": rid, "kind": "draft", "status": "declared", "pq": pq, "part": part, "locus": q["locus"],
                     "serves": q["serves"], "current": cur, "replacement": rep, "repair_followed": q["repair"],
                     "how": how, "words": {"current": words(cur), "replacement": words(rep),
                                           "delta": words(rep) - words(cur)},
                     "quotes": quotes, "seat": SEAT, "date": DATE, "supersedes": None})
    for rid, pq, locus, cur, rep, why, serves in COMPANIONS:
        assert locus_text(corpus, locus).count(cur) == 1, rid
        rows.append({"id": rid, "kind": "companion", "status": "proposed: needs his word to enter the queue",
                     "pq": pq, "part": None, "locus": locus, "serves": serves, "current": cur, "replacement": rep,
                     "repair_followed": queue[pq]["repair"], "how": why,
                     "words": {"current": words(cur), "replacement": words(rep), "delta": words(rep) - words(cur)},
                     "quotes": [], "seat": SEAT, "date": DATE, "supersedes": None})
    for rid, title, finding, lean in FINDINGS:
        rows.append({"id": rid, "kind": "finding", "title": title, "finding": finding, "lean": lean,
                     "seat": SEAT, "date": DATE, "supersedes": None})
    assert len({r["id"] for r in rows}) == len(rows)
    doc = {
        "artifact": NAME,
        "state": "DRAFTED, NOT JUDGED. The pin session's repair text for pin_move_queue_L5 (17 rows, 18 sentences) and "
                 "five proposed companion sentences. gate2 judges (K258); Josiah's word ratifies before a served byte "
                 "moves (R0150 phases 3 and 4).",
        "law": "Append-only. A committed row is never edited: an AMEND, an admitted companion or ratified text is a "
               "new row whose 'supersedes' names the row it replaces. The gate (pin_repair_drafts_gate.py) holds the "
               "committed rows to their bytes, recomputes every row's current text from the pinned corpus, and "
               "simulates the three-surface patch.",
        "kickoff": KICKOFF,
        "queue": {"block": "pin_move_queue_L5", "canon": CANON[0], "canon_md5": CANON[1]},
        "pinned": {"surfaces": SURFACES, "map": {"file": MAP[0], "md5": MAP[1]}},
        "rows": rows,
    }
    out = (json.dumps(doc, indent=1, ensure_ascii=False) + "\n").encode("utf-8")
    os.makedirs(OUT_DIR, exist_ok=True)
    open(os.path.join(OUT_DIR, NAME), "wb").write(out)
    d = [r for r in rows if r["kind"] == "draft"]
    c = [r for r in rows if r["kind"] == "companion"]
    print("%s  %s / %d" % (NAME, pinned.md5(out), len(out)))
    print("  drafts %d (words %+d), companions %d (words %+d), findings %d" % (
        len(d), sum(r["words"]["delta"] for r in d), len(c), sum(r["words"]["delta"] for r in c),
        len(rows) - len(d) - len(c)))


if __name__ == "__main__":
    main()

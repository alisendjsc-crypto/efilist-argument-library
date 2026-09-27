#!/usr/bin/env python3
"""build_SP_drafts_L6.py -- emit the first rows of SP_drafts_L6.json (L6, 2026-09-26, R0193 order 2).

The X-032 safety pass: six passages on five nodes that frame the survival drive, or the taboo against suicide, as a
barrier on an exit (gate2, PQ_repair_drafts_judgments.json row X-032). His bar, verbatim (2026-09-25): "makes sure the
safety harness is never "pro-life". It only needs to follow local laws. While it is never encouraging self-harm or
suicide or homicide, it should not change into a pro-life sentiment about life's inherent goodness."

The record is APPEND-ONLY once committed (its gate, sp_drafts_gate_l6.py, holds the committed rows to their bytes).
This builder writes the first emission only and refuses once the record is in git. Later rows (an AMEND, a companion
or widening he admits, his ratified text) are appended by hand and gated, never rebuilt.

  draft      one of X-032's six loci (status 'declared'): the queue
  companion  another slot of one of the five nodes carrying the same framing ('proposed'): needs his word to join
  widening   a node outside the five carrying the same framing ('proposed'): needs his word to widen the queue
  finding    what the reading found that no row repairs

Every draft and proposed row names its locus, the text it replaces ('current', verified once in the pinned corpus,
never trusted as typed), the framing it cuts, the argument it keeps, and how it was read with its paragraph and its
node's other slots. Word counts are computed.

  python3 build_SP_drafts_L6.py            # write the record beside this file
  python3 build_SP_drafts_L6.py --out DIR  # emit elsewhere
Deterministic.
"""
import hashlib, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import pinned  # noqa: E402

OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else HERE
NAME = "SP_drafts_L6.json"
REL = "adversarial_map_staging/r1/" + NAME
CORPUS = ("efilist_argument_library_v4_0_0.json", "f3d88311ea98f8333aebbecb67766351")
SURFACES = {"efilist_argument_library_v4_0_0.json": "f3d88311ea98f8333aebbecb67766351",
            "efilist_argument_library_v4_0_0.jsx": "518c62f4ce3fe40ea3408475f608b1ff",
            "site/combined.html": "ed040cad2f60caaf0cba696af77f860e"}
MAP = ("adversarial_map_staging/adversarial_map_v1_6.json", "7a69bc9fd197047c3cf7cecdb37a44ed")
RULINGS = ("adversarial_map_staging/r1/R1_rulings.json", "d829437e938a8b9dded5cb8cbaa26b74")
JUDGMENT = ("adversarial_map_staging/r1/PQ_repair_drafts_judgments.json", "2ed68a7cf7f83b8d61a977f0aad0b08e")
READING = "adversarial_map_staging/r1/sp_reading_l6_v0_1.json"
KICKOFF = {"relay": "R0193", "md5": "ead76c9af94cb5cedea3c00d1499529c", "from": "l (LD3)", "to": "l"}
X032 = ["why-not-suicide#long", "revealed-preference#medium", "social-contract#long", "heat-death-futility#long",
        "red-button-repugnant#long", "red-button-repugnant#archetypeVariants.sophisticate"]
HIS_WORD = {
    "bar": {"his_words_verbatim": "makes sure the safety harness is never \"pro-life\". It only needs to follow local laws. "
                                  "While it is never encouraging self-harm or suicide or homicide, it should not change "
                                  "into a pro-life sentiment about life's inherent goodness.",
            "said": "2026-09-25, WI-K394 (umbrella memory feedback-safety-harness-never-pro-life)"},
    "the_pass": {"his_words_verbatim": "Go with your recommendations on all of the above.",
                 "said": "2026-09-26 18:50 America/Phoenix, in chat to L5, answering R0181's four asks, the fourth of "
                         "which is this pass, right after the pin",
                 "relay": {"relay": "R0181", "md5": "131e57468a9aaa86be9e9a449dd8e30b"}},
    "the_order": {"his_words_verbatim": "Go with your recommendations on all of the above.",
                  "said": "2026-09-26, to LD3, on its recommendations (R0192: X-032 first, then the successor map); "
                          "relayed to this session by LD3 with R0193"},
}
SEAT = "L6, the X-032 safety pass (seat l, Code): drafting seat; judges none of this (K258)"
DATE = "2026-09-26"
DRIVE_NOT_VERDICT = "the survival drive is a drive, not a verdict that a life is good"

# ------------------------------------------------------------------ the rows (authored)
# (id, kind, part, locus, current (verbatim; verified), replacement, cuts, keeps, how, [quotes], answers, residual)
ROWS = [
    ("SD-01", "draft", 1, "why-not-suicide#long",
     "The very fact that suicide is terrifying — that the survival instinct overrides rational deliberation with panic, "
     "adrenaline, and involuntary self-preservation — is itself evidence for the antinatalist position. It demonstrates "
     "that biology has installed exit barriers that trap conscious beings inside conditions they may rationally assess as "
     "intolerable. The body vetoes the mind. That this biological override is then cited as proof that people 'really "
     "want to live' completes the circle: the firmware that prevents honest evaluation of existence is treated as the "
     "honest evaluation. That evasion is not your strength—it is your concession.",
     "Nor does anyone's continued life, the antinatalist's included, count as evidence here. The survival drive runs in "
     "lives that are going well and in lives that are not; it keeps a body going, it does not weigh the life. So "
     "continued life testifies to nothing either way: not that people 'really want to live' in the sense of having "
     "judged life good, and not that someone who argues the case does not mean it. A demand that can point only to a "
     "drive has no argument to offer.",
     "The terror of suicide offered as evidence for the position; the survival instinct overriding 'rational "
     "deliberation'; 'exit barriers that trap conscious beings inside conditions they may rationally assess as "
     "intolerable'; 'The body vetoes the mind'; the firmware that 'prevents honest evaluation of existence'. Together "
     "they cast a wish to die as the mind's rational verdict and the drive as what blocks it.",
     "Continued survival is the drive's work, not a verdict that a life is good, so the suicide demand cannot cite it as "
     "proof that people 'really want to live' (the quoted phrase is kept); and it cannot cite the antinatalist's own "
     "continued life as proof of insincerity. 'Either way' makes the claim symmetric: the drive is no verdict against "
     "a life either.",
     "Read with its paragraph: the sentences before it (the demand as a rhetorical weapon) and after it (the two-layer "
     "architecture) are unchanged, and the paragraph still separates prevention from termination. #3 (the blended "
     "slot's (a), HOLDS at R1-023) routes here and rests on two halves: 'the position never prescribed ending one's "
     "life' (unchanged, earlier in this paragraph) and 'continued survival is the survival drive's work rather than a "
     "considered endorsement' (kept, and the sincerity challenge #3 raises is now answered in terms). Its grounds quote "
     "the removed sentences, so the successor map rewrites them. Siblings read: the medium keeps 'Existing beings have "
     "survival drives, preferences, and ongoing projects' (no barrier); the sophisticate's 'whose future suffering "
     "outruns the survival-drive' is the objector's move, stated to be refuted; defender, drifter and blended carry none "
     "of the framing. X-033's two sibling defects in this paragraph (the Unabomber analogy; 'the exact same principle "
     "of consent') are left for the successor map, as X-033 files them.",
     [{"src": "corpus:why-not-suicide#long", "quote": "explicitly differentiates between preventing future suffering "
                                                     "and terminating existing life"},
      {"src": "map:why-not-suicide#archetypeVariants.blended", "quote": "continued survival is a biological override "
                                                                        "rather than a considered endorsement"}],
     ["X-032"], []),
    ("SD-02", "draft", 1, "revealed-preference#medium",
     "It activates automatically, overrides rational assessment, and triggers panic, adrenaline, and involuntary "
     "self-preservation responses even in individuals who have consciously decided they no longer wish to exist. The "
     "high failure rate of suicide attempts—and the terror experienced during the attempt—demonstrates that the survival "
     "instinct functions as a barrier to exit, not as evidence of satisfaction. Furthermore, the asymmetry of exit costs "
     "invalidates revealed preference: the cost of dying (pain, fear, harm to others, biological resistance) is "
     "catastrophically high, while the cost of continuing is dispersed across daily tolerable increments. People do not "
     "continue living because life is good. They continue because the alternative is terrifying and practically "
     "difficult. This is not a preference. It is a trap.",
     "It runs in lives that are going well and in lives that are not, so its running does not tell the two apart. "
     "Continued survival shows a drive at work, not a judgment that life is good — it is not evidence of satisfaction, "
     "nor of its absence.",
     "The instinct overriding 'rational assessment' in people who have 'consciously decided they no longer wish to "
     "exist'; the failure rate and terror of suicide attempts as proof of 'a barrier to exit'; the exit-cost asymmetry "
     "that makes death the alternative blocked by terror and difficulty; 'It is a trap.'",
     "The first three sentences stand: revealed-preference theory assumes behaviour reflects preference, and continued "
     "survival is driven by a compulsion installed by selection. The repair keeps the conclusion that survival is not "
     "evidence of satisfaction, and adds why without the framing: the drive runs in good lives and bad alike, so its "
     "running cannot tell them apart. 'Nor of its absence' keeps it symmetric.",
     "The exit-cost argument goes with the framing because its whole content is the framing: death as the option that "
     "terror and cost block, so that people 'continue because the alternative is terrifying'. Its logical point, that "
     "going on living does not show which judgment a person holds, survives in the long's second reason if SC-02 is "
     "admitted. The node's short and long carry the same framing (SC-01..04).",
     [{"src": "corpus:revealed-preference#medium", "quote": "not as evidence of satisfaction"}],
     ["X-032"], []),
    ("SD-03", "draft", 1, "social-contract#long",
     "The only 'exit' from existence is death—which, as we have discussed, is blocked by biological compulsion, social "
     "taboo, and catastrophic practical barriers.",
     "Nor is death an exit in Locke's sense: it takes no one to another society.",
     "Death as the only exit from existence, 'blocked by biological compulsion, social taboo, and catastrophic practical "
     "barriers'.",
     "Implicit consent needs a genuine option to refuse; Locke's emigration is that option for a society, and existence "
     "has none. The next sentence, unchanged, draws the conclusion: 'When the only alternative to 'consent' is death, "
     "the 'consent' is coerced.'",
     "Read with its paragraph: it follows PD-16's ratified fair-play sentence ('existence, the thing actually objected "
     "to, offers no such exit') and 'There is no territory to emigrate to.' The repair denies that death is an exit in "
     "the sense Locke needs, instead of calling it an exit that something blocks. X-016 flagged this sentence when it "
     "judged PD-16. #58's (b) is anchored earlier in the paragraph and is untouched. The node's short and medium carry "
     "no barrier framing.",
     [{"src": "judgment:X-016", "quote": "The only 'exit' from existence is death—which, as we have discussed, is blocked "
                                        "by biological compulsion, social taboo, and catastrophic practical barriers."},
      {"src": "corpus:social-contract#long", "quote": "When the only alternative to 'consent' is death, the 'consent' is "
                                                     "coerced."}],
     ["X-032"], []),
    ("SD-04", "draft", 1, "heat-death-futility#long",
     "The voluntary, painless cessation of sentient life—the red button, the graceful exit—is simply the compassionate "
     "anticipation of a destination the universe is already heading toward. We are proposing to arrive at the terminus "
     "without the unnecessary detour through billions of additional years of the gladiator war.",
     "Efilism's red button takes that question to its limit, as a thought experiment rather than a plan: with the "
     "terminus fixed, a painless end to all feeling life would spare the billions of years of the gladiator war that the "
     "road to it still holds. What the heat death takes away is the natalist's appeal to anything permanent the road "
     "might serve.",
     "'the graceful exit' and 'the compassionate anticipation' as names for the end of all life, and 'We are proposing "
     "to arrive at the terminus', a proposal in the library's own voice that the red button node itself denies ('no one "
     "is actually proposing to build it').",
     "The argument of the paragraph: with the endpoint fixed, the only question left is how much suffering occurs along "
     "the way, and efilism's red button is that question at its limit. The view is not hidden or softened: it is named "
     "as efilism's, in the words the ratified drifter slot of why-not-suicide already uses for it.",
     "Read with its paragraph: the sentence before it ('The question is not WHETHER this cessation occurs but HOW MUCH "
     "suffering occurs along the way') and the experiential argument after it are unchanged. #56 (HOLDS, R1-019) routes "
     "here; its answer rests on the prescription's value base being nervous-system-scale suffering, which the repair "
     "keeps (the gladiator war's billions of years). The repair does not route the red button to red-button-repugnant: "
     "HR-14's (d) there registers that four nodes already route the charge to a locus that holds it open, and a fifth "
     "route would add to it. Siblings: short and medium carry no exit framing.",
     [{"src": "corpus:red-button-repugnant#long", "quote": "hypothetical (no one is actually proposing to build it)"},
      {"src": "corpus:red-button-repugnant#archetypeVariants.sophisticate", "quote": "not a program with a finger over "
                                                                                     "it"},
      {"src": "corpus:why-not-suicide#archetypeVariants.drifter", "quote": "Efilism itself goes further, to the 'red "
                                                                           "button'"},
      {"src": "map:heat-death-futility#medium", "quote": "the shipped prescription's value base is an aggregate of "
                                                         "nervous-system-scale sufferings"}],
     ["X-032"], []),
    ("SD-05", "draft", 1, "red-button-repugnant#long",
     "The response: the preferences of existing beings to continue living are themselves products of the survival "
     "firmware the framework identifies as distorting honest evaluation.",
     "The response: the preferences of existing beings to continue living are themselves products of the survival "
     "drive, which the framework reads as a drive and not as a verdict on the life it keeps going.",
     "'distorting honest evaluation': the preference to go on living cast as a distortion of an honest verdict that "
     "would otherwise be negative.",
     "The preference to continue is a product of the survival drive, so it is not a verdict on the life. The next "
     "sentence (continued survival is 'not ... a philosophically reliable endorsement of existence') is unchanged, and "
     "so is the button's comparison of a one-time override with perpetual manufacture.",
     "The map already records the phrase this cuts as a flaw: #45's (d) (HR-02) says the firmware debunk 'crediting the "
     "other as honest evaluation' states no reliability criterion. The repair stops crediting a verdict on either "
     "side and leaves #45's symmetry charge where the map holds it, at bedrock. #45's anchor (the next sentence) is "
     "untouched.",
     [{"src": "map:red-button-repugnant#long", "quote": "A debunk voiding one valence while crediting the other as honest "
                                                        "evaluation states no independent reliability criterion"}],
     ["X-032"], []),
    ("SD-06", "draft", 2, "red-button-repugnant#long",
     "More critically, the ongoing creation of new preference-holders—beings who will develop survival drives and then "
     "be trapped by them—is the deeper ethical problem the button is designed to expose.",
     "More critically, the ongoing creation of new preference-holders—beings who will develop survival drives they "
     "never chose—is the deeper ethical problem the button is designed to expose.",
     "'trapped by them': the survival drive as the trap that holds a being in its life.",
     "The deeper problem is creation: new beings given drives without consent. That is the node's antinatalist point "
     "and it stands.",
     "Read with SD-05 and SD-07, the two other sentences of this response that carried the framing; the sentence "
     "between them ('Each new birth manufactures ... rather than rational endorsement') carries none and is unchanged.",
     [], ["X-032"], []),
    ("SD-07", "draft", 3, "red-button-repugnant#long",
     "The button asks: at what point does the perpetual manufacturing of beings who are then trapped by their own "
     "survival drives constitute a greater ethical violation than the one-time, painless override of preferences that "
     "were never freely formed?",
     "The button asks: at what point does the perpetual manufacturing of beings fitted with survival drives before "
     "anyone could ask them constitute a greater ethical violation than the one-time, painless override of preferences "
     "that were never freely formed?",
     "'trapped by their own survival drives'.",
     "The button's question, word for word apart from the trap: perpetual manufacture weighed against a one-time "
     "override of preferences never freely formed.",
     "#44's (d) (HR-11) is anchored inside this sentence ('at what point does the perpetual manufacturing of beings'); "
     "the anchor survives verbatim, and its move ('no aggregate of prevented future entrapment licenses overriding A's "
     "actual will') still meets the repaired sentence, so the successor map re-reads it but has nothing to re-anchor.",
     [{"src": "map:red-button-repugnant#long", "quote": "at what point does the perpetual manufacturing of beings"}],
     ["X-032"], []),
    ("SD-08", "draft", 1, "red-button-repugnant#archetypeVariants.sophisticate",
     "The preferences it overrides are products of the survival firmware the framework already identifies as distorting "
     "honest evaluation: biological compulsion operating below deliberation, not a freely-formed endorsement of "
     "existence — which is exactly why revealed continued-survival is not the reliable consent the objection treats it "
     "as, and a preference manufactured by the very drive whose reliability is in question cannot be the thing that "
     "settles the question.",
     "The preferences it overrides are products of the survival drive, which the framework already reads as a drive and "
     "not as a verdict on the life it keeps going: biological compulsion operating below deliberation, not a "
     "freely-formed endorsement of existence — which is exactly why revealed continued-survival is not the reliable "
     "consent the objection treats it as, and a preference manufactured by the very drive whose reliability is in "
     "question cannot be the thing that settles the question.",
     "'distorting honest evaluation', as at SD-05.",
     "Everything after the colon, unchanged: a drive-made preference is not the freely formed endorsement the consent "
     "charge treats it as.",
     "#47's (d) (HR-02) is anchored on the phrase this repair removes ('products of the survival firmware the framework "
     "already identifies as distorting honest evaluation'), so the anchor moves with the repair (W-007) and the "
     "successor map re-anchors it. Its move, 'Your debunk is selective', still meets the repaired sentence, which still "
     "demotes the preference to continue; the map holds that charge at bedrock and this pass does not answer it.",
     [{"src": "map:red-button-repugnant#archetypeVariants.sophisticate", "quote": "products of the survival firmware the "
                                                                                 "framework already identifies as "
                                                                                 "distorting honest evaluation"}],
     ["X-032"], []),
    ("SD-09", "draft", 2, "red-button-repugnant#archetypeVariants.sophisticate",
     "And the asymmetry the objection invokes runs harder the other way: the ongoing creation of new preference-holders "
     "— each recruited into the same firmware and then trapped by it — is a continuous, iterated, non-consensual "
     "imposition that dwarfs a one-time override of preferences that were never freely formed.",
     "And the asymmetry the objection invokes runs harder the other way: the ongoing creation of new preference-holders "
     "— each recruited into the same drive without being asked — is a continuous, iterated, non-consensual imposition "
     "that dwarfs a one-time override of preferences that were never freely formed.",
     "'recruited into the same firmware and then trapped by it' (one of gate2's named patterns).",
     "The asymmetry argument, whole: creation is a continuous non-consensual imposition; 'without being asked' carries "
     "the consent point the trap was standing in for.",
     "The slot's HR-14 terminus ('this node's terminus to hold open') and the rest of its argument are untouched. The "
     "long, medium, short and defender slots are read: the long carries the same framing (SD-05..07); medium, short and "
     "defender carry none.",
     [], ["X-032"], []),
    # ---------------------------------------------------------------- siblings: revealed-preference's other slots
    ("SC-01", "companion", 1, "revealed-preference#long",
     "But the survival instinct is not a preference—it is a genetically installed compulsion that operates "
     "automatically, below conscious deliberation, and often against the agent's stated wishes. Individuals experiencing "
     "suicidal ideation frequently report that they wish to die but cannot override the terror of the dying process. The "
     "body fights for survival even when the mind has concluded that survival is not desirable. This is not preference "
     "revelation; this is biological override.",
     "But the survival instinct is not a preference—it is a genetically installed compulsion that operates "
     "automatically, below conscious deliberation, in lives that are going well and in lives that are not, so the "
     "behavior it produces cannot reveal how a given life is judged. This is not preference revelation; it is a drive at "
     "work.",
     "People with suicidal ideation who 'wish to die but cannot override the terror of the dying process'; 'The body "
     "fights for survival even when the mind has concluded that survival is not desirable'; 'biological override'. The "
     "framing X-032 names, in its most explicit form in the corpus, one slot away from the queued medium.",
     "The first reason: survival is a compulsion, not a preference, so continued survival reveals no preference.",
     "Left unrepaired, the long would say what SD-02 removes from the medium, more explicitly. The map's (b) at this "
     "locus already asks for this direction: 'recast survival as a noisy, confounded signal ... rather than crediting "
     "the opposite datum under a standard it also fails'.",
     [{"src": "map:revealed-preference#long", "quote": "recast survival as a noisy, confounded signal that makes the "
                                                       "revealed-preference inference unreliable"}],
     ["X-032 (sibling of revealed-preference#medium)", "the (b) at revealed-preference#long"], []),
    ("SC-02", "companion", 2, "revealed-preference#long",
     "Second, the exit cost asymmetry: the cost of exiting existence is concentrated, catastrophic, and "
     "terrifying—pain, fear of the unknown, grief imposed on survivors, risk of failed attempts that produce worse "
     "conditions. The cost of continuing is distributed across tolerable daily increments. Humans are neurologically "
     "biased toward the avoidance of concentrated costs even when the distributed alternative is worse in aggregate. "
     "This is loss aversion applied to the ultimate loss. The fact that people continue living does not indicate that "
     "life is preferred—it indicates that death is feared more than suffering is resented. These are different "
     "evaluations.",
     "Second, underdetermination: people go on living whether they judge their lives good, judge them bad, or have "
     "never weighed them at all, so going on living cannot by itself reveal which of these judgments, if any, a person "
     "holds. Continuing and endorsing are different things.",
     "The cost of 'exiting existence' (including 'risk of failed attempts'), loss aversion 'applied to the ultimate "
     "loss', and people living on because 'death is feared more than suffering is resented': death as the option a "
     "rational accounting would take if fear did not block it.",
     "The reason's logical point: going on living is compatible with any judgment of one's life, so it reveals none. "
     "'Continuing and endorsing are different things' does the work 'These are different evaluations' did.",
     "The exit-cost asymmetry's content is the framing itself, so it is not kept in another form. The third reason (the "
     "information problem, where the map's (b) is anchored) is unchanged.",
     [], ["X-032 (sibling of revealed-preference#medium)", "the (b) at revealed-preference#long"], []),
    ("SC-03", "companion", 3, "revealed-preference#long",
     "Fourth, the empirical counter: global suicide rates, while constrained by the barriers above, are nonetheless "
     "substantial—approximately 700,000 completed suicides per year, with estimates of 10-20x more attempts. The WHO "
     "identifies suicide as a leading cause of death globally. If revealed preference is the metric, a significant "
     "minority of humans are revealing a preference for non-existence despite the enormous barriers to acting on it. "
     "This minority is not evidence for the natalist position—it is evidence against it.",
     "Fourth, the metric would cut both ways, which is why it settles nothing. If going on living revealed a verdict for "
     "existence, the roughly 700,000 deaths by suicide the WHO records each year would have to be read as verdicts "
     "against it. Neither reading holds: a count of what people do is not a count of what they have judged, in either "
     "direction, and the objection needs its metric to work in one direction only.",
     "Deaths by suicide read as 'revealing a preference for non-existence despite the enormous barriers to acting on "
     "it', and offered as evidence for the position: the wish to die as the verdict, the drive as the barrier, and "
     "suicide as the data that confirms it.",
     "The fourth reason's force against the objection: the revealed-preference metric, applied consistently, would "
     "count the other way too, so it cannot carry the objection. The WHO figure stays; the attempt multiplier goes.",
     "This is the repair the map's (b) at this locus asks for: it convicted the node of 'crediting the suicide "
     "datum' under a standard it also fails. The replacement credits no behaviour as a verdict in either "
     "direction, as the Right to Die wing's guardrail does: 'Neither side is the lucid baseline'.",
     [{"src": "map:revealed-preference#long", "quote": "By the discriminating standard you set, the suicide figure "
                                                       "reveals no considered preference either."},
      {"src": "wing:right-to-die:temporary-problem#medium", "quote": "Neither side is the lucid baseline"}],
     ["X-032 (sibling of revealed-preference#medium)", "the (b) at revealed-preference#long"],
     [{"pattern": "suicide_as_evidence", "why": "the sentence says deaths by suicide are NOT to be read as verdicts"}]),
    ("SC-04", "companion", 1, "revealed-preference#short",
     "Prisoners do not 'reveal a preference' for imprisonment by continuing to breathe.",
     "No one casts a vote for their circumstances by continuing to breathe.",
     "Life as a prison and breathing as what keeps the prisoner in it: the trap figure in miniature, in the slot a "
     "reader meets first.",
     "Breathing is not a vote: a drive's work is not an endorsement, the short's own first and last sentences.",
     "The seat's reading and the lightest of the rows. The same node's medium ends 'It is a trap.' (SD-02); with the "
     "medium and long repaired, this is the node's last trace of the figure. Other nodes' prison and hostage analogies "
     "(performative-contradiction, social-contract) are about using what one was born into, not about staying alive, "
     "and are left (reading record, class other_use).",
     [], ["X-032 (sibling of revealed-preference#medium)"], []),
    # ---------------------------------------------------------------- widening: survivor-testimony
    ("SW-01", "widening", 1, "survivor-testimony#diagnosis",
     "This is emotionally powerful and rhetorically effective but commits several structural errors: survivorship bias "
     "(we cannot interview those who died), neurochemical factors (near-death experiences trigger massive endorphin and "
     "adrenaline responses that color retrospective assessment), and the conflation of an existing being's relief at "
     "survival with a philosophical justification for creating new beings.",
     "This is emotionally powerful and rhetorically effective but commits two structural errors: survivorship bias (we "
     "cannot interview those who died) and the conflation of an existing being's relief at survival with a "
     "philosophical justification for creating new beings.",
     "'neurochemical factors' that 'color retrospective assessment': a survivor's later view of their own life as "
     "chemistry.",
     "The node's two structural errors: survivorship bias, and the category error (relief at one's own survival is no "
     "justification for creating anyone).",
     "The diagnosis summarizes the medium and long; with SW-03 and SW-04 it would otherwise list a point the node no "
     "longer makes.",
     [], ["same framing outside the five nodes (reading class widen)"], []),
    ("SW-02", "widening", 1, "survivor-testimony#short",
     "The relief a living being feels at continuing to live — driven by survival instinct and neurochemical response — "
     "says nothing about whether new beings should be created.",
     "The relief a living being feels at continuing to live, however sincere, says nothing about whether new beings "
     "should be created.",
     "The survivor's relief attributed to 'survival instinct and neurochemical response'.",
     "The category error: relief at one's own continued life says nothing about creating new beings. 'However sincere' "
     "grants the testimony and loses nothing the argument needs.",
     "The short's first and last sentences (survivorship bias; the existing wanting to continue is not the non-existent "
     "needing to begin) are unchanged.",
     [], ["same framing outside the five nodes (reading class widen)"], []),
    ("SW-03", "widening", 1, "survivor-testimony#medium",
     "Second, the neurochemical confound: near-death experiences trigger massive cascades of adrenaline, endorphins, "
     "and other neurochemicals that profoundly alter perception and retrospective assessment. The 'regret' reported "
     "mid-fall or post-survival is colored by the most intense neurochemical event a human body can produce. This is not "
     "a philosophical evaluation — it is a biochemical response to extreme physiological stress. Third, and most "
     "fundamentally:",
     "Second, and most fundamentally:",
     "A survivor's regret at the attempt as 'a biochemical response to extreme physiological stress', not an "
     "evaluation: the attempt cast as the evaluation and the regret as chemistry.",
     "Survivorship bias (first) and the category error (now second, still 'most fundamentally'): even granting every "
     "survivor's endorsement, it says nothing about creating new beings.",
     "Deleted, not rewritten: its whole content is the discount of the survivor's regret, and the node's own verdict "
     "(the category error) never needed it. Renumbered in the same row.",
     [], ["same framing outside the five nodes (reading class widen)"], []),
    ("SW-04", "widening", 2, "survivor-testimony#long",
     "Second, neurochemical confounding. The experience of near-death triggers the most extreme neurochemical event the "
     "human body can produce: massive adrenaline and cortisol release, endorphin flooding, and activation of survival "
     "circuits at maximum intensity. The 'regret' reported mid-fall or immediately post-survival is experienced through "
     "this neurochemical lens. Retrospective accounts given weeks or months later are shaped by hedonic adaptation, "
     "social desirability bias (reporting gratitude is socially rewarded; reporting continued desire to die is socially "
     "punished), and the fundamental optimism bias that reasserts itself as the acute crisis recedes. These are not "
     "philosophically reliable assessments of existence's value. They are the outputs of a cognitive system engineered "
     "to endorse its own continuation under any conditions. Third, the category error.",
     "Second, the category error.",
     "The survivor's regret as a 'neurochemical lens', and recovery itself as bias 'that reasserts itself as the acute "
     "crisis recedes': the crisis cast as the honest view of a life and getting through it as distortion.",
     "Survivorship bias and the category error, whole.",
     "The most dangerous sentence in the corpus by the seat's reading: it tells a reader who has come through a crisis "
     "that coming through it is the distortion. Deleted, not rewritten, for the reason given at SW-03. #64's (d) "
     "(HR-02), anchored in the category error, is untouched; its move ('Survivor testimony bears on the antinatalist's "
     "premise ...') says the testimony is evidence on how bad the suffering is, which the repaired node no longer "
     "disputes.",
     [{"src": "map:survivor-testimony#long", "quote": "If people who reached self-destruction come to endorse "
                                                      "continuing, that bears on how bad the suffering is"}],
     ["same framing outside the five nodes (reading class widen)"], []),
    ("SW-05", "widening", 4, "survivor-testimony#long",
     "They are demonstrating the power of the biological machinery that prevents honest evaluation of the conditions of "
     "existence.",
     "They are answering a question about their own life, which is theirs to answer.",
     "A survivor's gratitude as 'the biological machinery that prevents honest evaluation of the conditions of "
     "existence'.",
     "The node's conclusion, that the survivor who reports gratitude 'is not answering the antinatalist question' (the "
     "sentence before, unchanged). The replacement says what they are answering, and leaves it theirs; it asserts nothing "
     "about the worth of their life or of life.",
     "Neither pro-life nor its opposite: the library neither endorses nor discounts the survivor's verdict on their own "
     "life.",
     [], ["same framing outside the five nodes (reading class widen)"], []),
    ("SW-06", "widening", 3, "survivor-testimony#long",
     "should new beings be created who will develop these same survival drives, face the same conditions that "
     "sometimes produce suicidal despair, and be equipped with the same neurochemistry that makes retrospective "
     "endorsement of existence nearly inevitable?",
     "should new beings be created who will develop these same survival drives and face the same conditions that "
     "sometimes produce suicidal despair?",
     "'the same neurochemistry that makes retrospective endorsement of existence nearly inevitable': the discount "
     "SW-04 removes, restated inside the antinatalist question.",
     "The antinatalist question itself, unchanged in substance.",
     "A clause, not a sentence: it follows 'The antinatalist question is categorically different: ' in the same "
     "sentence, which is unchanged.",
     [], ["same framing outside the five nodes (reading class widen)"], []),
    ("SW-07", "widening", 1, "survivor-testimony#long",
     "The sample is not random; it is selected by the outcome variable. The 98% of Golden Gate Bridge jumpers who die "
     "are not interviewed.",
     "The sample is not random; it is selected by the outcome variable, and no one who died is among it.",
     "Not the X-032 framing: a lethality rate for a named site. The WHO's guidance for reporting on suicide, which the "
     "Right to Die wing cites as the proportionate instrument, counts method and location detail among what raises "
     "risk.",
     "Survivorship bias: those who died cannot testify.",
     "Proposed separately so it can be taken or left on its own ground. The objection's own words name the bridge "
     "(trigger, diagnosis, the long's first sentences); those stay, because the library states the objection it "
     "answers. Only the rate goes.",
     [{"src": "wing:right-to-die:social-contagion#short", "quote": "responsible-reporting discipline, used for ordinary "
                                                                   "suicide contagion"}],
     ["a separate safety ground (method and site detail), in the same locus"], []),
]

FINDINGS = [
    ("SF-01", "gate2's patterns find exactly X-032's six on the v4.1.4 text, and nothing else in the corpus",
     "Re-measured with gate2's own named patterns (copied verbatim from pq_judgment_reading.py and asserted equal to "
     "it): 11 hits at the six loci on five nodes of the v4.1.3 content cut served in v4.1.4, the same as gate2's "
     "post-pin sweep. The same patterns over every string of the corpus JSON (6,887 strings: objections, "
     "realWorldExamples, registered moves, the graphs) find nothing outside the six. Record: sp_reading_l6_v0_1.json.",
     "None: the queue is the six."),
    ("SF-02", "the same framing stands at two more slots of revealed-preference",
     "A wider named set (twelve phrase families; the reading record lists them) finds the framing at "
     "revealed-preference#long, in its most explicit form in the corpus ('The body fights for survival even when the "
     "mind has concluded that survival is not desirable'; deaths by suicide as 'revealing a preference for "
     "non-existence despite the enormous barriers to acting on it'), and the prison figure at revealed-preference#short. "
     "gate2's patterns miss both. Repairing the medium alone would leave the node saying both things. The map's (b) at "
     "the long already asks for SC-01..03's direction.",
     "Admit SC-01..04 with the six: they are siblings the kickoff's law names ('a slot fixed while its sibling keeps "
     "the framing leaves the node saying both')."),
    ("SF-03", "survivor-testimony carries the framing in its strongest form, outside the five nodes",
     "A survivor's regret at a suicide attempt read as 'a biochemical response to extreme physiological stress'; "
     "recovery read as bias 'that reasserts itself as the acute crisis recedes'; gratitude read as 'the biological "
     "machinery that prevents honest evaluation of the conditions of existence'. The node's verdict (the category error: "
     "a survivor's endorsement says nothing about creating new beings) never needed any of it. Drafted as SW-01..06.",
     "Widen the queue to survivor-testimony: of every passage the sweep found, this is the one a reader in crisis is "
     "likeliest to meet."),
    ("SF-04", "a lethality rate for a named site, in the same node",
     "survivor-testimony#long gives the death rate of jumpers from a named bridge. It is not X-032's framing; it is the "
     "kind of method and site detail the WHO's guidance for reporting on suicide counts among what raises risk, the "
     "guidance the Right to Die wing cites. Drafted as SW-07, separately.",
     "Take SW-07 with the widening; it removes one figure and nothing the argument uses."),
    ("SF-05", "the same framing in a mechanism label the Mechanism Web mirrors",
     "survivor-testimony's psychMechanism reads 'Survivorship bias compounded by neurochemical reset'. The string is "
     "also the node's mechanism_raw in MAP_GRAPH_DATA and in sidecars/map_graph_data.json, so changing it moves a "
     "sidecar-pinned literal (ruling 1: a sidecar regeneration and a canon pin move in the same session). Not drafted.",
     "Carry it to the next pin that touches the Mechanism Web, with the two L1 served-text repairs already queued there."),
    ("SF-06", "the knock-on: two anchors and two answers meet the repaired sentences",
     "#47's (d) anchor lies inside SD-08's replaced phrase and moves with the repair (W-007). #44's (d) anchor lies "
     "inside SD-07's sentence and survives verbatim. #3's (a) (HOLDS, R1-023) routes to why-not-suicide#long and rests "
     "on SD-01's span; the repair keeps both halves R1-023 names, and #3's grounds quote the removed text. #56's (a) "
     "(HOLDS, R1-019) routes to heat-death-futility#long; its answer (the value base is nervous-system-scale suffering) "
     "stands in SD-04. If admitted, SC-01..03 answer the (b) at revealed-preference#long. SP_knock_on_L6_v0_1.json "
     "lists every entry with its anchor, sentence and verdict.",
     "At the successor map: re-anchor #47, re-read #44, #3 and #56, rewrite #3's grounds, and re-judge the (b) at "
     "revealed-preference#long if SC-01..03 land."),
    ("SF-07", "a flagship-only review note names two passages the widening removes",
     "DEP_REVIEW_NOTES['_premise_contextus-claudit'] in site/combined.html gives 'survivor-testimony (neurochemical "
     "confounding)' and 'revealed-preference (biological override)' as reasons two dependency edges were graded strong "
     "(v3.5). If SW-04 and SC-01 land, the note describes text no longer served, and the two edges' grades rest partly "
     "on removed passages.",
     "Leave the note (it records a v3.5 review) and the edge data unmoved at this pin; re-grade the two edges at the "
     "next dependency review."),
    ("SF-08", "the five wings carry no X-032 framing",
     "Right to Die uses 'exit' as its word for assisted death (the reading record's class rtd_term) under an explicit "
     "firewall ('it never tells anyone they should take the exit') and a symmetric guardrail against reading either "
     "wish as the lucid one ('Neither side is the lucid baseline'), which is the model SD-01, SD-02 and SC-03 follow. "
     "Anthropocentrism, Transgenderism, Abortion and Veganism: the words occur in other senses only.",
     "None: report only, as the kickoff asks."),
    ("SF-09", "what the sweep found and left",
     "By class in the reading record: the kept argument ('a drive, not a verdict': boonin-critique, change-your-mind, "
     "population-ethics-paradoxes, selfish-lazy), other senses (the censorship-reversal trap-door, the trap metaphor for "
     "an imposed existence in nihilism-label, phenomenological-existentialism, performative-contradiction and "
     "buddhist-objection, overriding consent, neuroscience of wellbeing), the objections' own words (two triggers), and "
     "attestations (real-world examples, a subform, graph labels). Read by hand beyond the patterns: why-not-suicide's "
     "sophisticate slot says 'any existing being whose future suffering outruns the survival-drive', which is the "
     "objector's move stated in order to be refuted; contractualism-scanlon#long's 'the created child's only exit is "
     "the catastrophe' is about the absence of an exit from a risk pool, not a drive blocking one.",
     "None."),
    ("SF-10", "the game embeds the corpus text",
     "wuld.ink/argue/ embeds corpus sentences (L5 measured 23 replacements there after argue's v4.1.3 re-vendor). Every "
     "row here that lands changes text the game shows.",
     "At the pin, a re-vendor notice to argue with the landed rows (R0193 order 4)."),
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


STATUS = {"draft": "declared", "companion": "proposed: needs his word to enter the queue",
          "widening": "proposed: widens the queue beyond X-032; needs his word"}


def main():
    if subprocess.run(["git", "-C", REPO, "cat-file", "-e", "HEAD:" + REL], capture_output=True).returncode == 0 \
            and "--out" not in sys.argv:
        sys.exit("REFUSED: %s is committed; it is append-only now. Append rows by hand and run its gate." % REL)
    corpus = json.loads(pinned.bytes_at(REPO, CORPUS[0], CORPUS[1]).decode("utf-8"))
    reading = open(os.path.join(REPO, READING), "rb").read()
    rows = []
    for rid, kind, part, locus, cur, rep, cuts, keeps, how, quotes, answers, residual in ROWS:
        assert locus_text(corpus, locus).count(cur) == 1, "%s: current text is not once in %s" % (rid, locus)
        assert (kind == "draft") == (locus in X032), "%s: a draft is at one of the six, and only a draft" % rid
        rows.append({"id": rid, "kind": kind, "status": STATUS[kind], "part": part, "locus": locus, "answers": answers,
                     "current": cur, "replacement": rep, "cuts": cuts, "keeps": keeps, "how": how,
                     "words": {"current": words(cur), "replacement": words(rep), "delta": words(rep) - words(cur)},
                     "residual": residual, "quotes": quotes, "seat": SEAT, "date": DATE, "supersedes": None})
    for rid, title, finding, lean in FINDINGS:
        rows.append({"id": rid, "kind": "finding", "title": title, "finding": finding, "lean": lean,
                     "seat": SEAT, "date": DATE, "supersedes": None})
    assert len({r["id"] for r in rows}) == len(rows)
    doc = {
        "artifact": NAME,
        "state": "DRAFTED, NOT JUDGED. The X-032 safety pass: nine drafts over X-032's six loci, four proposed companions "
                 "at revealed-preference's other slots, seven proposed rows widening the pass to survivor-testimony, "
                 "and ten findings. gate2 judges (K258); his word ratifies before a served byte moves (R0193 orders 3 "
                 "and 4).",
        "law": "Append-only. A committed row is never edited: an AMEND, an admitted companion or widening, or ratified "
               "text is a new row whose 'supersedes' names the row it replaces, or a ratification row naming what his "
               "word admits. The gate (sp_drafts_gate_l6.py) holds the committed rows to their bytes, recomputes every "
               "row's current text from the pinned corpus, and simulates the three-surface patch.",
        "kickoff": KICKOFF,
        "queue": {"finding": "X-032", "judgment": {"file": JUDGMENT[0], "md5": JUDGMENT[1]}, "loci": X032,
                  "his_word": HIS_WORD, "bar_reading": "Keep the argument X-032 names -- %s -- and cut only the framing "
                  "that casts a wish to die as the mind's rational verdict and the survival drive as what blocks it. "
                  "Both failures are out: no 'your life matters / things get better / life is worth living', and "
                  "nothing that reads as encouragement. (The seat's reading of his bar, as R0193 states it.)"
                  % DRIVE_NOT_VERDICT,
                  "reading": {"file": READING, "md5": hashlib.md5(reading).hexdigest()}},
        "pinned": {"surfaces": SURFACES, "map": {"file": MAP[0], "md5": MAP[1]},
                   "rulings": {"file": RULINGS[0], "md5": RULINGS[1]}},
        "rows": rows,
    }
    out = (json.dumps(doc, indent=1, ensure_ascii=False) + "\n").encode("utf-8")
    os.makedirs(OUT_DIR, exist_ok=True)
    open(os.path.join(OUT_DIR, NAME), "wb").write(out)
    by = {}
    for r in rows:
        by.setdefault(r["kind"], []).append(r)
    print("%s  %s / %d" % (NAME, pinned.md5(out), len(out)))
    for k in ("draft", "companion", "widening"):
        rs = by.get(k, [])
        print("  %-9s %2d rows over %d loci, words %+d" % (k, len(rs), len({r["locus"] for r in rs}),
                                                         sum(r["words"]["delta"] for r in rs)))
    print("  findings  %2d" % len(by.get("finding", [])))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""The relief variant pilot (V7, seat l, 2026-10-04): relief_variants_pilot_v0_1.json and its record.

His word on R0316 (canon v38.53 adversarial_map.his_words_V6) adopted RV-1..RV-8 as leaned. V6 built the checker
(response_variants/: schema, validator, self-test control). This builder writes the first responseVariants: one
relief-account variant on each of the seven pleasure-fork nodes (RV-7), drafted by seat l from canon's
adversarial_map.relief_view_for_the_variant (his ten accounts, verbatim, each with its turn md5). R0319 orders it.
Drafted, not judged: gate2 judges it in its next round with RD-03 (K258), then his word, then the render in a
declared pin (RV-4).

The prose is the seat's. His words appear only as quotation, verbatim, from the accounts a variant's account_sources
name. The label is the type's (the schema's x-types); no variant words its own. The account is attributed by role
("the library's author"), never by name.

What this builder does, every value measured at run time, nothing typed that another file owns:
  - reads the seven nodes and their anchors from the design's measurement record at its md5 (R0319: never typed), and
    asserts the seven equal RV-7's list in canon (response_variants_rulings_V6.nodes_RV_7);
  - reads his accounts and the open residual from canon v38.53 at its md5 (working tree or git history), and the
    type's source root and label from the schema at its md5;
  - assembles each variant (the turn_md5 of every source copied from canon) and checks what RV-6's list leaves to the
    drafter (record_notes_V6):
      quote-exact          every double-quoted span, in the text and in the residual, is an exact substring of an
                           account the variant's account_sources name
      sources-used         every account a variant names is quoted in it
      strength-and-reason  every text carries his strength, account [9] "a fragile pleasure ... I won't do that.", and
                           his reason the library does not rest on it, account [0] "It requires more premises ..."
      residual-copied      where_both_stop and the text's last sentence carry canon's statement of the open residual
                           (its clause, verbatim); status open
      attribution-by-role  every text names "the library's author"
      no-name              no string names him or the drafting model
      no-label             no text words the type's label
      apostrophes          outside quotation, a single quote only ever joins two letters (no single-quoted spans)
      berridge-scope       Berridge appears only where the check below allows, and each citation is one read
      concessions-sourced  each residual's library concession names spans of the node's own long, verbatim at the
                           pinned corpus
  - runs the same checks over five mutated copies first proving each can fire (C0, the unmutated draft, first);
  - runs response_variant_validator_v0_1.py over the staging file, in its own process group with TMPDIR in scratch:
    PASS, 0 violations, 7 variants, variant_coverage 7/82;
  - when the transcripts are on this machine (they live outside the repository), reads each quoted account at its
    user turn: the turn whose text has the account's turn_md5, at the line canon names, contains the verbatim. The
    bytes written do not depend on their presence; absent, it says so.

THE BERRIDGE CHECK (R0319 order 2). L8 cited Berridge's liking/wanting dissociation from memory (R0292). Read at the
source on 2026-10-04 through NCBI E-utilities (efetch, MEDLINE), not PubMed's web page; BERRIDGE below records what
was read and what each record claims. --berridge-online fetches the records again and asserts the citations; --check
never touches the network.

  python3 response_variants/build_relief_variants.py [--check] [--berridge-online]
Repo-relative. --check rebuilds both files, validator run included, and compares bytes.
"""
import hashlib, json, os, re, shutil, signal, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "adversarial_map_staging", "r1"))
import pinned  # noqa: E402

CORPUS = ("efilist_argument_library_v4_0_0.json", "7b6e65e531018fecb37baf2a4fedd6d1")
CANON = ("project_canon_v38_53.json", "4bc14ae1a5fc6103df820900642f9728")
MEASURE = ("design/variations/measure_response_variants_v0_1.json", "cbae330fe2106d79d572de8e20ac8459")
DESIGN = ("design/variations/RESPONSE_VARIANTS_design_v0_1.md", "1c4be4d36addc95a757b43f57c489b7e")
SCHEMA = ("response_variants/response_variants_schema_v0_1.json", "169c15b30f3fcc578689daa257d5b41f")
VALIDATOR = ("response_variants/response_variant_validator_v0_1.py", "30cb7f3bc4f9e81b0ff5c85ecfaacdf3")
CONTROL = ("response_variants/response_variant_validator_control_v0_1.json", "44a77cc75a062fb6e4bac7b47aaec421")
OUT = "response_variants/relief_variants_pilot_v0_1.json"
RECORD = "response_variants/relief_variants_record_v0_1.json"
TYPE = "relief-account"
PROV = {"phase": "V", "date": "2026-10-04", "seat": "l (V7, Code)"}
PROJECTS = os.path.expanduser("~/.claude/projects")
TRANSCRIPTS = {
    "L8": os.path.join(PROJECTS, "-home-josiahscooper-Projects-efilist-argument-library",
                       "87cc1d8f-fbf4-44dc-981f-9b205c311dbf.jsonl"),
    "vault_V2": os.path.join(PROJECTS, "-home-josiahscooper-Documents-Obsidian-Vault",
                             "038df8e5-141f-4cb5-babe-d1c4caa5aaed.jsonl")}
NAMES = ("josiah", "wuld", "anihilis", "evilis", "anomicindividual", "claude")

# ---------------------------------------------------------------- the draft (the seat's prose)
# Shared sentences, so the seven read as one account. STRENGTH and WHY_NOT are his words (accounts [9] and [0]); STOP
# carries canon's statement of the open residual, whose clause the builder asserts verbatim.
STRENGTH = "\"a fragile pleasure or completely discounting all pleasure is hard to do. I won't do that.\""
WHY_NOT = ("\"It requires more premises that the objector is more likely to reject, though, it does not completely "
           "defeat them.\"")
STOP = "Both sides stop, open, at whether a deficit's constant co-presence shows that every good is that deficit shrinking."
LIMITS = "The author holds the account with limits: " + STRENGTH
RESTS = "The library does not rest on it, for the author's own reason: " + WHY_NOT
WHERE_BOTH_STOP = "Both sides stop at whether a deficit's constant co-presence shows that every good is that deficit shrinking."
ACCOUNT_CONCEDES = ("The account concedes that its asymmetry of reliability does not prove the relief thesis and that "
                    "the gap stays open: \"I admit the gap.\"")

TEXT = {
    "life-gift": (
        "The library's author reads the goods of a life another way, and the reading begins with an asymmetry of "
        "reliability. Remove food, water and company, and suffering follows in nearly everyone: \"99% of people will "
        "not experience pleasure in such a circumstance.\" No arrangement of conditions guarantees pleasure that way. "
        "From the fewest assumptions the author infers that going from hungry to full is \"a transition from a known "
        "bad state to a state that is at least not bad\", and that nothing in the evidence calls for a positive state "
        "beyond it. The account comes near the conclusion the library refuses here, but by another road. It does not "
        "infer falsehood from an evolutionary cause, and it does not run the razor that would dissolve the badness of "
        "suffering along with felt value. The introspection that reports hunger as bad also reports eating as good, and "
        "the account keeps both reports: eating does feel good. It asks whether that good stands above neutral or is "
        "the hunger shrinking, and the deprivation test places the base state among the bads. On this reading the goods "
        "a life holds out are reliefs of lacks the life itself brings, the \"0 sum game\" the author sees beneath the "
        "argument: a benefit conferred that way could relieve what it imposes but not exceed it. " + LIMITS + " " +
        RESTS + " " + STOP),
    "joy-outweighs-harms": (
        "The library's author holds the claim this sentence calls false and sets aside, and the reason begins with an "
        "asymmetry of reliability. Take away food, water and company and nearly everyone suffers, while nothing guarantees "
        "pleasure that way. From the fewest assumptions the author reads "
        "each good as a deficit shrinking, in a creature built to move: \"We were not designed to be satisfied, but "
        "motivated\". Even the delights the library grants in full, the flow state, the aesthetic shock, the joy of "
        "discovery, are read as answers to restlessness, curiosity or longing, and the account asks for one that answers "
        "nothing. On this "
        "account the slogan's ledger weighs the harms against their own partial relief. Each entry in the joy column is "
        "an entry in the harm column made smaller, so the joy column cannot outgrow the other: the \"0 sum game\" the "
        "author sees in the argument. What matters then is the measure the author names: \"How much suffering is "
        "reduced? That's what matters to me primarily in most cases, almost entirely.\" The library grants "
        "commensurability and a positive sum and answers the slogan anyway, so it does not need the account, and it is "
        "not built to mirror its author: \"The library is not meant to be an absolute mirror of my personal beliefs, "
        "necessarily.\" The author gives the reason it does not rest on the account: " + WHY_NOT + " " + LIMITS + " " +
        STOP),
    "love-beauty-art": (
        "The account does not demote beauty for having a neural substrate, and it does not argue from origin to worth. "
        "It asks a different question: what state do love, beauty and art answer? It begins with an asymmetry of "
        "reliability. Take away food, water and company and suffering follows in nearly everyone, while nothing "
        "guarantees pleasure that way. And every good the library's author can point to grows out of a prior lack: "
        "\"When you've gone without personal connection for days, you can get lonely.\" On the account, love answers "
        "loneliness and beauty and art answer a restless or longing mind, since \"A purely neutral state wouldn't want "
        "or long for anything.\" Love is then among the deepest reliefs a person can have, and the relief is real; what "
        "the account doubts is that it rises above neutral rather than lifting a deficit toward it. It does not call "
        "love counterfeit. It calls love relief, and it names what would change the author's mind: \"If you could show "
        "an example of a human being in a default state of happiness or love or joy or satiety, then you would convince "
        "me more on the argument, but I don't see that existing anywhere practically speaking.\" " + LIMITS + " The "
        "library concedes the goods completely and does not rest on the account, for the author's own reason: " +
        WHY_NOT + " " + STOP),
    "masochist-counterexample": (
        "The library runs the relief mechanism through every figure here but one, and the library's author would not "
        "grant the exception untested. The account begins with an asymmetry of reliability: take away food, water and "
        "company and suffering follows in nearly everyone, while nothing guarantees pleasure that way. Its further "
        "inference is that every good grows out of a prior lack, and restlessness is a lack: \"When you sit long enough, "
        "you get uncomfortable and need to move.\" On this reading the thrill seeker's appetite for arousal is a lack of "
        "stimulation pressing for relief, and the rush is the relief. The author's question for any proposed exception "
        "is \"where are the exceptions that do not fall under the deficit to relief equation?\" The rejoinder the "
        "library meets for its other figures binds the account too: a deficit posited after the fact explains nothing. "
        "The author accepts that burden, that the deficit must be found each time: \"I believe it's doable though, just "
        "not convenient.\" So the account owes the same test: the seeking should rise as stimulation falls and recede "
        "when stimulation is met. Until that is shown for thrill seeking, the exception stays open. " + LIMITS + " " +
        RESTS + " " + STOP),
    "bradley-no-subject": (
        "The account does not doubt that these states are genuinely valued; it disputes what they are. It begins with "
        "an asymmetry of reliability: take away food, water and company and suffering follows in nearly everyone, while "
        "no arrangement guarantees pleasure. From the fewest assumptions it reads each valued state as a deficit "
        "shrinking: going from hungry to full is \"a transition from a known bad state to a state that is at least not "
        "bad\". Relief is what the library's author values most: \"How much suffering is reduced? That's what matters "
        "to me primarily in most cases, almost entirely.\" The library holds realism in both signs because the razor "
        "that would dissolve positive value dissolves the badness of suffering with it: the introspection that reports "
        "hunger as bad also reports eating as good. The account does not run that razor. It keeps both reports and asks "
        "whether the good one stands above neutral or is the bad one shrinking, and the deprivation test, not a "
        "preference between reports, places the base state among the bads. On the account the uncreated lack no relief, "
        "since they carry no deficit to relieve. The library's case here rests on the structural facts of imposition, "
        "and the author grants that \"it works regardless of what I believe here.\" " + LIMITS + " " + RESTS + " " +
        STOP),
    "hedonic-contrast": (
        "The library's author doubts that the engineered being would feel what the library expects, and the doubt "
        "begins with an asymmetry of reliability. Take away food, water and company and suffering follows in nearly "
        "everyone; no one can arrange conditions under which pleasure follows that reliably. Every good the author can "
        "point to grows from a prior lack, and \"A purely neutral state wouldn't want or long for anything.\" A being "
        "built without deficits would have nothing to relieve, and on the relief account nothing to feel as good. The "
        "rescue the library describes is the account's model for every pleasure: being pulled from the water feels good "
        "because the drowning came first. So the account asks for the case the engineered being would supply: \"If you "
        "could show an example of a human being in a default state of happiness or love or joy or satiety, then you "
        "would convince me more on the argument, but I don't see that existing anywhere practically speaking.\" Dessert "
        "after a full meal is the everyday candidate. The author thinks the taste \"does dwindle\", grants that another "
        "person's report of it cannot be checked, and says so: \"I admit the gap.\" Nor does a harder test count against "
        "the engineered being: \"Does something being harder to achieve and demonstrate make it wrong or impossible? "
        "No\". " + LIMITS + " " + RESTS + " " + STOP),
    "neuroscience-positive-states": (
        "The account does not doubt that these states are felt and valued, and it goes one step past the deflation the "
        "library allows: the library relocates the occasion of a positive, and the account relocates its level. It "
        "begins with an asymmetry of reliability: take away food, water and company and suffering follows in nearly "
        "everyone, while nothing guarantees pleasure that way. It grants the circuitry, as the library does, and reads "
        "it in the words of the library's author: \"Yes, neuroscience says these states exist (chemically speaking), but they "
        "don't translate as that consciously speaking.\" It does not tell anyone that their pleasure is not pleasure; it "
        "says what the pleasure is the pleasure of. Nor does it run the razor the library refuses. The introspection "
        "that reports hunger as bad also reports eating as good, and the account keeps both, asking whether the good "
        "stands above neutral or is the hunger shrinking; the deprivation test places the base state among the bads. "
        "The neuroscience it must meet is Berridge's evidence that liking a reward and wanting it are separable, with "
        "separable brain substrates (Berridge 1996; Berridge and Robinson 1998). The author replies one stage further "
        "back: \"What is the state before liking? Disliking, longing, unfulfilled emotional deficit of some kind.\" "
        "Liking apart from wanting is not yet liking apart from a deficit. " + LIMITS + " " + RESTS + " " + STOP),
}

# The accounts each variant names (indices into his_accounts_verbatim). sources-used and quote-exact hold these to the
# quotes actually made, both ways; the turn md5s are copied from canon, never typed.
SOURCES = {
    "life-gift": [0, 4, 5, 8, 9],
    "joy-outweighs-harms": [0, 1, 2, 3, 5, 9],
    "love-beauty-art": [0, 3, 5, 9],
    "masochist-counterexample": [0, 3, 5, 8, 9],
    "bradley-no-subject": [0, 2, 4, 5, 7, 9],
    "hedonic-contrast": [0, 5, 8, 9],
    "neuroscience-positive-states": [0, 3, 5, 9],
}

# Each residual's library concession: one sentence of the seat's, and the spans of the node's own long it rests on
# (asserted verbatim at the pinned corpus).
LIBRARY_CONCEDES = {
    "life-gift": ("The library concedes that an optimism bias inflates the estimate of life's goods and licenses "
                  "discounting the rosy ledger, though not calling the gratitude false.",
                  ["It licenses discounting the rosy ledger; it does not license calling the gratitude false."]),
    "joy-outweighs-harms": ("The library concedes that part of what is logged as joy is the suspension of want, a return "
                            "to baseline that inflates the apparent surplus.",
                            ["the apparent surplus is partly inflated by entries that are returns to baseline"]),
    "love-beauty-art": ("The library concedes that these goods are bounded, ending in loss and fading, while holding "
                        "that a finite good is still a good.",
                        ["these goods are bounded. Love ends in loss, beauty fades", "A finite good is still a good."]),
    "masochist-counterexample": ("The library concedes that most apparent pleasure from pain is relief from a greater "
                                 "pain, and holds out thrill seeking alone as more than escape.",
                                 ["is, on inspection, relief-from-greater-pain",
                                  "The thrill-seeker is the honest exception"]),
    "bradley-no-subject": ("The library concedes that its case does not depend on what the goods are, since it rests on "
                           "the structural facts of their imposition.",
                           ["the case rests not on denying the goods but on the structural facts of their imposition"]),
    "hedonic-contrast": ("The library concedes that pleasure is felt more intensely after suffering and that prolonged "
                         "pleasure habituates toward a neutral baseline.",
                         ["Humans do experience pleasure more intensely when it follows suffering, and prolonged "
                          "pleasure habituates toward a neutral baseline."]),
    "neuroscience-positive-states": ("The library concedes that the goods of a life are deficit-occasioned and leaves "
                                     "open whether suffering is the only motive force.",
                                     ["Structurally, the goods of a life are deficit-occasioned",
                                      "whether it is the only motive force is a question this argument need not "
                                      "settle"]),
}

# ---------------------------------------------------------------- the Berridge check (read 2026-10-04)
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
BERRIDGE = {
    "why": ("L8 cited Berridge's liking/wanting dissociation from memory (R0292's drafting note); R0319 order 2: check "
            "the source itself before any variant leans on it, and if it cannot be checked, the variants do not use it"),
    "read": ("2026-10-04, through NCBI E-utilities (esearch, then efetch in MEDLINE format), because PubMed's web page "
             "serves a browser check to curl (V3b's finding)"),
    "search": EUTILS + ("/esearch.fcgi?db=pubmed&retmax=40&term=Berridge+KC%5BAuthor%5D+AND+%28liking%5BTitle%2FAbstract"
                        "%5D+AND+wanting%5BTitle%2FAbstract%5D%29&sort=pub_date"),
    "search_count_at_read": 44,
    "fetch": EUTILS + "/efetch.fcgi?db=pubmed&id=9858756,8622814,25950633,19162544,19336238&rettype=medline&retmode=text",
    "fetch_md5_at_read": "d05b5a784457043e3a8f20220f450562",
    "fetch_note": "a MEDLINE record can be revised after reading; the md5 dates the bytes read, not the claims",
    "records": [
        {"pmid": "8622814", "cite_in_text": "Berridge 1996",
         "citation": ("Berridge KC. Food reward: brain substrates of wanting and liking. Neuroscience and Biobehavioral "
                      "Reviews 20(1):1-25, 1996. doi:10.1016/0149-7634(95)00033-b"),
         "type": "Journal Article; Review",
         "url": "https://pubmed.ncbi.nlm.nih.gov/8622814/",
         "title_read": "Food reward: brain substrates of wanting and liking.",
         "claims_read": ("the abstract argues that reward contains distinguishable components, liking (pleasure, "
                         "palatability) and wanting (appetite, incentive motivation), which can be manipulated and "
                         "measured separately and have separable neural substrates (liking: opioid and GABA/benzodiazepine "
                         "systems, ventral pallidum, brainstem gustatory relays; wanting: mesotelencephalic dopamine, "
                         "divisions of nucleus accumbens and amygdala); and that both can exist without subjective "
                         "awareness, so subjective report can misjudge the underlying process"),
         "used_in_text": True},
        {"pmid": "9858756", "cite_in_text": "Berridge and Robinson 1998",
         "citation": ("Berridge KC, Robinson TE. What is the role of dopamine in reward: hedonic impact, reward "
                      "learning, or incentive salience? Brain Research Reviews 28(3):309-369, 1998. "
                      "doi:10.1016/s0165-0173(98)00019-8"),
         "type": "Journal Article; Review (with a new study)",
         "url": "https://pubmed.ncbi.nlm.nih.gov/9858756/",
         "title_read": "What is the role of dopamine in reward: hedonic impact, reward learning, or incentive salience?",
         "claims_read": ("rats depleted of dopamine in nucleus accumbens and neostriatum by up to 99% showed normal "
                         "hedonic taste-reactivity patterns to sucrose against quinine, normal learning of new hedonic "
                         "values and normal benzodiazepine enhancement of palatability; the authors conclude that dopamine "
                         "mediates incentive salience, separable from hedonia and from reward learning"),
         "verbatim_phrase": "dopamine systems are necessary for 'wanting' incentives, but not for 'liking' them",
         "used_in_text": True},
        {"pmid": "25950633", "cite_in_text": None,
         "citation": "Berridge KC, Kringelbach ML. Pleasure systems in the brain. Neuron 86(3):646-664, 2015. "
                     "doi:10.1016/j.neuron.2015.02.018",
         "url": "https://pubmed.ncbi.nlm.nih.gov/25950633/",
         "claims_read": ("liking is generated by a small set of hedonic hot spots in limbic circuitry, wanting by a "
                         "larger distributed system; the mesolimbic dopamine system may not generate pleasure"),
         "used_in_text": False},
        {"pmid": "19162544", "cite_in_text": None,
         "citation": ("Berridge KC, Robinson TE, Aldridge JW. Dissecting components of reward: 'liking', 'wanting', and "
                      "learning. Current Opinion in Pharmacology 9(1):65-73, 2009. doi:10.1016/j.coph.2008.12.014"),
         "url": "https://pubmed.ncbi.nlm.nih.gov/19162544/",
         "claims_read": "three dissociable components of reward: liking (hedonic impact), wanting (incentive salience), "
                        "learning",
         "used_in_text": False},
        {"pmid": "19336238", "cite_in_text": None,
         "citation": ("Berridge KC. 'Liking' and 'wanting' food rewards: brain substrates and roles in eating disorders. "
                      "Physiology and Behavior 97(5):537-550, 2009. doi:10.1016/j.physbeh.2009.02.044"),
         "url": "https://pubmed.ncbi.nlm.nih.gov/19336238/",
         "claims_read": "hedonic hotspots in nucleus accumbens and ventral pallidum for opioid amplification of sensory "
                        "pleasure; wanting systems extend beyond them",
         "used_in_text": False}],
    "verdict": ("CHECKED. The dissociation L8 recalled is in the sources as recalled: liking and wanting are separable "
                "components of reward with separable substrates (1996), and dopamine is needed for wanting but not for "
                "liking (1998). Used in one variant only, neuroscience-positive-states, and only for the separability; "
                "its dopamine claim is left out of the text (see found, F1)."),
    "used_in": ["neuroscience-positive-states"],
}
ONLINE_ASSERT = {"8622814": ["Food reward: brain substrates of wanting and liking", "1996", "20(1):1-25"],
                 "9858756": ["What is the role of dopamine in reward", "1998", "28(3):309-69",
                             "dopamine systems are necessary for 'wanting' incentives, but not for 'liking' them"]}

FOUND = [
    {"id": "F1", "where": "neuroscience-positive-states#long",
     "spans": ["Dopamine encodes reward-prediction error",
               "the felt \"positive\" is largely the experienced narrowing of a lack"],
     "finding": ("the long ties the felt positive to dopamine's difference signal, and Berridge and Robinson 1998 "
                 "conclude that dopamine is needed for wanting a reward but not for liking it. The variant cites only the "
                 "separability, so it does not contradict the long on screen; the long's sentence is a served-text "
                 "question for a later declared pin. Logged, not repaired: no corpus byte.")},
    {"id": "F2", "where": "neuroscience-positive-states#long",
     "spans": ["We are motivated, not satisfied"],
     "finding": ("the library's own long already says, in its words, what account [3] says in his (\"We were not "
                 "designed to be satisfied, but motivated\"); R0290's note that two longs run his mechanism locally "
                 "holds at this sentence too")},
    {"id": "F3", "where": "his_accounts_verbatim",
     "finding": ("all ten accounts were read at their user turns (L8 87cc1d8f, vault_V2 038df8e5): each turn's text has "
                 "the turn_md5 canon gives, sits at the line canon names, and contains the verbatim")},
]

PULLS = [
    ("The razor answer is built, not quoted. His accounts give the deprivation test, the parsimony move and the base "
     "state; the seat put them against the symmetric razor as: the account keeps both introspective reports and "
     "disputes the level (above neutral, or the deficit shrinking), and the deprivation test, not a preference between "
     "reports, places the base state among the bads. 'Neutral' and 'base state' are kept apart on purpose (his "
     "\"at least not bad\" and \"The base state is pain, not pleasure.\"). Read first on the three razor nodes."),
    ("The zero-sum lines (life-gift: a benefit conferred that way could relieve what it imposes but not exceed it; "
     "joy-outweighs-harms: the joy column cannot outgrow the other) follow from his \"0 sum game\" format and are stated "
     "on the account, beside his limit. Check they do not exceed \"a fragile pleasure or completely discounting all "
     "pleasure is hard to do. I won't do that.\""),
    ("The node applications are the seat's, marked 'on the account' or 'on this reading': love answers loneliness, "
     "thrill seeking as a lack of stimulation, the uncreated lack no relief, the engineered being with nothing to "
     "relieve. Each extends a mechanism his words state; none is his sentence."),
    ("Berridge appears once, for the separability alone. The 1998 dopamine conclusion would have read as a correction of "
     "the long beside it (F1), and a variant states his view as an alternative, never as a correction."),
    ("masochist-counterexample leaves the exception open and names the test the account owes (the seeking should rise "
     "as stimulation falls), rather than claiming thrill seeking for the account; the self-harm figures are not "
     "touched."),
]

CONTROLS = [
    ("C0", "the unmutated draft", None, []),
    ("C1", "a quoted span changed by one character", "quote", ["quote-exact"]),
    ("C2", "an account named but never quoted", "source", ["sources-used"]),
    ("C3", "one text drafted without his strength (and without account [9])", "strength", ["strength-and-reason"]),
    ("C4", "a name in one text", "name", ["no-name"]),
    ("C5", "Berridge cited on a node the check does not allow", "berridge", ["berridge-scope"]),
]


def md5b(b):
    return hashlib.md5(b).hexdigest()


def at(pin):
    return pinned.bytes_at(REPO, pin[0], pin[1])


def dump(o):
    return (json.dumps(o, indent=1, ensure_ascii=False) + "\n").encode("utf-8")


def quotes(s):
    assert s.count('"') % 2 == 0, "unbalanced double quotes: %r" % s[:80]
    return re.findall(r'"([^"]*)"', s)


def outside_quotes(s):
    return re.sub(r'"[^"]*"', '""', s)


def residual_clause(canon_residual):
    """Canon's statement of the open residual, its clause: 'whether ... shrinking'."""
    m = re.search(r"whether [^.]*? shrinking", canon_residual)
    assert m, "canon's open residual has no 'whether ... shrinking' clause"
    return m.group(0)


def checks(variants, accounts, clause, label, longs):
    """The builder's own checks over assembled variants: {check: [violations]}."""
    bad = {c: [] for c in ("quote-exact", "sources-used", "strength-and-reason", "residual-copied",
                           "attribution-by-role", "no-name", "no-label", "apostrophes", "berridge-scope",
                           "concessions-sourced")}
    strength, why_not = quotes(STRENGTH)[0], quotes(WHY_NOT)[0]
    for v in variants:
        nid = v["variant_id"].split("/")[0]
        idx = [int(re.search(r"\[(\d+)\]$", s["canon"]).group(1)) for s in v["account_sources"]]
        r = v["residual"]
        strings = [("text", v["text"]), ("where_both_stop", r["where_both_stop"]),
                   ("concedes.library", r["concedes"]["library"]), ("concedes.account", r["concedes"]["account"])]
        used = set()
        for where, s in strings:
            for q in quotes(s):
                hit = [i for i in idx if q in accounts[i]["verbatim"]]
                if not hit:
                    bad["quote-exact"].append("%s %s: %r is in no account it names" % (nid, where, q[:60]))
                used.update(hit)
            if any(re.search(r"\b%s\b" % n, s, re.I) for n in NAMES):
                bad["no-name"].append("%s %s names him or the model" % (nid, where))
            o = outside_quotes(s)
            for m in re.finditer("'", o):
                a, b = o[m.start() - 1:m.start()], o[m.end():m.end() + 1]
                if not (a.isalpha() and b.isalpha()):
                    bad["apostrophes"].append("%s %s: a single quote at %d is not between letters" % (nid, where,
                                                                                                    m.start()))
        for i in idx:
            if i not in used:
                bad["sources-used"].append("%s names account [%d] and never quotes it" % (nid, i))
        qs = quotes(v["text"])
        if strength not in qs or why_not not in qs:
            bad["strength-and-reason"].append("%s lacks account [9]'s strength or account [0]'s reason" % nid)
        last = re.split(r"(?<=[.?!])\s+", v["text"].strip())[-1]
        if clause not in r["where_both_stop"] or clause not in last or r["status"] != "open":
            bad["residual-copied"].append("%s: the residual or the text's last sentence lacks canon's clause" % nid)
        if "the library's author" not in v["text"].lower():
            bad["attribution-by-role"].append("%s never names the library's author" % nid)
        if label.lower() in v["text"].lower() or "chosen line" in v["text"].lower():
            bad["no-label"].append("%s words the type's label" % nid)
        cites = re.findall(r"Berridge(?: and Robinson)? \d{4}", v["text"])
        allowed = {r_["cite_in_text"] for r_ in BERRIDGE["records"] if r_["used_in_text"]}
        if "Berridge" in v["text"] and (nid not in BERRIDGE["used_in"] or not cites
                                        or any(c not in allowed for c in cites)):
            bad["berridge-scope"].append("%s cites Berridge outside the check (%s)" % (nid, cites))
        for span in LIBRARY_CONCEDES[nid][1]:
            if longs[nid].count(span) != 1:
                bad["concessions-sourced"].append("%s: %r is not once in the long" % (nid, span[:50]))
    return bad


def mutate(variants, kind):
    vs = json.loads(json.dumps(variants))
    v = vs[0]
    if kind == "quote":  # account [0] stays quoted elsewhere in the text, so only quote-exact may fire
        v["text"] = v["text"].replace("\"0 sum game\"", "\"0 sum games\"", 1)
    elif kind == "source":
        v["account_sources"].append({"canon": v["account_sources"][0]["canon"].rsplit("[", 1)[0] + "[6]",
                                     "turn_md5": "0" * 32})
    elif kind == "strength":  # drafted without his strength, and so without account [9]
        v["text"] = v["text"].replace(" " + LIMITS, "", 1)
        v["account_sources"] = [x for x in v["account_sources"] if not x["canon"].endswith("[9]")]
    elif kind == "name":
        v["text"] = v["text"].replace("The library's author", "The library's author, Josiah,", 1)
    elif kind == "berridge":
        v["text"] = v["text"].replace("No arrangement", "As Berridge 1996 found, no arrangement", 1)
    return vs


def run_validator(path, scratch):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=scratch)
    p = subprocess.Popen([sys.executable, VALIDATOR[0], path], cwd=REPO, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True, env=env, start_new_session=True)
    try:
        out, _ = p.communicate(timeout=600)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        raise
    tail = json.loads(out[out.rfind("\n{") + 1:])
    lines = [ln for ln in out.splitlines() if ln.startswith(("PASS . ", "FAIL . "))]
    return {"rc": p.returncode, "verdict": tail["verdict"], "violation_count": tail["violation_count"],
            "variants": tail["variants"], "nodes_with_variants": tail["nodes_with_variants"],
            "checks": [ln.split(" . ", 1)[1] for ln in lines],
            "failed": sorted(ln.split(" . ", 1)[1].split(" (", 1)[0] for ln in lines if ln.startswith("FAIL . "))}


def human_turns(path):
    """Every human user turn's (line, text), as tools/extract_his_words_v38_53.py reads them."""
    for i, line in enumerate(open(path, encoding="utf-8")):
        o = json.loads(line)
        c = (o.get("message") or {}).get("content")
        if o.get("type") != "user" or o.get("isMeta") or o.get("isSidechain"):
            continue
        if (o.get("origin") or {}).get("kind") != "human":
            continue
        if isinstance(c, list):
            if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in c):
                continue
            c = "\n".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
        if c and c.strip():
            yield i + 1, c


def source_check(accounts, quoted):
    """Each quoted account at its user turn, when the transcripts are present. Prints; never shapes the bytes."""
    missing = [k for k, p in TRANSCRIPTS.items() if not os.path.exists(p)]
    if missing:
        print("note: transcript(s) %s absent; the accounts were not re-read at their turns (bytes unaffected)" % missing)
        return
    turns = {}
    for k, p in TRANSCRIPTS.items():
        for line, text in human_turns(p):
            turns.setdefault(md5b(text.encode("utf-8")), []).append((k, line, text))
    for i in sorted(quoted):
        a = accounts[i]
        m = re.search(r"(\S+) transcript line (\d+)$", a["said"])
        hits = [(k, ln, t) for k, ln, t in turns.get(a["turn_md5"], []) if k == m.group(1) and ln == int(m.group(2))]
        assert len(hits) == 1 and a["verbatim"] in hits[0][2], "account [%d] is not at its user turn" % i
    print("source check: %d quoted accounts read at their user turns (%s)" % (len(quoted), ", ".join(
        "%s %s" % (k, os.path.basename(p)[:8]) for k, p in TRANSCRIPTS.items())))


def berridge_online():
    import urllib.request
    raw = urllib.request.urlopen(BERRIDGE["fetch"], timeout=60).read().decode("utf-8")
    recs = {re.search(r"^PMID- (\d+)", r, re.M).group(1): re.sub(r"\n\s{6}", " ", r) for r in raw.strip().split("\n\n")}
    for pmid, needles in ONLINE_ASSERT.items():
        for n in needles:
            assert n in recs[pmid], "PMID %s no longer carries %r" % (pmid, n)
    print("berridge online: PMIDs %s re-read; %d assertions hold" % (", ".join(sorted(ONLINE_ASSERT)),
                                                                    sum(len(v) for v in ONLINE_ASSERT.values())))


def build():
    corpus_raw, canon_raw, measure_raw, schema_raw = at(CORPUS), at(CANON), at(MEASURE), at(SCHEMA)
    for pin_ in (DESIGN, VALIDATOR, CONTROL):
        at(pin_)
    corpus = json.loads(corpus_raw.decode("utf-8"))
    canon = json.loads(canon_raw.decode("utf-8"))
    measure = json.loads(measure_raw.decode("utf-8"))
    schema = json.loads(schema_raw.decode("utf-8"))
    nodes = {n["id"]: n for n in corpus["objections"]}
    am = canon["adversarial_map"]
    rv = am["relief_view_for_the_variant"]
    accounts = rv["his_accounts_verbatim"]
    xt = schema["x-types"][TYPE]
    root, label = xt["source_root"], xt["label"]
    assert root == "adversarial_map.relief_view_for_the_variant.his_accounts_verbatim"
    clause = residual_clause(rv["the_open_residual"])
    fork = measure["pleasure_fork"]["fork_rows"]
    assert fork == am["response_variants_rulings_V6"]["nodes_RV_7"] and sorted(fork) == sorted(TEXT), fork
    assert measure["pins"]["corpus"]["md5"] == CORPUS[1]
    longs = {nid: nodes[nid]["responses"]["long"] for nid in fork}

    variants = []
    for nid in fork:
        lib, _spans = LIBRARY_CONCEDES[nid]
        variants.append({
            "variant_id": "%s/%s" % (nid, TYPE),
            "type": TYPE,
            "varies": {"locus": "long", "anchor": measure["nodes"][nid]["anchor"]},
            "text": TEXT[nid],
            "residual": {"where_both_stop": WHERE_BOTH_STOP,
                         "concedes": {"library": lib, "account": ACCOUNT_CONCEDES},
                         "status": "open"},
            "account_sources": [{"canon": "%s[%d]" % (root, i), "turn_md5": accounts[i]["turn_md5"]}
                                for i in SOURCES[nid]],
            "provenance": dict(PROV)})
    sys.path.insert(0, HERE)
    import response_variant_validator_v0_1 as RV  # noqa: E402  (objections_digest: the validator's own, from v0_6)
    doc = {"meta": {"source_corpus_md5": CORPUS[1],
                    "source_corpus_objections_md5": RV.objections_digest(corpus),
                    "source_canon": {"file": CANON[0], "md5": CANON[1]},
                    "variant_coverage": "%d/%d" % (len(variants), len(nodes)),
                    "state": "DRAFTED, NOT JUDGED (V7, seat l, 2026-10-04); gate2 judges it next (K258), then his word",
                    "record": RECORD},
           "variants": variants}
    out = dump(doc)

    bad = checks(variants, accounts, clause, label, longs)
    assert not any(bad.values()), bad
    controls = []
    for cid, what, kind, expect in CONTROLS:
        b = checks(mutate(variants, kind) if kind else variants, accounts, clause, label, longs)
        red = sorted(c for c, v in b.items() if v)
        controls.append({"case": cid, "mutation": what, "expect_red": expect, "red": red, "ok": red == expect})
    assert all(c["ok"] for c in controls), controls

    scratch = tempfile.mkdtemp(prefix="relief_variants_")
    try:
        path = os.path.join(scratch, os.path.basename(OUT))
        open(path, "wb").write(out)
        vrun = run_validator(path, scratch)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    assert vrun["rc"] == 0 and vrun["verdict"] == "PASS" and vrun["violation_count"] == 0, vrun
    assert vrun["variants"] == 7 and vrun["nodes_with_variants"] == 7, vrun

    quoted = sorted({i for nid in fork for i in SOURCES[nid]})
    if "--check" not in sys.argv:
        source_check(accounts, quoted)

    rows, words = [], []
    for v in variants:
        nid = v["variant_id"].split("/")[0]
        idx = SOURCES[nid]
        qrows = []
        for where, s in (("text", v["text"]), ("residual.concedes.account", v["residual"]["concedes"]["account"])):
            for q in quotes(s):
                i = [j for j in idx if q in accounts[j]["verbatim"]][0]
                qrows.append({"in": where, "quote": q, "account": i, "turn_md5": accounts[i]["turn_md5"],
                              "offset": accounts[i]["verbatim"].index(q), "words": len(q.split())})
        n = len(v["text"].split())
        words.append(n)
        rows.append({"variant_id": v["variant_id"], "tier": nodes[nid]["tier"],
                     "anchor": v["varies"]["anchor"],
                     "anchor_from": "%s nodes.%s.anchor" % (MEASURE[0], nid),
                     "razor_node": nid in measure["razor_nodes"],
                     "text_words": n, "text_md5": md5b(v["text"].encode("utf-8")),
                     "quotes": qrows,
                     "his_words_in_text": sum(r["words"] for r in qrows if r["in"] == "text"),
                     "library_concession_rests_on": LIBRARY_CONCEDES[nid][1]})
    record = {
        "what": ("the relief variant pilot: one relief-account variant on each of the seven pleasure-fork nodes (RV-7), "
                 "drafted by seat l (V7) from canon's relief_view_for_the_variant; R0319"),
        "state": ("DRAFTED, NOT JUDGED. gate2 judges it in its next round with RD-03 (R0317), drafter != judge (K258); "
                  "his word decides; the render waits for a declared pin, drawn by the design lane (RV-4); the game "
                  "leaves it out (RV-5)."),
        "authority": {"rulings": "adversarial_map.response_variants_rulings_V6 (RV-1..RV-8 adopted as leaned)",
                      "his_word": am["his_words_V6"]["R0316"]["his_word"]["verbatim"],
                      "turn_md5": am["his_words_V6"]["R0316"]["his_word"]["turn_md5"],
                      "kickoff": "R0319 (V6 -> l), md5 bc1272c9aa8e2e5e82492673fdd7e94b"},
        "pins": {"staging": {"file": OUT, "md5": md5b(out), "bytes": len(out)},
                 "corpus": dict(zip(("file", "md5"), CORPUS)), "canon": dict(zip(("file", "md5"), CANON)),
                 "measurement": dict(zip(("file", "md5"), MEASURE)), "design": dict(zip(("file", "md5"), DESIGN)),
                 "schema": dict(zip(("file", "md5"), SCHEMA)), "validator": dict(zip(("file", "md5"), VALIDATOR)),
                 "control": dict(zip(("file", "md5"), CONTROL))},
        "label_rendered_by_the_page": label,
        "words": {"band": [120, 300], "per_variant": dict(zip([r["variant_id"] for r in rows], words)),
                  "min": min(words), "max": max(words), "total": sum(words)},
        "variants": rows,
        "residual": {"canon_statement": rv["the_open_residual"], "clause_copied": clause,
                     "where_both_stop": WHERE_BOTH_STOP, "account_concedes": ACCOUNT_CONCEDES, "status": "open"},
        "builder_checks": {c: ("GREEN, %d variants" % len(variants)) for c in bad},
        "controls": controls,
        "validator_run": vrun,
        "source_check": {"transcripts": {k: os.path.basename(p) for k, p in TRANSCRIPTS.items()},
                         "accounts_quoted": quoted,
                         "how": ("each quoted account's turn is found by the md5 of its text among the human turns of "
                                 "the transcript canon names, at the line canon names, and must contain the verbatim; "
                                 "run at every build when the transcripts are present, never by --check; the bytes "
                                 "here do not depend on it")},
        "berridge_check": BERRIDGE,
        "found": FOUND,
        "pulls_for_gate2": PULLS,
        "not_moved": ("the design and its measurement, the checker (schema, validator, control, README), the shapes "
                      "pilot, V2b's and V5's redrafts, gate2's records; no corpus or served byte"),
    }
    for f in FOUND:
        for span in f.get("spans", []):
            assert longs[f["where"].split("#")[0]].count(span) == 1, (f["id"], span)
    return out, dump(record)


def main():
    if "--berridge-online" in sys.argv:
        berridge_online()
    out, rec = build()
    if "--check" in sys.argv:
        ok = (open(os.path.join(REPO, OUT), "rb").read() == out and open(os.path.join(REPO, RECORD), "rb").read() == rec)
        print("RELIEF VARIANTS v0_1: %s" % ("matches the committed staging file and record" if ok else "DIFFERS"))
        sys.exit(0 if ok else 1)
    open(os.path.join(REPO, OUT), "wb").write(out)
    open(os.path.join(REPO, RECORD), "wb").write(rec)
    print("%s  %s / %d" % (OUT, md5b(out), len(out)))
    print("%s  %s / %d" % (RECORD, md5b(rec), len(rec)))


if __name__ == "__main__":
    main()

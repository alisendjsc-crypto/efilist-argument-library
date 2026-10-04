#!/usr/bin/env python3
"""The argument-shapes pilot (V2, seat l, 2026-10-03): shapes_pilot_v0_1.json and its measurement.

Drafted under R0295 (R0228's drafting orders and laws, restated), on the six R-V4 nodes. Drafted, not judged: gate2
judges it in V3 (K258). Only (a) shapes go to the corpus, in V4, on his word, after the successor map's pin; (b) goes to
the regen queue, (d) to the map, (c) to the intake (R-V2).

What this builder does, every value measured at run time:
  - writes the staging file from SHAPES below (bound_for staging, phase S), pinned to corpus 7b6e65e5 and its
    objections digest;
  - copies each (d) shape's bedrock from the registered (d) its line reaches (the map v1_8 entry named by node, locus
    and anchor) and finds that entry's bedrock and facet in register v0_9; it never types a bedrock (L4's law);
  - names the (b) entry each (b) shape lands on, with its regen axis and severity, from the map;
  - runs the collision check for every routed shape: R1's rule v0_2 restated for shapes (a (b) or (d) at an answering
    locus, anywhere on the shape's own node, or on another slot of an answering node), beside the drafter's reading;
  - measures the four things design section 5 asks for, against R1's rulings read at their pinned md5 and against map
    v1_8's own cross-node share for (a) entries;
  - runs shape_validator_v0_1.py over the staging file and records its last line.

  python3 argument_shapes/build_shapes_pilot.py [--check]
Repo-relative. The validator runs in its own process group with TMPDIR in scratch.
"""
import hashlib, json, os, shutil, signal, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, "adversarial_map_staging", "r1"))
import pinned  # noqa: E402
import shape_validator_v0_1 as SV  # noqa: E402

CORPUS = ("efilist_argument_library_v4_0_0.json", "7b6e65e531018fecb37baf2a4fedd6d1")
MAP = ("adversarial_map_staging/adversarial_map_v1_8.json", "691930ab76908a85a6850bdb714d3827")
REGISTER = ("adversarial_map_staging/honest_residuals_register_v0_9.json", "8e53d920099e8b850baa2879dfd3e351")
RULINGS = ("adversarial_map_staging/r1/R1_rulings.json", "f7d02b16f6837e53033b3c7fb68332a9")
VALIDATOR = ("argument_shapes/shape_validator_v0_1.py", "64553b25b6db0ff67edeb87b89178297")
OUT = "argument_shapes/shapes_pilot_v0_1.json"
MEASURE = "argument_shapes/shapes_pilot_measure_v0_1.json"
NODES = ["life-gift", "joy-outweighs-harms", "future-solve", "free-will-defense", "meta-ethical-pluralism",
         "meaning-through-suffering"]
PROV = {"phase": "S", "date": "2026-10-03", "seat": "l (V2, Code)"}
URLS = {
    "hare": ["https://onlinelibrary.wiley.com/doi/10.1111/j.1467-8519.1988.tb00055.x",
             "https://www.researchgate.net/publication/8557150_The_Golden_Rule_and_the_Potentiality_Principle_Future_Persons_and_Contingent_Interests"],
    "hick": ["https://iep.utm.edu/hick/", "https://en.wikipedia.org/wiki/Irenaean_theodicy"],
    "morioka": ["https://www.cambridge.org/core/journals/cambridge-quarterly-of-healthcare-ethics/article/paradox-of-sentiocentric-antinatalism-the-obligation-of-extinction-or-the-obligation-of-survival/5D1402C6047D2D9AAF936070364D985A",
                "https://pubmed.ncbi.nlm.nih.gov/42028605/", "https://w-rdb.waseda.jp/html/100001337_en.html"],
}
CITATIONS = {
    "hare": "R. M. Hare, Possible People, Bioethics 2(4), 1988, pp. 279-293",
    "hick": "John Hick, Evil and the God of Love, 1966, the soul-making (Irenaean) theodicy",
    "morioka": ("Masahiro Morioka, The Paradox of Sentiocentric Antinatalism: The Obligation of Extinction or the "
                "Obligation of Survival?, Cambridge Quarterly of Healthcare Ethics 34(4), 2025, pp. 634-645"),
}
CHECKED = {
    "hare": ("Checked 2026-10-03 against the publisher's record (volume, issue, pages) and a secondary summary of its "
             "thesis: we can harm possible people by preventing them from becoming actual, by a golden rule read as "
             "'do to others as we are glad that they did to us'. Full text not read."),
    "hick": ("Checked 2026-10-03 against the Internet Encyclopedia of Philosophy entry on Hick and summaries: the 1966 "
             "book is the main presentation of the soul-making theodicy, in which God is responsible for evil but "
             "justified by its benefit for the moral and spiritual growth of free persons. Full text not read."),
    "morioka": ("Checked 2026-10-03 against the journal's and PubMed's records and the abstract: sentiocentric "
                "antinatalists who would end all births must bear an obligation to survive to prevent other "
                "creatures from being born. Full text not read."),
}

# The shapes. route: answered_by for (a) and (b); via: the registered (d) whose bedrock a (d) shape's line reaches,
# named by node, locus and anchor; lands_on: the (b) entry a (b) shape meets. reading: the drafter's reading of the
# collision check, which gate2 judges.
SHAPES = [
    {"shape_id": "life-gift/the-giver-vouches-for-the-gift", "class": "b",
     "label": "The giver vouches for the gift",
     "statement": ("Life is a gift because of who gives it. A perfectly good God does not hand out harms dressed as "
                   "presents, so whatever pain a life contains belongs to a good we cannot yet see from inside it. To "
                   "refuse to pass life on is to call the Giver a liar about His own gift."),
     "differs_by": ("The gift's goodness is vouched for by the giver's nature, with apparent harms deferred to a good "
                    "beyond our sight, not by the life's contents or by the recipient's later affirmation."),
     "attested_by": ["life-gift-001", "life-gift-002"],
     "answered_by": [{"locus": "gods-plan#long", "anchor": "No theodicy has resolved this trilemma"}],
     "lands_on": ("gods-plan", "long", "No theodicy has resolved this trilemma"),
     "reading": ("FAILS as an (a), so (b). Its strongest form trusts a good we cannot see from inside the harm, which "
                 "is skeptical theism; the (b) at gods-plan#long records exactly that the node never engages "
                 "skeptical theism or divine-command theory. The shape waits on that (b)'s repair. The own-node (d) at "
                 "life-gift#long is not met: it presses the antecedent-stake condition, and this route never uses it.")},
    {"shape_id": "life-gift/a-gift-to-the-world", "class": "d",
     "label": "A gift to the world",
     "statement": ("Forget whether the child owes thanks. Every person born is a gift to everyone else: new love, new "
                   "work, new minds, the people who will carry knowledge and culture forward. Children are the most "
                   "valuable resource humanity has, and a world that stops making them throws away the source of "
                   "everything worth valuing."),
     "differs_by": ("Moves the beneficiary from the child to humanity and the world, so the gift is the value a new "
                    "person adds, not a benefit conferred on that person."),
     "attested_by": ["anton-children-most-valuable-001"],
     "answered_by": [],
     "via": ("extinction-culture", "long", "The absence of culture is not bad for the non-existent"),
     "reading": ("(d). The library's answer is that a lost good registers only for a valuer; the (d) at "
                 "extinction-culture#long records that an impersonal-value claim is never reached by it.")},
    {"shape_id": "life-gift/the-golden-rule-passes-it-on", "class": "d",
     "label": "The golden rule passes it on",
     "statement": ("You are glad you were brought into existence, and so are nearly all of us. The golden rule says do "
                   "to others what you are glad was done to you. A person who would be glad to exist is harmed if we "
                   "choose never to create them, so passing life on is a duty, not a gamble."),
     "differs_by": ("Rests on universalizing one's own gladness by the golden rule, and on the claim that a possible "
                    "person is harmed by not being created, rather than on gratitude as a virtue or on the "
                    "recipient's later affirmation as evidence."),
     "attested_by": [{"citation": CITATIONS["hare"]}],
     "answered_by": [],
     "via": ("joy-outweighs-harms", "long", "a merely possible person can be a genuine beneficiary of being brought into"),
     "reading": ("(d). The line turns on whether a merely possible person is harmed by non-creation; the (d) at "
                 "joy-outweighs-harms#long records that question as the open premise the corpus routes to and does "
                 "not meet.")},
    {"shape_id": "joy-outweighs-harms/good-in-itself-not-a-sum", "class": "d",
     "label": "Good in itself, not a sum",
     "statement": ("I am not adding anything up, and pleasure and pain may not even be addable. Music, love, discovery, "
                   "the sheer size of the universe to learn about: these make a life good in itself, in a way its "
                   "pains do not cancel. Giving someone a life that holds them gives them something good."),
     "differs_by": ("Drops the hedonic arithmetic that the trigger, layman and scholar lines all rely on: the goods "
                    "make a life good in itself rather than outnumbering its bads."),
     "attested_by": ["joy-outweighs-harms-001"],
     "answered_by": [],
     "via": ("joy-outweighs-harms", "long", "a merely possible person can be a genuine beneficiary of being brought into"),
     "reading": ("(d). Grant the goods in full, as the long does; the claim that giving such a life benefits its "
                 "recipient is the merely-possible-beneficiary premise the (d) at the same locus records as "
                 "bedrock.")},
    {"shape_id": "future-solve/raise-the-people-who-fix-it", "class": "a",
     "label": "Raise the people who fix it",
     "statement": ("Who is going to solve tomorrow's problems if the people who care about them stop having children? "
                   "A child raised well, taught to care and to think, is one of the best things anyone can add to the "
                   "future. Having one is not a bet on luck; it is an investment in the people who will fix things."),
     "differs_by": ("The warrant is the parent's deliberate formation of a problem-solver, an investment through "
                    "upbringing, rather than generational progress at large or the lottery chance of a genius."),
     "attested_by": ["future-solve-001"],
     "answered_by": [{"locus": "next-person-cure-cancer#long",
                      "anchor": "creating a new consciousness to serve the interests of those already existing"}],
     "reading": ("HOLDS. next-person-cure-cancer carries no (b) or (d) on any slot. The machine collision is the (b) "
                 "at future-solve#short, which presses the over-broad transitional-sacrifice framing; this shape "
                 "makes no transitional-sacrifice claim, so the (b) is not met.")},
    {"shape_id": "future-solve/the-obligation-to-survive", "class": "b",
     "label": "The obligation to survive",
     "statement": ("Take your own premise seriously: suffering is what matters, and not only human suffering. Animals "
                   "will keep being born into pain for as long as this planet can hold life. If anything is ever to "
                   "stop that, someone has to remain who can. Ending human births leaves all of it in place."),
     "differs_by": ("Argues from the antinatalist's own sentiocentric premise to an obligation of human survival, "
                    "since only a remaining humanity could ever stop non-human births into suffering, instead of from "
                    "human welfare or technological optimism."),
     "attested_by": [{"citation": CITATIONS["morioka"]}],
     "answered_by": [{"locus": "wild-animal-suffering-consistency#long",
                      "anchor": "do not create new instances of unconsented suffering where creation is discretionary"},
                     {"locus": "transhumanist-objection#long", "anchor": "carried where the terminus is defended"}],
     "lands_on": ("transhumanist-objection", "long", "carried where the terminus is defended"),
     "reading": ("FAILS as an (a), so (b). wild-animal-suffering-consistency#long answers the antinatalist core: the "
                 "framework forbids discretionary creation and was never committed to ending all births. But the "
                 "library also holds an extinction terminus that rests on suffering-minimisation, and the (b) at "
                 "transhumanist-objection#long (headline) records that terminus as defended nowhere. The shape "
                 "presses exactly that gap, so the library answers it with a commitment its own terminus contradicts. "
                 "The repair belongs where the terminus is stated. The (b) at future-solve#short is not met: the "
                 "shape makes no transitional-sacrifice claim.")},
    {"shape_id": "free-will-defense/everyone-comes-home-at-last", "class": "c",
     "label": "Everyone comes home at last",
     "statement": ("If God brings every person, in the end, freely into eternal life with Him, then no life created is "
                   "a loss on the whole. However hard a worldly life turns out, it is a finite stretch before an "
                   "infinite good. On that view, having a child is permissible even when the child's life will be "
                   "hard."),
     "differs_by": ("Justifies creation by a guaranteed eschatological outcome for every person, not by the value of "
                    "freedom or of a world with free agents, so free will drops out of the argument."),
     "attested_by": ["sophia-christian-universalism-procreation-001"],
     "answered_by": [],
     "reading": ("(c). The warrant is eschatological compensation, which free will does not carry; the instance's own "
                 "attachment note says a schema revision might split it from this objection. No node states it: "
                 "gods-plan's trigger is divine purpose, not universal salvation. It goes to the intake.")},
    {"shape_id": "free-will-defense/a-vale-of-soul-making", "class": "a",
     "label": "A vale of soul-making",
     "statement": ("What freedom is for is growth. Courage, compassion and patience cannot be handed over ready-made; a "
                   "free person has to grow into them against real hardship. A painless world could make comfortable "
                   "people, never good ones. So to create someone who will suffer is to create someone who can freely "
                   "become good."),
     "differs_by": ("Suffering is justified as the necessary means of free moral growth, not as the permitted cost of "
                    "freedom's possibility, which is the free-will defense the scholar line states."),
     "attested_by": [{"citation": CITATIONS["hick"]}],
     "answered_by": [{"locus": "free-will-defense#long", "anchor": "Free will does not mitigate the proxy gamble"}],
     "reading": ("HOLDS. free-will-defense carries no (b) or (d) on any slot, so no machine collision. The long's third "
                 "level grants the good for argument's sake and answers at creation: the being is made without "
                 "consent and exposed to a world where growth may never come. That answer needs no axiology. The "
                 "pull, for gate2: the statement's constitutive clause is the move the (d) at "
                 "meaning-through-suffering#long records as reaching HR-03, but that (d) bites only on an impersonal "
                 "reading, and this shape's conclusion is about the person created.")},
    {"shape_id": "meta-ethical-pluralism/many-peaks-one-landscape", "class": "d",
     "label": "Many peaks, one landscape",
     "statement": ("Grant that well-being is the only basis of value. It still has many peaks, not one: different ways "
                   "of living well that are equally good. Avoiding the worst valleys is part of morality, not the "
                   "whole of it. A view that counts only the valleys has thrown away half the landscape."),
     "differs_by": ("Pluralism of optima inside a single well-being realism, not pluralism of frameworks under moral "
                    "uncertainty as in the scholar line."),
     "attested_by": ["harris-moral-landscape-meta-ethical-pluralism-001"],
     "answered_by": [],
     "via": ("meta-ethical-pluralism", "medium", "Negative utilitarianism merely refuses the tolerance"),
     "reading": ("(d). The library's answer is that negative utilitarianism refuses the tolerance others accept; the "
                 "(d) at the same locus records that a pluralist who weighs and names his price stays coherent: a "
                 "stake, not a defeat.")},
    {"shape_id": "meaning-through-suffering/heroism-redeems-being", "class": "d",
     "label": "Heroism redeems being itself",
     "statement": ("Suffering is not a cost that meaning pays off. It is the field on which people can freely stand up "
                   "to tragedy and malice, and that voluntary heroism is the highest thing a human being can do. It "
                   "redeems existence as a whole. Stop every new life and you abolish the possibility of redemption "
                   "with it."),
     "differs_by": ("Locates the value in the voluntary heroic response that redeems being as a whole, an act-centred "
                    "theodicy of heroism, rather than in meaning made after suffering or in goods that adversity "
                    "makes possible."),
     "attested_by": ["peterson-renegade-meaning-through-suffering-001"],
     "answered_by": [],
     "via": ("meaning-through-suffering", "long", "a survival mechanism, not an ethical justification"),
     "reading": ("(d). The library's consent answer meets the voluntary-heroism clause (the hero volunteers; the "
                 "created person is drafted), but the shape's conclusion is an impersonal loss, the possibility of "
                 "redemption itself, which the (d) at the same locus records as reaching HR-03.")},
]

DROPPED = [
    {"node": "life-gift", "candidate": "unconsented benefit is ordinary (the rescue and vaccination analogy)",
     "why": "no checkable published source makes the move in this session; the long states it as the natalist's best "
            "analogy, which is the library's voice, not attestation"},
    {"node": "joy-outweighs-harms", "candidate": "expected value across the lives one might create",
     "why": "no checked source; Hare 1988, searched for it, makes the golden-rule move instead, which became "
            "life-gift/the-golden-rule-passes-it-on"},
    {"node": "joy-outweighs-harms", "candidate": "we impose risks on children for expected good all the time",
     "why": "no checked source"},
    {"node": "free-will-defense", "candidate": "the determinism dilemma (if no one is free your ought is idle; if we "
                                              "are, freedom is the good)", "why": "no checked source"},
    {"node": "meta-ethical-pluralism", "candidate": "under moral uncertainty keep options open, since extinction is "
                                                   "irreversible", "why": "another node's objection (epistemic-humility)"},
    {"node": "meaning-through-suffering", "candidate": "life is a series of ethical decisions, not a hedonic ledger "
                                                      "(peterson-better-never-meaning-through-suffering-001)",
     "why": "a surface: the scholar line already makes the frame substitution (the hedonic ledger is the wrong "
            "instrument; meaning is the superordinate category); only the substituted noun differs"},
    {"node": "future-solve", "candidate": "the world is measurably getting better", "why": "another node's objection "
                                                                                          "(pinker-better-world)"},
    {"node": "future-solve", "candidate": "a good beyond suffering is not impossible, so waiting for it is not "
                                         "illogical", "why": "reserved for the post-pilot intake (R0296): it is "
                                                             "love-from-the-void's modal move; no pilot shape uses it"},
]
BAR = ("A different shape changes the premise that carries the conclusion. It keeps the objection's conclusion and its "
       "trigger family, but the node's trigger, layman line and scholar line do not state its warrant, and its "
       "objector would not accept them as a fair statement of the argument. A new noun for the same move is a surface "
       "(the dropped Peterson 2017 candidate). A shape that is another node's objection belongs to that node, not "
       "here. Where an answer exists, the shape is classed by where the library's answer ends: a clean answer is (a); "
       "an answer the map records as flawed is (b); an answer the map records as ending at bedrock is (d), with the "
       "bedrock copied from that (d); and an argument whose warrant this objection does not carry is (c).")
RESERVED = ("love-from-the-void (his own argument for life, R0296) is the post-pilot intake's first item. Its modal "
            "move, that a good able to make up for suffering is not impossible, so waiting for it is not illogical, "
            "is reserved for that intake: no future-solve shape uses it (checked by the builder).")


def md5b(b):
    return hashlib.md5(b).hexdigest()


def at(rel, m):
    return pinned.bytes_at(REPO, rel, m)


def run_validator(path):
    scratch = tempfile.mkdtemp(prefix="shapes_pilot_")
    try:
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=scratch)
        p = subprocess.Popen([sys.executable, VALIDATOR[0], path], cwd=REPO, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, text=True, env=env, start_new_session=True)
        try:
            out, _ = p.communicate(timeout=600)
        except subprocess.TimeoutExpired:
            os.killpg(p.pid, signal.SIGKILL)
            raise
        return p.returncode, out
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def build():
    corpus = json.loads(at(*CORPUS).decode("utf-8"))
    cmap = json.loads(at(*MAP).decode("utf-8"))
    reg = json.loads(at(*REGISTER).decode("utf-8"))
    rul = json.loads(at(*RULINGS).decode("utf-8"))
    assert md5b(open(os.path.join(REPO, VALIDATOR[0]), "rb").read()) == VALIDATOR[1], "validator moved"
    ids = [o["id"] for o in corpus["objections"]]
    entries = cmap["entries"]

    def entry(node, locus, anchor, cls):
        hit = [e for e in entries if (e["target_id"], e["target_locus"], e["target_anchor"]) == (node, locus, anchor)]
        assert len(hit) == 1 and hit[0]["class"] == cls, "%s#%s %r: want one (%s)" % (node, locus, anchor, cls)
        return hit[0]

    def register_of(node, locus, anchor):
        found = [(b["bedrock_id"], b["name"], f["facet_id"]) for b in reg["bedrocks"] for f in b["facets"]
                 for t in f["tributaries"] if (t.get("node"), t.get("locus"), t.get("anchor")) == (node, locus, anchor)]
        assert len(found) == 1, "%s#%s: %d register tributaries" % (node, locus, len(found))
        return found[0]

    def bd_on(node, skip_locus=None):
        return [{"node": e["target_id"], "locus": e["target_locus"], "class": e["class"], "anchor": e["target_anchor"]}
                for e in entries if e["target_id"] == node and e["class"] in "bd" and e["target_locus"] != skip_locus]

    shapes, rows = [], []
    for s in SHAPES:
        node = s["shape_id"].split("/")[0]
        assert node in NODES
        shapes.append({"shape_id": s["shape_id"], "label": s["label"], "statement": s["statement"],
                       "differs_by": s["differs_by"], "class": s["class"], "attested_by": s["attested_by"],
                       "answered_by": s["answered_by"], "provenance": dict(PROV)})
        row = {"shape_id": s["shape_id"], "class": s["class"], "words": SV.wc(s["statement"]),
               "answer_nodes": sorted({a["locus"].split("#")[0] for a in s["answered_by"]})}
        if s["answered_by"]:
            mc = []
            for a in s["answered_by"]:
                n, loc = a["locus"].split("#")
                mc += [dict(x, why="at the answering locus") for x in bd_on(n) if x["locus"] == loc]
                mc += [dict(x, why="another slot of an answering node") for x in bd_on(n, skip_locus=loc)]
            mc += [dict(x, why="the shape's own node") for x in bd_on(node)]
            uniq = []
            for x in mc:
                if x not in uniq:
                    uniq.append(x)
            row["machine_collisions"] = uniq
            row["cross_node"] = any(n != node for n in row["answer_nodes"])
        if s["class"] == "d":
            n, loc, anc = s["via"]
            e = entry(n, loc, anc, "d")
            hr, name, facet = register_of(n, loc, anc)
            row["terminus"] = {"via": "%s#%s" % (n, loc), "via_anchor": anc,
                               "bedrock_name": e["routing"]["residue"]["bedrock_name"],
                               "terminus_routing": e["routing"]["residue"]["terminus_routing"],
                               "register": {"bedrock_id": hr, "name": name, "facet": facet}}
            row["cross_node"] = n != node
        if s["class"] == "b":
            n, loc, anc = s["lands_on"]
            e = entry(n, loc, anc, "b")
            row["lands_on"] = {"entry": "%s#%s" % (n, loc), "anchor": anc,
                               "regen_candidate": e["routing"]["regen_candidate"]}
        if s["class"] == "c":
            row["intake"] = "a candidate for the new-objection intake (R-V2, R-V6), after the pilot is judged"
        row["reading"] = s["reading"]
        att = []
        for a in s["attested_by"]:
            if isinstance(a, str):
                rw = next(r for r in corpus["realWorldExamples"] if r["instance_id"] == a)
                fit = next(x for x in rw["attached_objections"] if x["objection_id"] == node)["fit_to_trigger_phrases"]
                att.append({"instance_id": a, "fit_to_trigger_phrases": fit, "polarity": rw["instance_polarity"]})
            else:
                key = next(k for k, v in CITATIONS.items() if v == a["citation"])
                att.append({"citation": a["citation"], "checked": CHECKED[key], "urls": URLS[key]})
        row["attestation"] = att
        rows.append(row)

    per_node = {}
    for s in shapes:
        per_node.setdefault(s["shape_id"].split("/")[0], []).append(s["shape_id"])
    doc = {"meta": {"source_corpus_md5": CORPUS[1], "source_corpus_objections_md5": SV.objections_digest(corpus),
                    "bound_for": "staging", "shape_coverage": "%d/%d" % (len(per_node), len(ids))},
           "shapes": shapes}
    pilot = (json.dumps(doc, indent=1, ensure_ascii=False) + "\n").encode("utf-8")

    for s in SHAPES:  # the reserved move stays out of the pilot (R0296)
        if s["shape_id"].startswith("future-solve/"):
            low = s["statement"].lower()
            assert "not impossible" not in low and "illogical" not in low, s["shape_id"]

    latest = {}
    for r in rul["rows"]:
        latest[r["n"]] = r["verdict"]
    r1 = {"entries": len(latest), "FAILS": sum(v == "FAILS" for v in latest.values()),
          "HOLDS": sum(v == "HOLDS" for v in latest.values())}
    a_targets = [(e["target_id"], loc) for e in entries if e["class"] == "a"
                 for loc in e["routing"].get("answered_by", [])]
    map_cross = sum(loc.split("#")[0] != t for t, loc in a_targets)
    words = [r["words"] for r in rows]
    cls = {c: sum(r["class"] == c for r in rows) for c in "abcd"}
    routed = [r for r in rows if "cross_node" in r]
    a_rows = [r for r in rows if r["class"] == "a"]
    measure = {
        "what": "the argument-shapes pilot's measurement (design section 5), V2, seat l, 2026-10-03; drafted, not judged",
        "pins": {"pilot": {"file": OUT, "md5": md5b(pilot), "bytes": len(pilot)},
                 "corpus": dict(zip(("file", "md5"), CORPUS)), "map": dict(zip(("file", "md5"), MAP)),
                 "register": dict(zip(("file", "md5"), REGISTER)), "rulings": dict(zip(("file", "md5"), RULINGS)),
                 "validator": dict(zip(("file", "md5"), VALIDATOR))},
        "counts": {"shapes": len(rows), "nodes": len(per_node), "per_node": {n: len(v) for n, v in per_node.items()},
                   "classes": cls},
        "measures": {
            "right_card_another_objections": {
                "a_shapes": "%d of %d" % (sum(r["cross_node"] for r in a_rows), len(a_rows)),
                "all_routed_shapes": "%d of %d" % (sum(r["cross_node"] for r in routed), len(routed)),
                "routed_means": "every shape with an answering or terminus locus; the (c) has neither",
                "map_v1_8_a_targets_cross_node": "%d of %d" % (map_cross, len(a_targets)),
                "design_prior": "20 of 40 (map v1_6, design section 5)"},
            "classes_against_R1": {
                "not_shipping_as_a": "%d of %d" % (len(rows) - cls["a"], len(rows)),
                "R1_FAILS": "%d of %d" % (r1["FAILS"], r1["entries"]), "R1_HOLDS": r1["HOLDS"],
                "note": ("Not the same quantity: R1 ruled continuations against the answers the map routed them to; "
                         "a shape is classed by where the library's answer to it ends. Both count how often a route "
                         "meets a recorded (b) or (d).")},
            "words_per_shape": {"min": min(words), "max": max(words), "mean": round(sum(words) / len(words), 1),
                                "band": [30, 70]},
            "bar_for_a_different_shape": BAR},
        "attestation": {"rwe": sum(isinstance(a, str) for s in SHAPES for a in s["attested_by"]),
                        "citations": sum(not isinstance(a, str) for s in SHAPES for a in s["attested_by"]),
                        "binding": ("Attestation bound the pilot below about 18: the six nodes carry 9 instances, "
                                    "and 4 of the 6 nodes carry one or none that makes a non-surface move. Every "
                                    "citation was checked against a publisher, journal or encyclopedia record this "
                                    "session; none was read in full, and each says so. Nothing is cited from memory.")},
        "reserved_for_the_intake": RESERVED,
        "dropped": DROPPED,
        "shapes": rows,
        "the_pull": [
            "future-solve/the-obligation-to-survive: (a) at wild-animal-suffering-consistency#long alone was the "
            "easier call; (b) was chosen because the library's extinction terminus is the commitment the shape "
            "presses, and the map records it as undefended.",
            "free-will-defense/a-vale-of-soul-making against meaning-through-suffering/heroism-redeems-being: the "
            "same constitutive move is (a) where the conclusion is about the person created and (d) where it is an "
            "impersonal loss. gate2 should test whether that line holds.",
            "meta-ethical-pluralism/many-peaks-one-landscape: Harris's surrounding argument also reaches an empty "
            "world's rank (HR-03); the statement was cut to the plurality of optima, so its terminus is the "
            "tolerance stake. Whether the cut understates his move is gate2's to read."],
    }
    out_m = (json.dumps(measure, indent=1, ensure_ascii=False) + "\n").encode("utf-8")
    return pilot, out_m


def main():
    pilot, meas = build()
    if "--check" in sys.argv:
        ok = (open(os.path.join(REPO, OUT), "rb").read() == pilot
              and json.loads(open(os.path.join(REPO, MEASURE), "rb").read())["shapes"] == json.loads(meas)["shapes"])
        rec = json.loads(open(os.path.join(REPO, MEASURE), "rb").read())
        mine = json.loads(meas)
        mine["validator_run"] = rec.get("validator_run")
        ok = ok and (json.dumps(mine, indent=1, ensure_ascii=False) + "\n").encode("utf-8") == \
            open(os.path.join(REPO, MEASURE), "rb").read()
        print("SHAPES PILOT: %s" % ("matches the committed pilot and measurement" if ok else "DIFFERS"))
        sys.exit(0 if ok else 1)
    open(os.path.join(REPO, OUT), "wb").write(pilot)
    rc, out = run_validator(OUT)
    m = json.loads(meas)
    tail = json.loads(out[out.rfind("\n{") + 1:])
    m["validator_run"] = {"rc": rc, "verdict": tail["verdict"], "violation_count": tail["violation_count"],
                          "shapes": tail["shapes"], "nodes_with_shapes": tail["nodes_with_shapes"]}
    meas = (json.dumps(m, indent=1, ensure_ascii=False) + "\n").encode("utf-8")
    open(os.path.join(REPO, MEASURE), "wb").write(meas)
    print(out.strip()[-1500:])
    print("%s  %s / %d" % (OUT, md5b(pilot), len(pilot)))
    print("%s  %s / %d" % (MEASURE, md5b(meas), len(meas)))
    sys.exit(0 if rc == 0 else 1)


if __name__ == "__main__":
    main()

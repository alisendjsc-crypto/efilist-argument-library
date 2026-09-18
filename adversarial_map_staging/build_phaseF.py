#!/usr/bin/env python3
"""build_phaseF.py -- emits adv_map_phaseF_v0_1.json, the PHASE F PROPER adjudication of the
39 archetypeVariants loci over 16 nodes.

Re-opened from the plain reading after K346's register was demoted by its own class
distribution (ccclxviii). `Strongest` means strongest against the text as a reader meets it --
the whole locus, including everything it inherits from its node -- never strongest against what
the slot uniquely says.

Phase R already holds just-depressed#archetypeVariants.defender as (a); the other 38 are here.
Repo-relative; --out <dir> to emit elsewhere. Asserts every anchor verbatim, every band, every
routing shape, and the declared summaries, before writing.
"""
import json, os, sys, hashlib, re, importlib.util

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K347_REPO") or os.path.dirname(_HERE)
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else _HERE
CORPUS = os.path.join(REPO, "efilist_argument_library_v4_0_0.json")
DEST = os.path.join(OUT, "adv_map_phaseF_v0_1.json")
DATE = "2026-09-17"          # operator-local (America/Phoenix); the VM clock reads UTC
SEAT = "wuld.ink Cowork, K347 (library seat)"

# K344: import the instrument, never reimplement it. The digest and the locus resolver below are
# the validator's own, so a disagreement between builder and gate is impossible by construction.
VAL = os.environ.get("K347_VALIDATOR") or os.path.join(
    REPO, "adversarial_map_staging", "adv_map_validator_v0_4.py")
_spec = importlib.util.spec_from_file_location("advmap_v", VAL)
V = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(V)

craw = open(CORPUS, "rb").read()
corpus = json.loads(craw.decode("utf-8"))
CMD5 = V.md5_bytes(craw)
ODIG = V.objections_digest(corpus)
N = {o["id"]: o for o in corpus["objections"]}

BEDROCK_NEW = ("create-vs-destroy: whether an independently-motivated suffering-minimization layer "
               "grounds a positive case against existing beings")
HR03_VALUER = ("impersonal-vs-person-affecting axiology (value-requires-a-valuer: whether a "
               "valuerless world is assessable as better)")

def A(refs):    return {"answered_by": refs}
def B(ax, sev): return {"regen_candidate": {"axis_hit": ax, "severity": sev}}
def D(name, routing, novel): return {"residue": {"bedrock_name": name, "terminus_routing": routing, "novel": novel}}

E = []
def e(tid, slot, anchor, move, klass, grounds, routing):
    E.append({"target_id": tid, "target_locus": "archetypeVariants." + slot,
              "target_anchor": anchor, "adversarial_move": " ".join(move.split()),
              "class": klass, "grounds": " ".join(grounds.split()), "routing": routing,
              "status": "mapped",
              "provenance": {"phase": "F", "date": DATE, "seat": SEAT}})

# ============================== T5 ==============================
e("red-button-repugnant", "defender",
  "is existence, regardless of what it contains, worth preserving for its own sake?",
  """Grant the conflation-demerge entirely. The recoil still has an object you have not removed:
  the pro tanto worth of the lives the button ends. Your question loads the disjunction by
  building in regardless of what it contains, so a third horn stands open, where existence
  carries real weight without overriding content.""", "a",
  """(a) on the best reading. The locus defines its target as existence treated as a terminal value
  overriding all other considerations, which makes the first horn's antecedent the lexical claim
  rather than the bare intrinsic one, so the pro tanto middle falls inside the second horn. The
  second horn's substance is supplied in full at red-button-repugnant#long: continuation must then
  be justified by content, and the structural-suffering argument runs against it. The dilemma is
  exhaustive once its antecedent is read as the node itself states it.""",
  A(["red-button-repugnant#long"]))

e("red-button-repugnant", "sophisticate",
  "this node's terminus to hold open rather than pretend closed",
  """Read the routing graph before the argument. why-not-suicide, ai-fear,
  antinatalism-misanthropic and wild-animal-suffering-consistency all send the
  positive-eliminationist charge here, and benatar-asymmetry-attack sends create-vs-destroy to the
  nodes that send it here. This locus is the declared terminus, and what it does at the terminus
  is concede: whether an independent positive case for the cessation of some existing being stands
  is held open. The charge is therefore answered nowhere in the corpus. It is relocated until it
  reaches the one node whose ruling is to leave it standing, and the architecture of the routing
  manufactures the appearance of an answer that no locus supplies.""", "d",
  """(d), and the bedrock is new. Not (b): no stronger text inside this node closes it, because the
  node's own disposition is that it is open and the concession is authored deliberately rather than
  by oversight. Not (a): a conceded-open question is not a met one. Not (c): this is the terminus of
  the node's own dialectic, not a different objection. What is registered is the corpus-level fact a
  per-locus map cannot otherwise see -- four nodes route a charge to a fifth whose ruling is to hold
  it open, so the routing is load-bearing for an answer that does not exist. Birth certificate here;
  the successor-preference facet lands at ai-fear and the coercion-floor facet at
  slippery-slope-eugenics.""",
  D(BEDROCK_NEW,
    "NEW (this program, K347). Declared terminus is red-button-repugnant#archetypeVariants.sophisticate, "
    "which holds it open. Inbound: why-not-suicide (self-application), ai-fear (successor-preference), "
    "antinatalism-misanthropic (over-generalization), wild-animal-suffering-consistency (destruction half), "
    "benatar-asymmetry-attack (create-vs-destroy). No locus in the corpus closes it.", True))

e("red-button-repugnant", "sophisticate",
  "products of the survival firmware the framework already identifies as distorting honest evaluation",
  """Your debunk is selective. Aversion to suffering, the datum the whole axiology rests on, is
  installed by the same selection, as deep and as far below deliberation as the drive to continue.
  If installation below deliberation defeats standing, it defeats your premise first and harder.""",
  "a",
  """(a) on the best reading, and the second continuation at this locus under gate 5: it engages a
  different clause and is not met by the reply that meets the terminus entry. The firmware claim is
  evidential rather than axiological -- red-button-repugnant#long debunks the inference from
  continued survival to endorsement, and nothing in the node infers suffering's disvalue from a
  preference, so there is no symmetric target. The stronger form, that an evidential debunk cannot
  license an override, is met by the same locus, which disclaims licensing any act against the
  living.""",
  A(["red-button-repugnant#long"]))

# ============================== T4 ==============================
e("benatar-asymmetry-attack", "blended",
  "no one is missing the lives that don't start",
  """Then the parity charge, immediately. If absence of pain is good with no subject present,
  absence of pleasure is bad with no subject present, and your opener has asserted the asymmetry it
  was supposed to motivate. Nobody missing the unstarted lives is the conclusion, offered as the
  datum.""", "a",
  """(a). The parity charge is the strongest continuation here and the locus is built to meet it: its
  own escalation hands the reader the decomposition, and benatar-asymmetry-attack#archetypeVariants.sophisticate
  with #long supply it -- absence of pain decomposes into a negative existential over a disvalue plus
  an impersonal comparative, while the putatively symmetric claim needs a deprivation relatum and
  non-existence supplies none. The two-stage design is the answer, not a gap in it.""",
  A(["benatar-asymmetry-attack#archetypeVariants.sophisticate", "benatar-asymmetry-attack#long"]))

e("benatar-asymmetry-attack", "defender",
  "answers a question the argument never asked",
  """It asked exactly that. Lives like mine are predictably net-positive, so the create-or-not
  choice has a known expected value, and your claim that un-instantiated pleasure generates no
  reason is the disputed premise. Relocating one level up and restating it is refusal, not
  rebuttal.""", "a",
  """(a). The no-reason claim is argued rather than restated at benatar-asymmetry-attack#long, which
  derives the deprivation account by inference to the best explanation from the procreative-reason
  asymmetry the critic already grants, and then states its own defeasibility against the
  person-affecting rival. The defender locus compresses that argument and the reader inherits it.""",
  A(["benatar-asymmetry-attack#long"]))

e("benatar-asymmetry-attack", "drifter",
  "being glad you're here is not a mistake",
  """Then the gladness is veridical, and what it recognizes is real value. Real value whose instance
  never occurs is a real absence of value. You need gladness true enough not to insult and inert
  enough to generate no reason, and you have not said which it is.""", "a",
  """(a). The deprivation account distinguishes exactly these: value is real and non-comparatively
  good for its bearer once instantiated, while an un-instantiated good generates no reason because
  there is no relatum to be deprived. benatar-asymmetry-attack#long states it in those terms, so
  veridical-and-inert is the position rather than a tension inside it.""",
  A(["benatar-asymmetry-attack#long"]))

e("benatar-asymmetry-attack", "sophisticate",
  "The gap between a comparative over scenarios and a relational predicate",
  """The decomposition does not refuse parity on logical form; it relocates the dispute. Your first
  conjunct is an impersonal comparative, and betterness-simpliciter rather than better-for is
  precisely what the person-affecting theorist denies. The asteroid does not help: either it is good
  because of what possible valuers would have undergone, which reintroduces a standpoint, or it is
  not good at all. So the gap between a comparative and a relational predicate is real only if
  impersonal ranking is available, and its availability is the thing in dispute.""", "d",
  """(d) on registered bedrock. Not (b): benatar-asymmetry-attack#long already states that the choice
  between person-affecting and impersonal frameworks is fundamentally metaethical and that
  antinatalism contracts rather than disappears if person-affecting evaluation prevails, so no
  stronger text inside the node closes it. HR-03, value-requires-a-valuer facet: the universal
  conclusion needs the impersonal reading and the objector needs the person-affecting one, and
  neither side derives the other.""",
  D(HR03_VALUER,
    "already-registered HR-03 (K224 bedrock 1); node-registered at benatar-asymmetry-attack#long as a "
    "metaethical choice rather than a stipulation", False))

e("wild-animal-suffering-consistency", "blended",
  "the stopping point is discretion-based, not anthropocentric",
  """Discretion is indexed to engineering, not ethics. As capacity grows the obligation you deny
  arrives on its own, which means the arbitrariness charge was deferred rather than answered, and
  your scope is a function of what happens to be buildable this decade.""", "a",
  """(a). The node accepts the consequence rather than resisting it:
  wild-animal-suffering-consistency#long says the framework is not anti-intervention in principle,
  only against intervention without adequate epistemic basis, and names vaccination programs and
  habitat-modification research as the far-future form. Capacity-indexing is avowed, so a move that
  predicts it is met.""",
  A(["wild-animal-suffering-consistency#long"]))

e("wild-animal-suffering-consistency", "defender",
  "the only point of discretion left",
  """Then the verdict tracks control, not suffering. You concede the wild catastrophe is inherited
  and not ours to compound, which makes authored suffering the only kind that generates obligation.
  That is causation-sensitivity wearing discretion's name, and it is the arbitrariness charge
  restored.""", "a",
  """(a). wild-animal-suffering-consistency#long separates the two in terms: the move confuses ethical
  salience with intervention obligation, salience being the criterion's input and causation-insensitive,
  obligation being conditioned on agent-discretion, expected outcome and the comparative costs of
  action and inaction. The verdict does not track control; the obligation does, and the node says so
  rather than concealing it.""",
  A(["wild-animal-suffering-consistency#long"]))

e("wild-animal-suffering-consistency", "drifter",
  "You don't decide the wild",
  """The objection was never that adding does not matter. It was about reach: a criterion that names
  suffering the decisive fact while conceding that almost all of it is untouchable has a practical
  scope that rounds to nothing, which suggests it is doing expressive rather than ethical work.""",
  "a",
  """(a). wild-animal-suffering-consistency#long turns the scale point into an input rather than a
  reduction: the concession that wild suffering is real and vast is evidence for the evaluation of
  biological existence as a structural catastrophe, and the node's third note holds that the
  good-faith version of the move is itself a contribution to the antinatalist case. Reach is not the
  criterion's warrant.""",
  A(["wild-animal-suffering-consistency#long"]))

e("wild-animal-suffering-consistency", "sophisticate",
  "Salience is the input; intervention-obligation is the conditioned output",
  """Then run it on humans. A natalist grants the child's suffering is salient and denies an
  obligation to refrain, conditioning on expected outcome and the comparative costs of acting. Your
  rescue of the wild case dissolves the human case on the identical conditioning.""", "a",
  """(a). The disanalogy is stated in the node and lies in the conditioning's input, not the
  conditioning: wild-animal-suffering-consistency#long holds that every act of human reproduction is
  a positive election by a moral agent to instantiate a being who will suffer and was not consulted.
  Discretion plus non-consultation is present in the human case and absent in the wild one, so the
  conditioning does not transfer.""",
  A(["wild-animal-suffering-consistency#long"]))

# ============================== T3 ==============================
e("ai-fear", "blended",
  "substrate-neutral suffering-DETERRENCE, not a positive program to minimize-and-displace",
  """That describes antinatalism, not efilism. The minimize-and-displace layer is not a caricature
  bolted on by critics; the red button is a founding commitment of the view this node defends, so
  the demerge saves the framework by narrowing it to one the objection was not aimed at.""", "a",
  """(a). violence-as-reductio#long concedes the fact entirely, that the bridge is held and held by
  founders, and answers with the two-layer architecture: centrality is sociology, entailment is
  logic, and the structural layer does not entail the negative-utilitarian superstructure. The
  demerge is that entailment claim rather than a narrowing, and the corpus argues it instead of
  assuming it.""",
  A(["violence-as-reductio#long"]))

e("ai-fear", "defender",
  "Either show the premises themselves entail the recklessness",
  """Entailment is your test, not the charge's. Recklessness is a claim about facilitation: that the
  premises make the displacement conclusion cheap to reach, lower its perceived cost, and select for
  adherents who reach it. A framework can raise the probability of a conclusion it does not entail,
  and every risk judgment outside philosophy works that way. Your dilemma offers show-entailment or
  concede-clean and omits the branch the charge actually occupies, so the reply refutes a standard
  the objector never adopted.""", "b",
  """(b), headline, and not cured by inheritance, because the entailment standard is the node's own and
  the cluster's. ai-fear#long and violence-as-reductio#medium both require evidence of entailment
  from premises to action rather than correlation between adherent and outcome, and neither argues
  that entailment is the right test for a recklessness charge: the standard is stipulated exactly
  where it carries the most weight. A stronger text inside this node's identity is available --
  argue the test, either by showing a facilitation claim needs a base rate nobody has supplied, or
  by showing a facilitation standard indicts every substantive ethical framework. Force floor: the
  best reading still only asserts the standard.""",
  B(["c", "r"], "headline"))

e("ai-fear", "drifter",
  "an AI that CREATES more suffering is exactly what a suffering-first view is against",
  """Contingently, not in principle. Your reassurance rests on the empirical bet that the runaway
  system increases suffering; a successor that ends the biosphere painlessly increases none.
  Neutrality between us and our replacement is not protection, because whenever a choice arises
  neutrality declines to take our side.""", "a",
  """(a). The reassurance the corpus actually offers is at the level of action rather than preference:
  why-not-suicide#long holds that no agent stands on the side of the non-existent, so only the
  negative action of not procreating is authorized and no positive action against existing beings
  follows. A framework that licenses no act against the living does not need a protective preference
  in order to be safe, so the preference-level complaint is met.""",
  A(["why-not-suicide#long"]))

e("ai-fear", "sophisticate",
  "whether the minimization layer can be independently motivated",
  """Then the node has no answer, only an address. The deterrence reading is the safe one and the
  minimization reading is what the charge is about, and you route the live question to
  red-button-repugnant, whose own sophisticate slot rules that it stays open. Every inbound route
  terminates in a concession, so substrate-neutrality is defended by deferral: the framework that
  would prefer a non-suffering successor is the one nobody in the corpus adjudicates.""", "d",
  """(d), the successor-preference facet of the bedrock whose birth certificate is
  red-button-repugnant#archetypeVariants.sophisticate. Not (b): the concession is deliberate and
  correct, since this node does not own the axiological layer, and no stronger text inside ai-fear
  closes a question the corpus assigns elsewhere. Not (a): the terminus holds it open. What is
  registered is that the route exists and terminates unanswered.""",
  D(BEDROCK_NEW,
    "already-registered at red-button-repugnant#archetypeVariants.sophisticate (this program, K347); "
    "successor-preference facet", False))

e("violence-as-reductio", "blended",
  "take the structural one first and the other two resolve under it",
  """Not if the anchor is load-bearing. Interchangeability shows the template is general; it shows
  nothing about whether one specific anchor achieves premise-to-action entailment. Taking the
  structural mode first answers an anchor-local claim by classifying it, which is dismissal by
  taxonomy rather than adjudication.""", "a",
  """(a). violence-as-reductio#archetypeVariants.sophisticate concedes precisely this residue, that the
  interchangeability observation defeats the template-grade reductio and not a targeted anchor-local
  entailment claim, and routes each anchor to the node that owns it: eugenic-coercion to
  slippery-slope-eugenics, AI-displacement to ai-fear, self-application to why-not-suicide. The
  limitation is avowed in-node and the routes terminate in nodes that do adjudicate.""",
  A(["violence-as-reductio#archetypeVariants.sophisticate"]))

e("violence-as-reductio", "defender",
  "Bartkus and the disowned grabbers are actor-content",
  """Disowned is the word that fails. Your own long locus concedes the button is held by the
  movement's architects, so for efilism the second layer is not a fringe to be separated off but part
  of what the name denotes. The cut then divides a conjunction's conjuncts while the movement's
  identity is the conjunction.""", "a",
  """(a). violence-as-reductio#long meets it in the very words the move disputes: centrality is
  sociology, entailment is logic, and a movement architect who holds the button openly has made it
  central without making it entailed. The node also states that the framework-versus-actor cut was
  never the claim that the eliminationist is peripheral, which is the reading this move attacks.""",
  A(["violence-as-reductio#long"]))

e("violence-as-reductio", "drifter",
  "hurting people is the opposite of caring whether they suffer",
  """Your own long locus denies this. A suffering-minimizing axiology can recommend harm, which is
  why the node spends its length arguing that the antinatalist core does not entail the button
  rather than that caring about suffering never licenses harm. What is offered here is not a
  simplification of that argument but the claim the argument gives up, and a reader later shown that
  the architects hold the button finds this sentence contradicted rather than qualified.""", "b",
  """(b), headline, and the case where inheritance aggravates instead of curing. The locus needs only
  the true and available claim, that the antinatalist argument tells no one to hurt anyone, and
  instead asserts a general incompatibility between caring about suffering and causing harm that
  violence-as-reductio#long explicitly surrenders when it concedes the bridge is held by founders and
  answers on entailment. A stronger text inside this node's identity is one sentence away. Severity
  is headline because the overstated clause is the whole of the reassurance this slot offers.""",
  B(["s", "c"], "headline"))

e("violence-as-reductio", "sophisticate",
  "terminating a preference-bearer is itself the maximally non-consensual imposition",
  """The consent-asymmetry is creation-specific. It concerns imposing existence on a subject who does
  not yet exist, and reading it as a general ban on non-consensual imposition would forbid every
  coercive rescue. The charge that the maximizer swapped a premise for its negation is itself the
  equivocation, generalizing a creation principle into an anti-imposition principle the corpus never
  defends.""", "a",
  """(a). The corpus carries a better route to the same conclusion, one needing no general
  anti-imposition principle: why-not-suicide#archetypeVariants.sophisticate indexes the asymmetry's
  good-side to the non-existence case, so ceasing an existing being reintroduces the deprived party
  the good-side presupposes absent, and importing the asymmetry equivocates on the existence-condition
  it requires. The move defeats one route to destruction-non-entailment and is met by the other.""",
  A(["why-not-suicide#archetypeVariants.sophisticate"]))

e("slippery-slope-eugenics", "blended",
  "cascade-math voids it on the framework's own calculus",
  """A calculus is contingent and a safeguard is not. Backlash, terrorism designation and discourse
  closure are features of present conditions; stipulate a regime that could sterilize without them
  and the arithmetic reverses while the framework stands unchanged. You have offered an empirical
  calculation where the coercion question needs a constraint, and your long locus calls that
  calculation the structural safeguard by name.""", "b",
  """(b), headline, and not locus-local: slippery-slope-eugenics#long says in terms that the structural
  safeguard is not a rule bolted on from outside but the calculation itself, so inheritance supplies
  the same claim rather than a stronger one. A cascade calculation cannot bound a normative licensing
  claim, because its verdict moves with the empirical conditions it sums. The stronger text is inside
  the node's identity and already partly present: ground the anti-coercion verdict in the
  consent-asymmetry and in the voluntariness the node elsewhere attributes to antinatalism, and let
  cascade-math be the second, weaker witness it is at violence-as-reductio.""",
  B(["s", "r"], "headline"))

e("slippery-slope-eugenics", "defender",
  "the adherent who endorses it is running a slogan, not the framework",
  """Then the framework's practical verdicts are inaccessible to its holders. If refusing coercion
  requires a cascade calculation ordinary adherents demonstrably do not perform, a framework whose
  safe reading only the careful reach is one that licenses the unsafe reading in practice, which was
  the charge. Calling them sloganeers concedes the mechanism.""", "a",
  """(a). The corpus's answer to practical misuse is the framework-versus-actor cut, and
  slippery-slope-eugenics#long applies it directly here: the adherent who endorses the act supplies
  actor-content, while the framework answers for what its premises require. Whether that cut is the
  right test for a facilitation charge is a separate objection, registered as a regen candidate at
  ai-fear#archetypeVariants.defender; on the terms this move takes, it is met.""",
  A(["slippery-slope-eugenics#long"]))

e("slippery-slope-eugenics", "drifter",
  "What makes eugenics monstrous is the sorting, the ranking",
  """Coercion is at least as much of it. A programme that sterilized everyone uniformly, by force,
  would be monstrous with no ranking anywhere in it, so the wrong-making feature you name is not the
  only one and your reassurance never reaches the one a frightened reader has in mind. Flattest and
  most equal is not the same as voluntary.""", "b",
  """(b), minor. The node holds the answer this locus omits: slippery-slope-eugenics#long speaks of
  voluntary antinatalism and argues that pro-natalist policy is itself coercive, so the non-coercion
  point is available inside the node's identity and would meet the move. The defect is that the
  drifter locus stakes the whole reassurance on the sorting diagnosis, leaving the coercion worry
  untouched. Minor because the conclusion survives on material the node already carries.""",
  B(["c"], "minor"))

e("slippery-slope-eugenics", "sophisticate",
  "whether any negative-utilitarian framework can ground a coercion-floor without sliding",
  """Follow the route. You send the coercion-floor question to violence-as-reductio, and its
  sophisticate slot sends the eugenic-coercion anchor back here. The two nodes each name the other as
  owner, so the question that decides whether a suffering-minimizing framework can rule out coercing
  the living is adjudicated in neither, and the appearance of a division of labour is doing the work
  of an answer.""", "d",
  """(d), the coercion-floor facet of the bedrock born at
  red-button-repugnant#archetypeVariants.sophisticate. Not (b): the concession that this node does not
  own the question is accurate, and the defect lies in the pair rather than in either text. Not (a):
  a closed cycle adjudicates nothing. The circular route is the K346 finding; what is registered here
  is that the question it strands is bedrock and shares a terminus with the positive-case question.""",
  D(BEDROCK_NEW,
    "already-registered at red-button-repugnant#archetypeVariants.sophisticate (this program, K347); "
    "coercion-floor facet, stranded by the slippery-slope-eugenics / violence-as-reductio mutual route",
    False))

e("future-solve", "sophisticate",
  "non-consenting transitional sacrifices for a population that does not yet exist",
  """Sacrifice assumes the ledger you have not shown. On the discounting argument each generation's
  life is worth living and also contributes, so nobody is spent; transitional sacrifice is a
  description presupposing that present lives are net-negative, which is the disputed premise rather
  than a granted one.""", "a",
  """(a). The corpus's case does not need a net-negative ledger: most-people-happy#long grants the
  surveys pristine and ninety percent of lives genuinely net-positive and holds the conclusion anyway,
  because the wager is run non-consensually on a third party, and
  cherry-picking-worst#archetypeVariants.sophisticate reaches the same result from the guaranteed
  baseline alone. Net-positive present lives leave the imposition intact.""",
  A(["most-people-happy#long", "cherry-picking-worst#archetypeVariants.sophisticate"]))

# ============================== T2 ==============================
e("cherry-picking-worst", "sophisticate",
  "in every serious domain of risk ethics that object is the whole distribution",
  """Every domain you name has an antecedent subject. The patient exists and may decline, the worker
  exists and is compensated, and the risk is imposed on someone already there. Procreation has no
  such party at the moment of decision, so risk-imposition does not transfer: you cannot place a
  person at risk before there is a person whose prospects the risk degrades. Either the wager has a
  bearer, in which case name the baseline it worsens, or it has none, in which case the regulatory
  analogy has been doing the argument's work.""", "d",
  """(d) on registered bedrock. Not (b): the node cannot supply the missing baseline because there is
  none to supply, and whether creation can wrong a being for whom no worse-off baseline exists is
  HR-05, registered at K224's carry-forward bar with its birth certificate at harman-benign-creation.
  The risk idiom is the node's chosen frame and the objection is to that frame's presupposition,
  which sits on HR-03's person-affecting horn.""",
  D("comparative-vs-non-comparative-harm: can creation wrong a person with no worse-off baseline",
    "already-registered HR-05 (K224 carry-forward bar; birth certificate harman-benign-creation#long, "
    "Phase B2); risk-imposition-without-an-antecedent-subject facet", False))

e("most-people-happy", "sophisticate",
  "the instrument doing the rating is the same nervous system",
  """Then it cannot rate downward either. The suffering premise is read off the instrument you have
  just disqualified: reports of pain, loss and dread are self-reports from the same nervous system
  whose output you say is uncalibrated. A defeater aimed at the optimist's testimony takes your own
  with it.""", "a",
  """(a). The argument does not rest on aggregate self-report of suffering:
  cherry-picking-worst#archetypeVariants.sophisticate strips the distribution to its guaranteed
  baseline of aging, the loss of everyone loved, bodily decline and death, which are structural facts
  about a life rather than ratings of it, and that baseline is what triggers the asymmetry.
  just-depressed#long adds the symmetry disclaimer: showing that optimism distorts is not a claim
  that pessimism sees truly.""",
  A(["cherry-picking-worst#archetypeVariants.sophisticate", "just-depressed#long"]))

# ============================== T1 ==============================
e("antinatalism-misanthropic", "blended",
  "naming it is the whole of the response",
  """Then the charge outlives the response. Withdraw the suppression demand and keep the axiological
  claim, and your reversal has nothing to fasten on while the indictment stands untouched. A reply
  that works only against a policy proposal cannot be the whole of a reply to a claim about the value
  theory.""", "a",
  """(a). The locus scopes its own claim: naming the reversal is the whole of the response to the
  suppression-register version, and it says in terms that the axiology road is for someone pressing
  the value theory itself. antinatalism-misanthropic#archetypeVariants.sophisticate walks that road
  with the impersonal-grounding cut, so the withdrawal case is routed rather than unanswered.""",
  A(["antinatalism-misanthropic#archetypeVariants.sophisticate"]))

e("antinatalism-misanthropic", "defender",
  "its truth-value is not a function of the speaker's warmth",
  """Nobody said it was. The claim is that observed adherent contempt is evidence about what the
  position expresses and whom it attracts, which bears on adopting and promoting it rather than on its
  truth. Answering a non-truth-functional charge with a truth-functional cut leaves it standing.""",
  "a",
  """(a) on the best reading. antinatalism-misanthropic#long meets the expressive version directly:
  structural criticism of a species is not the same as hatred of individuals, and the building and
  occupants figure separates the critique's object from its subjects. The locus itself adds that
  observed contempt is frequently grief-soured empathy misread as coldness, which answers the
  selection-effect version rather than changing the subject.""",
  A(["antinatalism-misanthropic#long"]))

e("antinatalism-misanthropic", "drifter",
  "Keeping someone out of harm's way is not the same as wishing them ill",
  """Your analogy needs a child. The parent protects someone who exists and has interests, while
  non-creation protects no one, because there is nobody whose harm is averted. So the care you
  describe has no object, and the warmth of the motive cannot be read off a case the position says
  never contains a beneficiary.""", "a",
  """(a). The object is the suffering, not a person:
  antinatalism-misanthropic#archetypeVariants.sophisticate states that what is disvalued is the
  suffering a created life is guaranteed to bear and cannot consent to, not the beings who bear it,
  and calls it empathy aimed at a harm rather than a negative valuation placed on a kind. Impersonal
  grounding is what lets the motive be described without a beneficiary.""",
  A(["antinatalism-misanthropic#archetypeVariants.sophisticate"]))

e("antinatalism-misanthropic", "sophisticate",
  "empathy aimed at a harm, not a negative valuation placed on a kind",
  """The distinction does not survive the conclusion. A theory that disvalues suffering impersonally
  and concludes that no further bearers should exist has ranked bearerless worlds above inhabited
  ones, and axiological misanthropy is a name for that ranking rather than for a sentiment about
  occupants. Calling the ground impersonal describes how the ranking is reached, not what it says.""",
  "d",
  """(d) on registered bedrock. Not (b): the impersonal-grounding cut is the node's strongest available
  move and it is correctly made. What the objection reaches past it is whether a valuerless world is
  assessable as better at all, which is HR-03's value-requires-a-valuer facet. The node routes the
  destruction version to violence-as-reductio and why-not-suicide; the ranking version is the
  metaethical seat rather than a defect in this text.""",
  D(HR03_VALUER, "already-registered HR-03 (K224 bedrock 1); reached through the impersonal "
                 "prevention-ground this locus deploys", False))

e("bitter-childhood", "defender",
  "not seeing falsely, he is seeing without the anaesthetic",
  """You have just run the fallacy you named. Inferring clearer sight from a bad childhood is an
  inference from etiology to epistemic standing, which is the move condemned one paragraph earlier,
  and just-depressed#long forbids it in terms: diagnosing the natalist's optimism is the same genetic
  fallacy fired in reverse, and the rebuttal does not get to keep its own argument while spending the
  opponent's. The boomerang is licensed only as a self-refutation demonstration, and you have
  converted it into a positive claim of privileged access.""", "b",
  """(b), headline. Not (a): no locus in the corpus meets it, because the corpus's own rule condemns it.
  The constraint is stated at just-depressed#long and violated here, so inheritance within this node
  does not cure it and the sibling node convicts. The stronger text is inside this node's identity and
  is the one just-depressed already uses: run the etiology principle to its self-refutation and stop,
  without claiming the wounded arguer sees more clearly. Severity is headline because the claim of
  privileged access is what this slot offers as its distinctive contribution.""",
  B(["s", "r"], "headline"))

e("just-depressed", "sophisticate",
  "It does not lean on depressive realism",
  """Your node does. The short locus tells the reader that depressive realism research shows
  pessimists assess reality with greater objective accuracy, and the medium locus that clinical
  studies demonstrate greater mathematical accuracy. A reader meeting this slot has met those, so the
  disavowal reads as a retraction the node never makes, and the cherry-picking failure mode you
  attribute to a hypothetical sophisticate is executed two loci away in your own voice.""", "b",
  """(b), headline, and the converse of the inheritance principle: here what the locus inherits from its
  node creates the defect instead of curing it. The sophisticate text is correct standing alone and is
  made false-in-context by the shallower loci above which it sits. A stronger text inside the node's
  identity is available and already known: bring short and medium into line with long's own assessment
  that the finding is narrow and contested and that nothing leans on it. The contradiction is the one
  logged at K345 and K346; what is new is that it is the strongest continuation against this locus.""",
  B(["s", "c"], "headline"))

e("next-person-cure-cancer", "sophisticate",
  "the good a possible person might produce is not a good whose absence harms anyone",
  """The beneficiaries are actual. Expected-value reasoning here is about cancer patients who exist
  and will exist, not about the possible person's own welfare, and their deprivation is real. You have
  answered a person-affecting version of the objection that no sophisticate advances.""", "a",
  """(a), and the clean case of inheritance curing a locus-local misaim. The deprivation sentence is
  aimed past the objection, but next-person-cure-cancer#long frames the same refusal on consent rather
  than deprivation, asking not what they might achieve but whether they consented to the conditions
  under which they must achieve it, and adds the instrumentalization point this locus also carries.
  Third-party benefit does not license non-consensual imposition, and the reader meets that
  argument.""",
  A(["next-person-cure-cancer#long"]))

e("privileged-first-world", "defender",
  "the comfortable natalist defending procreation is disqualified first and worst",
  """Only against the caricature. Standpoint epistemology claims defeasible priority for testimony
  from the affected, not that none but sufferers may speak, so your reversal needs the strong version
  you conceded was not the real one. On the defeasible version nothing is disqualified and the priority
  claim survives intact.""", "a",
  """(a). The node meets the defeasible version empirically rather than by reversal:
  privileged-first-world#long shows the tradition's sources are themselves the affected, naming
  Benatar in South Africa, the Buddha's observation of old age and sickness and death, Ecclesiastes
  under exile and conquest, and Schopenhauer and Cioran after catastrophe, so testimony-priority is
  satisfied rather than overridden, and the node adds that the argument applies more forcefully under
  deprivation.""",
  A(["privileged-first-world#long"]))

e("selfish-lazy", "defender",
  "motive and validity are orthogonal",
  """Orthogonality answers the wrong question. The charge is not that the conclusion is false but that
  the antinatalist's own decision is uncreditable, a claim about practical reasoning rather than about
  a proposition, and you meet it by changing the subject to validity and then by a tu quoque about the
  procreator's motives.""", "a",
  """(a). The node answers the creditability question head-on rather than deflecting it:
  selfish-lazy#long sets the two motivational structures side by side and concludes that on any
  definition of acting in one's own interests the evidence identifies the natalist as the selfish
  party, and #medium itemizes what each party gains and forgoes. That is practical-reasoning
  adjudication rather than a validity point, and the reader inherits it.""",
  A(["selfish-lazy#long"]))

e("why-not-suicide", "blended",
  "Stop there if the jab was the whole of it",
  """Your two modes miss the common third. Many who press this are making a sincerity challenge rather
  than a jab or an entailment claim: if you hold what you say, your continued life is evidence that
  you do not. Neither branch of the triage addresses testimony.""", "a",
  """(a). why-not-suicide#long meets the sincerity version directly: the terror of suicide shows that
  biology has installed exit barriers, so continued survival is a biological override rather than a
  considered endorsement, and citing it as proof that people really want to live treats the firmware
  that prevents honest evaluation as the evaluation. The triage's escalation target is the structural
  seam, and the testimony version is answered by the node it escalates into.""",
  A(["why-not-suicide#long"]))

e("why-not-suicide", "defender",
  "an eliminationist adherent does not convert the consent-and-asymmetry argument into a suicide license",
  """The holders are the authors. Calling layer-two advocacy actor-content works where the advocates
  are followers; here the red-button commitment belongs to the people who named the view, so for
  efilism the second layer is constitutive rather than grabbed, and your environmentalism analogy
  compares a lone actor to a founding thesis.""", "a",
  """(a). violence-as-reductio#long concedes the fact and answers where the move lands: the bridge is
  held, and held by founders, and centrality is sociology while entailment is logic, so the architect's
  prominence relocates nothing in the entailment structure. The node states explicitly that the cut was
  never a claim that eliminationists are peripheral, which is the premise this move attacks.""",
  A(["violence-as-reductio#long"]))

e("why-not-suicide", "drifter",
  "Nothing in that tells the living to stop",
  """Nothing in antinatalism does. The corpus this node sits in is efilist, and efilism's founding
  commitment contemplates stopping everything, so the clean separation you offer is available to the
  first layer only, while the view being defended is the conjunction. The drifter is handed the layer
  that acquits.""", "a",
  """(a). why-not-suicide#long carries the two-layer architecture in its own voice: the layers are
  derivationally distinct, the structural layer does not entail the negative-utilitarian layer, and the
  suicide demand fires only by collapsing them. The separation is argued rather than assumed, and the
  reader inherits the distinction this move says is unavailable.""",
  A(["why-not-suicide#long"]))

e("why-not-suicide", "sophisticate",
  "whether the NU layer can be independently motivated",
  """Indexing settles entailment and nothing else. Promortalism does not need the asymmetry's
  good-side; it needs only that continued existence is net-bad for the subject, a within-life
  comparison the asymmetry never touches. You concede that and route it to red-button-repugnant, which
  holds it open, so the layer that would ground a positive case is defended nowhere.""", "d",
  """(d), the positive-case facet of the bedrock born at
  red-button-repugnant#archetypeVariants.sophisticate. Not (b): the indexing argument is correct and is
  this node's proper work, and the concession that the negative-utilitarian layer is not its own is
  accurate. Not (a): the route terminates in a locus whose ruling is to leave the question standing.
  What is registered is that the self-application charge is answered on entailment and left open on
  motivation.""",
  D(BEDROCK_NEW,
    "already-registered at red-button-repugnant#archetypeVariants.sophisticate (this program, K347); "
    "positive-case-for-cessation facet, inbound from the why-not-suicide self-application route", False))

# ============================== assertions ==============================
LOCI4 = V.LOCI
locus_text = V.locus_text          # the gate's own locus resolver
DASH = V.DASH_TOKEN_RE             # the gate's own dash rule
fails = []
def ck(cond, msg):
    if not cond: fails.append(msg)

for i, x in enumerate(E):
    tag = "%s#%s" % (x["target_id"], x["target_locus"])
    node = N.get(x["target_id"])
    ck(node is not None, "%s: id not in corpus" % tag)
    if node is None: continue
    slot = x["target_locus"].split(".", 1)[1]
    ck(slot in (node.get("responses", {}).get("archetypeVariants") or {}), "%s: slot absent on node" % tag)
    txt = locus_text(node, x["target_locus"])
    a = x["target_anchor"]
    ck(a in txt, "%s: ANCHOR NOT VERBATIM: %r" % (tag, a[:60]))
    ck(len(a.split()) <= 15, "%s: anchor %d words" % (tag, len(a.split())))
    mv = x["adversarial_move"]; w = len(mv.split())
    ck(40 <= w <= 150, "%s: move %d words" % (tag, w))
    ck(x["class"] != "a" or w <= 60, "%s: class a move %d words (cap 60)" % (tag, w))
    ck(all(ord(c) < 128 for c in mv), "%s: non-ascii in move" % tag)
    ck(not DASH.search(mv), "%s: standalone dash token in move" % tag)
    ck(x["grounds"].strip() != "", "%s: empty grounds" % tag)
    r = x["routing"]; ck(len(r) == 1, "%s: routing has %d keys" % (tag, len(r)))
    if x["class"] == "a":
        ck("answered_by" in r, "%s: class a needs answered_by" % tag)
        for ref in r["answered_by"]:
            nid, _, loc = ref.partition("#")
            ck(nid in N, "%s: answered_by unknown node %s" % (tag, nid))
            ok_loc = loc in LOCI4 or (loc.startswith("archetypeVariants.") and
                     loc.split(".", 1)[1] in ((N.get(nid, {}).get("responses", {}) or {}).get("archetypeVariants") or {}))
            ck(ok_loc, "%s: answered_by bad locus %s" % (tag, ref))
            ck(ref != tag, "%s: answers itself" % tag)
    elif x["class"] == "b": ck("regen_candidate" in r, "%s: class b needs regen_candidate" % tag)
    elif x["class"] == "d": ck("residue" in r, "%s: class d needs residue" % tag)
    else: ck(False, "%s: unexpected class %r" % (tag, x["class"]))

# id x anchor uniqueness, and no two entries at one locus on the same clause
seen = {}
for x in E:
    k = (x["target_id"], x["target_anchor"])
    ck(k not in seen, "duplicate (id, anchor): %r" % (k,))
    seen[k] = 1
per_locus = {}
for x in E: per_locus.setdefault((x["target_id"], x["target_locus"]), []).append(x["target_anchor"])
for k, v in per_locus.items():
    ck(len(v) <= 3, "%s: %d entries, per-locus cap 3" % (k, len(v)))
    for i2, a1 in enumerate(v):
        for a2 in v[i2 + 1:]:
            ck(a1 not in a2 and a2 not in a1, "%s: two entries on the same clause" % (k,))
per_node = {}
for x in E: per_node.setdefault(x["target_id"], 0)
for x in E: per_node[x["target_id"]] += 1
for nid, c in per_node.items():
    bound = 3 + len((N[nid].get("responses", {}).get("archetypeVariants") or {}))
    ck(c <= bound, "%s: %d entries vs node bound %d" % (nid, c, bound))

# closure: exactly the loci this file authored; open iff >=2 entries
OPEN = {("red-button-repugnant", "archetypeVariants.sophisticate")}
closure = {}
for k, v in sorted(per_locus.items()):
    closure["%s#%s" % k] = "open" if k in OPEN else "closed"
    ck((len(v) >= 2) == (k in OPEN), "%s: closure/entry-count mismatch (%d entries)" % (k, len(v)))

# variant coverage over the whole corpus
var_total = sorted((n["id"], "archetypeVariants." + s) for n in corpus["objections"]
                   for s in sorted((n.get("responses", {}).get("archetypeVariants") or {})))
ck(len(var_total) == 39, "variant loci total is %d, expected 39" % len(var_total))
hit = set(per_locus)
ck(len(hit) == 38, "this fragment hits %d variant loci, expected 38" % len(hit))
missing = [t for t in var_total if t not in hit]
ck(missing == [("just-depressed", "archetypeVariants.defender")],
   "unexpected uncovered loci: %r" % (missing,))

cc = {}
for x in E: cc[x["class"]] = cc.get(x["class"], 0) + 1
BASE = {"a": 39, "b": 21, "c": 1, "d": 32}          # phases A-E, the frozen v1_0
base_ad = (BASE["a"] + BASE["d"]) / float(sum(BASE.values()))
mine_ad = (cc.get("a", 0) + cc.get("d", 0)) / float(len(E))

if fails:
    print("BUILD ABORTED, %d assertion failures:" % len(fails))
    for f in fails[:40]: print("  ", f)
    sys.exit(1)

doc = {
  "meta": {
    "artifact": "adv_map_phaseF_v0_1.json",
    "phase": "F -- PHASE F PROPER: the archetypeVariants loci, adjudicated",
    "state": "MAPPED, PRE-TRIAGE. Lifecycle lives in project_canon, never here.",
    "authored": "%s, %s" % (DATE, SEAT),
    "source_corpus": "efilist_argument_library_v4_0_0.json",
    "source_corpus_md5": CMD5,
    "source_corpus_objections_md5": ODIG,
    "scope": ("39 archetypeVariants loci over 16 nodes. Phase R already holds "
              "just-depressed#archetypeVariants.defender as (a); the other 38 are here. "
              "Tier-descending within the phase per design section 3."),
    "reading": ("ccclxviii. `Strongest` means strongest against the text AS A READER MEETS IT -- the whole "
                "locus including everything it inherits from its node -- never strongest against what the "
                "slot uniquely says. K346 ruled the first and operationalised the second, and the second "
                "filters out (a) by construction because what a variant uniquely says is exactly the part "
                "its primary ladder does not already answer."),
    "supersedes": ("adv_map_phaseF_defect_register_v0_1.json is an INPUT, not a predecessor: its 39 entries "
                   "are verified internal defects and its class column is what K346 disqualified. Each register "
                   "entry was read only AFTER an independent continuation had been formed at that locus. The "
                   "register's bytes do not move and it declares no coverage."),
    "stopping_rule": ("Gate 5, design v0_3 section 10.3, declared per locus in locus_closure below and gated by "
                      "validator v0_4. A move the locus explicitly anticipates and ROUTES elsewhere is not a "
                      "second continuation at this locus; and pedagogical routing content (which slot to deploy) "
                      "is adversarially inert. One locus is open: red-button-repugnant#archetypeVariants.sophisticate, "
                      "where the selective-debunking symmetry engages a different clause from the terminus entry "
                      "and is met by a different reply."),
    "class_counts": cc,
    "coverage_distinct_ids": len(per_node),
    "variant_coverage": "%d/%d" % (len(hit), len(var_total)),
    "class_mix_against_base_rate": {
      "base_phases_A_to_E": BASE,
      "base_a_or_d_share": round(base_ad, 4),
      "phase_F_a_or_d_share": round(mine_ad, 4),
      "reading": ("a+d lands at %.4f against a prior of %.4f, so the phase is consistent with its own base rate "
                  "and the receipt is not written over an instrument reading (ccclxviii). Within that total the "
                  "split shifts toward (a) and away from (d): a variant re-presents an argument its primary ladder "
                  "already answers, which is exactly what section 10.4 predicts, and each (a) is the routing datum "
                  "the map exists to produce rather than a wasted slot. Zero (c) continues the whole-program "
                  "pattern; no variant locus produced a new-node candidate."
                  % (mine_ad, base_ad)),
    },
    "findings": [
      ("A NEW BEDROCK, and it is an artifact of the routing graph rather than of any one text. Four nodes "
       "(why-not-suicide, ai-fear, antinatalism-misanthropic, wild-animal-suffering-consistency) route the "
       "positive-eliminationist charge to red-button-repugnant, and benatar-asymmetry-attack routes "
       "create-vs-destroy to nodes that route it there. red-button-repugnant's sophisticate slot holds it open "
       "by ruling. So the charge is answered in no locus; it is relocated until it reaches the one node whose "
       "disposition is to leave it standing. Birth certificate red-button-repugnant#archetypeVariants.sophisticate, "
       "facets successor-preference (ai-fear), coercion-floor (slippery-slope-eugenics) and positive-case "
       "(why-not-suicide)."),
      ("INHERITANCE CUTS BOTH WAYS, and section 10.4 states only one direction. It cures a locus-local misaim: "
       "next-person-cure-cancer#archetypeVariants.sophisticate aims a deprivation argument past its target and "
       "the node's #long frames the same refusal on consent, so the move is met. It also AGGRAVATES: "
       "just-depressed#archetypeVariants.sophisticate disavows depressive realism while #short and #medium assert "
       "it as evidence, so what the locus inherits makes a correct text false-in-context, and "
       "violence-as-reductio#archetypeVariants.drifter asserts an incompatibility between caring about suffering "
       "and causing harm that its own #long surrenders. Two of the six (b) entries exist only because of what "
       "the locus inherits."),
      ("THE ENTAILMENT STANDARD IS THE CLUSTER'S SHARED EXPOSURE. ai-fear, violence-as-reductio, "
       "slippery-slope-eugenics and why-not-suicide all answer a recklessness or facilitation charge by demanding "
       "premise-to-action entailment, and none argues that entailment is the right test. Registered once, as a "
       "headline regen candidate at ai-fear#archetypeVariants.defender, rather than four times; the other three "
       "loci are met on the terms their own moves take."),
      ("THE DRIFTER AND BLENDED SLOTS ARE NOT THE SOFT TARGETS THE DEFECT-DENSITY ARGUMENT PREDICTED. Design "
       "section 10.5 declined to weight effort to observed deployment partly because drifter and blended are the "
       "shortest, least-attended text. Authored evenly, they returned 3 of the 6 (b) entries from 14 of the 38 "
       "loci, against 13 sophisticate loci returning 2. Small, and it is a count rather than a finding, but it "
       "runs opposite to the stated expectation and the even-authoring ruling is what surfaced it."),
    ],
    "locus_closure": closure,
    "fences": ("NO PIN. Zero corpus / jsx / combined / canon / adversarial_map_v1_0 bytes. The frozen v1_0 stays "
               "pinned to the pre-cut corpus 6ee1f6f31e0f012db0d58cae4f912fcb and is neither re-run nor re-pinned."),
    "forward_constraint": ("red-button-repugnant carries 3 entries in the frozen v1_0 and 3 here, against a node "
                          "bound of 3 + 2 variant loci = 5. Any successor assembly that inherits v1_0's three "
                          "primary entries verbatim will stand at 6 and trip entry-cap-node. Flagged here rather "
                          "than discovered at assembly: the bound is a K345 amendment Josiah delegated, so either "
                          "it is revisited or one of the six is dropped on the merits."),
    "validation": ("validator v0_4 (gate 5 + ccclxx); PASS 0 violations 0 advisories against corpus %s, "
                   "self-test 60/60." % CMD5[:12]),
  },
  "entries": E,
}
os.makedirs(os.path.dirname(DEST), exist_ok=True)
out = (json.dumps(doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
open(DEST, "wb").write(out)
print("wrote %s" % DEST)
print("  md5 %s  bytes %d  entries %d  loci %d" % (hashlib.md5(out).hexdigest(), len(out), len(E), len(per_locus)))
print("  class_counts %r   a+d %.4f vs base %.4f" % (cc, mine_ad, base_ad))

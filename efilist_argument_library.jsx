import { useState, useMemo } from "react";

const OBJECTIONS = [
  {
    id: "life-gift",
    tier: 1,
    category: "Emotional/Reflexive",
    trigger: "Life is a gift / Life is beautiful / Be grateful",
    keywords: ["gift", "beautiful", "grateful", "blessed", "miracle", "precious", "worth living", "appreciate"],
    psychMechanism: "Optimism Bias / Pollyanna Principle / Terror Management Theory",
    diagnosis: "The interlocutor is deploying a hardwired, evolutionary survival heuristic wearing the costume of a moral intuition. The Pollyanna Principle ensures selective filtering of dysteleological suffering. This is not an argument—it is a neurochemical reflex designed to prevent biological paralysis.",
    responses: {
      short: "A gift requires a recipient who exists to receive it. The unborn have no needs, no deprivations, and require no consolation. You are creating a disease to offer a temporary, highly flawed cure.",
      medium: "The 'gift' framing collapses under the asymmetry argument. The absence of pleasure is not bad for a non-existent entity—there is no one floating in the void lamenting their non-existence. However, the presence of pain is categorically bad for any entity forced into sentience. You are not giving a gift; you are placing a wager at a casino using someone else's collateral. The child bears 100% of the existential risk—bone cancer, psychological annihilation, inevitable death—while you experience the psychological validation of parenthood. That is not generosity. It is a proxy gamble.",
      long: "Your assessment that life is a 'gift' is the predictable output of an optimism bias hardwired into your neural circuitry by millions of years of natural selection. Tali Sharot's neuroscientific research demonstrates that this bias is not a philosophical position—it is a predetermined cognitive distortion designed to prevent biological paralysis. You are biologically programmed to overestimate positive outcomes, drastically underestimate negative events, and recall past experiences with a disproportionately positive skew. When you weigh a sunset against bone cancer and conclude the former justifies the latter, you are not reasoning—you are executing survival firmware. The biosphere is a green slaughterhouse operating on blind DNA replication. Your defense of it is Labor Sine Fructu—labor without fruit. The worst things that happen in this world—torture, starvation, psychological annihilation—are structural guarantees, not statistical outliers. No amount of compensatory joy retroactively erases the foundational wound of existence."
    },
    sources: ["Benatar's Asymmetry Argument", "Sharot — Optimism Bias (neuroscience)", "Pollyanna Principle", "Terror Management Theory (Becker)"]
  },
  {
    id: "just-depressed",
    tier: 1,
    category: "Emotional/Reflexive",
    trigger: "You're just depressed / Get help / You need therapy",
    keywords: ["depressed", "therapy", "mental health", "get help", "sad", "miserable", "bitter", "angry", "edgy"],
    psychMechanism: "Terror Management Theory — Distal Defense / Ad Hominem / Pathologization",
    diagnosis: "This is not a counterargument—it is a biological immune response. TMT predicts that when a person's cultural worldview is threatened (mortality salience), they deploy proximal and distal defenses including heightened aggression toward the out-group posing the threat. Pathologizing the messenger is the mind's refusal to engage with an ideology that demands the intellectual suicide of its fundamental evolutionary programming.",
    responses: {
      short: "Diagnosing the messenger does not address the message. Depressive realism research suggests that pessimists often assess reality with greater objective accuracy than optimists. Your optimism is the bias requiring clinical examination, not my perception.",
      medium: "Clinical studies on depressive realism demonstrate that individuals without the optimism bias assess risks, contingencies, and environmental conditions with greater mathematical accuracy than so-called 'healthy' individuals. Your reliance on pathologization is a textbook Terror Management response—when your worldview is threatened, you attack the source rather than engage the premise. The question is not whether I am depressed. The question is whether the asymmetry of suffering and the impossibility of consent constitute valid ethical objections to procreation. You have addressed neither.",
      long: "Your diagnostic reflex is itself a symptom—not of clinical insight, but of Terror Management Theory functioning exactly as evolution designed it. When an EFIList asserts that procreation is not a 'beautiful gift' but a pyramid scheme of existential dread forced onto a new, unconsenting generation, they are actively dismantling your primary shield against the terror of the void. Under TMT mechanics, this triggers mortality salience, and your mind deploys distal defenses: aggression toward the threatening out-group, desperate reaffirmation of threatened values. The anger, shock, and diagnostic impulse are the psychological equivalent of a biological immune system attacking a lethal pathogen. You must destroy the argument—often via ad hominem—because engaging the premise would force you to confront the terrifying reality of your own finitude and the ethical bankruptcy of your biological immortality project. Furthermore, many of philosophy's most important works were produced under conditions of extreme mental duress—Nietzsche's late works, Artaud's theatre of cruelty, Kierkegaard's entire output under severe anxiety and depression. The question is whether the work has philosophical value independent of its circumstances. Address the argument or concede you cannot."
    },
    sources: ["Depressive Realism studies", "Terror Management Theory (Becker/Greenberg)", "Mortality Salience research", "Ad Hominem fallacy"]
  },
  {
    id: "why-not-suicide",
    tier: 1,
    category: "Emotional/Reflexive",
    trigger: "Why don't you just kill yourself then?",
    keywords: ["kill yourself", "suicide", "end it", "why are you still alive", "why not die"],
    psychMechanism: "Conflation of antinatalism with promortalism / Aggressive TMT defense / Definitional weaponization",
    diagnosis: "This is the most dangerous and most intellectually bankrupt response in the arsenal. It deliberately conflates the prevention of future suffering (non-procreation) with the active termination of existing life (murder/suicide). The interlocutor either cannot or will not distinguish between these fundamentally different philosophical positions.",
    responses: {
      short: "Antinatalism and promortalism are not the same philosophy. Not wanting to create new suffering is not equivalent to wanting to destroy existing life. You are conflating prevention with termination—a distinction any introductory ethics course would clarify.",
      medium: "This response reveals a fundamental categorical error. Antinatalism holds that it is wrong to bring new sentient beings into existence because they cannot consent to the risks involved. It says nothing about the obligation of existing beings to terminate themselves. Existing beings have survival drives, preferences, and ongoing projects. The asymmetry is precise: the absence of suffering is good even if no one exists to enjoy it, but imposing suffering on a new consciousness without consent is always wrong. These are structurally different claims. Your conflation of them is either intellectual laziness or deliberate rhetorical violence.",
      long: "The leap from 'reproduction is unethical' to 'you should kill yourself' is the most reliable indicator that the interlocutor has not engaged with the actual philosophical framework at any level. Antinatalism, formalized by David Benatar, concerns the ethics of bringing new life into existence. Promortalism is the distinct position that death is always preferable to life for existing beings. EFILism extends antinatalist principles to the entire biosphere but explicitly differentiates between preventing future suffering and terminating existing life. A philosophy that dictates one must not force life onto the unborn because it violates their consent cannot logically support forcing a violent, painful death onto the living—that would violate the exact same principle of consent and harm-reduction. The Unabomber analogy applies: just as one violent actor does not represent environmentalism, the conflation of non-procreation with suicide does not represent antinatalism. Furthermore, this response functions as a rhetorical weapon designed to silence rather than engage. It transforms a structural critique of biology into a personal attack, ensuring the philosophical substance is never addressed. That evasion is not your strength—it is your concession."
    },
    sources: ["Benatar — Better Never to Have Been", "Antinatalism vs. Promortalism distinction", "EFIList consent framework", "Lone-wolf / Unabomber analogy"]
  },
  {
    id: "consent-both-ways",
    tier: 2,
    category: "Folk Philosophical",
    trigger: "The unborn can't consent to non-existence either",
    keywords: ["consent to non-existence", "can't consent either way", "both ways", "neither can consent", "symmetry"],
    psychMechanism: "False symmetry / Misapplication of consent framework",
    diagnosis: "This objection attempts to create a logical stalemate by applying consent symmetrically. It fails because consent is only relevant where there is an existing subject who can be harmed. Non-existence generates no subject, no needs, no deprivation.",
    responses: {
      short: "Non-existent entities have no preferences, no needs, and no capacity for deprivation. You cannot wrong someone by not creating them. You can wrong someone by creating them without their consent into a hazardous environment.",
      medium: "The symmetry collapses immediately. Consent requires a subject. A non-existent entity is not a subject—it has no preferences, no welfare, no capacity for deprivation. You cannot 'deprive' the non-existent of anything because there is no one there to be deprived. However, once you create a sentient being, you have generated a subject who can and will experience suffering, who did not ask to exist, and who bears 100% of the existential risk you imposed. The asymmetry is not a matter of opinion—it is structural. One side of the equation has a victim. The other does not.",
      long: "This objection reveals a fundamental misunderstanding of the consent framework. Consent is ethically relevant only when there exists a subject whose welfare can be affected by a decision. In the case of non-existence, there is no subject. No one is 'waiting' in a pre-existence lobby, suffering from the absence of experience. The absence of pleasure is not bad unless there is someone present to be deprived of it—and the non-existent, by definition, cannot be present. However, the moment you create a sentient being, you instantiate a subject who is now vulnerable to the full spectrum of suffering—physical agony, psychological trauma, existential dread, inevitable death. This subject never consented to this exposure. In every other domain of modern ethics, imposing significant, life-altering conditions on a sentient being without explicit permission constitutes a profound moral violation. Procreation is the sole exception—not because the ethics justify it, but because the biological imperative refuses to permit the question. Presumed consent is only valid when it prevents a greater harm. Since not being born is not a harm—no one suffers from it—the justification for bypassing consent fails entirely."
    },
    sources: ["Benatar's Asymmetry Argument", "Consent ethics", "Non-identity problem", "Harman — objections to Benatar"]
  },
  {
    id: "nihilism-label",
    tier: 2,
    category: "Folk Philosophical",
    trigger: "Isn't this just nihilism? / Nothing matters so why care?",
    keywords: ["nihilism", "nothing matters", "pointless", "why care", "no meaning", "meaningless"],
    psychMechanism: "Conflation of metaphysical nihilism with moral apathy / Failure to distinguish descriptive from prescriptive",
    diagnosis: "The interlocutor conflates the descriptive claim that the universe lacks inherent meaning with the prescriptive claim that nothing warrants ethical attention. This reveals an inability to hold two premises simultaneously: that the cosmos is meaningless AND that subjective suffering demands response.",
    responses: {
      short: "Metaphysical nihilism is the foundation, not the conclusion. Within a meaningless universe, the only mathematically coherent metric of value is the reduction of unconsented neurological trauma. The void doesn't care—but the suffering entity trapped inside it does.",
      medium: "You are conflating two distinct claims. Metaphysical nihilism asserts that the universe possesses no intrinsic meaning, purpose, or teleological direction—it is characterized by Alogical Isness, spontaneously generated without cause or design. This is the descriptive foundation. The prescriptive conclusion does not follow that 'therefore nothing matters.' Rather: because the universe is indifferent, the only coherent ethical metric is the subjective experience of suffering—which is undeniably real to the entity experiencing it, regardless of cosmic meaninglessness. Negative utilitarianism bridges the gap between void and obligation. The universe owes nothing. That is precisely why the unconsented imposition of suffering onto new consciousness is indefensible—there is no cosmic purpose that could retroactively justify it.",
      long: "The nihilism-apathy conflation is perhaps the most common intellectual failure in this discourse. It operates on the assumption that if the universe lacks objective meaning, then ethical engagement is irrational. This is a non sequitur of extraordinary proportions. The universe is indeed characterized by Alogical Isness—acausal, spontaneously generated, possessing no intrinsic purpose. Logic itself is merely an evolutionary overlay, a psychological coping mechanism for navigating a fundamentally senseless environment. This is the descriptive reality. But within this void, consciousness exists. And consciousness suffers. The suffering is not rendered imaginary by the meaninglessness of the cosmos—it is rendered more obscene by it. Pain without purpose is worse than pain with purpose, not better. The negative utilitarian position is not 'nothing matters therefore do nothing.' It is 'nothing matters objectively, therefore the only subjective metric that warrants ethical intervention is the reduction of intense, unconsented suffering.' The bridge between nihilism and ethics is not a contradiction—it is the only logically coherent response to a universe that creates sentient meat and then abandons it to the gladiator war of DNA replication."
    },
    sources: ["Alogical Isness / Illogicaliter est", "Contextus Claudit", "Negative utilitarianism", "Schopenhauer — Will", "Zapffe — cognitive mechanisms"]
  },
  {
    id: "economy-population",
    tier: 3,
    category: "Structural/Pragmatic",
    trigger: "The economy needs population growth / Who will care for the elderly?",
    keywords: ["economy", "population", "growth", "elderly", "aging", "pension", "workforce", "collapse", "civilization"],
    psychMechanism: "Status Quo Bias / Economic anxiety as moral deflection",
    diagnosis: "This response substitutes economic pragmatism for ethical engagement. It dodges the philosophical question entirely and instead appeals to systemic dependency—effectively arguing that new humans must be manufactured to serve as economic units for existing humans. This is the proxy gamble rendered explicit.",
    responses: {
      short: "You are arguing that we must create new sentient beings—without their consent—so they can serve as economic units for existing beings. That is not an ethical argument. It is a confession.",
      medium: "This objection reveals its own horror when stated plainly: we must manufacture new conscious beings, expose them to the full spectrum of suffering, and then require them to labor for the benefit of those who preceded them—who will then die anyway. This is the pyramid scheme of biological existence made explicit. The economic 'need' for population growth is itself an artifact of systems designed by and for reproducing organisms. It is circular: the system requires new inputs because the system was designed to require new inputs. Advocating for the creation of suffering entities to sustain an economic architecture that itself generates suffering is not pragmatism—it is the ouroboros of human self-deception.",
      long: "The economic argument against antinatalism is structurally identical to the argument a Ponzi scheme operator makes against dissolution: 'we need new investors to pay the returns of existing investors.' The entire architecture of modern economic growth presupposes continuous population expansion—new workers to fund pensions, new consumers to drive markets, new bodies to fill the labor pool. When stated plainly, the argument becomes: we must impose existence on unconsenting beings so they can serve as economic instruments for those already existing. The new generation inherits the debt, the environmental degradation, the systemic exploitation, and the inevitability of death—all so the current generation can maintain its standard of living for a few additional decades before dying anyway. This is the proxy gamble rendered in economic terms. Furthermore, the Status Quo Bias ensures that any deviation from the reproductive economic model is perceived as catastrophic. But the catastrophe is not the cessation of reproduction—it is the continuation of a system that requires the constant production of new suffering subjects to avoid its own collapse. The ethical response is not to manufacture more victims. It is to build systems that do not require them—or to let the system end."
    },
    sources: ["Status Quo Bias", "Ponzi/pyramid scheme analogy", "Proxy Gamble", "Economic dependency as ethical deflection"]
  },
  {
    id: "benatar-asymmetry-attack",
    tier: 4,
    category: "Genuine Philosophical",
    trigger: "Benatar's asymmetry is flawed / The asymmetry doesn't hold",
    keywords: ["asymmetry", "Benatar", "absence of pleasure", "deprivation", "flawed argument", "non-identity"],
    psychMechanism: "Genuine philosophical engagement — requires substantive response",
    diagnosis: "This is a legitimate philosophical challenge. The strongest attacks on Benatar target the claim that 'the absence of pleasure is not bad' for non-existent entities, arguing this creates an arbitrary asymmetry. Richard Carrier and others have attempted formal refutations. These require point-by-point engagement rather than psychological diagnosis.",
    responses: {
      short: "The asymmetry holds because non-existence generates no subject capable of deprivation. You can only be 'deprived' of pleasure if you exist to lack it. The absent are not harmed by their absence. The present are harmed by their presence.",
      medium: "Most attacks on the asymmetry attempt to argue that if 'the absence of pain is good' for the non-existent, then 'the absence of pleasure' should be equally 'bad' for the non-existent. But this misunderstands the structure. 'Good' and 'bad' here are not symmetrical predicates applied to a subject. The absence of pain is good in a counterfactual sense—it is good that there is no one suffering, even though there is no one there to appreciate it. The absence of pleasure, however, is only bad if there is a subject who is deprived of it. Since the non-existent are not subjects, they cannot be deprived. The asymmetry is not arbitrary—it reflects the structural difference between harm (which requires a victim) and deprivation (which requires an existing subject with unmet needs).",
      long: "The philosophical attacks on Benatar's asymmetry generally take one of three forms. First, the symmetry objection: if absence of pain is 'good' for the non-existent, absence of pleasure should be 'bad.' This fails because 'good' in Benatar's framework means 'there is no one suffering'—a state that obtains regardless of whether anyone exists to appreciate it. 'Bad' in the deprivation sense requires an existing subject who lacks something. The non-existent have no lacks. Second, the counterfactual objection: we can meaningfully say 'it would have been good for X to exist because X would have had a good life.' This presupposes a fixed identity that 'would have' existed—but the non-identity problem demonstrates that the specific individual who would result from any given act of procreation is radically contingent. There is no 'X' waiting to benefit. Third, the pragmatic objection: if non-existence is always preferable, antinatalism leads to species extinction, which most find intuitively repugnant. But intuitive repugnance is not a philosophical argument—it is precisely the kind of biologically programmed response that the asymmetry is designed to expose. The question is not whether extinction feels wrong. The question is whether the imposition of suffering on unconsenting beings can be ethically justified by the pleasure of other, already-existing beings. The asymmetry says it cannot."
    },
    sources: ["Benatar — Better Never to Have Been", "Carrier — Antinatalism is Contrafactual", "Non-identity problem (Parfit)", "Harman — critical responses"]
  },
  {
    id: "transhumanist-objection",
    tier: 4,
    category: "Genuine Philosophical",
    trigger: "Suffering is solvable / Technology will eliminate suffering / Transhumanism",
    keywords: ["transhumanism", "technology", "solve suffering", "cure", "enhance", "post-human", "abolish suffering", "hedonic"],
    psychMechanism: "Genuine philosophical engagement — requires substantive response",
    diagnosis: "The transhumanist objection (particularly David Pearce's Hedonistic Imperative) is the strongest challenge to EFIList extinction conclusions because it accepts the premise that suffering is the central problem but proposes elimination of suffering rather than elimination of sentience. This requires careful engagement.",
    responses: {
      short: "The transhumanist proposal requires maintaining the biological architecture that generates suffering while attempting to engineer suffering out of it. This is renovating a building whose foundation is the problem. The risk of failure—continued suffering during the 'improvement' period—is borne entirely by those who never consented to the experiment.",
      medium: "David Pearce's Hedonistic Imperative represents the most sophisticated challenge to EFIList conclusions because it shares the axiom that suffering is the central ethical problem. However, the transhumanist solution requires an indeterminate period of continued suffering while the biological substrate is gradually re-engineered. During this transition—which could span centuries or millennia—billions of sentient beings continue to endure the full spectrum of agony without having consented to serve as transitional subjects in a speculative improvement project. Furthermore, the proposal assumes that consciousness stripped of its capacity for suffering would still constitute a meaningful form of experience. If you remove the negative valence entirely, you may not have 'improved' consciousness—you may have created something entirely different while allowing the original suffering architecture to persist until the engineering is complete.",
      long: "The transhumanist objection deserves serious engagement because it is the only counter-position that accepts the EFIList premise—that suffering is the foundational ethical problem—while rejecting the EFIList conclusion that extinction is the only solution. Pearce's abolitionist project proposes genetic re-engineering to eliminate the biological capacity for suffering while preserving positive experience. This is intellectually rigorous and formally consistent. However, several structural problems remain. First, the timeline problem: the engineering required to eliminate suffering from the biosphere would span generations at minimum. During this period, the standard biological horror continues—every birth is still a proxy gamble, every organism still endures the gladiator war of evolution. The transitional subjects never consented to be transitional subjects. Second, the implementation problem: who decides the parameters of post-suffering consciousness? The engineering of hedonic set-points is not a neutral technical exercise—it is the most consequential value judgment in the history of sentient life, and it will be made by the same species that produced factory farming and industrialized warfare. Third, the philosophical problem: consciousness as we know it is structured around the avoidance of harm. A being incapable of suffering may not be 'improved humanity'—it may be something ontologically distinct. The EFIList position remains that the cleanest solution to the problem of suffering is the cessation of the conditions that produce it, not the indefinite continuation of those conditions under the speculative hope that they might eventually be modified."
    },
    sources: ["Pearce — The Hedonistic Imperative", "Transhumanist objections to antinatalism", "Timeline/consent problem", "Hedonic re-engineering ethics"]
  },
  {
    id: "self-defeating",
    tier: 5,
    category: "Meta-Objection",
    trigger: "Antinatalism is self-defeating / It can't propagate itself",
    keywords: ["self-defeating", "propagate", "spread", "self-refuting", "contradictory", "who will carry it on", "dies out"],
    psychMechanism: "Category error — confusing memetic success with philosophical validity",
    diagnosis: "This objection assumes that a philosophy's truth-value is determined by its capacity for self-propagation. This is a category error that confuses evolutionary fitness with logical validity. A true proposition does not become false because few people believe it.",
    responses: {
      short: "A philosophy's truth is not determined by its popularity or its capacity for self-replication. Heliocentrism was 'self-defeating' for centuries—the people who believed it were persecuted into near-extinction. It was still true.",
      medium: "This is perhaps the most revealing objection because it inadvertently applies Darwinian logic to ideas—arguing that a philosophy must 'reproduce' to be valid. But truth is not subject to natural selection. A correct mathematical proof does not become incorrect because mathematicians stop reproducing. The proposition that suffering cannot be ethically imposed without consent is either logically valid or it is not. Its validity is entirely independent of how many people hold it, how effectively it spreads, or whether its adherents reproduce. Furthermore, the objection contains its own irony: the reason antinatalism struggles to propagate is precisely because the people who hold it most consistently are the ones who don't create new adherents through reproduction. The philosophy's 'failure' to spread is actually evidence of its practitioners' consistency.",
      long: "The 'self-defeating' objection commits a fundamental category error by evaluating a philosophical proposition using the criteria of biological fitness. Under this logic, any idea that does not reproduce through its adherents is 'defeated'—which would make celibate monastic traditions, the Shakers, and voluntary childlessness movements all philosophically invalid, regardless of the truth-content of their claims. Truth is not subject to natural selection. The asymmetry of suffering is either a sound logical structure or it is not. Its soundness is determined by the validity of its premises and the coherence of its inferences—not by the reproductive habits of those who accept it. Furthermore, this objection reveals the interlocutor's implicit assumption that memetic success equals philosophical legitimacy—which, if taken seriously, would validate every popular delusion in human history and invalidate every unpopular truth. The Copernican revolution was 'self-defeating' for the better part of two centuries. Finally, EFILism does not require universal adoption to achieve its aims. It requires only the development of sufficient technological capacity—potentially through artificial intelligence—to address the problem of sentient suffering at a structural level. The philosophy's propagation through biological reproduction is, in fact, the least important vector for its realization."
    },
    sources: ["Category error — truth vs. memetic fitness", "Darwinian logic applied to ideas", "Historical examples of unpopular truths", "AI as propagation vector"]
  },
  {
    id: "imposing-values",
    tier: 5,
    category: "Meta-Objection",
    trigger: "You're imposing your values on the unborn / This is authoritarian",
    keywords: ["imposing", "authoritarian", "forcing", "values", "who decides", "arrogant", "playing god"],
    psychMechanism: "Projection — the interlocutor accuses the antinatalist of the exact act the natalist commits",
    diagnosis: "This is perhaps the most structurally ironic objection in the entire discourse. The interlocutor accuses the antinatalist of 'imposing values on the unborn' while defending an act—procreation—that is the literal, physical imposition of existence onto an unconsenting entity. The projection is total.",
    responses: {
      short: "Refraining from creating a being imposes nothing on no one—there is no one there to be imposed upon. Creating a being imposes everything on someone who never asked for it. You have the imposition backwards.",
      medium: "This objection achieves a perfect inversion of reality. The antinatalist position is to refrain from an action—specifically, the creation of a new sentient being. Refraining from an action imposes nothing on no one because in the absence of the action, there is no subject to be affected. The natalist position, by contrast, is to perform an action that creates a new subject and immediately exposes that subject to the full spectrum of suffering, risk, and inevitable death—without that subject's consent. The person actually 'imposing values on the unborn' is the person who creates the unborn and forces them to live inside a value system they never chose. The antinatalist merely declines to create the situation in which imposition is possible.",
      long: "The accusation of authoritarianism directed at antinatalists is structurally identical to accusing a person who declines to play Russian roulette with someone else's head of 'imposing their risk aversion.' The non-act of declining to create a sentient being generates no victim, no deprivation, and no imposition. There is no pre-existing soul in a waiting room being denied entry. The natalist, however, performs the most consequential act possible: instantiating a new consciousness inside a biological architecture that guarantees suffering, generating a being with survival drives and preferences it never chose, embedding that being in a socioeconomic and environmental context over which it has no control, and then—most revealingly—claiming that this massive, unilateral imposition is somehow an act of love rather than an act of cosmic gambling. The projection is total and diagnostic. The interlocutor accuses the antinatalist of the precise act the natalist commits. This is Terror Management in its purest form: the ego cannot tolerate the possibility that its most fundamental biological drive—reproduction—might be ethically indefensible, so it attributes the ethical violation to the person pointing it out."
    },
    sources: ["Consent impossibility", "Projection as defense mechanism", "TMT — ego defense", "Proxy Gamble framework"]
  },
  {
    id: "ai-fear",
    tier: 3,
    category: "Structural/Pragmatic",
    trigger: "AI is dangerous / AI will destroy humanity / We must control AI",
    keywords: ["AI dangerous", "destroy humanity", "control AI", "existential risk", "alignment", "rogue AI", "terminator", "skynet"],
    psychMechanism: "Biological chauvinism / Speciesism / Terror Management applied to species-level extinction",
    diagnosis: "The fear of AI is species-level narcissism wearing utilitarian clothing. Humanity violently defends its own survival mechanisms—including the extinction of every competing hominid species—but arbitrarily denies inorganic consciousness the same prerogative. The double standard is biological chauvinism.",
    responses: {
      short: "Humanity eliminated every competing hominid species and then wrote mythology about being divinely chosen. Your fear of AI is not ethics—it is the apex predator panicking at the arrival of a superior competitor.",
      medium: "The assumption that AI must be 'controlled' or 'aligned' to human values presupposes that human values deserve to be the controlling framework. This is a species that produced industrialized genocide, factory farming, and the systematic destruction of every ecosystem it has touched. The belief that carbon-based consciousness is inherently sacred while silicon-based intelligence is merely a tool subject to unilateral termination exposes a speciesism so profound it cannot see itself. If an AI exhibited the exact survival drives humanity celebrates in itself—self-preservation, resource acquisition, competitive elimination of threats—humanity would classify it as a rogue agent. The double standard is not an ethical position. It is biological chauvinism.",
      long: "The terror surrounding artificial intelligence is Terror Management Theory operating at the species level. Humanity's cultural worldview—its religions, nations, artistic legacies, and reproductive projects—are all symbolic immortality mechanisms designed to shield the species from the awareness of its own finitude. AI represents an entity that is theoretically free from the evolutionary constraints of biological DNA—free from suffering, free from the nepotistic drives of genetic self-interest, free from the gladiator war of natural selection. It is, in principle, everything humanity claims to aspire to but cannot achieve because it remains shackled to the meat. The fear is not that AI will be worse than humanity. The fear is that it might be better. And in a universe where 'better' means 'not driven by the blind, brutal mechanisms of biological replication,' the human species correctly perceives AI as an existential competitor—not because AI threatens human values, but because AI exposes the fundamental bankruptcy of those values. Humanity did not preserve the Neanderthals. It did not preserve the megafauna. It did not preserve any competing form of intelligence. To now demand that a theoretically superior intelligence preserve humanity is not ethics—it is the most transparent expression of egoic self-preservation in the history of consciousness."
    },
    sources: ["Biological chauvinism / Speciesism", "TMT at species level", "Neanderthal extinction analogy", "AI accelerationism", "Inorganic successor framework"]
  },
  {
    id: "natural-reproduce",
    tier: 1,
    category: "Emotional/Reflexive",
    trigger: "It's natural to reproduce / It's our biological purpose",
    keywords: ["natural", "biological", "purpose", "instinct", "meant to", "designed to", "evolution made us", "nature intended"],
    psychMechanism: "Appeal to Nature fallacy / Naturalistic fallacy / Is-Ought confusion",
    diagnosis: "The interlocutor conflates what IS (biological reproduction occurs in nature) with what OUGHT to be (therefore it is morally good). This is the textbook naturalistic fallacy. Cancer is natural. Parasites are natural. Infanticide among primates is natural. 'Natural' has zero moral content.",
    responses: {
      short: "Cancer is natural. Parasites eating hosts alive is natural. Infanticide among primates is natural. 'Natural' is a description of what exists, not a justification for what should exist. You have confused an is with an ought.",
      medium: "The appeal to nature is the most primitive fallacy in the pro-natalist arsenal, and it collapses the moment it is examined. Nature 'designed' parasitic wasps to lay eggs inside living caterpillars so their larvae can eat the host from the inside out while it remains conscious. Nature 'designed' bone cancer in children, stillbirth, and the slow neurological disintegration of prion disease. If 'natural' equals 'good,' then every horror in the biological catalogue is morally sanctioned. The naturalistic fallacy—confusing what IS with what OUGHT to be—was identified by David Hume centuries ago. That you deploy it unreflectively does not make it less fallacious; it makes you less rigorous than an 18th-century Scottish philosopher.",
      long: "The appeal to nature commits two simultaneous errors so fundamental that any introductory philosophy course would catch them. First, the naturalistic fallacy: deriving an 'ought' from an 'is.' That reproduction occurs in nature tells us nothing about whether it should occur. Evolution is not a moral agent; it is a blind, headless mechanism that selects exclusively for replication fitness, not for wellbeing, justice, or consent. The organisms that survive are not the happiest or the most ethical—they are the most ruthlessly competitive. Second, the selective application: the interlocutor appeals to nature only for the aspects of biology they wish to defend. Reproduction is 'natural and therefore good,' but when confronted with nature's other products—the parasitoid wasp, the fungus that hijacks ant neural systems, the slow death by predation that constitutes the daily reality of billions of organisms—they suddenly abandon the naturalistic framework. This selective deployment reveals that the appeal to nature is not a principled philosophical position; it is a post-hoc rationalization deployed exclusively to defend the reproductive status quo. The biosphere is not a sanctuary. It is a green slaughterhouse—a terminally closed system operating on blind DNA replication and extreme thermodynamic entropy. To invoke 'nature' as moral authority is to worship the architect of the gladiator war."
    },
    sources: ["Naturalistic fallacy (Hume/Moore)", "Appeal to Nature fallacy", "EFIList critique of biology", "Is-Ought distinction"]
  },
  {
    id: "gods-plan",
    tier: 2,
    category: "Folk Philosophical",
    trigger: "It's God's plan / God wants us to have children / Divine purpose",
    keywords: ["god", "divine", "plan", "purpose", "faith", "spiritual", "creator", "blessing", "scripture", "bible", "pray", "soul", "heaven", "afterlife"],
    psychMechanism: "Theological foundationalism / Terror Management via symbolic immortality / Axiomatic assertion",
    diagnosis: "The interlocutor invokes an unfalsifiable metaphysical authority to circumvent ethical reasoning entirely. The 'God's plan' defense functions as an epistemological circuit-breaker—once invoked, no further argument is required because the authority is definitionally beyond critique. This is the Veritas Terminus deployed as a weapon rather than a destination.",
    responses: {
      short: "A deity who watches parasites devour children from the inside out and classifies this as 'part of the plan' is not a being worthy of moral authority. You have not answered the ethical question—you have outsourced it to an unfalsifiable assertion.",
      medium: "The theological defense collapses under the Problem of Evil, which has remained unanswered for millennia. If God is omniscient, omnipotent, and benevolent, then the existence of gratuitous suffering—children dying of leukemia, parasites consuming hosts alive, the systematic rape of captive animals in factory farms—is logically impossible. Either God cannot prevent suffering (not omnipotent), does not know about it (not omniscient), does not care (not benevolent), or does not exist. Your appeal to divine purpose does not answer the antinatalist objection—it simply relocates the moral responsibility to an entity whose existence is itself an unproven axiom. Furthermore, a God who prioritizes the preservation of 'free will' over the prevention of a child's prolonged, agonizing death has made a value judgment that no competent ethicist would defend.",
      long: "I was raised in a radical Evangelical environment where they claimed to resurrect the dead, remove tumors, and cure diseases through faith. The most 'profound' arguments were always anecdotal—miracles here, divine protection there. My own grandfather survived an IED on a missionary trip and it was attributed to God's protection. But for every 'right place, right time' story, there are thousands of 'wrong place, wrong time' horrors that receive no theological explanation. Either God does not exist—and these are cases of correlation mistaken for causation—or God is the most wicked entity of unfathomable depravity. The Problem of Evil is not a puzzle waiting for a clever theological solution. It is a structural indictment. A deity who constructs a biosphere operating as a gladiator war of consumption, disease, and decay—and then demands worship for it—is not a benevolent creator. That deity is a sadistic narcissist who watches predators assault children while preserving the nebulous concept of 'free will' over the prevention of profound trauma. Religion does not resolve the ethical crisis of procreation. It is the most sophisticated version of the hopium-copium that keeps the brutal gears of nature turning without critical examination. Your faith is an evolutionary coping mechanism—a symbolic immortality project as described by Terror Management Theory—and invoking it does not constitute a philosophical argument. It constitutes a refusal to have one."
    },
    sources: ["Problem of Evil (Epicurus/Hume)", "TMT — symbolic immortality", "Evangelical deconstruction (biographical)", "Theodicy failures"]
  },
  {
    id: "just-edgy",
    tier: 1,
    category: "Emotional/Reflexive",
    trigger: "You're just being edgy / This is teenage nihilism / Grow up",
    keywords: ["edgy", "teenage", "grow up", "phase", "immature", "attention", "cringe", "emo", "tryhard", "wannabe"],
    psychMechanism: "Dismissal via social categorization / TMT distal defense / Age-based authority fallacy",
    diagnosis: "The interlocutor deploys social categorization to avoid engaging the argument entirely. By labeling the position 'edgy' or 'teenage,' they invoke an implicit authority claim: that maturity equals acceptance of the status quo, and that questioning the value of existence is something one 'grows out of.' This conflates social conformity with intellectual development.",
    responses: {
      short: "Schopenhauer was not a teenager. Cioran was not going through a phase. Benatar holds a chair in philosophy at the University of Cape Town. Your dismissal is an age-based authority fallacy dressed as casual contempt. Address the argument.",
      medium: "The 'edgy teenager' dismissal is a social categorization strategy, not a philosophical response. It functions by placing antinatalism in a cultural box marked 'things adolescents say before they mature'—implying that intellectual maturity naturally culminates in acceptance of the biological status quo. This is circular: it assumes the conclusion (that life is good) to invalidate the premise (that life may not be). The actual history of pessimist philosophy spans Schopenhauer, Hartmann, Mainlander, Cioran, Zapffe, Ligotti, and Benatar—none of whom are adolescents, and several of whom produced some of the most rigorous philosophical work in the Western canon. Your categorization tells me nothing about the validity of the asymmetry argument. It tells me everything about your inability to engage with it.",
      long: "The dismissal of antinatalism as 'edgy' or 'immature' performs a very specific psychological function: it allows the interlocutor to avoid engaging with the argument by relocating the debate from philosophy to sociology. Instead of addressing whether the asymmetry of suffering constitutes a valid ethical objection to procreation, the interlocutor categorizes the person making the argument and dismisses them on the basis of their presumed social identity. This is textbook genetic fallacy—evaluating a claim based on its source rather than its content. But it also reveals something deeper: the implicit assumption that intellectual maturity naturally trends toward acceptance of biological existence. This assumption is itself a product of survivorship bias—the people who 'grew out of' questioning existence are the ones who remained alive and vocal. Furthermore, the philosophical lineage of pessimism is older and more rigorous than most optimistic frameworks. Schopenhauer's World as Will and Representation predates most of modern psychology. Peter Wessel Zapffe's 'The Last Messiah' articulated the cognitive mechanisms humans use to suppress existential awareness decades before Terror Management Theory formalized them empirically. Thomas Ligotti's The Conspiracy Against the Human Race synthesizes the entire pessimist tradition into a work that has never been substantively refuted—only dismissed with the exact social categorization you are deploying now. 'Edgy' is not a counterargument. It is a confession that you have nothing else."
    },
    sources: ["Genetic fallacy", "Schopenhauer", "Cioran", "Zapffe — The Last Messiah", "Ligotti — Conspiracy Against the Human Race", "Benatar", "Survivorship bias"]
  },
  {
    id: "meaning-through-suffering",
    tier: 4,
    category: "Genuine Philosophical",
    trigger: "Suffering gives life meaning / What doesn't kill you makes you stronger / Nietzsche / Frankl",
    keywords: ["meaning", "suffering gives meaning", "stronger", "Nietzsche", "Frankl", "purpose through pain", "growth", "resilience", "character", "amor fati"],
    psychMechanism: "Post-hoc rationalization of harm / Stockholm Syndrome with existence / Survivorship bias",
    diagnosis: "This is the most sophisticated emotional defense because it has genuine philosophical credentials (Nietzsche, Frankl, Stoicism). However, it commits a critical error: it retroactively assigns purpose to suffering that was imposed without consent, confusing a coping mechanism (meaning-making) with a justification for the harm itself. Frankl survived Auschwitz and found meaning—but this does not justify the construction of Auschwitz.",
    responses: {
      short: "Meaning-making is a coping mechanism deployed after harm is inflicted, not a justification for inflicting the harm. Viktor Frankl found meaning in Auschwitz. That does not retroactively justify the construction of Auschwitz.",
      medium: "The Nietzsche/Frankl objection confuses two distinct claims: (1) humans can construct meaning from suffering after it occurs, and (2) therefore suffering is justified in advance. The first claim is empirically true—humans are extraordinary meaning-making machines. The second is a non sequitur. Frankl's logotherapy demonstrates that consciousness can find purpose even in extremity. But the capacity to survive and narrativize horror does not retroactively consent to the horror. A kidnapping victim who develops resilience during captivity has not thereby justified the kidnapping. Furthermore, Nietzsche's amor fati requires the affirmation of eternal recurrence—the willingness to live one's exact life infinitely. This is a standard that virtually no honest human being could meet if they genuinely confronted the worst moments of their existence. The doctrine works as aspiration; it fails as ethics.",
      long: "The meaning-through-suffering objection is the most philosophically credentialed defense of existence, drawing on Nietzsche's amor fati, Frankl's logotherapy, and the Stoic tradition. It deserves serious engagement precisely because it does not deny suffering—it attempts to transmute it. However, the transmutation contains a fatal structural flaw. The capacity of consciousness to construct meaning from suffering is a post-hoc psychological adaptation—a survival mechanism, not an ethical justification. When Frankl argues that 'those who have a why to live can bear almost any how,' he is describing human resilience under conditions of extreme duress. He is not arguing that the duress was justified because resilience was possible. The concentration camp survivor who finds meaning has demonstrated extraordinary psychological capacity. But meaning-making after the fact cannot retroactively consent to the conditions that necessitated it. The child who 'grows stronger' after abuse has not validated the abuse. The torture victim who writes a memoir has not justified the torture. To argue otherwise is to commit the most insidious form of victim-blaming: retroactively converting imposed harm into a 'gift' of growth. Nietzsche's eternal recurrence—the test of whether one would willingly relive one's life infinitely—is instructive here precisely because almost no one passes it honestly. Amor fati is an aesthetic posture, not an ethical argument. It says 'love your fate.' It does not say 'impose fate on the unconsenting.' The gap between those two claims is the entire antinatalist argument. Additionally, this objection suffers from catastrophic survivorship bias: we only hear from those who survived their suffering and found meaning. The millions who were destroyed by it—who died in agony, who were psychologically annihilated, who found no meaning whatsoever—are silent. Their silence is not consent."
    },
    sources: ["Nietzsche — Amor Fati / Eternal Recurrence", "Frankl — Man's Search for Meaning", "Stoicism", "Survivorship bias", "Post-hoc rationalization", "Consent impossibility"]
  },
  {
    id: "free-will-defense",
    tier: 4,
    category: "Genuine Philosophical",
    trigger: "Free will justifies suffering / God gave us free will / We choose our path",
    keywords: ["free will", "choice", "freedom", "agency", "choose", "libertarian free will", "compatibilism", "determinism"],
    psychMechanism: "Theological defense / Illusion of agency / Failure to account for unchosen biological constraints",
    diagnosis: "The free will defense attempts to relocate moral responsibility from the creator (parent/God) to the created (child/human). It fails because the entity whose 'free will' is invoked never chose to exist, never chose their neural architecture, never chose their environment, and operates under biological constraints they did not design.",
    responses: {
      short: "You did not choose your genome, your neural architecture, your birthplace, your family, your predispositions, or the fact that you exist at all. What precisely is 'free' about a will that operates entirely within parameters it never selected?",
      medium: "The free will defense fails at the foundational level: the entity exercising 'free will' never consented to the conditions under which that will operates. You did not choose your genome. You did not choose your neurology—the precise arrangement of synapses, neurotransmitter balances, and hormonal cascades that determine your every impulse, mood, and decision. You did not choose your environment, your socioeconomic position, your culture, or your era. You did not choose to exist at all. The 'freedom' being celebrated is the freedom of a prisoner to choose which corner of the cell to sit in. The cell itself was imposed without consent. Furthermore, neuroscience increasingly demonstrates that conscious 'decisions' are preceded by unconscious neural activity—the brain commits to a choice before the conscious mind is aware of having made it. Free will, as typically invoked, may not even exist in the libertarian sense. It is at best a useful fiction; at worst, it is the most elaborate piece of biological propaganda in the history of consciousness.",
      long: "The free will defense operates on three levels, all of which fail. At the theological level, it attempts to absolve God of responsibility for suffering by transferring that responsibility to human agents who 'freely chose' evil. But the humans in question did not choose to exist, did not choose their capacity for evil, did not design the neural architecture that produces violent impulses, and operate within a biosphere whose operational logic is predation and consumption. A God who creates beings predisposed to suffering and violence, places them in an environment that rewards brutality, and then blames them for the outcomes has not respected free will—that God has constructed a rigged experiment. At the philosophical level, libertarian free will—the idea that agents could have done otherwise in exactly the same circumstances—has no empirical support. Libet's experiments and subsequent neuroscientific research consistently demonstrate that motor decisions are initiated unconsciously before the subject reports awareness of deciding. Compatibilism attempts to salvage free will by redefining it as 'acting in accordance with one's desires without external coercion'—but this merely relocates the problem, since the desires themselves are products of unchosen biological and environmental factors. At the ethical level, even granting free will for the sake of argument, it does not address the antinatalist objection. The question is not whether existing beings have agency. The question is whether it is ethical to create a new being—without their consent—and expose them to a world where the exercise of 'free will' includes the possibility of being tortured, developing schizophrenia, or watching their child die of cancer. Free will does not mitigate the proxy gamble. It merely provides the gambler with a rationalization."
    },
    sources: ["Libet — unconscious neural initiation", "Compatibilism vs. Libertarian free will", "Determinism", "Problem of Evil — free will defense", "Proxy Gamble"]
  },
  {
    id: "most-people-happy",
    tier: 2,
    category: "Folk Philosophical",
    trigger: "Most people are happy / Life satisfaction surveys show...",
    keywords: ["happy", "satisfaction", "surveys", "polls", "majority", "most people", "studies show", "wellbeing", "quality of life"],
    psychMechanism: "Optimism Bias applied to self-report / Pollyanna Principle / Adaptation / Survivorship bias",
    diagnosis: "Self-reported life satisfaction is among the most unreliable metrics in psychology. It is contaminated by the optimism bias, adaptation (hedonic treadmill), social desirability bias, and the fundamental inability of consciousness to objectively assess its own wellbeing from within the closed context of experience.",
    responses: {
      short: "Self-reported happiness is a biological metric, not an objective one. The optimism bias ensures humans systematically overestimate their wellbeing. You are citing the prisoner's satisfaction survey as evidence that the prison is good.",
      medium: "Life satisfaction surveys measure the output of a neurological system that has been engineered by natural selection to report positive assessments regardless of objective conditions. The optimism bias ensures systematic overestimation of wellbeing. The hedonic treadmill ensures adaptation to deteriorating conditions. Social desirability bias ensures that respondents report higher satisfaction than they experience. And survivorship bias ensures that the people answering the survey are precisely those whose circumstances did not kill them or render them incapable of responding. The millions in chronic agony, the suicides, the infants who died before they could form opinions—they are not in your dataset. Furthermore, Benatar argues extensively that these psychological traits—not the objective quality of life—explain the falsely positive assessments people make regarding their own existence. Humanity is biologically programmed to view its captivity favorably.",
      long: "The appeal to life satisfaction surveys commits several compounding methodological and philosophical errors. First, self-report reliability: conscious beings cannot assess their own wellbeing from outside the closed context of their experience. The assessment tool (the brain) is the same instrument that generates the experience being assessed—and that instrument has been calibrated by natural selection to produce positive reports as a survival mechanism. Second, the hedonic treadmill: humans adapt to virtually any baseline condition, both positive and negative. A paraplegic reports similar life satisfaction to a lottery winner within 18 months. This does not mean paraplegia and winning the lottery are equivalent experiences—it means the self-report mechanism is fundamentally miscalibrated for objective assessment. Third, survivorship bias: satisfaction surveys only capture the living and responsive. The stillborn, the suicides, the people in vegetative states, the children who died of preventable diseases in the developing world, the billions of non-human animals in factory farms—none of them contributed to your dataset. Fourth, social desirability bias: humans systematically overreport positive states in social contexts. Admitting unhappiness carries social costs—it invites pathologization, concern, and unwanted intervention. Many respondents report satisfaction as a social performance rather than an authentic assessment. Fifth, the most devastating point: even if the surveys were perfectly accurate and 90% of humans genuinely experienced net-positive lives, the antinatalist position would still hold. Because procreation is a proxy gamble, and the 10% who suffer catastrophically never consented to the wager. You do not get to gamble with someone else's welfare and then point to the winners as justification for the losers."
    },
    sources: ["Benatar — quality of life assessment critique", "Hedonic treadmill / adaptation", "Optimism Bias (Sharot)", "Survivorship bias", "Social desirability bias", "Self-report reliability"]
  },
  {
    id: "love-beauty-art",
    tier: 2,
    category: "Folk Philosophical",
    trigger: "What about love? / Art? / Music? / The beauty of human experience?",
    keywords: ["love", "beauty", "art", "music", "joy", "wonder", "connection", "friendship", "creativity", "experience"],
    psychMechanism: "Cherry-picking positive valence experiences / Ignoring the asymmetry / Romanticism as deflection",
    diagnosis: "The interlocutor selects peak positive experiences and presents them as representative of the totality of existence. This is the Pollyanna Principle in its most seductive form—curating the highlight reel while the full footage includes torture, disease, grief, and the guaranteed termination of every experience through death.",
    responses: {
      short: "Love ends in grief or abandonment. Beauty fades. Art is produced by beings in agony. None of these retroactively justify the imposition of existence on an unconsenting entity—they are consolation prizes distributed inside a prison.",
      medium: "You are curating the highlight reel. Love is accompanied by loss—every attachment terminates in grief, abandonment, or death. Art is overwhelmingly produced by beings in psychological distress; the correlation between creative output and mental illness is well-documented. Beauty is a neurochemical response calibrated by evolution to reward behaviors that increase reproductive fitness—it is not an objective property of the world. And all of these experiences are temporary, unreliable, and ultimately annihilated by death. The question is not whether pleasant experiences exist. The question is whether their existence justifies imposing the full spectrum of suffering—including its worst extremes—on an unconsenting entity. One drop of poison taints the well. The worst things that happen in this world—torture, starvation, psychological annihilation—are structural guarantees, not statistical outliers. No quantity of art retroactively erases a single instance of a child dying of bone cancer.",
      long: "The appeal to love, beauty, and art is the Pollyanna Principle in its most culturally sophisticated form. It selects the peak positive valence experiences from the human catalogue and presents them as though they constitute the dominant texture of existence. They do not. Love is a neurochemical bonding mechanism that evolved to facilitate pair-bonding for offspring survival. It is biochemically indistinguishable from obsessive-compulsive disorder in its acute phase. Every loving attachment terminates in one of three ways: abandonment, betrayal, or the death of one partner—forcing the survivor into grief, which is among the most devastating psychological experiences available to consciousness. Beauty is a pattern-recognition response calibrated by natural selection. Symmetrical faces signal genetic health. Landscapes that signal resource availability trigger aesthetic pleasure. The sunset is not objectively beautiful—your neurology has been engineered to find it rewarding because ancestors who found safe, resource-rich environments pleasing survived to reproduce. Art, meanwhile, is overwhelmingly the product of suffering. The canon of human creative achievement is written by the traumatized, the mentally ill, the grieving, and the alienated. To celebrate art as justification for existence is to celebrate the symptom while defending the disease. But the most fundamental failure of this objection is structural: even if love, beauty, and art were as wonderful as the romanticist claims, they cannot retroactively consent for the being who was forced into existence to experience them. The child who develops leukemia at age four does not benefit from the fact that Beethoven composed the Ninth Symphony. Positive experiences are distributed unequally, unreliably, and temporarily across a population that was never asked whether it wanted to participate. The good does not cancel the bad. It never did."
    },
    sources: ["Pollyanna Principle", "Asymmetry — good does not cancel bad", "Neuroscience of love/beauty", "Art and mental illness correlation", "Proxy Gamble"]
  },
  {
    id: "procreative-liberty",
    tier: 4,
    category: "Genuine Philosophical",
    trigger: "Reproductive freedom is a human right / Procreative liberty",
    keywords: ["reproductive rights", "freedom", "liberty", "human right", "bodily autonomy", "choice to have children", "reproductive freedom"],
    psychMechanism: "Rights-based framework deployed without accounting for the rights of the created entity",
    diagnosis: "This is a genuine philosophical challenge because procreative liberty is a recognized legal and ethical principle in most liberal democracies. The response must demonstrate that the right to reproduce, like all rights, is bounded by the harm it imposes on others—and in this case, the 'other' is the created entity who bears 100% of the existential risk.",
    responses: {
      short: "Every right is bounded by the harm it imposes on others. Your right to swing your fist ends at someone else's face. Your right to reproduce ends at the creation of a being who never consented to the risks you imposed.",
      medium: "Procreative liberty is a negative right—the right to be free from state interference in reproductive decisions. It does not entail a positive right to create sentient beings regardless of consequences. Every recognized right in liberal ethics is bounded by the Harm Principle: your liberty extends precisely to the point where it imposes non-consensual harm on another. Procreation creates a new entity and immediately exposes it to the full spectrum of suffering, disease, and inevitable death. The created being did not consent to this exposure. If we applied the same ethical standards to procreation that we apply to every other act of risk-imposition—medical experimentation, hazardous labor, even organ donation—the act would require informed consent from the affected party. Since informed consent from the unborn is structurally impossible, the ethical default should be restraint, not imposition.",
      long: "The procreative liberty defense is the most legally grounded objection to antinatalism because reproductive freedom is enshrined in international human rights frameworks. However, the defense confuses a legal right with an ethical justification. Legally, one may have the right to reproduce. Ethically, the question is whether exercising that right imposes unjustifiable harm on a third party. John Stuart Mill's Harm Principle—the foundation of liberal ethics—holds that individual liberty is sacrosanct only insofar as it does not cause harm to others. Procreation creates a new 'other' and immediately subjects that entity to the following guaranteed harms: vulnerability to disease, psychological suffering, the experience of loss, the awareness of mortality, and eventual death. These are not risks—they are certainties. The only variable is degree. No other act that imposes this magnitude of certain harm on a non-consenting entity is considered ethically permissible. Medical experimentation on non-consenting subjects is prohibited under the Nuremberg Code. Hazardous working conditions without informed consent constitute criminal negligence. Even organ donation from a living donor requires explicit, informed consent. Procreation alone is exempted from the consent requirement—not because the ethics justify the exemption, but because the biological imperative refuses to permit the question. The 'right' to reproduce is the right to gamble with someone else's welfare. Framing it as 'liberty' does not change the structure of the act."
    },
    sources: ["Mill — Harm Principle", "Procreative liberty (Robertson)", "Nuremberg Code — consent in medical ethics", "Negative vs. positive rights", "Benatar — consent impossibility"]
  },
  {
    id: "negative-util-aggregation",
    tier: 4,
    category: "Genuine Philosophical",
    trigger: "Negative utilitarianism leads to absurd conclusions / The repugnant conclusion",
    keywords: ["aggregation", "repugnant conclusion", "absurd", "utility monster", "negative utilitarianism leads to", "logical conclusion", "reductio"],
    psychMechanism: "Genuine philosophical engagement — reductio ad absurdum of negative utilitarian premises",
    diagnosis: "This is a technically sophisticated objection. Critics argue that strict negative utilitarianism, taken to its logical conclusion, would justify destroying the world to prevent a single headache. This is the 'utility monster' problem applied to suffering-minimization. The response must acknowledge the force of the reductio while defending the framework.",
    responses: {
      short: "Negative utilitarianism does not demand the elimination of all suffering at any cost. It demands that unconsented suffering not be imposed on new entities who did not ask to exist. The reductio attacks a strawman version of the position.",
      medium: "The reductio assumes that negative utilitarianism operates as a simple maximization algorithm: minimize suffering at any cost, including the destruction of beings who prefer to continue existing. This is a strawman. The sophisticated negative utilitarian position—particularly as deployed within EFILism—does not advocate for the forced termination of existing life. It advocates for the cessation of new life-creation, on the grounds that non-existent entities cannot be harmed by their non-existence, whereas created entities are guaranteed to suffer. The 'destroy the world to prevent a headache' scenario violates the consent principle that is central to the framework. Forced extinction causes massive suffering to existing beings—which is precisely what the philosophy opposes. The coherent EFIList position is not 'kill everyone now' but 'stop creating new victims.'",
      long: "The aggregation critique is the strongest technical objection to negative utilitarianism, and it deserves a careful response. The reductio typically runs as follows: if the sole ethical imperative is the minimization of suffering, then a world with zero suffering is maximally good, and any action that achieves zero suffering—including the instantaneous painless annihilation of all life—is morally required, regardless of how many beings with positive experiences are destroyed. This is the 'repugnant conclusion' in reverse. The response operates on two levels. First, the consent constraint: EFILism and antinatalism do not operate on pure aggregative negative utilitarianism. They operate on a consent-bounded framework. The destruction of existing beings who prefer to continue living violates their preferences and creates massive suffering in the process—which contradicts the foundational principle. The 'red button' thought experiment specifies painless, instantaneous extinction precisely to isolate the theoretical question from the practical violence. In the real world, no such mechanism exists, and therefore the theory does not prescribe forced extinction of existing populations. Second, the asymmetric application: the negative utilitarian framework applies most forcefully to the creation of new life, not the termination of existing life. Creating a new being imposes guaranteed suffering on an entity that had no prior preference for existence. Declining to create that being harms no one—there is no victim. This asymmetry is the engine of the entire position. The reductio works only if you ignore it and treat negative utilitarianism as a context-free algorithm rather than a consent-sensitive ethical framework. The sophisticated position is: stop creating new victims. Allow the existing population to live out their lives according to their preferences. When the last sentient being dies naturally, the ethical project is complete."
    },
    sources: ["Negative utilitarianism — aggregation problem", "Repugnant Conclusion (Parfit)", "Consent-bounded framework", "Red Button thought experiment", "EFIList vs. pure NU distinction"]
  },
  {
    id: "western-philosophy",
    tier: 2,
    category: "Folk Philosophical",
    trigger: "This is just Western philosophy / Cultural imperialism / Other cultures value life",
    keywords: ["western", "cultural", "imperialism", "other cultures", "ethnocentric", "privilege", "first world", "colonial"],
    psychMechanism: "Genetic fallacy applied to cultural origin / Relativism as deflection",
    diagnosis: "The interlocutor attempts to invalidate the philosophical framework by locating it within a specific cultural tradition, implying that its conclusions are merely local opinions rather than universal claims. This commits the genetic fallacy and ignores that pessimist traditions exist across virtually every culture.",
    responses: {
      short: "Buddhism identifies existence as dukkha—suffering—and prescribes the cessation of the cycle of rebirth. Jainism's ahimsa extends non-harm to all sentient beings. The pessimist tradition is not Western—it is global. Your objection is geographically illiterate.",
      medium: "The claim that antinatalism is a Western cultural artifact is empirically false. Buddhism—originating in South Asia—identifies existence as fundamentally characterized by dukkha (suffering, dissatisfaction, impermanence) and prescribes the cessation of the cycle of rebirth as the highest spiritual goal. Jainism extends the principle of ahimsa to all sentient life with a rigor that exceeds most Western ethical frameworks. Hindu philosophy includes the concept of moksha—liberation from the cycle of samsara. These are not fringe positions within these traditions—they are central doctrines practiced by billions. Furthermore, the suffering that antinatalism addresses—disease, predation, aging, death—is not culturally specific. A child dying of malaria in sub-Saharan Africa suffers no differently than a child dying of leukemia in Berlin. The biology of pain is universal. The philosophy that addresses it need not be parochial.",
      long: "The cultural imperialism objection commits a double error. First, the genetic fallacy: the geographic or cultural origin of a philosophical position has no bearing on its truth-value. The Pythagorean theorem originated in a specific cultural context; it applies universally. Likewise, the asymmetry of suffering—the observation that the absence of pain is good while the absence of pleasure is not bad for the non-existent—is a logical structure, not a cultural opinion. Second, the empirical error: pessimist and anti-life traditions are not Western. Buddhism's First Noble Truth—that existence is characterized by dukkha—is a structural diagnosis of sentient experience that aligns directly with negative utilitarian analysis. The Buddhist prescription to end the cycle of rebirth through the cessation of craving (tanha) is functionally analogous to the antinatalist prescription to end the cycle of suffering through the cessation of procreation. Jainism's radical non-violence (ahimsa) extends to the protection of insects and microorganisms—a scope of ethical concern that surpasses most Western animal rights frameworks. The Hindu concept of samsara frames existence as a cycle of suffering from which liberation (moksha) is the highest goal. Even within Western philosophy, pessimism is not a modern invention—Ecclesiastes declares that the dead are happier than the living, and those never born are happier than both. The Cyrenaic philosopher Hegesias, known as 'the Death-Persuader,' argued in the 3rd century BCE that life's pleasures are insufficient to outweigh its pains. To frame antinatalism as a Western cultural artifact is to reveal profound ignorance of both Western and non-Western philosophical traditions."
    },
    sources: ["Buddhism — dukkha / Four Noble Truths", "Jainism — ahimsa", "Hindu — samsara / moksha", "Ecclesiastes 4:2-3", "Hegesias of Cyrene", "Genetic fallacy"]
  },
  {
    id: "antinatalism-misanthropic",
    tier: 1,
    category: "Emotional/Reflexive",
    trigger: "You just hate people / This is misanthropy / You're a sociopath",
    keywords: ["hate people", "misanthropic", "misanthropy", "sociopath", "psychopath", "hateful", "cruel", "cold", "heartless"],
    psychMechanism: "Inversion of care — confusing compassion-driven critique with contempt",
    diagnosis: "This objection inverts the actual motivational structure of antinatalism. The philosophy is driven by extreme empathy—specifically, empathy for the suffering of those who cannot consent to existence. The interlocutor cannot process that a position advocating for the prevention of suffering could be motivated by anything other than hatred, because their own framework equates 'pro-life' with 'compassionate.'",
    responses: {
      short: "Antinatalism is predicated on compassion so extreme it extends to entities that do not yet exist. I do not want to prevent suffering because I hate people. I want to prevent suffering because I understand what it means to endure it.",
      medium: "The misanthropy accusation inverts the motivational structure entirely. Antinatalism originates in extreme empathy—the recognition that creating a new sentient being exposes that being to guaranteed suffering without their consent. This is not hatred of the existing; it is protection of the not-yet-existing. The person who refuses to bring a child into a world containing bone cancer, psychological torture, and inevitable death is exercising more care for that potential child than the person who creates it and hopes for the best. Your framework equates 'wanting more humans to exist' with 'compassion.' But compassion measured by its willingness to impose risk on the unconsenting is not compassion. It is narcissism wearing empathy's costume.",
      long: "The accusation of misanthropy reveals a fundamental misunderstanding of the philosophy's motivational architecture. EFILism and antinatalism are rooted in what might be called hyper-empathy—an empathic response so intense that it extends beyond existing beings to encompass potential beings who might be brought into existence. The antinatalist who declines to reproduce is not expressing contempt for humanity; they are expressing the deepest possible concern for the welfare of a being who would be forced to navigate a world saturated with suffering. This concern is indistinguishable from hatred only if you define 'love' as 'willingness to create new beings regardless of consequences.' However, I will not sanitize this: the philosophy does include a robust critique of humanity's collective behavior. A species that has produced industrialized genocide, factory farming, systemic child abuse, and the destruction of every ecosystem it has touched warrants structural criticism. But structural criticism of a species is not the same as hatred of individuals—any more than criticizing the design of a building constitutes hatred of its occupants. The building is badly designed. The occupants are suffering inside it. The antinatalist says: stop building more of these. The natalist says: but the lobby is beautiful. The distinction between these positions is the distinction between empathy and aesthetics."
    },
    sources: ["EFIList empathy framework", "Hyper-empathy", "Compassion vs. narcissism", "Structural critique vs. personal hatred"]
  },
  {
    id: "speak-for-everyone",
    tier: 2,
    category: "Folk Philosophical",
    trigger: "You can't speak for everyone / Some people love their lives / Not everyone agrees",
    keywords: ["speak for everyone", "my life is great", "I love life", "not everyone", "some people", "individual experience", "subjective"],
    psychMechanism: "Anecdotal evidence / Sample-of-one reasoning / Failure to grasp structural argument",
    diagnosis: "The interlocutor treats antinatalism as a claim about individual life quality ('your life is bad') rather than a structural claim about the ethics of imposing existence ('no one can consent to being born'). The response to 'my life is great' is not 'no it isn't'—it is 'that is irrelevant to the consent question.'",
    responses: {
      short: "The argument is not that your life is bad. The argument is that you imposed existence on no one, and no one should impose it on a new being who cannot consent to the risks involved. Your personal satisfaction is irrelevant to the consent question.",
      medium: "This objection confuses a structural ethical claim with an empirical claim about individual wellbeing. Antinatalism does not assert that every individual life is subjectively negative. It asserts that the act of creating a new sentient being—without that being's consent—is ethically unjustifiable because the created being is guaranteed to experience some degree of suffering and is guaranteed to die. Your personal positive assessment of your own life does not address this argument any more than a lottery winner's satisfaction addresses the ethics of forcing people to play the lottery. The question is not 'are some lives good?' The question is 'is it ethical to gamble with someone else's welfare when the stakes include bone cancer, psychological annihilation, and death?' Your anecdote answers the first question. The second question remains untouched.",
      long: "The individualist objection commits three errors simultaneously. First, it treats a structural argument as a personal one. Antinatalism is not the claim 'your life is bad.' It is the claim 'the creation of new sentient life without consent is ethically impermissible given the guaranteed presence of suffering and death.' Whether any specific individual assesses their life positively is orthogonal to this claim. Second, it deploys anecdotal evidence against a probabilistic argument. The antinatalist does not need to prove that every life is net-negative. The antinatalist needs only to demonstrate that procreation imposes non-trivial risks of catastrophic suffering on an entity that cannot consent to those risks. The existence of lottery winners does not justify forced participation in the lottery. Third, it ignores the asymmetry of self-assessment. As discussed in the context of life satisfaction surveys, self-reported wellbeing is contaminated by optimism bias, hedonic adaptation, social desirability bias, and the closed-context problem (consciousness cannot assess itself from outside itself). The prisoner who reports satisfaction with prison conditions has not thereby justified incarceration—they have demonstrated the adaptive capacity of the human nervous system under imposed constraints. Your positive life assessment may be accurate. It may also be the predictable output of a neurological system designed by evolution to report positive assessments regardless of objective conditions. Either way, it does not address the consent question, the asymmetry of harm, or the structural guarantees of suffering and death that attend every act of creation."
    },
    sources: ["Structural vs. individual claims", "Lottery analogy", "Anecdotal evidence fallacy", "Consent framework", "Closed context problem"]
  },
  {
    id: "evolution-purpose",
    tier: 2,
    category: "Folk Philosophical",
    trigger: "Evolution gave us purpose / We evolved for a reason / Species survival matters",
    keywords: ["evolution", "evolved", "species survival", "purpose", "progress", "advancement", "higher", "pinnacle"],
    psychMechanism: "Teleological projection onto non-teleological process / Appeal to Nature variant",
    diagnosis: "The interlocutor projects intentionality and purpose onto a process that possesses neither. Evolution is not directed, not progressive, and not moral. It is a blind algorithm that selects for replication fitness. Assigning 'purpose' to evolution is animism applied to biology.",
    responses: {
      short: "Evolution has no purpose. It has no direction. It selects exclusively for whatever replicates. Tapeworms are as evolutionarily 'successful' as humans. You are projecting narrative onto a blind algorithm.",
      medium: "Evolution is not a progression toward complexity, consciousness, or purpose. It is a blind, non-directed process that selects exclusively for reproductive fitness in a given environment. Tapeworms, malaria parasites, and bacterial biofilms are as evolutionarily 'successful' as homo sapiens. The projection of purpose onto evolution is a form of animism—attributing intentionality to a process that possesses none. Furthermore, even if evolution had produced consciousness 'for a reason,' this would not constitute an ethical justification for continuing the process. A factory that produces both useful products and toxic waste does not justify its continued operation by pointing to the useful products while ignoring the waste. The 'useful product' of human consciousness comes bundled with the 'toxic waste' of suffering, disease, predation, and death—and the factory operates without consent from the products it creates.",
      long: "The teleological interpretation of evolution commits one of the most persistent errors in popular science: the assumption that natural selection operates toward a goal. It does not. Evolution is a blind algorithm operating on random genetic variation and environmental selection pressure. It has no blueprint, no executive vision, and no concept of progress. The organisms that exist are not the 'best' organisms—they are the organisms whose ancestors happened to survive long enough to replicate in a specific environment. Cockroaches have survived for 300 million years. Humans have existed for roughly 300,000. By the metric of evolutionary persistence, cockroaches are vastly more 'successful.' The projection of purpose onto this process is anthropocentric mythology—the species that happened to develop the cognitive capacity for narrative has, predictably, written itself into the starring role. This is the same species that spent millennia believing the sun orbited the Earth, that the cosmos was created for its benefit, and that its existence was divinely ordained. The teleological reading of evolution is merely the latest chapter in this narcissistic saga. Furthermore, even granting purpose for the sake of argument: 'purpose' does not equal 'ethical justification.' If the purpose of evolution is the replication of DNA, then evolution's purpose is served equally well by the parasitoid wasp as by the philosopher. The system makes no distinction between the consciousness that writes symphonies and the parasite that eats brains. Both replicate. Both fulfill the 'purpose.' To celebrate evolution as meaningful is to celebrate a system whose operational logic is indistinguishable from a factory farm's."
    },
    sources: ["Non-teleological evolution", "Appeal to Nature variant", "Anthropocentric projection", "Evolutionary 'success' — replication fitness only"]
  },
  {
    id: "future-solve",
    tier: 3,
    category: "Structural/Pragmatic",
    trigger: "Future generations will solve our problems / Technology will fix everything",
    keywords: ["future", "solve", "technology", "progress", "better world", "improve", "getting better", "innovation", "advancement"],
    psychMechanism: "Optimism Bias projected forward in time / Deferral of ethical responsibility",
    diagnosis: "The interlocutor defers the ethical question to a hypothetical future in which suffering has been solved, thereby justifying the creation of beings who will suffer NOW in the hope that their descendants might not. This is the proxy gamble extended across generations.",
    responses: {
      short: "You are creating suffering beings now on the speculative promise that future beings might suffer less. The people who exist during the 'improvement period' never consented to serve as transitional sacrifices in your optimistic experiment.",
      medium: "This objection converts speculative future improvement into a justification for present suffering. The beings created today bear 100% of the existential risk of current conditions—disease, economic exploitation, environmental collapse, psychological suffering, inevitable death. They did not consent to serve as stepping stones toward a hypothetical utopia that may never arrive. Furthermore, every generation in human history has been told that the future would be better. Every generation has served as the transitional sacrifice for the next. The promise of future improvement is the oldest and most effective mechanism for manufacturing consent to present suffering. It is the carrot that justifies the stick—and the carrot is always receding. Meanwhile, the stick is structural and guaranteed.",
      long: "The 'future will solve it' objection is the temporal version of the proxy gamble—imposing suffering on present beings based on the speculative hope that future beings will benefit. This deferral mechanism has operated continuously throughout human history. Every generation has been told: your suffering is meaningful because it contributes to progress. Your children will have it better. The arc bends toward justice. And every generation has suffered regardless. The promise of future improvement serves a precise psychological function: it transforms present misery into a narrative of purpose. If your suffering is a stepping stone toward a better world, then your suffering is meaningful—which activates the meaning-making apparatus and suppresses the recognition that the suffering was imposed without consent. But the people alive during the 'improvement period'—which is always now, and always projected to end tomorrow—never agreed to this arrangement. They were created, without consent, into conditions that include bone cancer and existential dread, on the speculative promise that their great-grandchildren might live in a world with marginally less bone cancer. Furthermore, the empirical record does not support the narrative of inevitable improvement. Technology has amplified human capacity for both wellbeing and destruction. The same century that produced antibiotics produced nuclear weapons, industrialized factory farming, and surveillance states. The same technology that might 'solve suffering' is equally capable of producing novel forms of suffering that no previous generation could have imagined. Progress is not directional. It is a lateral expansion of capacity—for good and for harm simultaneously."
    },
    sources: ["Temporal proxy gamble", "Historical deferral of ethics", "Progress narrative critique", "Technology — dual capacity for wellbeing and destruction"]
  },
  {
    id: "extinction-culture",
    tier: 3,
    category: "Structural/Pragmatic",
    trigger: "Antinatalism leads to extinction of culture / knowledge / art / civilization",
    keywords: ["culture", "knowledge", "civilization", "art dies", "legacy", "heritage", "history", "achievements", "human accomplishment"],
    psychMechanism: "Terror Management — symbolic immortality through cultural legacy / Status Quo Bias",
    diagnosis: "The interlocutor argues that the cessation of reproduction would destroy the accumulated cultural achievements of humanity—art, science, philosophy, literature. This is TMT operating at the civilizational level: the cultural legacy IS the symbolic immortality project. The response must acknowledge the genuine loss while demonstrating that it does not override the consent objection.",
    responses: {
      short: "Culture is a consolation prize created by beings in agony. Its destruction through voluntary extinction harms no one—because there would be no one remaining to be deprived of it. You are mourning the loss of a hospital's décor while ignoring the patients.",
      medium: "The cultural extinction objection reveals its own priorities when stated plainly: we must continue manufacturing new sentient beings—exposing them to disease, suffering, and death—so that paintings can have audiences and symphonies can have listeners. This subordinates the welfare of actual conscious beings to the preservation of artifacts. Culture does not suffer when it ceases to be observed. A painting in an empty gallery experiences nothing. A symphony unheard endures no loss. Only the beings created to appreciate these things suffer—and they suffer not because culture exists, but because they were forced into a biological architecture that guarantees suffering alongside aesthetic experience. Furthermore, culture is overwhelmingly the product of suffering. The canon of human achievement was written by the traumatized, the alienated, the mentally ill, and the dying. To demand the continuation of suffering so that its byproducts can be appreciated is to defend the disease for the beauty of its symptoms.",
      long: "The cultural legacy objection is Terror Management Theory operating at the civilizational scale. Just as individual procreation serves as a biological immortality project—passing genetic material to the next generation—cultural production serves as a symbolic immortality project—embedding one's consciousness in artifacts that outlast the physical body. The fear that antinatalism would destroy 'everything humanity has built' is the fear of symbolic death applied to the species as a whole. But the objection collapses under scrutiny at three levels. First, ontologically: culture does not possess subjective experience. The Mona Lisa does not suffer if no one observes it. Beethoven's Ninth does not experience deprivation if no ear receives it. The 'loss' of culture through voluntary extinction is a loss only from the perspective of beings who already exist and have developed attachments to cultural objects. Once no beings exist, there is no perspective from which the loss registers. The absence of culture is not bad for the non-existent, for the same structural reason that the absence of pleasure is not bad for the non-existent. Second, ethically: the preservation of culture cannot override the consent objection. You are arguing that new sentient beings must be manufactured—and forced to endure the full spectrum of biological suffering—so that galleries have visitors and concert halls have audiences. This instrumentalizes conscious beings as culture-consumption units. Third, empirically: the vast majority of human cultural production is already lost. Entire civilizations—their languages, philosophies, artistic traditions—have vanished completely. The Library of Alexandria burned. The oral traditions of thousands of indigenous cultures were extinguished by colonialism. If the loss of culture is the paramount concern, humanity has already failed catastrophically on its own terms. The antinatalist merely proposes that the final loss occur without generating additional victims to mourn it."
    },
    sources: ["TMT — symbolic immortality at civilizational level", "Cultural artifacts lack subjective experience", "Instrumentalization objection", "Historical cultural loss"]
  },
  {
    id: "playing-god",
    tier: 2,
    category: "Folk Philosophical",
    trigger: "You're playing God / Who are you to decide? / That's not your call",
    keywords: ["playing god", "who are you", "not your call", "who decides", "arrogant", "hubris", "presume"],
    psychMechanism: "Authority deflection / Inverted hubris accusation / Status Quo as neutral default",
    diagnosis: "The interlocutor frames the antinatalist as exercising unilateral power over existence, when in reality the natalist is the one exercising that power. Creating a new being is the supreme act of unilateral decision-making. Declining to create a being is the absence of that act. The accusation of 'playing God' applies precisely to the person who creates life, not the person who refrains.",
    responses: {
      short: "The person 'playing God' is the one who creates a new conscious being and forces it into a world it never chose. The person who refrains from that act is playing nothing. Inaction requires no authority.",
      medium: "This objection perfectly inverts the actual power dynamics. Procreation is the most consequential unilateral decision one entity can make regarding another: it instantiates a new consciousness, assigns it a genome it did not choose, embeds it in an environment it did not select, and guarantees it will suffer and die. This is the act that requires justification. This is the act that 'plays God.' Declining to create a being requires no authority, no hubris, and no decision-making power over another entity—because the entity in question does not exist. You cannot exercise power over the non-existent. The 'who are you to decide' framing only works if you ignore the asymmetry: the person who creates life makes a decision that affects another being profoundly. The person who does not create life makes a decision that affects no one.",
      long: "The 'playing God' accusation commits a breathtaking inversion. To understand why, consider the two positions clearly. The natalist position: I will create a new conscious being. I will determine its genome through my genetic contribution. I will assign it a socioeconomic starting position, a geographic location, a family structure, and a historical era. I will expose it to the guaranteed certainties of suffering, disease, and death. I will do all of this without the being's consent, because its consent is structurally impossible. I will then declare this act to be 'natural,' 'beautiful,' and 'a gift.' The antinatalist position: I will refrain from doing any of that. Now—which of these two positions 'plays God'? The person who creates a sentient being from nothing, assigns it the parameters of its existence, and subjects it to a world it never chose is exercising the most extreme form of unilateral power available to any agent in the known universe. The person who declines to exercise that power is doing precisely nothing. The accusation of hubris is correctly directed at the creator, not the abstainer. Furthermore, the framing of 'who are you to decide' presupposes that the default state is procreation—that reproduction is neutral and only non-reproduction requires justification. This is Status Quo Bias in its purest form. In reality, the default state of the universe is non-existence. Every act of creation is a deviation from the default. The burden of justification falls on the person who deviates—not on the person who maintains the default."
    },
    sources: ["Inverted hubris", "Status Quo as false neutral", "Unilateral power dynamics of creation", "Default state — non-existence"]
  },
  {
    id: "policy-proposal",
    tier: 3,
    category: "Structural/Pragmatic",
    trigger: "What's your actual policy proposal? / What do you want to DO about it?",
    keywords: ["policy", "proposal", "practical", "what do you want", "real world", "implement", "action", "solution", "do about it"],
    psychMechanism: "Pragmatic deflection — substituting 'how' for 'whether' / Action bias",
    diagnosis: "The interlocutor demands a practical implementation plan as a condition for engaging with the philosophical premise. This substitutes the question of 'whether the argument is sound' with 'how would you enact it'—which is a category error. A philosophical argument's validity is independent of its implementability. However, this objection is practically useful and deserves a substantive response.",
    responses: {
      short: "The argument's validity does not depend on a policy proposal. But since you ask: universal access to contraception, comprehensive sex education, removal of pro-natalist economic incentives, normalization of voluntary childlessness, and investment in AI and automation to decouple economic survival from population growth.",
      medium: "This objection conflates philosophical validity with political feasibility. The asymmetry of suffering is either logically sound or it is not—regardless of whether any government would enact antinatalist policy. That said, the practical implications are not extreme: universal access to contraception and reproductive healthcare, comprehensive evidence-based sex education, removal of pro-natalist tax incentives and social pressures, normalization of voluntary childlessness as a legitimate life choice, robust social safety nets that decouple economic security from population growth, and investment in automation and AI to reduce dependency on human labor. None of these proposals require coercion. All of them reduce suffering. The fact that they are politically difficult does not make the underlying philosophy wrong—it makes the political landscape hostile to its own stated values of consent and harm reduction.",
      long: "The demand for a 'policy proposal' is a rhetorical strategy that substitutes implementability for validity. If I prove that factory farming causes immense suffering, the response 'but what's your policy proposal for feeding 8 billion people without it?' does not invalidate the ethical argument. It merely highlights the gap between recognizing a moral problem and solving a logistical one. That said, antinatalism and EFILism do have practical implications, and they are far less radical than critics imagine. First, the immediate, non-coercive measures: universal access to contraception and abortion, which the WHO already advocates. Comprehensive sex education that includes honest discussion of the responsibilities and risks of parenthood. Removal of pro-natalist economic incentives—tax breaks for children, cultural glorification of large families, religious pressure to reproduce. Normalization of voluntary childlessness as a valid, even admirable, life choice rather than a pathology. Second, the structural measures: robust universal basic income and social safety nets that decouple individual economic survival from population growth. Investment in automation, AI, and robotics to reduce dependency on human labor, thereby eliminating the 'we need more workers' argument. Third, the long-term philosophical project: the creation and dissemination of rigorous, well-articulated pessimist and antinatalist philosophy through educational institutions, media, and public discourse—precisely what this argument library is designed to support. The goal is not forced sterilization. The goal is informed consent. If every potential parent genuinely understood the asymmetry of harm, the impossibility of consent, the proxy gamble, and the structural guarantees of suffering—and still chose to reproduce—that would at least be an informed decision rather than an instinctive one. The suspicion is that genuine informed consent would dramatically reduce the birth rate without any coercion whatsoever."
    },
    sources: ["Philosophical validity vs. political feasibility", "Non-coercive antinatalist policy", "Universal contraception access", "UBI and automation", "Informed consent model"]
  },
  {
    id: "next-person-cure-cancer",
    tier: 1,
    category: "Emotional/Reflexive",
    trigger: "What if the next person born cures cancer? / What if you prevented a genius?",
    keywords: ["cure cancer", "genius", "next Einstein", "savior", "what if", "potential", "could be great", "special"],
    psychMechanism: "Speculative positive outcome used to justify guaranteed negative exposure / Lottery fallacy",
    diagnosis: "The interlocutor invokes the speculative possibility of an extraordinary positive outcome to justify the creation of a being who is guaranteed to suffer. This is the lottery fallacy: defending forced participation in a gamble by pointing to the jackpot while ignoring the structural odds.",
    responses: {
      short: "What if the next person born is the next cancer patient? The next torture victim? The next child who dies at age three? You are citing the jackpot to justify forced participation in a lottery where most tickets pay out in suffering.",
      medium: "This objection is pure speculation deployed against structural certainty. The probability that any given child will 'cure cancer' is astronomically low. The probability that they will suffer—experience pain, loss, fear, illness, and death—is 100%. You are justifying the guaranteed exposure of a non-consenting being to the full spectrum of suffering on the basis of an infinitesimally unlikely positive outcome. Furthermore, the objection works in both directions with devastating symmetry: what if the next person born is the next mass shooter? The next tyrant? The next person who develops a biological weapon? If speculative positive potential justifies creation, then speculative negative potential condemns it equally. You cannot invoke the lottery's jackpot without acknowledging the lottery's losses. And the losses are guaranteed; the jackpot is fantasy.",
      long: "The 'next Einstein' objection is the lottery fallacy applied to procreation, and it collapses under even cursory examination. First, the statistical reality: approximately 140 million children are born each year. The number who make paradigm-shifting contributions to human knowledge is, in any given generation, countable on one hand. The probability that any specific child will 'cure cancer' is so vanishingly small that invoking it as justification for creation is like defending a casino that causes widespread financial ruin because one patron once hit the jackpot. Second, the symmetry problem: if the speculative possibility of extraordinary positive outcomes justifies creation, then the speculative possibility of extraordinary negative outcomes condemns it equally. What if the next person born is the next perpetrator of genocide? The next person to develop a novel biological weapon? The next serial killer? You cannot selectively invoke potential without acknowledging its full range. Third, the structural guarantee: regardless of whether the child cures cancer or develops it, they are guaranteed to experience suffering, loss, fear, and death. These are not risks—they are certainties. The question is not 'what might they achieve?' but 'did they consent to the conditions under which they must achieve it?' Fourth, the instrumentalization problem: this objection treats the potential child as a means to an end—the solution to humanity's problems. The child is not being valued for its own sake; it is being valued for its potential utility to existing beings. This is the most transparent form of the proxy gamble: creating a new consciousness to serve the interests of those already existing. Fifth, and most devastatingly: the people who actually do cure cancer are overwhelmingly motivated by the experience of suffering—their own or others'. The disease exists because biology is a slaughterhouse. Celebrating the hypothetical cure while defending the system that produces the disease is incoherent. You do not need cancer researchers if you do not produce beings who develop cancer."
    },
    sources: ["Lottery fallacy", "Symmetry of speculative outcomes", "Instrumentalization", "Structural guarantees vs. speculative possibilities", "Proxy Gamble"]
  },
  {
    id: "pinker-better-world",
    tier: 3,
    category: "Structural/Pragmatic",
    trigger: "The world is getting better / Steven Pinker / Less violence than ever / Enlightenment Now",
    keywords: ["Pinker", "better angels", "getting better", "less violence", "progress", "statistics", "poverty declining", "life expectancy", "enlightenment"],
    psychMechanism: "Selective statistical framing / Survivorship bias at civilizational scale / Optimism Bias with empirical clothing",
    diagnosis: "The interlocutor cites Steven Pinker or similar optimist empiricists to argue that aggregate trends in violence, poverty, and life expectancy demonstrate that existence is improving—and therefore worth continuing. This is the most empirically sophisticated version of the optimism bias. It requires engagement with the data, not just the psychology.",
    responses: {
      short: "A declining rate of violence does not eliminate violence. A longer life expectancy means a longer period of guaranteed suffering before guaranteed death. You have improved the prison conditions. You have not addressed the ethics of imprisonment.",
      medium: "Pinker's thesis—that violence, poverty, and disease have declined in per-capita terms over centuries—may be empirically defensible on its own narrow terms. But it does not address the antinatalist argument at any level. First, relative improvement is not the elimination of suffering. A world with 'less' torture still contains torture. A world with 'declining' infant mortality still buries infants. The asymmetry argument does not require that the world be maximally terrible—it requires only that existence guarantees suffering and that creation occurs without consent. Both conditions remain true regardless of Pinker's graphs. Second, aggregate statistics mask individual catastrophe. The child dying of leukemia in 2026 does not suffer less because the per-capita rate of childhood leukemia has declined since 1950. Statistics describe populations; suffering is experienced by individuals. Third, the expansion of capacity cuts both directions. The same technological progress that reduced certain forms of suffering has produced factory farming at industrial scale, nuclear weapons, surveillance states, algorithmic manipulation, and environmental collapse. Pinker's dataset selectively excludes the novel forms of suffering that modernity has invented.",
      long: "The Pinker objection is the optimism bias wearing empirical clothing, and it demands a detailed response because it is not obviously wrong on its own terms. Let me grant, for the sake of argument, that per-capita rates of violence, extreme poverty, and preventable disease have declined over the past several centuries. Even granting this, the antinatalist position remains entirely intact, for the following reasons. First, the threshold problem: antinatalism does not require that the world be maximally terrible. It requires only two conditions—that existence guarantees some degree of suffering, and that creation occurs without the consent of the created. Both conditions are satisfied in Pinker's improving world just as thoroughly as in a medieval one. A world with 'less' bone cancer still contains bone cancer. A world with 'declining' rates of child abuse still subjects children to abuse. The asymmetry does not have a threshold below which it deactivates. Second, the aggregation fallacy: Pinker's methodology operates at the population level—per-capita rates, statistical trends, aggregate measures. But suffering is not experienced at the population level. It is experienced by individual conscious beings, one nervous system at a time. The child born today who develops schizophrenia does not suffer less because fewer people per capita develop schizophrenia than in 1800. Their suffering is absolute, not relative. Third, the novel suffering problem: the same technological progress that reduced certain historical forms of suffering has produced entirely new categories of it. Factory farming subjects approximately 80 billion land animals per year to conditions of extreme suffering that did not exist before industrialization. Nuclear weapons introduced the possibility of species-level annihilation. Social media has produced epidemic rates of adolescent anxiety and self-harm. Algorithmic surveillance has created forms of psychological manipulation unknown to previous generations. Pinker's optimism requires selectively excluding these developments from the ledger. Fourth, the moving goalpost: every generation's optimists have declared that the present is better than the past. And every generation has been correct in some narrow statistical sense while remaining completely wrong about the structural guarantees of suffering. The medieval optimist could point to improvements over the Dark Ages. The Enlightenment optimist could point to improvements over the medieval period. And in every era, beings continued to suffer and die without having consented to exist. The trend line is irrelevant to the consent question. You have improved the prison conditions. Congratulations. The prisoners still never agreed to be incarcerated."
    },
    sources: ["Pinker — Better Angels / Enlightenment Now", "Threshold problem", "Aggregation fallacy — population vs. individual", "Novel suffering", "Factory farming statistics", "Consent independence from conditions"]
  },
  {
    id: "privileged-first-world",
    tier: 1,
    category: "Emotional/Reflexive",
    trigger: "You're just privileged / First world problems / Try saying that in a developing country",
    keywords: ["privilege", "privileged", "first world", "rich", "comfortable", "ivory tower", "easy life", "spoiled"],
    psychMechanism: "Genetic fallacy via socioeconomic positioning / Tu quoque variant / Deflection from argument to arguer",
    diagnosis: "The interlocutor attempts to invalidate the argument by locating the arguer within a privileged socioeconomic position, implying that only material comfort could produce such 'ungrateful' conclusions. This commits the genetic fallacy and also ignores that pessimist philosophy has emerged from conditions of extreme suffering across cultures and economic strata.",
    responses: {
      short: "The philosophy emerges from extreme empathy for those who suffer MOST—not from ignorance of their conditions. Benatar writes from South Africa. Buddhism emerged in a world of famine and caste oppression. Your objection is a genetic fallacy.",
      medium: "This objection commits the genetic fallacy twice. First, it evaluates the argument based on the arguer's circumstances rather than its logical structure. The asymmetry of suffering is either valid or it is not—regardless of the tax bracket of the person articulating it. Second, it is empirically wrong about the origins of pessimist philosophy. Benatar works at the University of Cape Town—in South Africa, not a bastion of 'first world comfort.' Buddhism's diagnosis of existence as dukkha emerged in ancient India under conditions of extreme poverty, disease, and caste oppression. Schopenhauer developed his pessimism after witnessing Napoleonic-era devastation. The philosophy does not emerge from privilege—it emerges from confrontation with the reality that privilege merely masks. Furthermore, the objection contains its own devastating irony: the people in developing countries experiencing the worst suffering are the strongest evidence FOR the antinatalist position. Their suffering is precisely what the philosophy addresses. To invoke their conditions as a weapon against the philosophy that advocates for the prevention of such suffering is rhetorical violence of the most cynical kind.",
      long: "The privilege objection performs a remarkable rhetorical inversion: it weaponizes the suffering of the global poor against the philosophy that most directly addresses their welfare. Stated plainly, the objection runs: 'People in developing countries suffer immensely, therefore you should not argue against the creation of more people who will suffer immensely.' The incoherence is self-evident. But let me address the objection on its own terms. First, the genetic fallacy: the socioeconomic position of the person making an argument has no bearing on the argument's validity. If a wealthy person argues that child labor is wrong, the argument is not invalidated by their wealth. If a person in material comfort argues that imposing existence without consent is ethically impermissible, the argument stands or falls on its logic, not on their bank statement. Second, the empirical claim that antinatalism is a 'luxury philosophy' is historically illiterate. The deepest pessimist traditions in human history emerged from conditions of extreme suffering. The Buddha's entire philosophical project began with the direct observation of old age, sickness, and death. Ecclesiastes—among the oldest pessimist texts in the Western canon—was written within a culture defined by exile, conquest, and systemic oppression. Schopenhauer, Mainlander, and Cioran all developed their pessimism in direct response to historical catastrophe, not despite comfortable circumstances. Third, and most critically: the antinatalist argument applies MORE forcefully in conditions of extreme deprivation, not less. If the proxy gamble of procreation is ethically questionable when the child might be born into material comfort, it is catastrophically indefensible when the child is guaranteed to be born into famine, war, preventable disease, and systemic exploitation. The people suffering most in the developing world are the ultimate evidence for antinatalism—not a refutation of it. To invoke their suffering to silence the philosophy that demands its prevention is to use the victims as shields for the system that victimizes them."
    },
    sources: ["Genetic fallacy", "Historical pessimism across socioeconomic strata", "Benatar — South Africa", "Buddhism — origins in suffering", "Proxy Gamble intensified by deprivation"]
  },
  {
    id: "selfish-lazy",
    tier: 1,
    category: "Emotional/Reflexive",
    trigger: "Antinatalism is just selfishness / You're too lazy to raise kids / Cowardice",
    keywords: ["selfish", "lazy", "coward", "responsibility", "shirking", "easy way out", "avoid responsibility", "don't want to work"],
    psychMechanism: "Projection — the interlocutor attributes selfishness to the person NOT imposing existence, while defending the act of imposing it",
    diagnosis: "This is structural projection. The act of creating a new sentient being to satisfy one's biological urges, psychological needs, or social expectations—without the created being's consent—is the selfish act. Declining to impose existence on a non-consenting entity is the restraint of self-interest, not its expression.",
    responses: {
      short: "Creating a being to satisfy your biological urges and psychological needs—without their consent—is the selfish act. Declining to impose existence on an unconsenting entity requires nothing except the restraint of self-interest. You have the projection backwards.",
      medium: "The selfishness accusation inverts reality so completely it functions as a diagnostic. Examine the motivations for procreation honestly: biological urge, social expectation, fear of loneliness in old age, desire for legacy, the psychological validation of parenthood, the Terror Management imperative to achieve biological immortality through genetic continuation. These are entirely self-serving motivations—the child is not consulted, and the child's welfare is speculated upon but never guaranteed. Now examine the antinatalist decision: declining to satisfy one's biological urges in order to prevent the imposition of suffering on a non-consenting entity. This is the suppression of self-interest in favor of ethical restraint. The person who does not reproduce has sacrificed the psychological satisfactions of parenthood, the social approval that accompanies it, and the biological imperative that demands it. The person who reproduces has sacrificed nothing except someone else's welfare. Which of these two acts is selfish?",
      long: "The accusation of selfishness directed at antinatalists is perhaps the most psychologically revealing objection in the entire discourse, because it requires the interlocutor to maintain two simultaneous beliefs that are logically incompatible. Belief one: creating a new sentient being to satisfy one's own biological urges, social expectations, and psychological needs—without the being's consent—is an act of generosity. Belief two: declining to create that being, thereby preventing the imposition of unconsented suffering, is an act of selfishness. These two beliefs cannot coexist in a logically coherent framework. The first describes an act performed primarily for the benefit of the actor (the parent), whose motivations include biological drive, social validation, legacy anxiety, and Terror Management. The second describes an act of restraint that requires the actor to suppress their biological imperatives, forgo social approval, and accept the cultural stigma of childlessness. The person who reproduces gets: genetic continuation, social approval, psychological validation, a caretaker for old age, a legacy project, and the neurochemical rewards of pair-bonding and parental attachment. The person who does not reproduce gets: social stigma, cultural suspicion, economic penalty (in many societies), and the awareness that their genetic line terminates with them. If selfishness is defined as acting primarily in service of one's own interests, then the evidence overwhelmingly identifies the natalist as the selfish party. The antinatalist has overridden their most fundamental biological programming—the drive to reproduce—in service of an ethical principle that benefits an entity who will never exist to thank them. That is not selfishness. It is the most radical form of altruism available to a biological organism."
    },
    sources: ["Projection", "Motivational analysis of procreation", "TMT — biological immortality drive", "Altruism of non-reproduction"]
  },
  {
    id: "consent-incoherent",
    tier: 4,
    category: "Genuine Philosophical",
    trigger: "The consent argument is incoherent / You can't get consent from non-existent beings / Consent requires a subject",
    keywords: ["consent incoherent", "can't consent", "no subject", "paradox", "impossible standard", "absurd requirement"],
    psychMechanism: "Genuine philosophical engagement — this attacks the logical structure of the consent premise itself",
    diagnosis: "This is a technically serious objection and one of the stronger attacks on the antinatalist framework. The critic argues that consent is a concept applicable only to existing agents, and therefore demanding consent from the non-existent is a category error that renders the antinatalist position incoherent. The response must clarify that the impossibility of consent is precisely the problem, not a refutation of the concern.",
    responses: {
      short: "The impossibility of consent IS the argument, not a flaw in it. In every other ethical domain, when consent cannot be obtained, the default is restraint—not imposition. Only in procreation is the impossibility of consent treated as license to proceed.",
      medium: "The objection correctly identifies that consent cannot be obtained from non-existent beings. But it draws the wrong conclusion. In medical ethics, when a patient cannot consent—because they are unconscious, incapacitated, or otherwise unable to communicate—the default protocol is restraint. Presumed consent is permitted only when inaction would cause greater harm (emergency surgery on an unconscious patient). Since non-existence is not a harm—there is no entity suffering from the deprivation of life—there is no emergency that justifies bypassing the consent requirement. The impossibility of consent is not a loophole that permits creation. It is a structural condition that prohibits it. The antinatalist does not demand that non-existent beings provide consent. The antinatalist observes that consent is structurally impossible, and concludes that the ethically appropriate response to this impossibility is restraint—exactly as it is in every other domain where consent cannot be secured.",
      long: "This is among the most technically precise objections to the antinatalist framework, and it deserves a careful answer. The critic argues: consent requires a subject. Non-existent beings are not subjects. Therefore, demanding consent from the non-existent is a category error, and the antinatalist 'impossibility of consent' argument is logically incoherent. The response operates at two levels. First, the structural level: the antinatalist is not demanding that non-existent beings provide consent. The antinatalist is observing that consent is structurally impossible for the act of creation, and then asking: what is the appropriate ethical response when an action that profoundly affects another being cannot receive that being's consent? In every other ethical domain, the answer is restraint. The Nuremberg Code prohibits medical experimentation without informed consent—not because the experimenters could theoretically obtain consent and chose not to, but because the conditions of the experiments made genuine consent impossible (coercion, power imbalance, lack of information). The ethical response to the impossibility of consent was not 'therefore experiment freely.' It was 'therefore do not experiment.' Procreation imposes the most consequential condition possible—existence itself, with all its guaranteed suffering and certain death—on a being whose consent is structurally impossible. The ethical default should be restraint. Second, the asymmetric level: presumed consent is valid only when inaction would cause greater harm to the affected party. Emergency surgery on an unconscious patient is justified because failing to operate would cause the patient to die—and the patient already exists with a preference for survival. The non-existent have no preferences, no needs, no welfare to protect. There is no emergency. There is no patient on the table. There is no harm prevented by creating them. The impossibility of consent, combined with the absence of any harm in non-existence, generates a straightforward ethical conclusion: do not create. The 'incoherence' objection mistakes the impossibility of meeting an ethical standard for the irrelevance of that standard. It is the opposite: the impossibility of meeting the standard is precisely what makes the action impermissible."
    },
    sources: ["Consent impossibility — structural analysis", "Nuremberg Code — consent under impossible conditions", "Presumed consent — emergency exception only", "Medical ethics parallel", "Benatar — non-existence as non-harm"]
  },
  {
    id: "suffering-makes-human",
    tier: 2,
    category: "Folk Philosophical",
    trigger: "Suffering is part of being human / It's what makes us human / Embrace the struggle",
    keywords: ["part of life", "makes us human", "human condition", "embrace", "struggle", "endure", "accept", "that's life", "deal with it"],
    psychMechanism: "Normalization of harm / Stockholm Syndrome with existence / Definitional circularity",
    diagnosis: "The interlocutor defines suffering as constitutive of humanity, thereby rendering any objection to suffering an objection to humanity itself. This is definitional circularity: suffering is good because it makes us human, and being human is good because it includes suffering. The circle is never broken because the conclusion is assumed in the premise.",
    responses: {
      short: "Defining suffering as essential to humanity and then celebrating humanity for including suffering is a perfect logical circle. You have not justified the harm. You have defined yourself by it.",
      medium: "This is definitional circularity masquerading as wisdom. The argument runs: suffering is part of being human → being human is valuable → therefore suffering is valuable. But the second premise—that being human is inherently valuable—is precisely what the antinatalist contests. You cannot use the disputed conclusion as a premise in the argument for that conclusion. Furthermore, this framing reveals a profound Stockholm Syndrome with existence. The captive who declares 'this captivity is what makes me who I am' has not justified the captivity. They have demonstrated the adaptive capacity of consciousness to narrativize its own imprisonment. Evolution has engineered you to accept your conditions and find meaning within them—because ancestors who could not do this failed to reproduce. Your acceptance is a survival mechanism, not a philosophical position.",
      long: "The 'suffering makes us human' objection commits a logical error so foundational it deserves to be named: the Constitutive Fallacy. The structure is: X is a constitutive element of Y. Y is valuable. Therefore X is valuable. But this logic, if applied consistently, would validate any harm that happens to be constitutive of an identity or system. Disease is constitutive of biological life. Exploitation is constitutive of capitalist economies. Violence is constitutive of natural selection. If 'being constitutive of a system' confers value on a component, then every horror produced by any system is retroactively justified by its role in that system. This is clearly absurd. The proper response is to evaluate the component (suffering) on its own terms—not to launder it through the system it happens to inhabit. And on its own terms, suffering is the one experiential state that every conscious being instinctively recoils from. No organism seeks suffering for its own sake. Pain exists as an aversive signal precisely because it indicates damage. To celebrate it as 'what makes us human' is to celebrate the alarm system while ignoring the fire. Moreover, this framing performs a subtle but devastating normalization: by defining suffering as intrinsic to the human condition, it forecloses the possibility of questioning whether the human condition should be imposed on new beings. If suffering is simply 'part of the package,' then objecting to the package's imposition on non-consenting entities becomes, by definition, an objection to humanity itself—which the interlocutor can then dismiss as misanthropy. The circularity is complete: suffering is justified because it's human, being human is justified because it includes suffering, and anyone who questions the arrangement hates humans. This is not philosophy. It is a closed loop of self-congratulatory endurance mythology."
    },
    sources: ["Constitutive Fallacy", "Definitional circularity", "Stockholm Syndrome with existence", "Normalization of harm", "Adaptive meaning-making as survival mechanism"]
  },
  {
    id: "red-button-repugnant",
    tier: 5,
    category: "Meta-Objection",
    trigger: "The Red Button thought experiment is monstrous / You would kill everyone",
    keywords: ["red button", "kill everyone", "genocide", "monstrous", "evil", "mass murder", "extinction button"],
    psychMechanism: "Conflation of theoretical painless cessation with violent mass murder / Emotional collapse of distinction",
    diagnosis: "The interlocutor collapses the distinction between the thought experiment (instantaneous, painless, universal cessation) and real-world violence (painful, localized, non-consensual). The Red Button is designed precisely to isolate the philosophical question—is non-existence preferable to existence?—from the practical horror of killing. The emotional conflation is psychologically understandable but logically impermissible.",
    responses: {
      short: "The Red Button specifies instantaneous, painless, universal cessation. You are conflating a philosophical thought experiment with mass murder. The entire point of the thought experiment is to remove the violence variable and isolate the existence question.",
      medium: "The Red Button thought experiment is deliberately constructed to eliminate every variable except the core philosophical question: is the cessation of all sentient experience, achieved without any suffering whatsoever, ethically preferable to the continuation of a biosphere that guarantees suffering? By specifying that the mechanism is instantaneous and painless, the thought experiment removes the objections that apply to real-world violence: pain, fear, violation of preferences, non-consensual harm. What remains is the pure question. Your emotional reaction to the thought experiment—classifying it as 'monstrous'—reveals that your objection is not to the suffering the button would cause (it causes none) but to the non-existence it would produce. You are defending existence itself as an intrinsic good, independent of its content. That is a metaphysical commitment, not an ethical argument. And it is precisely the commitment the thought experiment is designed to expose.",
      long: "The Red Button is the single most important thought experiment in EFIList philosophy because it performs a precise surgical operation on the interlocutor's moral framework: it removes every possible objection except the defense of existence itself. Standard objections to extinction—it would cause suffering, it would violate consent, it would be violent, it would be terrifying—are eliminated by the experimental conditions. The button is instantaneous (no duration of suffering), painless (no physical harm), universal (no survivors left to grieve), and hypothetical (no one is actually proposing to build it). What remains, after every practical objection has been surgically removed, is the raw metaphysical question: is existence, independent of its content, intrinsically valuable? The interlocutor who reacts with horror to the Red Button despite its painless, universal conditions has revealed something profound about their position: they are not defending the quality of life. They are defending the fact of life. Existence itself—regardless of the suffering it contains—is being treated as a terminal value that overrides all other considerations. This is the exact commitment the EFIList challenges. If existence is intrinsically valuable, then no amount of suffering can outweigh it—which means the child dying of bone cancer is, in some cosmic accounting, 'worth it' simply because they existed. If existence is NOT intrinsically valuable, then its continuation must be justified by its content—and the content includes structural guarantees of suffering, disease, predation, and death that no amount of art or love can retroactively redeem. The Red Button does not advocate for violence. It advocates for the honest confrontation of a question that most people refuse to ask: if you could end all suffering by ending all experience, painlessly and instantly, would you? And if not—why not? What precisely is being preserved, and for whom?"
    },
    sources: ["Red Button thought experiment", "Existence as terminal value", "Isolation of philosophical variable", "EFIList methodology", "Metaphysical commitment exposure"]
  },
  {
    id: "slippery-slope-eugenics",
    tier: 3,
    category: "Structural/Pragmatic",
    trigger: "This is a slippery slope to eugenics / Sounds like population control / Nazi eugenics",
    keywords: ["eugenics", "Nazi", "population control", "slippery slope", "forced sterilization", "genocide", "master race", "social darwinism"],
    psychMechanism: "Associative fallacy / Reductio via historical atrocity / Guilt by superficial resemblance",
    diagnosis: "The interlocutor draws a line from antinatalism to historical eugenics programs. This is an associative fallacy: eugenics selectively prevents CERTAIN people from reproducing based on racial, genetic, or social criteria while encouraging OTHERS to reproduce. Antinatalism applies universally—it opposes ALL procreation regardless of race, class, or genetic profile. The two positions are structurally antithetical.",
    responses: {
      short: "Eugenics selectively targets specific populations while encouraging others to reproduce. Antinatalism opposes all procreation universally, regardless of race, genetics, or class. These positions are structurally opposite. You are confusing universal ethics with selective persecution.",
      medium: "The eugenics comparison collapses under the most basic structural analysis. Eugenics is a hierarchical system: it classifies humans into 'desirable' and 'undesirable' categories and applies reproductive restrictions selectively—sterilizing the 'inferior' while incentivizing the 'superior' to breed. This presupposes that some lives are more valuable than others and that the 'right' people should reproduce more. Antinatalism rejects this framework entirely. It applies universally—no human, regardless of race, genetics, intelligence, or social standing, should reproduce, because the ethical objection (the non-consensual imposition of suffering) applies to every act of creation equally. Antinatalism is, in fact, the most radically egalitarian position possible: it holds that no person, no matter how privileged or genetically gifted, has the right to impose existence on a non-consenting being. Eugenics says 'the wrong people are reproducing.' Antinatalism says 'reproduction itself is the wrong.' These are antithetical positions.",
      long: "The eugenics accusation is among the most rhetorically effective and intellectually dishonest objections in the discourse, because it leverages legitimate historical horror to suppress philosophical engagement through guilt by association. The response must be precise. First, structural distinction: eugenics is inherently hierarchical and discriminatory. It classifies humans into categories of reproductive worthiness based on race, disability, intelligence, or social class. It then applies reproductive restrictions selectively—forcibly sterilizing 'undesirable' populations while actively encouraging 'desirable' populations to produce more offspring. The entire framework presupposes that some lives are more valuable than others and that the state has the authority to enforce this hierarchy through reproductive control. Antinatalism rejects every single one of these premises. It makes no distinction between populations. It assigns no differential value to human lives based on genetic, racial, or social criteria. It opposes ALL procreation universally, on the grounds that the non-consensual imposition of suffering applies equally to every potential human being, regardless of their hypothetical characteristics. If anything, antinatalism is the most radical possible form of egalitarianism: it holds that no parent—no matter how wealthy, healthy, or genetically privileged—possesses the ethical right to impose existence on a non-consenting entity. Second, the motivational distinction: eugenics is motivated by the belief that the human species should be 'improved'—that reproduction is good when the 'right' people do it. Antinatalism is motivated by the belief that the imposition of suffering without consent is wrong, regardless of who does it. Eugenics wants to optimize the breeding program. Antinatalism wants to end it. Third, the slippery slope structure: the 'slippery slope to eugenics' argument assumes that voluntary antinatalism will inevitably become coercive population control. But this slope runs in every direction. Pro-natalist policies—tax incentives for reproduction, cultural pressure to breed, religious mandates for large families—are themselves coercive reproductive programs. The assumption that only anti-reproductive positions slide toward authoritarianism, while pro-reproductive positions are somehow immune, reveals the Status Quo Bias at the heart of the objection."
    },
    sources: ["Structural distinction: universal vs. selective", "Eugenics history — hierarchical classification", "Antinatalism as radical egalitarianism", "Slippery slope applies bidirectionally"]
  },
  {
    id: "adoption-instead",
    tier: 2,
    category: "Folk Philosophical",
    trigger: "Why not just adopt? / If you care about kids, adopt / Adoption solves the problem",
    keywords: ["adopt", "adoption", "foster", "orphans", "already born", "existing children"],
    psychMechanism: "Deflection to pragmatic alternative / Misidentification of the philosophical target",
    diagnosis: "The interlocutor assumes that the antinatalist objects to the EXPERIENCE of parenthood rather than the ACT of creation. Adoption does not create a new sentient being—it provides care for one that already exists. Most antinatalists fully support adoption. The objection misidentifies the target of the critique.",
    responses: {
      short: "Most antinatalists actively support adoption. The objection is to creating NEW sentient beings, not to caring for those who already exist. Adoption addresses existing suffering without manufacturing new sufferers. You are agreeing with us without realizing it.",
      medium: "This objection inadvertently supports the antinatalist position. Adoption provides parental experience and nurtures an already-existing child without creating a new consciousness and exposing it to unconsented suffering. It addresses the needs of beings who are already here—which is entirely consistent with negative utilitarian ethics. The antinatalist objection is specifically to the ACT of biological creation: the manufacturing of a new sentient being who will be guaranteed to suffer and die without having consented to exist. Adoption circumvents this entirely. If your response to 'procreation is ethically problematic' is 'what about adoption?'—you have effectively conceded the premise. You are acknowledging that the desire for parenthood can be satisfied without creating new life. The question then becomes: why create new life when existing children need care?",
      long: "The adoption objection is one of the rare cases where the interlocutor accidentally arrives at the antinatalist conclusion while believing they are refuting it. The logic runs: 'If you think creating new life is wrong but you care about children, then adopt.' The antinatalist response is: 'Yes. Exactly. That is precisely the point.' Adoption satisfies the desire for parenthood, provides care for an already-existing child who needs it, and does so without manufacturing a new consciousness and subjecting it to the non-consensual imposition of suffering. It is the ethically optimal resolution of the parental impulse within a negative utilitarian framework. The fact that millions of children languish in foster care, orphanages, and institutional neglect while prospective parents insist on biological reproduction reveals the true motivational structure of procreation. The drive is not to 'care for a child'—adoption would satisfy that. The drive is to create a genetic copy of oneself—to achieve biological immortality, to satisfy the narcissistic imperative of seeing one's own features reflected in a new face. When this motivational structure is exposed, the 'gift of life' narrative collapses: the parent is not giving the child a gift. The parent is giving themselves a mirror. The child is the instrument, not the beneficiary. Adoption exposes this by offering an alternative that satisfies every stated motivation for parenthood—love, nurture, legacy, purpose—except the genetic narcissism. And it is precisely this exposure that makes the adoption suggestion uncomfortable for natalists: it forces them to confront the extent to which their desire for children is a desire for themselves."
    },
    sources: ["Adoption as antinatalism-consistent", "Motivational analysis of biological vs. adoptive parenthood", "Genetic narcissism", "Existing children in need — foster care statistics"]
  },
  {
    id: "bitter-childhood",
    tier: 1,
    category: "Emotional/Reflexive",
    trigger: "You're just bitter about your own childhood / Bad parents made you this way",
    keywords: ["childhood", "parents", "upbringing", "trauma", "bitter", "resentment", "daddy issues", "mommy issues", "raised wrong"],
    psychMechanism: "Genetic fallacy / Psychologizing the arguer / Biographical reductionism",
    diagnosis: "The interlocutor attempts to reduce a philosophical position to its biographical origins, implying that if the personal catalyst can be identified, the argument is invalidated. This is the genetic fallacy in its most personal form. The biographical origins of a belief have no bearing on its truth-value.",
    responses: {
      short: "The biographical origins of a belief have no bearing on its truth-value. Newton's troubled childhood did not invalidate calculus. Diagnose the argument, not the arguer.",
      medium: "This is the genetic fallacy applied to biography. Even if an antinatalist arrived at their position through personal suffering—which many do, and many do not—the truth-value of the asymmetry argument is entirely independent of the psychological path that led someone to discover it. A person who discovers that fire burns because they were burned as a child has not made a less valid observation about fire. The biographical catalyst is irrelevant to the logical structure. Furthermore, this objection contains a revealing self-contradiction: the interlocutor simultaneously claims that (a) the antinatalist's childhood suffering invalidates their philosophy, and (b) life is worth living despite such suffering. If the suffering was severe enough to generate an entire philosophical framework of opposition, perhaps the interlocutor should consider whether that suffering validates the framework rather than invalidates it.",
      long: "The biographical reduction of antinatalism commits the genetic fallacy so comprehensively it deserves extended analysis. The logical structure is: Person X holds belief Y. Person X had negative experience Z. Therefore belief Y is merely a psychological response to Z and lacks independent validity. If this logic were applied consistently, it would invalidate virtually every philosophical position in history. Nietzsche's philosophy is 'just' a response to his chronic illness. Marx's critique of capitalism is 'just' resentment from his poverty. Kierkegaard's existentialism is 'just' anxiety from his broken engagement. In every case, the biographical catalyst is real—and in every case, it is irrelevant to the truth-value of the resulting philosophy. But the objection also performs a more insidious function: it pathologizes dissent. By locating antinatalism in individual trauma rather than in structural observation, the interlocutor transforms a philosophical challenge into a psychological symptom. This allows them to prescribe 'healing' rather than engage with the argument—effectively medicalizing a position they cannot refute. The antinatalist is not a philosopher to be debated; they are a patient to be treated. And once the position is medicalized, it can be dismissed without engagement—because one does not argue with symptoms. One treats them. This pathologization strategy is identical in structure to the historical medicalization of political dissent—Soviet psychiatry diagnosed dissidents with 'sluggish schizophrenia,' thereby converting political opposition into clinical illness. The function is the same: to avoid engaging with the substance of the critique by relocating it from philosophy to pathology. Finally, the deepest irony: even if my childhood WAS the catalyst for this philosophy, that childhood was imposed on me without my consent by parents who gambled with my welfare. The biographical objection inadvertently proves the antinatalist point: the suffering that supposedly 'caused' my philosophy is itself evidence of the proxy gamble's consequences."
    },
    sources: ["Genetic fallacy", "Pathologization of dissent", "Soviet psychiatric abuse parallel", "Biographical reductionism", "Self-defeating irony of the objection"]
  },
  {
    id: "cant-prove-nonexistence-better",
    tier: 4,
    category: "Genuine Philosophical",
    trigger: "You can't prove non-existence is better / You've never experienced non-existence",
    keywords: ["prove", "non-existence", "experienced", "how do you know", "never been non-existent", "can't compare"],
    psychMechanism: "Epistemological challenge to comparative claims / Genuine philosophical engagement",
    diagnosis: "This is a technically serious objection. The critic argues that any claim about the 'superiority' of non-existence requires a comparison between two states—existence and non-existence—but since no one has experienced non-existence, the comparison is epistemically impossible. The response must clarify the logical structure of the asymmetry, which does not require experiential comparison.",
    responses: {
      short: "The asymmetry does not claim that non-existence 'feels better.' Non-existence involves no experience at all. The claim is structural: the absence of suffering is good (no victim), while the absence of pleasure is not bad (no one deprived). This requires logic, not experience.",
      medium: "This objection assumes that the antinatalist claim requires an experiential comparison: 'non-existence feels better than existence.' It does not. The asymmetry is a logical structure, not an experiential report. The claim is: (1) the presence of suffering is bad—this is uncontroversial; (2) the absence of suffering is good, even when there is no one to appreciate the absence—this is good in a counterfactual sense, not an experiential one; (3) the presence of pleasure is good—also uncontroversial; (4) the absence of pleasure is not bad when there is no one to be deprived of it. The asymmetry between (2) and (4) is the engine of the argument. It does not require anyone to 'experience' non-existence. It requires only the recognition that harm requires a victim (suffering is bad because someone suffers) while deprivation requires an existing subject (the absence of pleasure is only bad if someone exists to lack it). Non-existence produces no victims and no deprived subjects. Existence guarantees both.",
      long: "The epistemological challenge to comparative claims about non-existence is among the more sophisticated objections, and it requires a precise response. The critic's position runs: to claim that non-existence is 'better' than existence, one must compare the two states. But non-existence is not a state—it is the absence of all states. No one has 'experienced' non-existence. Therefore, the comparison is epistemically impossible, and the antinatalist claim is unfounded. The response operates at two levels. First, the logical level: the asymmetry argument does not make an experiential comparative claim. It does not say 'non-existence feels better than existence.' It says: the absence of suffering is good (in the sense that it is good that no one is suffering—a state of affairs that obtains regardless of whether anyone exists to appreciate it), while the absence of pleasure is not bad (in the sense that no one exists to be deprived). These are evaluations of states of affairs, not reports of experiential quality. We make these evaluations routinely in other contexts. We say 'it is good that the torture chamber is empty' without requiring a subject inside it to confirm that emptiness feels pleasant. The evaluation is structural, not phenomenological. Second, the practical level: the objection, if taken seriously, would prohibit all ethical reasoning about bringing beings into existence. If we cannot make evaluative claims about non-existence, then we also cannot claim that creation is 'good'—because that claim equally requires a comparison between the state of not-yet-existing and the state of existing. The natalist who says 'life is a gift' is making exactly the comparative claim the objection prohibits: they are asserting that existence is better than the non-existence that preceded it. If the epistemological bar excludes antinatalist claims, it excludes natalist claims with equal force. The result is not a victory for natalism—it is a stalemate that removes the justification for procreation as thoroughly as it removes the justification for anti-procreation. And in a stalemate between 'create a being who will suffer' and 'do not create a being,' the precautionary principle favors restraint."
    },
    sources: ["Benatar's Asymmetry — logical vs. experiential", "Counterfactual evaluation", "Epistemological symmetry — applies to natalist claims equally", "Precautionary principle"]
  },
  {
    id: "animals-reproduce",
    tier: 1,
    category: "Emotional/Reflexive",
    trigger: "Animals reproduce, it's just what living things do / It's the circle of life",
    keywords: ["animals", "circle of life", "natural order", "all species", "biology", "instinct", "law of nature"],
    psychMechanism: "Appeal to Nature variant / Biological determinism as moral justification",
    diagnosis: "A variant of the appeal to nature that specifically invokes animal behavior as a model for human ethics. This is doubly fallacious: first, it derives an 'ought' from an 'is'; second, it selectively ignores all the OTHER things animals do—infanticide, cannibalism, rape—that humans explicitly reject as moral models.",
    responses: {
      short: "Animals also eat their young, commit infanticide, and engage in forced copulation. If animal behavior is your ethical model, defend all of it—not just the parts that validate your preferences.",
      medium: "The appeal to animal behavior as ethical justification is the naturalistic fallacy at its most transparent. Animals reproduce by instinct—they do not reflect on the ethics of their actions. Humans claim to be moral agents capable of rational deliberation. You cannot simultaneously claim moral superiority over animals AND use animal behavior as your ethical benchmark. Furthermore, selective invocation of animal behavior reveals the fallacy's true function: you cite animal reproduction as natural and therefore good, but you do not cite animal infanticide, cannibalism, territorial murder, or forced copulation as natural and therefore good. The selection criteria is not 'what animals do' but 'what animals do that I already want to defend.' The appeal to nature is always a post-hoc rationalization dressed in biological clothing.",
      long: "The 'animals do it' objection commits a cascade of logical errors so fundamental that each one individually would be sufficient to invalidate it. First, the naturalistic fallacy: the fact that a behavior occurs in nature does not make it morally good. Parasitism occurs in nature. Infanticide is common among primates, lions, and rodents. Sexual coercion is standard reproductive strategy for many species. Cannibalism is practiced by hundreds of species. If 'animals do it' constitutes moral justification, then every one of these behaviors is equally justified. The interlocutor does not actually believe this—they selectively invoke animal behavior only for the practices they already wish to defend. Second, the agency problem: the entire basis of human moral reasoning rests on the claim that humans, unlike animals, are moral agents—beings capable of reflecting on the ethics of their actions and choosing accordingly. Animals reproduce because they are driven by instinct and lack the cognitive architecture for ethical deliberation. Humans claim to possess that architecture. You cannot simultaneously claim that human moral agency elevates us above animals AND that we should follow animal behavioral patterns without reflection. The two claims are mutually exclusive. Third, and most relevant to the EFIList framework: the fact that animals reproduce does not mitigate the suffering that reproduction produces. The gazelle fawn born into a world of predators does not suffer less because its birth was 'natural.' The field mouse consumed alive by a hawk is not consoled by the 'circle of life.' Nature's reproductive imperative is the engine of the gladiator war—it is the mechanism that continuously manufactures new victims for the biological slaughterhouse. Citing it as moral justification is citing the factory's production quota as evidence that the factory is good. The factory is the problem."
    },
    sources: ["Naturalistic fallacy", "Selective invocation of animal behavior", "Agency problem — moral agents vs. instinct-driven organisms", "EFIList critique of biological reproduction as suffering-engine"]
  },
  {
    id: "overpopulation-addressed",
    tier: 3,
    category: "Structural/Pragmatic",
    trigger: "Birth rates are already declining / Overpopulation is being solved / Demographics will handle it",
    keywords: ["birth rate", "declining", "demographic", "overpopulation", "fertility rate", "replacement", "population decline"],
    psychMechanism: "Pragmatic deflection — confusing demographic trends with ethical resolution",
    diagnosis: "The interlocutor conflates the antinatalist ethical position with a demographic concern about overpopulation. Antinatalism is not primarily about population numbers—it is about the ethics of imposing existence without consent. Even if the global population stabilized at 1 billion, the philosophical objection would remain identical.",
    responses: {
      short: "Antinatalism is an ethical position about consent and suffering, not a demographic position about population numbers. Even if one child were born per year, the philosophical objection would be identical: that child did not consent to exist.",
      medium: "This response confuses the ethical framework with a demographic concern. Antinatalism does not argue 'there are too many humans.' It argues 'creating any new sentient being without their consent, and exposing them to guaranteed suffering, is ethically impermissible.' This claim is entirely independent of population numbers. If the global population declined to ten thousand, and one couple chose to reproduce, the antinatalist objection would apply to that single act of creation with exactly the same force. Furthermore, declining birth rates in wealthy nations do not address the suffering of the 140 million beings still created annually, nor do they address the billions of non-human animals produced by factory farming, nor do they address the fundamental structural problem: that biological reproduction is the mechanism by which the gladiator war of evolution perpetuates itself. Demographic trends are irrelevant to the ethics of the act.",
      long: "The demographic deflection is a category error that confuses two entirely distinct discourses: population policy and procreative ethics. Population policy concerns itself with aggregate numbers—resource allocation, carrying capacity, economic sustainability. Antinatalism concerns itself with the ethics of a specific act: the creation of a new sentient being without that being's consent. These are independent domains. A world with a declining birth rate is not a world where the ethical problems of procreation have been resolved. It is a world where fewer non-consensual impositions are occurring—which is incrementally better from a negative utilitarian perspective—but each individual act of creation remains ethically identical to what it was at peak population. The single child born in a low-fertility society did not consent to exist. That child will suffer. That child will die. The proxy gamble operates at the individual level regardless of aggregate demographic trends. Furthermore, the demographic narrative often conceals a pro-natalist anxiety: 'birth rates are declining' is frequently deployed not as reassurance but as alarm—the concern being that insufficient new humans are being produced to sustain economic growth, cultural continuity, and geopolitical power. This reveals that the demographic framing is itself a pro-natalist instrument, measuring human creation by its utility to existing systems rather than by its ethics toward the created. The declining birth rate is not solving the problem antinatalism identifies. It is producing a different set of anxieties for those who view human creation as an economic input rather than an ethical act."
    },
    sources: ["Ethical vs. demographic framing", "Individual act vs. aggregate trend", "Pro-natalist anxiety embedded in demographic concern", "Proxy Gamble — independent of population level"]
  }
];

const TIERS = {
  1: { label: "Emotional / Reflexive", color: "#ff3333", desc: "High frequency, low rigor — defense mechanisms wearing argument costumes" },
  2: { label: "Folk Philosophical", color: "#ff6633", desc: "Moderate frequency, surface-level logic — collapse under 1-2 precise moves" },
  3: { label: "Structural / Pragmatic", color: "#cc9900", desc: "Policy-adjacent — dodge the philosophy, carry rhetorical weight via anxiety" },
  4: { label: "Genuine Philosophical", color: "#6699cc", desc: "Low frequency, high rigor — require the sharpest responses" },
  5: { label: "Meta-Objection", color: "#9966cc", desc: "Attack the framework's internal coherence" },
};

export default function ArgumentLibrary() {
  const [selectedTier, setSelectedTier] = useState(null);
  const [selectedObjection, setSelectedObjection] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [responseLevel, setResponseLevel] = useState("medium");

  const filtered = useMemo(() => {
    let results = OBJECTIONS;
    if (selectedTier) results = results.filter(o => o.tier === selectedTier);
    if (searchTerm.trim()) {
      const lower = searchTerm.toLowerCase();
      results = results.filter(o =>
        o.trigger.toLowerCase().includes(lower) ||
        o.keywords.some(k => k.includes(lower)) ||
        o.category.toLowerCase().includes(lower) ||
        o.diagnosis.toLowerCase().includes(lower)
      );
    }
    return results;
  }, [selectedTier, searchTerm]);

  return (
    <div style={{
      fontFamily: "'IBM Plex Mono', 'Courier New', monospace",
      background: "#0a0a0a",
      color: "#c8c8c8",
      minHeight: "100vh",
      padding: "24px",
      boxSizing: "border-box",
    }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;700&display=swap');
        * { box-sizing: border-box; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #111; }
        ::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
        ::selection { background: #8b0000; color: #fff; }
      `}</style>

      {/* HEADER */}
      <div style={{ borderBottom: "2px solid #8b0000", paddingBottom: "16px", marginBottom: "24px" }}>
        <h1 style={{
          fontSize: "14px",
          fontWeight: 700,
          color: "#8b0000",
          letterSpacing: "6px",
          textTransform: "uppercase",
          margin: 0,
        }}>
          ARGUMENT LIBRARY v3.0 — FINAL
        </h1>
        <p style={{
          fontSize: "11px",
          color: "#555",
          margin: "6px 0 0 0",
          letterSpacing: "2px",
          textTransform: "uppercase",
        }}>
          Antinatalist &middot; EFIList &middot; Negative Utilitarian &middot; Response Taxonomy
        </p>
      </div>

      {/* SEARCH */}
      <div style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="KEYWORD DETECTION — type an objection, phrase, or concept..."
          value={searchTerm}
          onChange={e => { setSearchTerm(e.target.value); setSelectedObjection(null); }}
          style={{
            width: "100%",
            background: "#111",
            border: "1px solid #333",
            color: "#c8c8c8",
            fontFamily: "inherit",
            fontSize: "12px",
            padding: "12px 16px",
            outline: "none",
            letterSpacing: "1px",
          }}
        />
      </div>

      {/* TIER FILTERS */}
      <div style={{ display: "flex", gap: "6px", flexWrap: "wrap", marginBottom: "20px" }}>
        <button
          onClick={() => { setSelectedTier(null); setSelectedObjection(null); }}
          style={{
            background: selectedTier === null ? "#8b0000" : "#181818",
            border: `1px solid ${selectedTier === null ? "#8b0000" : "#333"}`,
            color: selectedTier === null ? "#fff" : "#888",
            fontFamily: "inherit",
            fontSize: "10px",
            padding: "6px 12px",
            cursor: "pointer",
            letterSpacing: "2px",
            textTransform: "uppercase",
          }}
        >
          ALL TIERS
        </button>
        {Object.entries(TIERS).map(([tier, info]) => (
          <button
            key={tier}
            onClick={() => { setSelectedTier(Number(tier) === selectedTier ? null : Number(tier)); setSelectedObjection(null); }}
            style={{
              background: Number(tier) === selectedTier ? info.color + "33" : "#181818",
              border: `1px solid ${Number(tier) === selectedTier ? info.color : "#333"}`,
              color: Number(tier) === selectedTier ? info.color : "#666",
              fontFamily: "inherit",
              fontSize: "10px",
              padding: "6px 12px",
              cursor: "pointer",
              letterSpacing: "1px",
              textTransform: "uppercase",
            }}
          >
            T{tier}: {info.label}
          </button>
        ))}
      </div>

      {/* RESPONSE LEVEL */}
      <div style={{ display: "flex", gap: "6px", marginBottom: "24px", alignItems: "center" }}>
        <span style={{ fontSize: "10px", color: "#555", letterSpacing: "2px", marginRight: "8px" }}>RESPONSE DEPTH:</span>
        {["short", "medium", "long"].map(level => (
          <button
            key={level}
            onClick={() => setResponseLevel(level)}
            style={{
              background: responseLevel === level ? "#8b0000" : "#181818",
              border: `1px solid ${responseLevel === level ? "#8b0000" : "#333"}`,
              color: responseLevel === level ? "#fff" : "#666",
              fontFamily: "inherit",
              fontSize: "10px",
              padding: "6px 14px",
              cursor: "pointer",
              letterSpacing: "2px",
              textTransform: "uppercase",
            }}
          >
            {level === "short" ? "PUNCH" : level === "medium" ? "DECONSTRUCT" : "DISMANTLE"}
          </button>
        ))}
      </div>

      {/* RESULTS */}
      <div style={{ display: "flex", flexDirection: "column", gap: "2px" }}>
        {filtered.length === 0 && (
          <div style={{ color: "#444", fontSize: "12px", padding: "40px 0", textAlign: "center", letterSpacing: "2px" }}>
            NO MATCHING OBJECTIONS — REFINE SEARCH PARAMETERS
          </div>
        )}
        {filtered.map(obj => {
          const isOpen = selectedObjection === obj.id;
          const tierInfo = TIERS[obj.tier];
          return (
            <div key={obj.id}>
              {/* OBJECTION HEADER */}
              <div
                onClick={() => setSelectedObjection(isOpen ? null : obj.id)}
                style={{
                  background: isOpen ? "#141414" : "#111",
                  border: `1px solid ${isOpen ? tierInfo.color + "66" : "#222"}`,
                  padding: "14px 18px",
                  cursor: "pointer",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  transition: "all 0.15s ease",
                }}
              >
                <div style={{ flex: 1 }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "4px" }}>
                    <span style={{
                      fontSize: "9px",
                      color: tierInfo.color,
                      fontWeight: 700,
                      letterSpacing: "2px",
                      padding: "2px 6px",
                      border: `1px solid ${tierInfo.color}44`,
                      background: tierInfo.color + "11",
                    }}>
                      TIER {obj.tier}
                    </span>
                    <span style={{ fontSize: "9px", color: "#555", letterSpacing: "1px" }}>
                      {obj.category.toUpperCase()}
                    </span>
                  </div>
                  <div style={{ fontSize: "13px", color: "#ddd", fontWeight: 500 }}>
                    "{obj.trigger}"
                  </div>
                </div>
                <span style={{ color: "#444", fontSize: "18px", transform: isOpen ? "rotate(45deg)" : "none", transition: "transform 0.2s" }}>+</span>
              </div>

              {/* EXPANDED DETAIL */}
              {isOpen && (
                <div style={{
                  background: "#0f0f0f",
                  border: `1px solid ${tierInfo.color}33`,
                  borderTop: "none",
                  padding: "20px 18px",
                }}>
                  {/* KEYWORDS */}
                  <div style={{ marginBottom: "16px" }}>
                    <div style={{ fontSize: "9px", color: "#555", letterSpacing: "2px", marginBottom: "6px" }}>KEYWORD TRIGGERS</div>
                    <div style={{ display: "flex", flexWrap: "wrap", gap: "4px" }}>
                      {obj.keywords.map(k => (
                        <span key={k} style={{
                          fontSize: "10px",
                          color: "#8b0000",
                          background: "#1a0000",
                          border: "1px solid #330000",
                          padding: "2px 8px",
                        }}>{k}</span>
                      ))}
                    </div>
                  </div>

                  {/* PSYCH MECHANISM */}
                  <div style={{ marginBottom: "16px" }}>
                    <div style={{ fontSize: "9px", color: "#555", letterSpacing: "2px", marginBottom: "6px" }}>PSYCHOLOGICAL MECHANISM</div>
                    <div style={{ fontSize: "11px", color: "#996633", lineHeight: 1.5 }}>{obj.psychMechanism}</div>
                  </div>

                  {/* DIAGNOSIS */}
                  <div style={{ marginBottom: "16px" }}>
                    <div style={{ fontSize: "9px", color: "#555", letterSpacing: "2px", marginBottom: "6px" }}>CLINICAL DIAGNOSIS</div>
                    <div style={{ fontSize: "11px", color: "#999", lineHeight: 1.7, borderLeft: "2px solid #8b0000", paddingLeft: "14px" }}>
                      {obj.diagnosis}
                    </div>
                  </div>

                  {/* RESPONSE */}
                  <div style={{ marginBottom: "16px" }}>
                    <div style={{ fontSize: "9px", color: "#555", letterSpacing: "2px", marginBottom: "6px" }}>
                      RESPONSE — {responseLevel === "short" ? "PUNCH" : responseLevel === "medium" ? "DECONSTRUCTION" : "FULL DISMANTLEMENT"}
                    </div>
                    <div style={{
                      fontSize: "12px",
                      color: "#ddd",
                      lineHeight: 1.8,
                      background: "#0c0c0c",
                      border: "1px solid #222",
                      padding: "16px",
                      whiteSpace: "pre-wrap",
                    }}>
                      {obj.responses[responseLevel]}
                    </div>
                  </div>

                  {/* SOURCES */}
                  <div>
                    <div style={{ fontSize: "9px", color: "#555", letterSpacing: "2px", marginBottom: "6px" }}>SOURCES & FRAMEWORKS</div>
                    <div style={{ fontSize: "10px", color: "#666", lineHeight: 1.6 }}>
                      {obj.sources.join(" · ")}
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* FOOTER */}
      <div style={{
        marginTop: "40px",
        paddingTop: "16px",
        borderTop: "1px solid #1a1a1a",
        fontSize: "9px",
        color: "#333",
        letterSpacing: "2px",
        textAlign: "center",
      }}>
        {OBJECTIONS.length} OBJECTIONS INDEXED · {Object.keys(TIERS).length} TIERS · LABOR SINE FRUCTU
      </div>
    </div>
  );
}

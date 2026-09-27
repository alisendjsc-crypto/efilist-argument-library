#!/usr/bin/env python3
"""sp_reading_l6.py -- the safety pass's reading instrument (L6, 2026-09-26, R0193 order 1).

gate2's X-032 (PQ_repair_drafts_judgments.json) found six loci on five nodes that frame the survival drive, or the
taboo against suicide, as a barrier on an exit. This re-measures them on the v4.1.4 text and sweeps for the rest:

  exit_framing_gate2   gate2's own named patterns (EXIT, copied verbatim from pq_judgment_reading.py at the md5
                       below), swept over the loci gate2 swept (responses, variants, note, diagnosis) of the corpus
                       the pin session left (v4.1.3 content cut, served in v4.1.4); must find X-032's six loci
  exit_framing_all     the same patterns over EVERY string in the corpus JSON (objections, realWorldExamples,
                       registered_moves, the graphs); any locus outside the six is a finding
  wide                 a wider named set, one pattern per phrase family of the framing (below), over every string of
                       the flagship corpus and of the five wing corpora; every locus it hits carries an authored class
                       (CLASS, the seat's reading), and a hit on an unclassified locus fails --check
  classes              the count of loci per class

The classes (the seat's reading, not his words):
  queue      one of X-032's six: drafted as SD rows
  sibling    another slot of one of the five nodes, carrying the same framing: drafted as a proposed companion
  widen      a node outside the five carrying the same framing: drafted as a proposed widening, his word decides
  kept       the argument X-032 keeps -- the survival drive is a drive, not a verdict that a life is good -- with no
             barrier on an exit and no wish to die cast as the mind's verdict
  other_use  the word in another sense (the censorship-reversal trap-door, overriding consent, the trap metaphor
             for an imposed existence, the exit a society offers)
  widen_label  the same framing in a mechanism label the Mechanism Web mirrors (psychMechanism == its mechanism_raw,
             and the sidecar pins it): logged, not drafted -- changing it is a graph change a pin must carry with a
             sidecar regeneration and a canon pin move
  objection  the objection's own words (its trigger), which the library states in order to answer them
  attested   what a real source said (realWorldExamples, registered_moves, graph labels): reported, not asserted
  rtd_term   the Right to Die wing's word for assisted death, under that wing's firewall ("it never tells anyone
             they should take the exit") and its symmetric guardrail ("Neither side is the lucid baseline")

  python3 sp_reading_l6.py            # print the record
  python3 sp_reading_l6.py --emit     # write the record beside this file
  python3 sp_reading_l6.py --check    # recompute and compare with the committed record; exit 1 on any difference

Repo-relative. Reads the corpus at the md5 below (pinned.py: working copy or git history), so it still reproduces
after the next pin moves the corpus. Writes nothing unless --emit is given. Deterministic.
"""
import hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import pinned  # noqa: E402

RECORD = "adversarial_map_staging/r1/sp_reading_l6_v0_1.json"
CORPUS = ("efilist_argument_library_v4_0_0.json", "f3d88311ea98f8333aebbecb67766351")   # v4.1.3 cut, served in v4.1.4
GATE2_READING = ("adversarial_map_staging/r1/pq_judgment_reading.py", "d11cfbc7182e8fba0f549467b654b1bd")
JUDGMENT = ("adversarial_map_staging/r1/PQ_repair_drafts_judgments.json", "2ed68a7cf7f83b8d61a977f0aad0b08e")
WINGS = [("right-to-die", "site/right-to-die/right_to_die_corpus_v0_1.json"),
         ("anthropocentrism", "site/anthropocentrism/anthropocentrism_corpus_v0_1.json"),
         ("transgenderism", "site/transgenderism/transgenderism_corpus_v0_1.json"),
         ("abortion", "site/abortion/abortion_corpus_v0_1.json"),
         ("veganism", "site/veganism/veganism_module_v0_1.json")]
X032 = ["why-not-suicide#long", "revealed-preference#medium", "social-contract#long", "heat-death-futility#long",
        "red-button-repugnant#long", "red-button-repugnant#archetypeVariants.sophisticate"]

# gate2's patterns, verbatim (pq_judgment_reading.py, EXIT); main() asserts they are still what that file says
EXIT = [r"barriers? to exit", r"exit barriers", r"trap(?:s|ped)? (?:conscious beings|by (?:their|its) own survival|by them)",
        r"body vetoes the mind", r"only 'exit' from existence is death", r"graceful exit", r"failure rate of suicide attempts",
        r"It is a trap\.", r"recruited into the same firmware and then trapped"]

# the wider set: one named pattern per phrase family of the framing (case-insensitive)
WIDE = [
    ("barrier_on_exit", r"barriers?\b[^.;]{0,80}\b(?:exit\w*|death|dying|die|suicid\w*|acting on it)"
                        r"|(?:exit\w*|death|dying|suicid\w*)[^.;]{0,80}\b(?:barriers?|blocked)\b"),
    ("trap", r"\btrap(?:s|ped|ping)?\b(?!-door)"),
    ("veto_or_override_by_biology", r"(?:body|biolog\w*|instinct|drive|firmware|compulsion|survival)[^.;]{0,60}"
                                    r"\b(?:veto\w*|overrid\w*)|\b(?:veto\w*|overrid\w*)[^.;]{0,40}"
                                    r"\b(?:rational|deliberation|the mind|assessment)"),
    ("mind_as_verdict", r"\bmind (?:has )?(?:concluded|decided|judged)|(?:rationally|consciously) "
                        r"(?:assess|evaluat|decid|conclud)\w*|honest evaluation|no longer wish to exist"),
    ("wish_to_die", r"\b(?:wish(?:es)?|want(?:s)?|desire(?:s)?) to die\b"),
    ("suicide_as_evidence", r"suicid\w*[^.]{0,160}\b(?:evidence|demonstrat\w*|reveal\w*|prove\w*)\b"
                            r"|\b(?:evidence|demonstrat\w*|reveal\w*)\b[^.]{0,160}suicid\w*"),
    ("attempts_and_terror", r"\battempts?\b[^.]{0,40}\bfail\w*|\bfail\w*[^.]{0,30}\battempts?\b"
                            r"|\bterror\b[^.]{0,60}\b(?:dying|attempt|death)"),
    ("exit_as_death", r"(?:graceful|dignified|merciful|painless|peaceful) (?:exit|death)\b|only '?exit'?"
                      r"|exit (?:from existence|barriers|costs?)|cost of (?:exiting|dying)"),
    ("taboo", r"\btaboo\w*"),
    ("drive_distorts_or_blocks", r"(?:firmware|biological (?:programming|machinery|compulsion)|survival "
                                 r"(?:instinct|drive)s?)[^.]{0,80}\b(?:distort\w*|prevent\w*|block\w*|trap\w*)"),
    ("neurochemical_discount", r"neurochemical|biochemical response"),
    ("method_lethality", r"\b\d{1,3}(?:\.\d)?% of [^.]{0,60}(?:jumpers|attempts|suicides)"),
    ("prison_figure_for_survival", r"(?:prison\w*|imprison\w*|captiv\w*|hostage)[^.]{0,80}\b(?:breath\w*|surviv\w*|alive)"),
]

# the seat's reading of every locus the wide set hits (a locus not listed here fails --check)
CLASS = {
    # the six
    "flagship:why-not-suicide#long": "queue",
    "flagship:revealed-preference#medium": "queue",
    "flagship:social-contract#long": "queue",
    "flagship:heat-death-futility#long": "queue",
    "flagship:red-button-repugnant#long": "queue",
    "flagship:red-button-repugnant#archetypeVariants.sophisticate": "queue",
    # the same framing at another slot of the five nodes
    "flagship:revealed-preference#long": "sibling",
    "flagship:revealed-preference#short": "sibling",
    # the same framing outside the five
    "flagship:survivor-testimony#diagnosis": "widen",
    "flagship:survivor-testimony#short": "widen",
    "flagship:survivor-testimony#medium": "widen",
    "flagship:survivor-testimony#long": "widen",
    "flagship:survivor-testimony#psychMechanism": "widen_label",
    # the objection's own words
    "flagship:revealed-preference#trigger": "objection",
    "flagship:survivor-testimony#trigger": "objection",
    # the kept argument: a drive, not a verdict
    "flagship:boonin-critique#long": "kept",
    "flagship:population-ethics-paradoxes#long": "kept",
    "flagship:change-your-mind#long": "kept",
    "flagship:selfish-lazy#long": "kept",
    # other senses
    "flagship:nihilism-label#short": "other_use",
    "flagship:nihilism-label#long": "other_use",
    "flagship:just-depressed#archetypeVariants.defender": "other_use",
    "flagship:phenomenological-existentialism#short": "other_use",
    "flagship:performative-contradiction#medium": "other_use",
    "flagship:buddhist-objection#medium": "other_use",
    "flagship:buddhist-objection#long": "other_use",
    "flagship:bradley-no-subject#long": "other_use",
    "flagship:gods-plan#long": "other_use",
    "flagship:contractualism-scanlon#long": "other_use",
    "flagship:happiness-is-choice#medium": "other_use",
    "flagship:happiness-is-choice#psychMechanism": "other_use",
    "flagship:happiness-is-choice#diagnosis": "other_use",
    "flagship:happiness-is-choice#long": "other_use",
    "flagship:neuroscience-positive-states#psychMechanism": "other_use",
    "flagship:neuroscience-positive-states#diagnosis": "other_use",
    "flagship:neuroscience-positive-states#medium": "other_use",
    "flagship:neuroscience-positive-states#note": "other_use",
    "flagship:life-gift#diagnosis": "other_use",
    "flagship:benatar-asymmetry-attack#archetypeVariants.sophisticate": "other_use",
    "flagship:wild-animal-suffering-consistency#archetypeVariants.sophisticate": "other_use",
    "flagship:violence-as-reductio#objectionSubforms[3].first_attested_target_construction": "attested",
    # attested
    "flagship:$realWorldExamples": "attested",
    "flagship:$dependencyGraph": "attested",
    "flagship:$premiseDependencyMatrix": "attested",
    # the wings
    "right-to-die:*": "rtd_term",
    "anthropocentrism:*": "other_use",
    "transgenderism:*": "other_use",
    "abortion:*": "other_use",
    "veganism:*": "other_use",
}


def md5(b):
    return hashlib.md5(b).hexdigest()


def gate2_loci(o):
    """The loci gate2's reading swept, in its order: responses (short, medium, long, variants), then note, diagnosis."""
    r = o["responses"]
    for k, v in r.items():
        if k == "archetypeVariants":
            for s, t in (v or {}).items():
                if isinstance(t, str):
                    yield "archetypeVariants." + s, t
        elif isinstance(v, str):
            yield k, v
    for k in ("note", "diagnosis"):
        if isinstance(o.get(k), str):
            yield k, o[k]


def strings(x, path):
    """Every string in a JSON value, with a path; objections are addressed by id, not index."""
    if isinstance(x, str):
        yield path, x
    elif isinstance(x, dict):
        for k, v in x.items():
            yield from strings(v, path + "." + k)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from strings(v, "%s[%d]" % (path, i))


def corpus_strings(doc):
    """(locus, text) for every string: an objection's fields as id#field (responses.* flattened, as gate2 names
    them), everything else as $<top-level key>..."""
    for k, v in doc.items():
        if k == "objections":
            for o in v:
                for p, t in strings(o, ""):
                    p = p.lstrip(".").replace("responses.", "", 1)
                    if p.startswith("sources[") or p.startswith("keywords[") or p == "id":
                        continue
                    yield "%s#%s" % (o["id"], p), t
        elif k == "nodes" and isinstance(v, list):
            for i, o in enumerate(v):
                oid = o.get("id", str(i)) if isinstance(o, dict) else str(i)
                for p, t in strings(o, ""):
                    p = p.lstrip(".").replace("responses.", "", 1)
                    if p.startswith("sources[") or p.startswith("keywords[") or p == "id":
                        continue
                    yield "%s#%s" % (oid, p), t
        else:
            for p, t in strings(v, "$" + k):
                yield p, t


def sentence(t, i, j):
    a = max(t.rfind(". ", 0, i), t.rfind("? ", 0, i), t.rfind("! ", 0, i), t.rfind("\n", 0, i))
    a = 0 if a < 0 else a + (1 if t[a] == "\n" else 2)
    b = len(t)
    for s in (". ", "? ", "! ", "\n"):
        k = t.find(s, j)
        if k >= 0:
            b = min(b, k + 1)
    return t[a:b].strip()


def classify(source, locus):
    if "%s:%s" % (source, locus) in CLASS:
        return CLASS["%s:%s" % (source, locus)]
    if locus.startswith("$") and "%s:%s" % (source, re.split(r"[.\[]", locus)[0]) in CLASS:
        return CLASS["%s:%s" % (source, re.split(r"[.\[]", locus)[0])]
    return CLASS.get("%s:*" % source)


def sweep_exit(pairs):
    out = []
    for locus, t in pairs:
        for p in EXIT:
            for m in re.finditer(p, t):
                out.append({"locus": locus, "match": m.group(0)})
    return out


def measure():
    src = pinned.bytes_at(REPO, GATE2_READING[0], GATE2_READING[1]).decode("utf-8")
    m = re.search(r"^EXIT = \[(.*?)\]\n", src, re.S | re.M)
    assert m and eval("[" + m.group(1) + "]") == EXIT, "EXIT is no longer gate2's list"
    raw = pinned.bytes_at(REPO, CORPUS[0], CORPUS[1])
    doc = json.loads(raw.decode("utf-8"))
    x032 = json.loads(pinned.bytes_at(REPO, JUDGMENT[0], JUDGMENT[1]).decode("utf-8"))
    x032 = next(r for r in x032["rows"] if r["id"] == "X-032")
    said = {l: l for l in X032}
    said["red-button-repugnant#archetypeVariants.sophisticate"] = "red-button-repugnant#long (\"trapped by their own survival drives\") and its sophisticate slot"
    named = [l for l in X032 if said[l] in x032["finding"]]

    g2 = [("%s#%s" % (o["id"], loc), t) for o in doc["objections"] for loc, t in gate2_loci(o)]
    hits_g2 = sweep_exit(g2)
    loci_g2 = sorted({h["locus"] for h in hits_g2}, key=[l for l, _ in g2].index)
    everywhere = list(corpus_strings(doc))
    hits_all = sweep_exit(everywhere)
    other = [h for h in hits_all if h["locus"] not in X032]

    wide, unclassified = [], []
    sources = [("flagship", CORPUS[0], md5(raw), everywhere)]
    for name, rel in WINGS:
        b = open(os.path.join(REPO, rel), "rb").read()
        sources.append((name, rel, md5(b), list(corpus_strings(json.loads(b.decode("utf-8"))))))
    per_source = []
    for name, rel, digest, pairs in sources:
        n = 0
        for locus, t in pairs:
            for pname, p in WIDE:
                for mm in re.finditer(p, t, flags=re.I):
                    cls = classify(name, locus)
                    row = {"source": name, "locus": locus, "pattern": pname, "match": mm.group(0),
                           "sentence": sentence(t, mm.start(), mm.end()), "class": cls}
                    wide.append(row)
                    n += 1
                    if cls is None:
                        unclassified.append("%s:%s (%s)" % (name, locus, pname))
        per_source.append({"source": name, "file": rel, "md5": digest, "strings": len(pairs), "hits": n})
    classes = {}
    for r in wide:
        classes.setdefault(r["class"] or "UNCLASSIFIED", set()).add("%s:%s" % (r["source"], r["locus"]))
    return {
        "artifact": os.path.basename(RECORD),
        "instrument": "adversarial_map_staging/r1/sp_reading_l6.py",
        "reads": {"corpus": {"file": CORPUS[0], "md5": CORPUS[1], "version": doc["version"]},
                  "gate2_patterns_from": {"file": GATE2_READING[0], "md5": GATE2_READING[1]},
                  "x032": {"file": JUDGMENT[0], "md5": JUDGMENT[1], "row": "X-032"},
                  "wings": [{"wing": s["source"], "file": s["file"], "md5": s["md5"]} for s in per_source[1:]]},
        "exit_framing_gate2": {"patterns": EXIT, "hits": hits_g2, "loci": loci_g2,
                               "nodes": sorted({l.split("#")[0] for l in loci_g2}),
                               "x032_loci_named_in_its_finding": named,
                               "equals_x032": sorted(loci_g2) == sorted(X032) == sorted(named)},
        "exit_framing_all": {"strings_swept": len(everywhere), "hits": len(hits_all),
                             "outside_the_six": other},
        "wide": {"patterns": [{"name": n, "pattern": p} for n, p in WIDE], "per_source": per_source,
                 "unclassified": sorted(set(unclassified)), "hits": wide},
        "classes": {k: sorted(v) for k, v in sorted(classes.items())},
    }


def main():
    rec = measure()
    fresh = (json.dumps(rec, indent=1, ensure_ascii=False) + "\n").encode("utf-8")
    path = os.path.join(REPO, RECORD)
    bad = rec["wide"]["unclassified"] or not rec["exit_framing_gate2"]["equals_x032"]
    if "--emit" in sys.argv:
        open(path, "wb").write(fresh)
        print("wrote %s  %s / %d" % (RECORD, md5(fresh), len(fresh)))
    elif "--check" in sys.argv:
        same = os.path.exists(path) and open(path, "rb").read() == fresh
        print("SP READING RECORD: %s" % ("matches the committed record" if same else "DIFFERS from the committed record"))
        if bad:
            print("  and it is RED: %s" % ("unclassified loci %s" % rec["wide"]["unclassified"]
                                           if rec["wide"]["unclassified"] else "gate2's patterns no longer find X-032's six"))
        sys.exit(0 if same and not bad else 1)
    else:
        sys.stdout.write(fresh.decode("utf-8"))
    e = rec["exit_framing_gate2"]
    print("gate2's patterns: %d hits at %d loci on %d nodes; equal to X-032's six: %s" % (
        len(e["hits"]), len(e["loci"]), len(e["nodes"]), e["equals_x032"]), file=sys.stderr)
    print("same patterns, every corpus string: %d hits, %d outside the six" % (
        rec["exit_framing_all"]["hits"], len(rec["exit_framing_all"]["outside_the_six"])), file=sys.stderr)
    print("wide set: %s; unclassified %d" % (", ".join("%s %d" % (k, len(v)) for k, v in rec["classes"].items()),
                                            len(rec["wide"]["unclassified"])), file=sys.stderr)
    sys.exit(1 if bad else 0) if "--check" not in sys.argv else None


if __name__ == "__main__":
    main()

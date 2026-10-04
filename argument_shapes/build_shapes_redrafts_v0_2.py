#!/usr/bin/env python3
"""The golden rule's third pass (V5, seat l, 2026-10-04): shapes_redrafts_v0_2.json and its record.

gate2 judged V2b's two redrafts in V3b (R0313; shapes_redrafts_judgments.json): soul-making ACCEPT; the golden rule
AMEND (RJ-001), owed "in a new row or file". His word on R0314 adopted the judgment and folded this pass into the
responseVariants session (R0315). Drafted, not judged: gate2 judges it in its next round (K258).

  RJ-001  life-gift/the-golden-rule-passes-it-on  the statement: Hare's bound as his records state it (the total as a
                                                  limit, the shares held, the halt); the attestation: Hare 1975 added;
                                                  class (d) and route unchanged

What this builder does, every value measured at run time:
  - reads V2b's redrafts, their record, gate2's round-two record and the pilot at the md5s it pins; starts the row from
    v0_1's RD-01 (the redraft it replaces), changes only what RJ-001 owes, and asserts the changed fields are exactly
    those;
  - copies the (d)'s terminus from the registered (d) its line reaches (map v1_8, by node, locus and anchor) and from
    register v0_9, never typed (L4's law), and asserts it equals the route RJ-001 states;
  - asserts every quote in the record verbatim at its source, read at pinned bytes: the corpus, the map, and the
    scholar layer through `git show` at the game's pinned commit (skipped, and said, when that repository is absent;
    the bytes do not depend on it);
  - writes the staging file (bound_for staging, phase S, the pilot's corpus pin). Its one shape id repeats the pilot's
    on purpose: the row SUPERSEDES v0_1's RD-01, which superseded the pilot's shape, so the file validates alone and
    the record resolves the current set;
  - runs shape_validator_v0_1.py over the staging file alone and over three resolved views written to scratch: the
    pilot with both of its superseded shapes replaced (10 shapes), the set his words kept (the five ACCEPTs, soul-making
    from v0_1, this row), and the pilot loaded with this file, which must FAIL on shape-id. Each run is in its own
    process group, with TMPDIR in scratch.

  python3 argument_shapes/build_shapes_redrafts_v0_2.py [--check]
Repo-relative. --check rebuilds both files, validator runs included, and compares bytes.
"""
import hashlib, json, os, shutil, signal, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, "adversarial_map_staging", "r1"))
import pinned  # noqa: E402
import shape_validator_v0_1 as SV  # noqa: E402

PILOT = ("argument_shapes/shapes_pilot_v0_1.json", "1f9c5da6166b538a90efa6dc7598124e")
JUDGMENTS = ("argument_shapes/shapes_pilot_judgments.json", "73503bccdd3ddf8b3a82f280181251d4")
V01 = ("argument_shapes/shapes_redrafts_v0_1.json", "fc28cd12265e2712a9d610bbb2c1b69f")
V01_RECORD = ("argument_shapes/shapes_redrafts_record_v0_1.json", "ace5fb88886f7f7ce49a90658b590954")
RJUDG = ("argument_shapes/shapes_redrafts_judgments.json", "6f4974966c23920234f495cb20813d4c")
RJGATE = ("argument_shapes/shapes_redrafts_judgments_gate.py", "950c715c4b7ba35b6db8715600df8832")
CORPUS = ("efilist_argument_library_v4_0_0.json", "7b6e65e531018fecb37baf2a4fedd6d1")
MAP = ("adversarial_map_staging/adversarial_map_v1_8.json", "691930ab76908a85a6850bdb714d3827")
REGISTER = ("adversarial_map_staging/honest_residuals_register_v0_9.json", "8e53d920099e8b850baa2879dfd3e351")
VALIDATOR = ("argument_shapes/shape_validator_v0_1.py", "64553b25b6db0ff67edeb87b89178297")
WORDS = ("tools/v38_52_his_words.json", "660d13821c69aa59e2e99b9f5747c20d")
SCHOLAR = {"repo": "~/D/Argue the Argument", "commit": "76cbbd13ef967617b181697675bd15dbbf0a6a0b",
           "file": "data/flagship/scholar-objections_v1_1.json", "md5": "20999eb9b1b384d0f871a9deec464b2a"}
OUT = "argument_shapes/shapes_redrafts_v0_2.json"
RECORD = "argument_shapes/shapes_redrafts_record_v0_2.json"
PROV = {"phase": "S", "date": "2026-10-04", "seat": "l (V5, Code)"}
SHAPE_ID = "life-gift/the-golden-rule-passes-it-on"

STATEMENT = ("Glad to exist, you prescribe your own creation; universalized by the golden rule, that prescribes creating "
             "others relevantly like you, other things equal. A possible person who would be glad to exist is harmed if "
             "never created. So we ought to create them so long as the total good grows, the shares held as they are, "
             "stopping before the worst-off fall below a life just worth living.")
ATTESTED_BY = [
    {"citation": "R. M. Hare, Abortion and the Golden Rule, Philosophy and Public Affairs 4(3), 1975, pp. 201-222; "
                 "reprinted as chapter 10 of Essays on Bioethics, Oxford University Press, 1993, pp. 147-167"},
    {"citation": "R. M. Hare, Possible People, Bioethics 2(4), 1988, pp. 279-293"}]

# What the row says about its route, after reading the premise-sharers the new clauses touch (SJ-016's law, R0313).
READING = (
    "(d), unchanged, read against the premise-sharers the bound touches. The duty's ground is the possible person's own "
    "good (\"A possible person who would be glad to exist is harmed if never created\"); the total now only limits the "
    "duty, so the line is no longer licensed by others' goods, the horn the via locus sinks (\"indifferent to whose "
    "pleasure and whose pain are being summed\"). It is the opponent the copied (d) records, who will \"decline the "
    "monster (the goods and harms fall on one person, not interpersonally)\", and his L3 reading sends that move to "
    "HR-02. population-ethics-paradoxes does not take it: its scholar line attacks the antinatalist's own axiology "
    "(\"the world-destroyer conclusion\"), and the answer its long gives is the iteration claim its own (d) records as "
    "ending at bedrock (\"The node cannot keep both.\"), so no (a) can route there under R1's standard.")
QUOTES = [("statement", None, None, "A possible person who would be glad to exist is harmed if never created"),
          ("corpus", "joy-outweighs-harms", "long", "indifferent to whose pleasure and whose pain are being summed"),
          ("map", 41, "adversarial_move", "decline the monster (the goods and harms fall on one person, not "
                                          "interpersonally)"),
          ("scholar", "population-ethics-paradoxes", None, "the world-destroyer conclusion"),
          ("map", 109, "adversarial_move", "The node cannot keep both.")]
# Read for the record, quoted only in the pulls (asserted verbatim at the same sources)
PULL_QUOTES = [("corpus", "population-ethics-paradoxes", "medium",
                "devastating against Total utilitarianism, which must weigh aggregate welfare across populations"),
               ("corpus", "population-ethics-paradoxes", "long",
                "adding a person with positive but lower-than-average welfare"),
               ("corpus", "joy-outweighs-harms", "long",
                "across the distribution of lives the gamble might produce, the goods outweigh in prospect"),
               ("corpus", "rights-future-generations", "long", "The obligation would be literally infinite")]
PULLS = [
    "The golden-rule step is now worded as the SEP states it (source 1: glad that I exist, I prescribe my own creation; "
    "universalized, I prescribe creating others relevantly like me, ceteris paribus), not as 'do to others what you are "
    "glad was done to you'. RJ-008 found that wording in none of the records read, and no record read this session has "
    "it either. Not owed by RJ-001; changed because the statement may claim only what the records read support.",
    "The weighing SJ-003 owed ('weighed with everyone's preferences') is carried by the limit: the total is everyone's "
    "good, the possible person's included. Stated as a clause of the duty itself it read as the trigger (RJ-001), so "
    "it is not repeated there.",
    "The halt sits at the break-even point, the level at which the Repugnant Conclusion's lives already stand, so in an "
    "equal society Hare's bound narrows Parfit's chain without refusing its end. The held shares refuse the step the "
    "library's chain is built from (\"adding a person with positive but lower-than-average welfare\"). The card meets "
    "Hare's bound as his records state it; whether the library may still press the bare total view's verdict "
    "(\"devastating against Total utilitarianism, which must weigh aggregate welfare across populations\") against a "
    "bounded total is gate2's to read. The route does not move either way: the library's own answer at that node ends "
    "at bedrock (#109).",
    "Ex ante, a creation is a prospect over possible lives, and the via locus's first horn reads the prospect as "
    "interpersonal (\"across the distribution of lives the gamble might produce, the goods outweigh in prospect\"). At "
    "its strongest the line restricts the duty to a person who would be glad and treats the prospect as that person's "
    "own, which is the merely-possible-beneficiary premise again; read as an expectation over different possible "
    "people it is the weaker line the first horn meets. So the route is HR-02 for the line at its strongest.",
    "The bounded duty no longer meets the reductio at rights-future-generations#long (\"The obligation would be "
    "literally infinite\"), as RJ-001 found of v0_1; the no-claimant (d) there stays on the library's side, as RJ-001 "
    "read it."]
SOURCES = [
    {"what": "the Stanford Encyclopedia of Philosophy, 'Richard Mervyn Hare', section 6 (Possible People), and its "
             "bibliography",
     "url": "https://plato.stanford.edu/entries/hare/",
     "supports": "the golden-rule step, which the SEP cites to 1975, 1988b and 1988c, the 1975 paper first; the total "
                 "as a limit; and the bibliography's 1975 entry: Philosophy and Public Affairs 4: 201-22, reprinted in "
                 "1993a: 147-67",
     "excerpts": ["if I am glad that I exist, I tenselessly prescribe",
                  "I must prescribe, ceteris paribus, the bringing into existence of others relevantly like me",
                  "(1975, 1988b, 1988c)",
                  "so long as this will increase the total satisfaction of preference"]},
    {"what": "the MEDLINE record of Hare 1975 (PMID 11661183, indexed by the Kennedy Institute of Ethics), read through "
             "NCBI E-utilities",
     "url": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=11661183&retmode=xml",
     "supports": "the citation: Philos Public Aff. 1975 Spring; 4(3): 201-22, 'Abortion and the golden rule', Hare RM. "
                 "No abstract. Crossref carries no record of the 1975 printing (searched by title and author), so this "
                 "indexer's record and the SEP's bibliography are the two records of its pages read",
     "excerpts": []},
    {"what": "the publisher's record of the reprint, chapter 10 of Hare's Essays on Bioethics (Oxford University Press, "
             "1993, through Crossref)",
     "url": "https://api.crossref.org/works/10.1093/oso/9780198239833.003.0010",
     "supports": "the reprint: 'Abortion and the Golden Rule', Essays On Bioethics, pp. 147-167, 1993. Its abstract is "
                 "the chapter's opening section (10.1), which does not reach the golden-rule step",
     "excerpts": []},
    {"what": "the MEDLINE record of Hare 1988 (PMID 11651921), with the Kennedy Institute of Ethics' abstract, read "
             "through NCBI E-utilities",
     "url": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=11651921&rettype=abstract&retmode=text",
     "supports": "the bound: the population grows while the total grows, the shares held, until the worst-off reach "
                 "the break-even point",
     "excerpts": ["increasing the population of a society while increasing the total utility",
                  "without altering its proportionate distribution",
                  "until the lowest segment of the population comes below the break-even point",
                  "at which life is just worth living"]},
    {"what": "the publisher's record of Essays on Bioethics (Oxford University Press, 1993, through Crossref)",
     "url": "https://api.crossref.org/works/10.1093/oso/9780198239833.001.0001",
     "supports": "the harm clause, unchanged from v0_1",
     "excerpts": ["we can harm possible people by preventing them from becoming actual people"]},
    {"what": "the publisher's record of Hare 1988 (Wiley, through Crossref)",
     "url": "https://api.crossref.org/works/10.1111/j.1467-8519.1988.tb00055.x",
     "supports": "the second citation: Possible People, Bioethics 2(4), October 1988, pp. 279-293. No abstract",
     "excerpts": []}]
NOT_READ = ("The full text of either paper and of their reprints. The statement claims only what the six records above "
            "support. Checked 2026-10-04 (V5); the builder does not re-fetch them.")


def md5b(b):
    return hashlib.md5(b).hexdigest()


def at(rel, m):
    return pinned.bytes_at(REPO, rel, m)


def dump(o):
    return (json.dumps(o, indent=1, ensure_ascii=False) + "\n").encode("utf-8")


def scholar_lines():
    repo = os.path.expanduser(SCHOLAR["repo"])
    if not os.path.isdir(os.path.join(repo, ".git")):
        print("note: the game's repository is absent; the scholar quotes were not re-read (bytes unaffected)")
        return None
    raw = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (SCHOLAR["commit"], SCHOLAR["file"])],
                         capture_output=True, check=True).stdout
    assert md5b(raw) == SCHOLAR["md5"], "the scholar layer at the pinned commit is not the pinned bytes"
    return {n["id"]: n["scholar_objection"] for n in json.loads(raw.decode("utf-8"))["nodes"]}


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
    r = {"rc": p.returncode, "verdict": tail["verdict"], "violation_count": tail["violation_count"],
         "shapes": tail["shapes"], "nodes_with_shapes": tail["nodes_with_shapes"]}
    if tail["verdict"] != "PASS":  # the per-check report lines: "FAIL . <check> (n ok / m fail)"
        r["failed"] = sorted(ln.split(" . ", 1)[1].split(" (", 1)[0] for ln in out.splitlines()
                             if ln.startswith("FAIL . "))
    return r


def build():
    pilot = json.loads(at(*PILOT).decode("utf-8"))
    jrec = json.loads(at(*JUDGMENTS).decode("utf-8"))
    v01 = json.loads(at(*V01).decode("utf-8"))
    v01rec = json.loads(at(*V01_RECORD).decode("utf-8"))
    rj = json.loads(at(*RJUDG).decode("utf-8"))
    corpus = json.loads(at(*CORPUS).decode("utf-8"))
    cmap = json.loads(at(*MAP).decode("utf-8"))
    reg = json.loads(at(*REGISTER).decode("utf-8"))
    words = json.loads(at(*WORDS).decode("utf-8"))
    for rel, m in (VALIDATOR, RJGATE):
        assert md5b(open(os.path.join(REPO, rel), "rb").read()) == m, "%s moved" % rel
    assert rj["judged"]["redrafts"]["md5"] == V01[1] and rj["judged"]["redrafts_record"]["md5"] == V01_RECORD[1]
    assert rj["judged"]["pilot"]["md5"] == PILOT[1] and v01rec["pins"]["redrafts"]["md5"] == V01[1]
    O = {o["id"]: o for o in corpus["objections"]}
    E = cmap["entries"]
    rows_j = {r["id"]: r for r in rj["rows"]}
    j = rows_j["RJ-001"]
    assert j["kind"] == "shape" and j["shape_id"] == SHAPE_ID and j["verdict"] == "AMEND" and j["class_judged"] == "d"
    assert j["redraft"] == "RD-01" and j["supersedes"] is None
    later = [r for r in rj["rows"] if r.get("supersedes") == "RJ-001"]
    assert not later, "RJ-001 has been superseded in gate2's record"
    word = words["excerpts"]["R0314_word"]
    assert md5b(word["text"].encode("utf-8")) == word["md5"]

    base_rd = {r["id"]: r for r in v01rec["rows"]}["RD-01"]
    base = {s["shape_id"]: s for s in v01["shapes"]}[SHAPE_ID]
    new = dict(base)
    new.update({"statement": STATEMENT, "attested_by": ATTESTED_BY, "provenance": dict(PROV)})
    new = {k: new[k] for k in base}  # v0_1's key order, which is the pilot's
    changed = sorted(k for k in base if base[k] != new[k])
    assert changed == ["attested_by", "provenance", "statement"], changed  # owed: the statement and the attestation
    assert new["class"] == "d" and new["answered_by"] == [] and new["differs_by"] == base["differs_by"]
    assert 30 <= SV.wc(STATEMENT) <= 70 and STATEMENT.isascii() and all(a["citation"].isascii() for a in ATTESTED_BY)
    assert ATTESTED_BY[1] == base["attested_by"][0], "the 1988 citation is v0_1's, carried"

    # the terminus: copied from the registered (d) the line reaches, and from the register; never typed
    n, loc, anc = "joy-outweighs-harms", "long", base_rd["terminus"]["via_anchor"]
    assert anc in SV.locus_text(O[n], loc), "the terminus anchor is not at %s#%s" % (n, loc)
    hit = [i for i, e in enumerate(E) if (e["target_id"], e["target_locus"], e["target_anchor"]) == (n, loc, anc)]
    assert len(hit) == 1 and E[hit[0]]["class"] == "d"
    idx, e = hit[0], E[hit[0]]
    found = [(b["bedrock_id"], b["name"], f["facet_id"]) for b in reg["bedrocks"] for f in b["facets"]
             for t in f["tributaries"] if (t.get("node"), t.get("locus"), t.get("anchor")) == (n, loc, anc)]
    assert len(found) == 1
    hr, name, facet = found[0]
    terminus = {"via": "%s#%s" % (n, loc), "via_anchor": anc,
                "bedrock": {"bedrock_name": e["routing"]["residue"]["bedrock_name"],
                            "terminus_routing": e["routing"]["residue"]["terminus_routing"],
                            "register": {"bedrock_id": hr, "name": name, "facet": facet}},
                "copied_from": {"map_entry": idx, "register": "%s / %s" % (hr, facet)}}
    assert j["route"] == {"via": terminus["via"], "via_anchor": anc, "bedrock": terminus["bedrock"]}, "route moved"
    assert terminus == base_rd["terminus"], "the route is not v0_1's"

    # the premise-sharers: population-ethics-paradoxes has exactly one map entry, a (d) at its long
    pep = [i for i, x in enumerate(E) if x["target_id"] == "population-ethics-paradoxes"]
    joy = [i for i, x in enumerate(E) if x["target_id"] == "joy-outweighs-harms"]
    assert pep == [109] and E[109]["class"] == "d" and E[109]["target_locus"] == "long", pep
    assert joy == [41], joy
    sch = scholar_lines()
    quotes = []
    for src, a, b, q in QUOTES + PULL_QUOTES:
        if src == "statement":
            assert q in STATEMENT, q
            tag = "statement:%s" % SHAPE_ID
        elif src == "corpus":
            assert q in SV.locus_text(O[a], b), (a, b, q)
            tag = "corpus:%s#%s" % (a, b)
        elif src == "map":
            assert q in E[a][b], (a, b, q)
            tag = "map:#%d.%s" % (a, b)
        else:
            if sch is not None:
                assert q in sch[a], (a, q)
            tag = "scholar:%s" % a
        assert len(q.split()) <= 15, q
        quotes.append({"src": tag, "quote": q})
    for q in quotes[:len(QUOTES)]:
        assert '"%s"' % q["quote"] in READING, q
    pulls_text = " ".join(PULLS)
    for q in quotes[len(QUOTES):]:
        assert '"%s"' % q["quote"] in pulls_text, q
    for s in SOURCES:
        assert all(SV.wc(x) < 15 for x in s["excerpts"])

    doc = {"meta": {"source_corpus_md5": CORPUS[1], "source_corpus_objections_md5": SV.objections_digest(corpus),
                    "bound_for": "staging", "shape_coverage": "1/%d" % len(O)}, "shapes": [new]}
    assert doc["meta"]["source_corpus_objections_md5"] == v01["meta"]["source_corpus_objections_md5"]
    out = dump(doc)

    # the resolved views
    soul = {s["shape_id"]: s for s in v01["shapes"]}["free-will-defense/a-vale-of-soul-making"]
    repl = {SHAPE_ID: new, soul["shape_id"]: soul}
    superseded = [repl.get(s["shape_id"], s) for s in pilot["shapes"]]
    kept_ids = v01rec["validator_runs"]["ruled_view"]["shape_ids"]
    ruled = [s for s in superseded if s["shape_id"] in kept_ids]
    assert [s["shape_id"] for s in ruled] == kept_ids
    assert rows_j["RJ-002"]["verdict"] == "ACCEPT" and rows_j["RJ-002"]["shape_id"] == soul["shape_id"]

    def view(ss):
        nodes = {s["shape_id"].split("/")[0] for s in ss}
        return {"meta": dict(doc["meta"], shape_coverage="%d/%d" % (len(nodes), len(O))), "shapes": ss}

    together = {"meta": dict(doc["meta"], shape_coverage=pilot["meta"]["shape_coverage"]),
                "shapes": pilot["shapes"] + [new]}
    scratch = tempfile.mkdtemp(prefix="shapes_redrafts_v0_2_")
    try:
        runs = {}
        for nm, payload in (("redraft_alone", out), ("superseded_view", dump(view(superseded))),
                            ("ruled_view", dump(view(ruled))), ("pilot_and_this_file_together", dump(together))):
            path = os.path.join(scratch, nm + ".json")
            open(path, "wb").write(payload)
            runs[nm] = run_validator(path, scratch)
        for nm in ("redraft_alone", "superseded_view", "ruled_view"):
            assert runs[nm]["rc"] == 0 and runs[nm]["verdict"] == "PASS" and runs[nm]["violation_count"] == 0, \
                (nm, runs[nm])
        t = runs["pilot_and_this_file_together"]
        assert t["verdict"] == "FAIL" and "shape-id" in t["failed"], t
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    runs["redraft_alone"]["file"] = OUT
    runs["superseded_view"]["what"] = ("the pilot's ten shapes in its order, the golden rule replaced by this row and "
                                       "soul-making by v0_1's RD-02")
    runs["ruled_view"]["what"] = ("the shapes his words kept: gate2's five round-one ACCEPTs, soul-making (v0_1's RD-02, "
                                  "ACCEPT at RJ-002) and this row")
    runs["ruled_view"]["shape_ids"] = kept_ids
    runs["pilot_and_this_file_together"]["what"] = "a control: the pilot and this file loaded as one must fail on shape-id"
    cls = {}
    for s in ruled:
        cls[s["class"]] = cls.get(s["class"], 0) + 1

    row = {"id": "RD-03", "shape_id": SHAPE_ID,
           "answers": {"row": j["id"], "verdict": j["verdict"], "owed": j["owed"]},
           "supersedes": {"file": V01[0], "md5": V01[1], "row": "RD-01", "shape_id": SHAPE_ID},
           "changed": changed, "class": new["class"],
           "words": {"pilot": SV.wc({s["shape_id"]: s for s in pilot["shapes"]}[SHAPE_ID]["statement"]),
                     "v0_1": SV.wc(base["statement"]), "redraft": SV.wc(STATEMENT)},
           "owed_met": {"the total as a limit on the duty": "so long as the total good grows",
                        "the shares held as they are": "the shares held as they are",
                        "the halt before the worst-off fall below a life just worth living":
                            "stopping before the worst-off fall below a life just worth living",
                        "the duty's ground stays the possible person's own good":
                            "A possible person who would be glad to exist is harmed if never created",
                        "Hare 1975 added": ATTESTED_BY[0]["citation"]},
           "terminus": terminus, "route_equals_the_judged_route": True, "route_equals_v0_1": True,
           "premise_sharers_read": {
               "population-ethics-paradoxes": {"loci": ["trigger", "diagnosis", "short", "medium", "long"],
                                               "map_entries": pep, "scholar": SCHOLAR["file"] + " at " + SCHOLAR["commit"][:8]},
               "joy-outweighs-harms#long": {"horns": "the fork (pure aggregation or the side-constraint) and the "
                                                     "two horns of the strongest reply (expected value; the actual "
                                                     "person's actual balance)",
                                            "map_entries": joy, "scholar": SCHOLAR["file"] + " at " + SCHOLAR["commit"][:8]},
               "rights-future-generations#long": {"why": "the reductio v0_1 was read against"}},
           "reading": READING, "quotes": quotes, "pulls": PULLS, "sources_checked": SOURCES, "not_read": NOT_READ}
    for k, v in row["owed_met"].items():
        assert k == "Hare 1975 added" or v in STATEMENT, k

    record = {
        "what": ("the golden rule's third pass, owed by gate2's round-two judgment (RJ-001), V5, seat l, 2026-10-04; "
                 "drafted, not judged"),
        "state": "DRAFTED, NOT JUDGED. gate2 judges this row in its next round (K258); his word decides.",
        "authority": {"his_word": word["text"], "turn_md5": word["turn"]["turn_md5"], "utc": word["turn"]["utc"],
                      "answers": "R0314", "from": "%s at %s" % WORDS,
                      "adopted": ("gate2's three round-two asks: the judgment; soul-making to the map's (d)s; this pass "
                                  "folded into seat l's next session and judged in gate2's next round")},
        "supersession": ("RD-03 supersedes v0_1's RD-01 (file and md5 below), which superseded the pilot's shape of the "
                         "same id. v0_1 and the pilot stay byte-identical (gate2's gates pin them), so this file repeats "
                         "the id and validates alone. The current set is the pilot with the golden rule replaced by RD-03 "
                         "and soul-making by v0_1's RD-02: 'superseded_view' below. Loading the pilot and this file "
                         "together fails shape-id, as it should."),
        "pins": {"redraft": {"file": OUT, "md5": md5b(out), "bytes": len(out)},
                 "replaces": dict(zip(("file", "md5"), V01)), "replaces_record": dict(zip(("file", "md5"), V01_RECORD)),
                 "judgment": dict(zip(("file", "md5"), RJUDG)), "judgment_gate": dict(zip(("file", "md5"), RJGATE)),
                 "pilot": dict(zip(("file", "md5"), PILOT)), "pilot_judgments": dict(zip(("file", "md5"), JUDGMENTS)),
                 "corpus": dict(zip(("file", "md5"), CORPUS)), "map": dict(zip(("file", "md5"), MAP)),
                 "register": dict(zip(("file", "md5"), REGISTER)), "validator": dict(zip(("file", "md5"), VALIDATOR)),
                 "his_words": dict(zip(("file", "md5"), WORDS)), "scholar": SCHOLAR},
        "rows": [row],
        "validator_runs": runs,
        "after_round_three": {"ruled_set_classes": dict(sorted(cls.items())),
                              "routes": ("(d)s to the map at the successor map's next validator bump (many-peaks, "
                                         "heroism and soul-making now; the golden rule once gate2 accepts this row); "
                                         "the (a) to the corpus in V4 after the successor map's pin; the (b) to the "
                                         "regen queue; the (c) to the intake")},
        "not_moved": ("the pilot, V2b's redrafts and their record and builder, gate2's records, gates and readings, the "
                      "validator, its control and the schema; no corpus or served byte")}
    return out, dump(record)


def main():
    out, rec = build()
    if "--check" in sys.argv:
        ok = (open(os.path.join(REPO, OUT), "rb").read() == out and open(os.path.join(REPO, RECORD), "rb").read() == rec)
        print("SHAPES REDRAFTS v0_2: %s" % ("matches the committed redraft and record" if ok else "DIFFERS"))
        sys.exit(0 if ok else 1)
    open(os.path.join(REPO, OUT), "wb").write(out)
    open(os.path.join(REPO, RECORD), "wb").write(rec)
    print("%s  %s / %d" % (OUT, md5b(out), len(out)))
    print("%s  %s / %d" % (RECORD, md5b(rec), len(rec)))


if __name__ == "__main__":
    main()

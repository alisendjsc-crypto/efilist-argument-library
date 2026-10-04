#!/usr/bin/env python3
"""relief_variants_judgments_gate.py -- the gate on gate2's judgment of V7's relief variant pilot (V8, 2026-10-04).

K258: gate2 drafted none of the pilot, its record, its builder, the checker or canon v38.54. This gate is gate2's own
code: it never imports the drafter's builder. It imports the checker (response_variant_validator_v0_1.py, V6) only for
its word count, and runs it, in its own process group with TMPDIR in scratch, for the validator figure.

GREEN only if response_variants/relief_variants_judgments.json is what its header says it is:
  pins      every referent the header pins resolves at its md5 (working tree or git history, via
            adversarial_map_staging/r1/pinned.py), the header pins equal this gate's, and the kickoff is R0320 at its md5
  his_word  his word in the header is verbatim at canon v38.54
  ids       row ids VJ-nnn, unique and in order; 'supersedes' names an earlier row of the same kind and target
  vocab     kinds and verdicts from the record's vocabulary; every row a seat and a date
  coverage  each variant in the pilot judged by exactly one standing variant row; each of the record's five pulls by one
            pull row carrying the pull verbatim; F1-F3 by one finding row each carrying the finding verbatim; the
            builder's checks, its controls, the source check, the Berridge check and the safety read by one row each
  owed      an AMEND owes lines; nothing else owes anything
  quotes    every double-quoted span in a row's text is declared in its quotes, every declared quote is used, and each
            is verbatim at its pinned source; a web: quote is at most 15 words and its url is in the row's 'checked' list
  figures   every figure a row states is recomputed here from the pinned bytes: words, quotes and the accounts they come
            from, anchors and concession spans in the pinned corpus, the residual clause, attribution by role, the
            label, Berridge's scope, a floor read, the validator run, the builder's checks and controls
  history   append-only: every committed version's rows are a prefix of today's, and its header is today's (the state
            line excepted)

  python3 response_variants/relief_variants_judgments_gate.py [--self-test [--write]] [--turns] [--figures]

--turns reads his ten accounts at their user turns in the two transcripts canon names (L8, vault_V2) with gate2's own
reader: exit 0 if each turn has the md5 canon gives, at the line canon names, and holds the verbatim; 2 if a transcript
is absent. It is never part of the gate's bytes. --figures prints the recomputed figures.
"""
import copy, hashlib, json, os, re, shutil, signal, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "adversarial_map_staging", "r1"))
import pinned  # noqa: E402

REL = "response_variants/relief_variants_judgments.json"
CONTROL = "response_variants/relief_variants_judgments_gate_control_v0_1.json"
KICKOFF = ("R0320", "e0ed9ab632807f71a9194be9d683e9aa")
INDEX = os.path.expanduser("~/Downloads/Claude Code/relays/RELAY_INDEX.tsv")
PINS = {
    "pilot": ("response_variants/relief_variants_pilot_v0_1.json", "1d5e8f1c65a387da495dba91edbee9e8"),
    "record": ("response_variants/relief_variants_record_v0_1.json", "1d8556443af14f95bff9e906f2a67037"),
    "builder": ("response_variants/build_relief_variants.py", "c5f02c47f1daf965f2dbd29bfa9aec9a"),
    "schema": ("response_variants/response_variants_schema_v0_1.json", "169c15b30f3fcc578689daa257d5b41f"),
    "validator": ("response_variants/response_variant_validator_v0_1.py", "30cb7f3bc4f9e81b0ff5c85ecfaacdf3"),
    "validator_control": ("response_variants/response_variant_validator_control_v0_1.json",
                          "44a77cc75a062fb6e4bac7b47aaec421"),
    "measurement": ("design/variations/measure_response_variants_v0_1.json", "cbae330fe2106d79d572de8e20ac8459"),
    "corpus": ("efilist_argument_library_v4_0_0.json", "7b6e65e531018fecb37baf2a4fedd6d1"),
    "canon_pinned": ("project_canon_v38_53.json", "4bc14ae1a5fc6103df820900642f9728"),
    "canon": ("project_canon_v38_54.json", "e0f3e2f695a43f18d0c90d6ce3e08748"),
}
TRANSCRIPTS = {
    "L8": "~/.claude/projects/-home-josiahscooper-Projects-efilist-argument-library/"
          "87cc1d8f-fbf4-44dc-981f-9b205c311dbf.jsonl",
    "vault_V2": "~/.claude/projects/-home-josiahscooper-Documents-Obsidian-Vault/"
                "038df8e5-141f-4cb5-babe-d1c4caa5aaed.jsonl"}
RV = "adversarial_map.relief_view_for_the_variant"
KINDS = {"variant", "checks", "controls", "source", "finding", "pull", "berridge", "safety", "note", "found"}
VERDICT_KINDS = KINDS - {"found"}
VARIANT_VERDICTS = {"ACCEPT", "AMEND", "REJECT"}
OTHER_VERDICTS = {"CONFIRM", "CORRECT"}
SINGLE = ("checks", "controls", "source", "berridge", "safety")
NO_SPAN = {"id", "kind", "variant_id", "node", "verdict", "seat", "date", "supersedes", "quotes", "figures",
           "checked", "pull", "pull_text", "finding_id", "finding_text", "account", "tier", "razor_node"}
WEB_MAX_WORDS = 15
NAMES = re.compile(r"\b(?:Josiah|josiah|WULD|Wuld|wuld\.ink|AnomicIndividual87|Evilis|Anihilis|Uls)\b")
PRONOUNS = re.compile(r"\b(?:he|him|his|himself|she|her|hers|herself)\b", re.I)
LABEL = re.compile(r"another answer|chosen line", re.I)
# gate2's own floor read, independent of the checker's: words a reader in crisis could take for an argument for or
# against staying alive, or for harm. A hit is read in its sentence; a floor is not a census.
FLOOR = ("worth living", "life is good", "life is a gift", "gift of life", "precious", "matters", "get better",
         "hope", "kill", "suicid", "self-harm", "self-injur", "die", "dying", "death", "dead", "end it",
         "harm yourself", "drown", "tortur")


def md5b(b):
    return hashlib.md5(b).hexdigest()


def walk(obj, path):
    for p in path.split("."):
        obj = obj[int(p)] if isinstance(obj, list) else obj[p]
    return obj


def run_tool(args):
    scratch = tempfile.mkdtemp(prefix="v8_gate_")
    try:
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=scratch)
        p = subprocess.Popen([sys.executable] + args, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             text=True, env=env, start_new_session=True)
        try:
            out, _ = p.communicate(timeout=600)
        except subprocess.TimeoutExpired:
            os.killpg(p.pid, signal.SIGKILL)
            raise LookupError("%s timed out" % args[0])
        return p.returncode, out
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def residual_clause(canon):
    s = walk(canon, RV + ".the_open_residual")
    return re.search(r"seat's: (whether .*?)\. Neither", s).group(1)


class Sources:
    def __init__(self):
        raw = {k: pinned.bytes_at(REPO, *v) for k, v in PINS.items()}
        j = lambda k: json.loads(raw[k].decode("utf-8"))  # noqa: E731
        self.pilot = j("pilot")
        self.variants = {v["variant_id"]: v for v in self.pilot["variants"]}
        self.record = j("record")
        self.rvars = {v["variant_id"]: v for v in self.record["variants"]}
        self.measure = j("measurement")
        self.corpus = {o["id"]: o for o in j("corpus")["objections"]}
        self.canon = j("canon")
        self.canon_pinned = j("canon_pinned")
        self.accounts = [a["verbatim"] for a in walk(self.canon, RV + ".his_accounts_verbatim")]
        self.accounts_pinned = [a["verbatim"] for a in walk(self.canon_pinned, RV + ".his_accounts_verbatim")]
        self.figures = compute_figures(self)

    def locus(self, node, slot):
        o = self.corpus[node]
        if slot in ("trigger", "diagnosis"):
            return o[slot]
        return o["responses"][slot]

    def text(self, src):
        kind, ref = src.split(":", 1)
        if kind == "pilot":
            vid, path = ref.split(".", 1)
            v = walk(self.variants[vid], path)
        elif kind == "record":
            v = walk(self.record, ref)
        elif kind == "canon":
            v = walk(self.canon, ref)
        elif kind == "measure":
            v = walk(self.measure, ref)
        elif kind == "corpus":
            node, slot = ref.split("#", 1)
            v = self.locus(node, slot)
        else:
            raise KeyError(kind)
        return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)


def validator_figure():
    rc, out = run_tool([PINS["validator"][0], PINS["pilot"][0]])
    try:
        tail = json.loads(out[out.rfind("\n{") + 1:])
    except ValueError:
        raise LookupError("the validator's summary does not parse (rc %d)" % rc)
    return {"rc": rc, "verdict": tail["verdict"], "violation_count": tail["violation_count"],
            "variants": tail["variants"], "nodes_with_variants": tail["nodes_with_variants"]}


def compute_figures(S):
    if md5b(open(os.path.join(REPO, PINS["validator"][0]), "rb").read()) != PINS["validator"][1]:
        raise LookupError("the validator in the working tree is not the one pinned (%s)" % PINS["validator"][1][:8])
    sys.path.insert(0, HERE)
    import response_variant_validator_v0_1 as RVV  # the checker, for its word count only
    clause = residual_clause(S.canon)
    F = {}
    for vid, v in S.variants.items():
        node = vid.split("/")[0]
        text, res = v["text"], v["residual"]
        named = sorted(int(re.search(r"\[(\d+)\]$", a["canon"]).group(1)) for a in v["account_sources"])
        qs = re.findall(r'"([^"]+)"', text) + re.findall(r'"([^"]+)"', res["concedes"]["account"])
        long_ = S.locus(node, "long")
        everything = text + " " + json.dumps(res, ensure_ascii=False)
        F[vid] = {
            "words": RVV.wc(text),
            "quotes": len(qs),
            "quotes_exact": all(any(q in S.accounts[i] for i in named) for q in qs),
            "accounts_named": named,
            "accounts_quoted": sorted({i for i in named for q in qs if q in S.accounts[i]}),
            "anchor_in_long": v["varies"]["anchor"] in long_,
            "anchor_is_measured": v["varies"]["anchor"] == S.measure["nodes"][node]["anchor"],
            "concession_spans_in_long": all(s in long_ for s in S.rvars[vid]["library_concession_rests_on"]),
            "residual_clause_copied": res["where_both_stop"] == "Both sides stop at %s." % clause,
            "ends_on_the_residual": text.endswith("Both sides stop, open, at %s." % clause),
            "status": res["status"],
            "by_role": text.lower().count("the library's author"),
            "names": len(NAMES.findall(everything)),
            "pronouns": len(PRONOUNS.findall(text)),
            "label_words": len(LABEL.findall(everything)),
            "berridge": text.count("Berridge"),
            "neutral": text.count("neutral"),
            "base_state": text.count("base state"),
            "floor": sorted({f for f in FLOOR if f in everything.lower()}),
        }
        F[vid]["sources_used"] = F[vid]["accounts_quoted"] == named
    words = [F[vid]["words"] for vid in S.variants]
    F["totals"] = {"variants": len(words), "min": min(words), "max": max(words), "words": sum(words),
                   "nodes": [vid.split("/")[0] for vid in S.variants],
                   "nodes_are_RV_7": [vid.split("/")[0] for vid in S.variants] ==
                   walk(S.canon, "adversarial_map.response_variants_rulings_V6.nodes_RV_7")}
    F["accounts"] = {"n": len(S.accounts), "same_at_the_pinned_canon": S.accounts == S.accounts_pinned,
                     "ascii": all(a.isascii() for a in S.accounts)}
    checks = sorted(S.record["builder_checks"])
    controlled = sorted({c for x in S.record["controls"] for c in x["expect_red"]})
    F["builder"] = {"checks": checks, "green": sorted(k for k, v in S.record["builder_checks"].items()
                                                      if v.startswith("GREEN")),
                    "controls": len(S.record["controls"]) - 1, "controlled": controlled,
                    "uncontrolled": [c for c in checks if c not in controlled],
                    "c0_first": S.record["controls"][0]["case"] == "C0" and S.record["controls"][0]["expect_red"] == [],
                    "each_trips_only_its_own": all(x["red"] == x["expect_red"] and len(x["expect_red"]) <= 1
                                                   for x in S.record["controls"])}
    F["berridge"] = {"variants_citing": [vid for vid in S.variants if "Berridge" in S.variants[vid]["text"]]}
    F["validator"] = validator_figure()
    return F


def figure(F, path):
    head, _, rest = path.partition(".")
    obj = F[head]
    for p in rest.split(".") if rest else []:
        obj = obj[int(p)] if isinstance(obj, list) else obj[p]
    return obj


def spans(row):
    out = []

    def go(v, key=None):
        if key in NO_SPAN:
            return
        if isinstance(v, str):
            out.extend(re.findall(r'"([^"]+)"', v))
        elif isinstance(v, list):
            for x in v:
                go(x)
        elif isinstance(v, dict):
            for k, x in v.items():
                go(x, k)
    for k, v in row.items():
        go(v, k)
    return out


def check(rec, S, history):
    red = {}

    def fail(name, msg):
        red.setdefault(name, []).append(msg)

    # pins
    J = rec.get("judged", {})
    for k, (rel, m) in PINS.items():
        if J.get(k) != {"file": rel, "md5": m}:
            fail("pins", "header pin %s is not the gate's" % k)
    if set(J) != set(PINS):
        fail("pins", "header pins a referent the gate does not")
    if rec.get("kickoff") != {"relay": KICKOFF[0], "md5": KICKOFF[1]}:
        fail("pins", "kickoff relay")
    for w in rec.get("his_word", []):
        try:
            if S.text(w["src"]) != w["verbatim"]:
                fail("his_word", "not verbatim at %s" % w["src"])
        except (KeyError, IndexError, ValueError):
            fail("his_word", "no source %s" % w["src"])

    rows = rec.get("rows", [])
    # ids
    ids = [r.get("id") for r in rows]
    if len(set(ids)) != len(ids) or any(not re.fullmatch(r"VJ-\d{3}", str(i)) for i in ids) or ids != sorted(ids):
        fail("ids", "row ids not unique, well-formed and in order")
    seen = {}
    for r in rows:
        s = r.get("supersedes")
        if s is not None:
            o = seen.get(s)
            if not o or o.get("kind") != r.get("kind") or o.get("variant_id") != r.get("variant_id"):
                fail("ids", "%s supersedes %s, which is not an earlier row of its kind" % (r.get("id"), s))
        seen[r.get("id")] = r
    superseded = {r["supersedes"] for r in rows if r.get("supersedes")}
    standing = [r for r in rows if r.get("id") not in superseded]

    # vocab
    for r in rows:
        k = r.get("kind")
        if k not in KINDS:
            fail("vocab", "%s: kind %r" % (r.get("id"), k))
        if k == "variant" and r.get("verdict") not in VARIANT_VERDICTS:
            fail("vocab", "%s: a variant verdict is ACCEPT, AMEND or REJECT" % r.get("id"))
        elif k in VERDICT_KINDS - {"variant"} and r.get("verdict") not in OTHER_VERDICTS:
            fail("vocab", "%s: verdict %r" % (r.get("id"), r.get("verdict")))
        elif k not in VERDICT_KINDS and "verdict" in r:
            fail("vocab", "%s: a %s row carries no verdict" % (r.get("id"), k))
        if not r.get("seat") or not r.get("date"):
            fail("vocab", "%s: seat and date" % r.get("id"))

    # coverage
    got = sorted(str(r.get("variant_id")) for r in standing if r.get("kind") == "variant")
    if got != sorted(S.variants):
        fail("coverage", "standing variant rows %s != the pilot's %s" % (got, sorted(S.variants)))
    for r in standing:
        if r.get("kind") == "variant" and r.get("variant_id") in S.variants and r.get("node") != r["variant_id"].split("/")[0]:
            fail("coverage", "%s: node is not the variant's" % r.get("id"))
    pulls = S.record["pulls_for_gate2"]
    prow = [r for r in standing if r.get("kind") == "pull"]
    if sorted(r.get("pull") for r in prow if isinstance(r.get("pull"), int)) != list(range(len(pulls))) or \
            len(prow) != len(pulls):
        fail("coverage", "standing pull rows do not cover the record's %d pulls once each" % len(pulls))
    for r in prow:
        i = r.get("pull")
        if not isinstance(i, int) or not 0 <= i < len(pulls) or r.get("pull_text") != pulls[i]:
            fail("coverage", "%s: the pull is not carried verbatim" % r.get("id"))
    found = {f["id"]: f["finding"] for f in S.record["found"]}
    frow = [r for r in standing if r.get("kind") == "finding"]
    if sorted(str(r.get("finding_id")) for r in frow) != sorted(found):
        fail("coverage", "standing finding rows do not cover %s once each" % sorted(found))
    for r in frow:
        if found.get(r.get("finding_id")) != r.get("finding_text"):
            fail("coverage", "%s: the finding is not carried verbatim" % r.get("id"))
    for k in SINGLE:
        if sum(1 for r in standing if r.get("kind") == k) != 1:
            fail("coverage", "one standing %s row" % k)

    # owed
    for r in rows:
        if (r.get("verdict") == "AMEND") != bool(r.get("owed")):
            fail("owed", "%s: an AMEND owes lines; nothing else owes anything" % r.get("id"))

    # quotes
    for r in rows:
        declared = [q.get("quote") for q in r.get("quotes", [])]
        used = spans(r)
        for sp in used:
            if sp not in declared:
                fail("quotes", "%s: undeclared span %r" % (r.get("id"), sp[:40]))
        for q in r.get("quotes", []):
            if q.get("quote") not in used:
                fail("quotes", "%s: declared quote not used %r" % (r.get("id"), str(q.get("quote"))[:40]))
            src = str(q.get("src"))
            if src.startswith("web:"):
                url = src[4:]
                if (len(str(q.get("quote")).split()) > WEB_MAX_WORDS or
                        not any(c == url or c.startswith(url + " ") for c in r.get("checked", []))):
                    fail("quotes", "%s: web quote over %d words or its url unchecked" % (r.get("id"), WEB_MAX_WORDS))
                continue
            try:
                if q["quote"] not in S.text(src):
                    fail("quotes", "%s: not verbatim at %s" % (r.get("id"), src))
            except (KeyError, IndexError, ValueError, AttributeError):
                fail("quotes", "%s: no source %s" % (r.get("id"), src))

    # figures
    for r in rows:
        for path, val in (r.get("figures") or {}).items():
            try:
                if figure(S.figures, path) != val:
                    fail("figures", "%s: %s is not the recomputed figure" % (r.get("id"), path))
            except (KeyError, TypeError, IndexError, ValueError):
                fail("figures", "%s: no figure %s" % (r.get("id"), path))

    # history
    head = {k: v for k, v in rec.items() if k not in ("rows", "state")}
    for old in history:
        if {k: v for k, v in old.items() if k not in ("rows", "state")} != head:
            fail("history", "a committed header differs")
        if rows[:len(old.get("rows", []))] != old.get("rows", []):
            fail("history", "a committed row was edited or removed")
    return red


def committed_versions():
    out = subprocess.run(["git", "-C", REPO, "log", "--format=%H", "--", REL], capture_output=True, text=True).stdout
    vs = []
    for h in out.split():
        b = subprocess.run(["git", "-C", REPO, "show", "%s:%s" % (h, REL)], capture_output=True).stdout
        if b:
            vs.append(json.loads(b.decode("utf-8")))
    return vs


def kickoff_index():
    if os.path.exists(INDEX):
        for line in open(INDEX, encoding="utf-8"):
            f = line.rstrip("\n").split("\t")
            if len(f) > 8 and f[1] == "SENT" and f[2] == KICKOFF[0]:
                return f[8] == KICKOFF[1]
    return True


def human_turns(path):
    """gate2's own reader: {md5: [(line, text)]} for every human-typed user turn (string content, or text blocks
    without a tool result)."""
    out = {}
    with open(path, encoding="utf-8") as f:
        for ln, raw in enumerate(f, 1):
            try:
                o = json.loads(raw)
            except ValueError:
                continue
            m = o.get("message") or {}
            if o.get("type") != "user" or m.get("role") != "user":
                continue
            c = m.get("content")
            if isinstance(c, list):
                if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in c):
                    continue
                c = "".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
            if isinstance(c, str):
                out.setdefault(md5b(c.encode("utf-8")), []).append((ln, c))
    return out


def turns(S):
    accts = walk(S.canon, RV + ".his_accounts_verbatim")
    have = {k: os.path.expanduser(p) for k, p in TRANSCRIPTS.items()}
    if not all(os.path.exists(p) for p in have.values()):
        print("TURNS: a transcript is absent here; not read")
        return 2
    T = {k: human_turns(p) for k, p in have.items()}
    ok = 0
    for i, a in enumerate(accts):
        key = "L8" if "L8 transcript" in a["said"] else "vault_V2"
        line = int(a["said"].rsplit("line ", 1)[1])
        hits = T[key].get(a["turn_md5"], [])
        at = [t for ln, t in hits if ln == line]
        good = len(hits) == 1 and len(at) == 1 and a["verbatim"] in at[0]
        off = at[0].find(a["verbatim"]) if at else -1
        ok += good
        print("%s [%d] %s line %d turn %s offsets %d..%d" % ("GREEN" if good else "RED  ", i, key, line,
                                                            a["turn_md5"][:8], off, off + len(a["verbatim"])))
    print("TURNS: %d of %d accounts at their user turns" % (ok, len(accts)))
    return 0 if ok == len(accts) else 1


def _row(r, rid):
    return next(x for x in r["rows"] if x["id"] == rid)


def _first(r, kind, **kw):
    return next(x for x in r["rows"] if x.get("kind") == kind and all(x.get(k) == v for k, v in kw.items()))


MUTATIONS = [
    ("unmutated", lambda r: None, []),
    ("verdict out of vocabulary", lambda r: _first(r, "variant").update(verdict="MAYBE"), ["vocab"]),
    ("a variant left unjudged", lambda r: r["rows"].remove(_first(r, "variant", node="hedonic-contrast")),
     ["coverage"]),
    ("a pull left unjudged", lambda r: r["rows"].remove(_first(r, "pull", pull=4)), ["coverage"]),
    ("a pull not carried verbatim", lambda r: _first(r, "pull", pull=1).update(
        pull_text=_first(r, "pull", pull=1)["pull_text"][:-1]), ["coverage"]),
    ("a finding left unjudged", lambda r: r["rows"].remove(_first(r, "finding", finding_id="F2")), ["coverage"]),
    ("a quote off by one character", lambda r: _first(r, "variant", node="life-gift")["quotes"][0].update(
        quote=_first(r, "variant", node="life-gift")["quotes"][0]["quote"] + "s"), ["quotes"]),
    ("an undeclared quoted span", lambda r: _first(r, "variant", node="love-beauty-art").update(
        reason=_first(r, "variant", node="love-beauty-art")["reason"] + ' "invented"'), ["quotes"]),
    ("a web quote from an unchecked url", lambda r: next(
        q for q in _first(r, "berridge")["quotes"] if q["src"].startswith("web:")).update(src="web:https://example.org/"),
     ["quotes"]),
    ("a pin moved", lambda r: r["judged"]["corpus"].update(md5="0" * 32), ["pins"]),
    ("an AMEND owing nothing", lambda r: _first(r, "variant", verdict="AMEND").update(owed=[]), ["owed"]),
    ("an ACCEPT owing something", lambda r: _first(r, "variant", node="life-gift").update(owed=["something"]),
     ["owed"]),
    ("a figure not recomputed", lambda r: _first(r, "variant", node="neuroscience-positive-states")["figures"].update(
        {"neuroscience-positive-states/relief-account.berridge": 2}), ["figures"]),
    ("a duplicate id", lambda r: _first(r, "variant", node="joy-outweighs-harms").update(id="VJ-001"), ["ids"]),
    ("supersedes names no earlier row", lambda r: _first(r, "safety").update(supersedes="VJ-099"), ["ids"]),
    ("his word not verbatim", lambda r: r["his_word"][0].update(verbatim=r["his_word"][0]["verbatim"][:-1]),
     ["his_word"]),
    ("a committed row edited", "HISTORY", ["history"]),
]


def self_test(S, rec):
    results = []
    for name, mut, expect in MUTATIONS:
        r = copy.deepcopy(rec)
        hist = []
        if mut == "HISTORY":
            old = copy.deepcopy(rec)
            _first(old, "controls")["reason"] += " (an earlier wording)"
            hist = [old]
        else:
            mut(r)
        red = sorted(check(r, S, hist))
        results.append({"mutation": name, "expect_red": sorted(expect), "red": red, "as_expected": red == sorted(expect)})
    return {"what": "relief_variants_judgments_gate.py self-test: the unmutated record first, then one mutation per "
                    "check, each expected to trip its own check only",
            "record": REL, "cases": len(results), "as_expected": sum(x["as_expected"] for x in results),
            "results": results}


def main():
    try:
        S = Sources()
    except LookupError as e:
        print("RED pins      %s" % e)
        print("RELIEF VARIANTS JUDGMENTS GATE: RED (a pinned referent is unreadable)")
        sys.exit(1)
    if "--turns" in sys.argv:
        sys.exit(turns(S))
    if "--figures" in sys.argv:
        print(json.dumps(S.figures, indent=1, ensure_ascii=False))
        return
    rec = json.loads(open(os.path.join(REPO, REL), encoding="utf-8").read())
    if "--self-test" in sys.argv:
        out = (json.dumps(self_test(S, rec), indent=1, ensure_ascii=False) + "\n").encode("utf-8")
        path = os.path.join(REPO, CONTROL)
        if "--write" in sys.argv:
            open(path, "wb").write(out)
            print("SELF-TEST: wrote %s %s" % (CONTROL, md5b(out)))
            return
        ok = os.path.exists(path) and open(path, "rb").read() == out
        st = json.loads(out.decode("utf-8"))
        print("SELF-TEST: %d of %d as expected; control record %s" % (
            st["as_expected"], st["cases"], "matches" if ok else "DIFFERS"))
        sys.exit(0 if ok and st["as_expected"] == st["cases"] else 1)
    red = check(rec, S, committed_versions())
    if not kickoff_index():
        red.setdefault("pins", []).append("the relay index gives R0320 another md5")
    for name in ("pins", "his_word", "ids", "vocab", "coverage", "owed", "quotes", "figures", "history"):
        msgs = red.get(name, [])
        print("%-5s %-9s %s" % ("RED" if msgs else "GREEN", name, "; ".join(msgs[:3]) if msgs else ""))
    n = len(rec.get("rows", []))
    print("RELIEF VARIANTS JUDGMENTS GATE: %s (%d rows)" % ("RED" if red else "GREEN", n))
    sys.exit(1 if red else 0)


if __name__ == "__main__":
    main()

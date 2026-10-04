#!/usr/bin/env python3
"""r1_quote_check_v0_2.py -- R1's quote check, reading each row's quotes against the evidence the row names (L7).

r1_quote_check.py (v0_1, kept byte-identical and imported here at its pinned bytes) resolves `corpus:` at the
corpus R1's evidence pins (04bf6482, pre-cut) and `map:` in v1_3. From R1-071 a row may be ruled on the L7 addendum
(R1_evidence_L7_addendum.json), which pins the successor v1_8 and the v4.1.5 corpus 7b6e65e5: such a row quotes
the text as it stands there, and v0_1 would read it against text that no longer says it. v0_2 resolves a row's
`corpus:` and `map:` quotes at the corpus and map its evidence pins; `canon:` and `register:` resolve as in v0_1.
So v0_1's `--rulings` and `--self-test` are RED by design once such a row exists, and v0_2 is the live check.

  python3 r1_quote_check_v0_2.py --rulings     # every map_record quote in R1_rulings.json, against its row's evidence
  python3 r1_quote_check_v0_2.py --self-test   # controls; the unmutated control runs first

Repo-relative; writes nothing.
"""
import hashlib, json, os, sys, types

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import pinned  # noqa: E402

R = "adversarial_map_staging/r1"
V01 = (R + "/r1_quote_check.py", "0439d9428ee41a5faec31a34a6562aea")
ADDENDUM = (R + "/R1_evidence_L7_addendum.json", "ba55917f971520743773f0eb6fb518ea")
RULINGS = R + "/R1_rulings.json"


def load_v01():
    src = pinned.bytes_at(REPO, *V01).decode("utf-8")
    mod = types.ModuleType("r1_quote_check_v0_1")
    mod.__file__ = os.path.join(REPO, V01[0])
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)
    return mod


Q = load_v01()


def addendum_texts():
    """v0_1's Texts, with corpus and map moved to the addendum's pins."""
    add = json.loads(pinned.bytes_at(REPO, *ADDENDUM).decode("utf-8"))
    t = Q.Texts(corpus_md5=add["inputs"]["corpus"]["md5"])
    mp = add["inputs"]["map"]
    t.map = json.loads(pinned.bytes_at(REPO, mp["file"], mp["md5"]).decode("utf-8"))["entries"]
    return t


def rulings_quotes_by_source():
    doc = json.load(open(os.path.join(REPO, RULINGS), encoding="utf-8"))
    ev_md5 = doc["evidence"]["md5"]
    out = {"evidence": [], "addendum": [], "neither": []}
    for r in doc["rows"]:
        key = "evidence" if r["evidence_md5"] == ev_md5 else "addendum" if r["evidence_md5"] == ADDENDUM[1] else "neither"
        for m in r.get("map_record") or []:
            out[key].append({"tag": "%s (#%s)" % (r["row"], r["n"]), "src": Q.at_to_src(m["at"]), "quote": m["quote"]})
    return out


def check_all(groups, t_ev, t_add):
    ok1, f1 = Q.check(groups["evidence"], t_ev)
    ok2, f2 = Q.check(groups["addendum"], t_add)
    f3 = ["%s: the row names neither R1's evidence nor the addendum" % q["tag"] for q in groups["neither"]]
    return ok1 + ok2, f1 + f2 + f3


def self_test():
    t_ev, t_add = Q.Texts(), addendum_texts()
    g = rulings_quotes_by_source()
    if not g["addendum"]:
        sys.exit("SELF-TEST: no row names the addendum yet; nothing to test the per-row source against")
    a0 = g["addendum"][0]

    def only_in_successor(q):
        """A corpus quote the cut wrote: absent from R1's pre-cut corpus at its locus. A quote of an unchanged sentence
        reads true against either corpus, so it cannot show that the source matters."""
        try:
            return not any(q["quote"] in t for t in t_ev.resolve(q["src"]))
        except KeyError:
            return True

    corpus_q = next((q for q in g["addendum"] if q["src"].startswith("corpus:") and only_in_successor(q)), None)
    if corpus_q is None:
        sys.exit("SELF-TEST: no addendum row quotes text the cut wrote; C2 would be vacuous")
    controls = [
        ("C0 unmutated: every rulings quote, each against its row's evidence", g, 0),
        ("C1 an addendum row's quote, one character changed",
         {"evidence": [], "addendum": [dict(a0, quote=a0["quote"][:-1] + ("X" if a0["quote"][-1] != "X" else "Y"))],
          "neither": []}, 1),
        ("C2 an addendum row's corpus quote read against R1's pre-cut corpus",
         {"evidence": [corpus_q] if corpus_q else [], "addendum": [], "neither": []}, 1),
        ("C3 a row naming neither evidence", {"evidence": [], "addendum": [], "neither": [a0]}, 1),
        ("C4 an R1-evidence row's quote read against the successor (v1_3's first quote)",
         {"evidence": [], "addendum": [g["evidence"][0]], "neither": []}, None),
    ]
    good = 0
    results = []
    for name, grp, want_fail in controls:
        ok, fails = check_all(grp, t_ev, t_add)
        got = 1 if fails else 0
        if want_fail is None:     # informative: an old quote may or may not survive the cut; report, do not score
            print("%-72s reported (%s)" % (name, "not verbatim" if fails else "still verbatim"))
            continue
        results.append(got == want_fail)
        print("%-72s %s" % (name, "as expected" if got == want_fail else "UNEXPECTED (%d fail lines)" % len(fails)))
        if got != want_fail and name.startswith("C0"):
            for f in fails:
                print("   ", f)
            print("SELF-TEST: the unmutated control failed first; nothing after it means anything")
            return 1
    good = sum(results)
    print("SELF-TEST: %d of %d controls as expected" % (good, len(results)))
    return 0 if good == len(results) else 1


def main():
    a = sys.argv[1:]
    if a == ["--self-test"]:
        return self_test()
    if a != ["--rulings"]:
        print(__doc__)
        return 2
    g = rulings_quotes_by_source()
    ok, fails = check_all(g, Q.Texts(), addendum_texts())
    for f in fails:
        print("FAIL", f)
    n = sum(len(v) for v in g.values())
    print("%s: %d quotes (%d on R1's evidence, %d on the addendum), %d verbatim, %d not"
          % (RULINGS, n, len(g["evidence"]), len(g["addendum"]), ok, len(fails)))
    print("QUOTE CHECK v0_2: %s" % ("GREEN" if not fails else "RED"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

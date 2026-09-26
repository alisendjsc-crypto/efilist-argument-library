#!/usr/bin/env python3
"""r1_quote_check.py -- every quote a verdict leans on exists verbatim where it says (L3, 2026-09-25).

A ruling that quotes the corpus, the map or canon is only as good as the quote. This asserts each
quoted sentence is an exact substring of the text it names, and exits 1 on any miss.

Sources a quote may name:
  corpus:<id>#<locus>    the reader-facing text: short | medium | long | note | diagnosis | trigger |
                         archetypeVariants.<slot>
  map:<id>#<locus>       any map entry at that locus: its anchor, move, grounds, or a routing string
  canon:<dotted.path>    any string under that path in the one project_canon_v38_*.json
  register:<HR-nn>       any string in that bedrock of the honest-residuals register canon pins

  python3 r1_quote_check.py <quotes.json>   # a list of {"src": ..., "quote": ...}
  python3 r1_quote_check.py --rulings       # every map_record quote in R1_rulings.json
  python3 r1_quote_check.py --self-test     # controls; the unmutated control runs first

In R1_rulings.json a map_record's `at` reads "<id>#<locus>" (map), "corpus text, <id>#<locus>"
(corpus), "canon <dotted.path>" (canon) or "register <HR-nn>" (register). Exact match only: no case folding, no whitespace or
punctuation normalisation. Repo-relative; writes nothing.
"""
import glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
EVID = "adversarial_map_staging/r1/R1_evidence_2026-09-19.json"
RULINGS = "adversarial_map_staging/r1/R1_rulings.json"


def load(rel):
    return json.load(open(os.path.join(REPO, rel), encoding="utf-8"))


def strings(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)
    elif isinstance(o, str):
        yield o


class Texts:
    def __init__(self):
        ev = load(EVID)
        mp = ev["inputs"]["map"]
        if not os.path.exists(os.path.join(REPO, mp)):
            mp = os.path.join("adversarial_map_staging", os.path.basename(mp))
        self.map = load(mp)["entries"]
        self.corpus = {o["id"]: o for o in load(ev["inputs"]["corpus"])["objections"]}
        canons = sorted(glob.glob(os.path.join(REPO, "project_canon_v38_*.json")))
        if len(canons) != 1:
            sys.exit("REFUSED: expected exactly one project_canon_v38_*.json, found %d" % len(canons))
        self.canon = json.load(open(canons[0], encoding="utf-8"))
        am = self.canon["adversarial_map"]
        pin = am[sorted(k for k in am if k.startswith("honest_residuals_register_pin_v0_"))[-1]]
        self.register = {b["bedrock_id"]: b for b in
                         load(os.path.join("adversarial_map_staging", pin["artifact"]))["bedrocks"]}

    def resolve(self, src):
        """Return the list of texts the source names, or raise KeyError naming what is missing."""
        kind, _, rest = src.partition(":")
        if kind == "corpus":
            node, _, locus = rest.partition("#")
            o = self.corpus[node]
            if locus in ("short", "medium", "long"):
                t = o["responses"].get(locus)
            elif locus.startswith("archetypeVariants."):
                t = o["responses"].get("archetypeVariants", {}).get(locus.split(".", 1)[1])
            else:
                t = o.get(locus)
            if not isinstance(t, str):
                raise KeyError("no corpus text at %s" % rest)
            return [t]
        if kind == "map":
            node, _, locus = rest.partition("#")
            xs = [x for x in self.map if x["target_id"] == node and x["target_locus"] == locus]
            if not xs:
                raise KeyError("no map entry at %s" % rest)
            out = []
            for x in xs:
                out += [x["target_anchor"], x["adversarial_move"], x["grounds"]] + list(strings(x["routing"]))
            return out
        if kind == "canon":
            o = self.canon
            for part in rest.split("."):
                o = o[part]
            return list(strings(o))
        if kind == "register":
            if rest not in self.register:
                raise KeyError("no bedrock %s in the pinned register" % rest)
            return list(strings(self.register[rest]))
        raise KeyError("unknown source kind %r" % kind)


def at_to_src(at):
    at = at.strip()
    if at.startswith("canon "):
        return "canon:" + at[len("canon "):]
    if at.startswith("corpus text, "):
        return "corpus:" + at[len("corpus text, "):]
    if at.startswith("register "):
        return "register:" + at[len("register "):]
    return "map:" + at


def check(quotes, texts):
    fails, ok = [], 0
    for i, q in enumerate(quotes, 1):
        tag = q.get("tag") or "#%d" % i
        try:
            pool = texts.resolve(q["src"])
        except KeyError as err:
            fails.append("%s: source %s -- %s" % (tag, q["src"], err))
            continue
        if any(q["quote"] in t for t in pool):
            ok += 1
        else:
            fails.append("%s: NOT VERBATIM at %s: %r" % (tag, q["src"], q["quote"][:120]))
    return ok, fails


def rulings_quotes():
    out = []
    for r in load(RULINGS)["rows"]:
        for m in r.get("map_record") or []:
            out.append({"tag": "%s (#%s)" % (r["row"], r["n"]), "src": at_to_src(m["at"]), "quote": m["quote"]})
    return out


def self_test():
    texts = Texts()
    real = rulings_quotes()
    if not real:
        sys.exit("SELF-TEST: no rulings quotes to test against")
    q0 = real[0]
    controls = [
        ("C0 unmutated: every committed rulings quote", real, 0),
        ("C1 one character changed", [dict(q0, quote=q0["quote"][:-1] + ("X" if q0["quote"][-1] != "X" else "Y"))], 1),
        ("C2 whitespace doubled", [dict(q0, quote=q0["quote"].replace(" ", "  ", 1))], 1),
        ("C3 right words, wrong locus", [dict(q0, src=q0["src"].rsplit("#", 1)[0] + "#medium"
                                               if q0["src"].startswith("map:") else q0["src"] + "X")], 1),
        ("C4 unknown source kind", [dict(q0, src="wiki:" + q0["src"].split(":", 1)[1])], 1),
        ("C5 corpus quote checked against the map", [{"src": "map:life-gift#long",
                                                     "quote": texts.corpus["life-gift"]["responses"]["long"][:60]}], 1),
        ("C6 a register gloss, verbatim", [{"src": "register:HR-06",
                                            "quote": texts.register["HR-06"]["gloss"][:60]}], 0),
        ("C7 the same gloss under another bedrock", [{"src": "register:HR-05",
                                                      "quote": texts.register["HR-06"]["gloss"][:60]}], 1),
    ]
    good = 0
    for name, qs, want_fail in controls:
        ok, fails = check(qs, texts)
        got = 1 if fails else 0
        print("%-45s %s" % (name, "as expected" if got == want_fail else "UNEXPECTED (%d fail lines)" % len(fails)))
        good += got == want_fail
        if got != want_fail and name.startswith("C0"):
            for f in fails:
                print("   ", f)
            print("SELF-TEST: the unmutated control failed first; nothing after it means anything")
            return 1
    print("SELF-TEST: %d of %d controls as expected" % (good, len(controls)))
    return 0 if good == len(controls) else 1


def main():
    a = sys.argv[1:]
    if a == ["--self-test"]:
        return self_test()
    texts = Texts()
    if a == ["--rulings"]:
        quotes, what = rulings_quotes(), RULINGS
    elif len(a) == 1 and not a[0].startswith("-"):
        quotes, what = json.load(open(a[0], encoding="utf-8")), a[0]
    else:
        print(__doc__)
        return 2
    ok, fails = check(quotes, texts)
    for f in fails:
        print("FAIL", f)
    print("%s: %d quotes, %d verbatim, %d not" % (what, len(quotes), ok, len(fails)))
    print("QUOTE CHECK: %s" % ("GREEN" if not fails else "RED"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

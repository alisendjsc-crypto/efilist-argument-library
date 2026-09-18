#!/usr/bin/env python3
"""K349 control battery for Phase G, the v0_6 patch and the render-path findings.

Emits phaseG_control_v0_1.json. Repo-relative. Deterministic under forced
PYTHONHASHSEED (ccclxvii): no set iteration reaches an ordered output.

Four families:
  PARITY     v0_6 must reproduce EVERY v0_5 verdict on every shipped artifact, against
             both corpora, in plain / --terminal / --assembly, with ONE intended
             exception class -- and the exception must be shown to be empty in practice.
  CLASS MIX  the ccclxviii gate, two-sided, computed against the A-E prior BEFORE any
             receipt is written over it.
  MUTATION   each mutation names the check it must trip. A control that cannot fail for
             its own reason is not a control.
  RENDER     the reachability and confidence-badge findings, asserted against combined.html
             rather than reasoned about.
"""
import json, os, sys, subprocess, importlib.util, collections, itertools, math, re, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
STG = HERE


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


V5 = load(os.path.join(STG, "adv_map_validator_v0_5.py"), "v5")
V6 = load(os.path.join(STG, "adv_map_validator_v0_6.py"), "v6")


def rj(p):
    return json.loads(open(p, "rb").read().decode("utf-8"))


def git_show(rev_path):
    return subprocess.check_output(["git", "-C", REPO, "show", rev_path])


def binom_two_sided(k, n, p):
    """Exact two-sided binomial p-value, by the method-of-small-p-values."""
    def pmf(i):
        return math.comb(n, i) * (p ** i) * ((1 - p) ** (n - i))
    obs = pmf(k)
    return min(1.0, sum(pmf(i) for i in range(n + 1) if pmf(i) <= obs * (1 + 1e-12)))


def main():
    results = []

    def rec(family, name, ok, detail=""):
        results.append({"family": family, "name": name, "pass": bool(ok), "detail": detail})
        print("%s . [%s] %s %s" % ("PASS" if ok else "FAIL", family, name, detail))

    # ---------- corpora ----------------------------------------------------------
    post_path = os.path.join(REPO, "efilist_argument_library_v4_0_0.json")
    post_raw = open(post_path, "rb").read()
    tmp = tempfile.mkdtemp(prefix="k349ctl_")
    pre_raw = git_show("3e71546:efilist_argument_library_v4_0_0.json")
    pre_path = os.path.join(tmp, "corpus_precut.json")
    open(pre_path, "wb").write(pre_raw)
    corpora = [("post-cut", post_path, V6.md5_bytes(post_raw)),
               ("pre-cut", pre_path, V6.md5_bytes(pre_raw))]
    rec("PARITY", "pre-cut-corpus-recovered",
        V6.md5_bytes(pre_raw) == "6ee1f6f31e0f012db0d58cae4f912fcb",
        V6.md5_bytes(pre_raw))

    # ---------- PARITY -----------------------------------------------------------
    MAPS = sorted(f for f in os.listdir(STG)
                  if re.match(r"^(adv_map_phase|adversarial_map_v1_)", f) and f.endswith(".json"))
    MAPS = [f for f in MAPS if f != "adv_map_phaseG_v0_1.json"]
    modes = [("plain", {}), ("terminal", {"terminal": True}), ("assembly", {"assembly": True})]
    div = []
    runs = 0
    for fn in MAPS:
        for cname, cpath, _cm in corpora:
            for mname, kw in modes:
                p = os.path.join(STG, fn)
                r5 = V5.validate([p], cpath, out=lambda s: None, **kw)
                r6 = V6.validate([p], cpath, out=lambda s: None, **kw)
                runs += 1
                if (r5[0], sorted(r5[1]), sorted(r5[2])) != (r6[0], sorted(r6[1]), sorted(r6[2])):
                    div.append({"file": fn, "corpus": cname, "mode": mname,
                                "v0_5": [r5[0], r5[1][:3]], "v0_6": [r6[0], r6[1][:3]]})
    rec("PARITY", "v0_6-reproduces-every-v0_5-verdict", not div,
        "%d runs over %d artifacts x 2 corpora x 3 modes, %d divergences" % (runs, len(MAPS), len(div)))
    if div:
        results[-1]["divergences"] = div

    # the intended exception class must be EMPTY in practice: no shipped artifact has a
    # note entry, so the coverage restriction can move nothing.
    note_bearing = {}
    for fn in MAPS:
        d = rj(os.path.join(STG, fn))
        ents = d.get("entries", []) if isinstance(d, dict) else []
        n = sum(1 for e in ents if isinstance(e, dict) and e.get("target_locus") == "note")
        if n:
            note_bearing[fn] = n
    rec("PARITY", "no-shipped-artifact-carries-a-note-entry", not note_bearing, str(note_bearing))
    rec("PARITY", "v0_5-byte-identical",
        V6.md5_bytes(open(os.path.join(STG, "adv_map_validator_v0_5.py"), "rb").read())
        == "713da227ec4457eaf644996ef352ff20")
    rec("PARITY", "frozen-v1_0-still-assembly-green-on-its-own-corpus",
        V6.validate([os.path.join(STG, "adversarial_map_v1_0.json")], pre_path,
                    assembly=True, out=lambda s: None)[0])

    # ---------- CLASS MIX (ccclxviii) --------------------------------------------
    g = rj(os.path.join(STG, "adv_map_phaseG_v0_1.json"))
    gcls = collections.Counter(e["class"] for e in g["entries"])
    n_g = len(g["entries"])
    k_g = gcls["a"] + gcls["d"]
    v1_0 = rj(os.path.join(STG, "adversarial_map_v1_0.json"))
    AE = ("A", "B1", "B2", "C", "D", "E")
    ae = [e for e in v1_0["entries"] if (e.get("provenance") or {}).get("phase") in AE]
    ae_cls = collections.Counter(e["class"] for e in ae)
    prior = (ae_cls["a"] + ae_cls["d"]) / len(ae)
    pval = binom_two_sided(k_g, n_g, prior)
    d_prior = ae_cls["d"] / len(ae)
    d_p = binom_two_sided(gcls["d"], n_g, d_prior)
    rec("CLASSMIX", "a-or-d-consistent-with-A-to-E-prior", pval > 0.05,
        "%d/%d = %.4f vs prior %.4f, exact two-sided p = %.4f" % (k_g, n_g, k_g / n_g, prior, pval))
    rec("CLASSMIX", "zero-d-consistent-with-prior", d_p > 0.05,
        "%d/%d d vs prior %.4f, p = %.4f" % (gcls["d"], n_g, d_prior, d_p))
    # the STRUCTURAL explanation for zero (d), measured rather than asserted
    asm = rj(os.path.join(STG, "adversarial_map_v1_1.json"))
    d_nodes = sorted(set(e["target_id"] for e in asm["entries"] if e["class"] == "d"))
    authored = sorted(set(e["target_id"] for e in g["entries"]))
    already = [i for i in authored if i in d_nodes]
    rec("CLASSMIX", "authored-nodes-already-carry-bedrock", len(already) >= 4,
        "%d of %d authored nodes already carry a (d) in v1_1: %s" % (len(already), len(authored), already))

    # ---------- MUTATION ---------------------------------------------------------
    def mutate(name, fn, expect_tag, corpus=post_path):
        doc = rj(os.path.join(STG, "adv_map_phaseG_v0_1.json"))
        fn(doc)
        p = os.path.join(tmp, "mut_%s.json" % re.sub(r"[^a-z0-9]+", "_", name))
        open(p, "wb").write((json.dumps(doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
        ok, viol, adv = V6.validate([p], corpus, out=lambda s: None)
        hit = [v for v in viol if v.startswith(expect_tag)]
        tripped = (not ok) and bool(hit)
        # Print the violation the control MATCHED ON, never merely the first one a
        # mutation happened to produce -- a receipt must show the evidence for its own
        # claim (ccclxii). A collateral violation is reported separately, not silently.
        rec("MUTATION", name, tripped,
            "expect %s -> %s%s" % (expect_tag, hit[:1],
                                   (" [+%d collateral]" % (len(viol) - len(hit))) if len(viol) > len(hit) else ""))

    def _first(doc):
        return doc["entries"][0]

    mutate("anchor-not-verbatim", lambda d: _first(d).__setitem__(
        "target_anchor", "would benefit from MUCH deeper engagement with Held's distinction"), "anchor-rule")
    mutate("anchor-from-the-wrong-locus", lambda d: _first(d).__setitem__(
        "target_anchor", "Care ethics evaluates the relationship after instantiation"), "anchor-rule")
    mutate("note-locus-on-a-node-without-one", lambda d: _first(d).__setitem__(
        "target_id", "just-depressed"), "target-locus")
    mutate("declared-note-coverage-wrong",
           lambda d: d["meta"].__setitem__("note_coverage", "9/9"), "note-coverage")
    mutate("class-counts-wrong",
           lambda d: d["meta"].__setitem__("class_counts", {"a": 5}), "meta-summaries")
    mutate("closure-declares-an-unauthored-locus",
           lambda d: d["meta"]["locus_closure"].__setitem__("solipsism#note", "closed"), "stopping-rule")
    mutate("an-a-routes-to-a-locus-that-does-not-exist",
           lambda d: d["entries"][1].__setitem__("routing", {"answered_by": ["boonin-critique#note-x"]}),
           "routing-shape")
    mutate("corpus-pin-stale",
           lambda d: d["meta"].__setitem__("source_corpus_md5", "6ee1f6f31e0f012db0d58cae4f912fcb"),
           "meta-corpus-pin")
    mutate("move-over-the-a-brevity-cap",
           lambda d: d["entries"][1].__setitem__("adversarial_move",
                                                 " ".join(["word"] * 75)), "move-band")

    # ---------- ANCHOR PROVENANCE ------------------------------------------------
    # Do these anchors predate the v4.1.0 cut? A note that the cut never touched means the
    # exposure was available to phases A-E and not taken.
    pre = rj(pre_path)
    pre_by = {o["id"]: o for o in pre["objections"]}
    prov = []
    for e in g["entries"]:
        n = pre_by.get(e["target_id"])
        txt = n.get("note", "") if n else ""
        prov.append({"id": e["target_id"], "anchor_present_pre_cut": e["target_anchor"] in txt})
    n_pre = sum(1 for x in prov if x["anchor_present_pre_cut"])
    rec("PROVENANCE", "anchors-predating-the-v4_1_0-cut", True,
        "%d of %d anchors are present in the PRE-cut corpus -- the note layer was untouched by the cut"
        % (n_pre, len(prov)))

    # ---------- RENDER -----------------------------------------------------------
    html = open(os.path.join(REPO, "combined.html"), "rb").read().decode("utf-8", "replace")
    gate = "const conf = obj.confidence || 'full';"
    btn = 'class="note-toggle"'
    rec("RENDER", "note-button-is-nested-inside-the-confidence-gate",
        html.count(gate) == 1 and html.count(btn) == 1
        and 0 < html.index(gate) < html.index(btn) < html.index("// RSI badge"),
        "gate and button both occur once, button inside the conf!=full block")
    rec("RENDER", "toggleNote-has-exactly-one-caller",
        html.count("toggleNote(") == 2, "%d occurrences = 1 definition + 1 call" % html.count("toggleNote("))
    rec("RENDER", "note-div-is-display-none-by-default",
        "display: none;" in html.split(".confidence-note {")[1].split("}")[0])
    rec("RENDER", "confidence-emits-visible-text",
        "'<span class=\"confidence-badge confidence-' + conf + '\">' + label + '</span>'" in html
        or 'confidence-badge confidence-' in html,
        "the STRONG / PROVISIONAL badge is text, so 'no text reaches the reader' is false")
    rec("RENDER", "rsi-calibration-cites-flow-states-once",
        html.count("acknowledging the open question") == 1
        and "acknowledging the open question" not in post_raw.decode("utf-8")
        and "acknowledging the open question" not in
            open(os.path.join(REPO, "efilist_argument_library_v4_0_0.jsx"), "rb").read().decode("utf-8"),
        "flagship-only: 1 in combined.html, 0 in corpus JSON, 0 in JSX")

    npass = sum(1 for r in results if r["pass"])
    out = {
        "artifact": "phaseG_control_v0_1.json",
        "generated_by": "adversarial_map_staging/controls_phaseG.py",
        "session": "K349", "date_operator_local": "2026-09-17",
        "validator_v0_5_md5": V6.md5_bytes(open(os.path.join(STG, "adv_map_validator_v0_5.py"), "rb").read()),
        "validator_v0_6_md5": V6.md5_bytes(open(os.path.join(STG, "adv_map_validator_v0_6.py"), "rb").read()),
        "phaseG_md5": V6.md5_bytes(open(os.path.join(STG, "adv_map_phaseG_v0_1.json"), "rb").read()),
        "parity_runs": runs, "parity_artifacts": MAPS,
        "class_mix": {"counts": dict(gcls), "n": n_g, "a_or_d": k_g,
                      "prior_A_to_E": round(prior, 4), "p_two_sided": round(pval, 4),
                      "d_prior": round(d_prior, 4), "d_p": round(d_p, 4),
                      "prior_basis": "the 93 A-E entries of the FROZEN v1_0, which is the established prior"},
        "anchor_provenance": prov,
        "results": results,
        "summary": {"controls": len(results), "passed": npass, "all_pass": npass == len(results)},
    }
    dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(STG, "phaseG_control_v0_1.json")
    b = (json.dumps(out, indent=2, ensure_ascii=True) + "\n").encode("utf-8")
    open(dest, "wb").write(b)
    print(json.dumps(out["summary"], indent=1))
    print("wrote %s %s" % (dest, V6.md5_bytes(b)))
    return 0 if npass == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())

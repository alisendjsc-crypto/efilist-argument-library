#!/usr/bin/env python3
"""K349 control battery for adversarial_map_v1_2.json. Emits assembly_control_v0_2.json.

Runs the PREDECESSOR's builder first and requires v1_1 back byte-for-byte (ccclxiv applied
to an artifact rather than to a serialization), then mutates v1_2 nine ways, each naming the
check it must trip. A control that cannot fail for its own reason is not a control.
"""
import json, os, sys, re, subprocess, tempfile, importlib.util, collections, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


V = load(os.path.join(HERE, "adv_map_validator_v0_6.py"), "v6")
CORPUS = os.path.join(REPO, "efilist_argument_library_v4_0_0.json")
md5f = lambda p: V.md5_bytes(open(p, "rb").read())


def main():
    results = []
    tmp = tempfile.mkdtemp(prefix="k349asm_")

    def rec(name, ok, detail=""):
        results.append({"name": name, "pass": bool(ok), "detail": detail})
        print("%s . %s %s" % ("PASS" if ok else "FAIL", name, detail))

    v1_1 = os.path.join(HERE, "adversarial_map_v1_1.json")
    v1_2 = os.path.join(HERE, "adversarial_map_v1_2.json")
    v1_0 = os.path.join(HERE, "adversarial_map_v1_0.json")
    m11, m12, m10 = md5f(v1_1), md5f(v1_2), md5f(v1_0)

    # ---- 1. ccclxiv on the ARTIFACT: the predecessor's builder must still reproduce it
    out_dir = os.path.join(tmp, "repro")
    os.makedirs(os.path.join(out_dir, "adversarial_map_staging"), exist_ok=True)
    r = subprocess.run([sys.executable, os.path.join(HERE, "build_assembly_v1_1.py"),
                        "--out", out_dir], capture_output=True, text=True, cwd=HERE)
    repro = os.path.join(out_dir, "adversarial_map_staging", "adversarial_map_v1_1.json")
    ok = r.returncode == 0 and os.path.exists(repro) and md5f(repro) == m11
    rec("v1_1-reproduces-byte-identically-from-its-own-builder", ok,
        "%s vs %s" % (md5f(repro) if os.path.exists(repro) else "(not written)", m11))

    # ---- 2. the predecessors are UNMOVED by this session
    rec("v1_1-unmoved", m11 == "e9e5abf820e3f7a687e2b84443883ade", m11)
    rec("v1_0-frozen-unmoved", m10 == "c4989e98b042e2f787a82df3f11ecdad", m10)

    # ---- 3. v1_2 is a pure SUPERSET of v1_1: nothing inherited moved
    d11, d12 = json.load(open(v1_1, "rb")), json.load(open(v1_2, "rb"))
    key = lambda e: (e["target_id"], e["target_locus"], e["target_anchor"])
    s11 = {key(e): json.dumps(e, sort_keys=True) for e in d11["entries"]}
    s12 = {key(e): json.dumps(e, sort_keys=True) for e in d12["entries"]}
    missing = sorted(k for k in s11 if k not in s12)
    changed = sorted(k for k in s11 if k in s12 and s11[k] != s12[k])
    added = sorted(k for k in s12 if k not in s11)
    rec("every-v1_1-entry-inherited-byte-for-byte", not missing and not changed,
        "%d missing, %d changed, %d added" % (len(missing), len(changed), len(added)))
    rec("exactly-the-phase-G-entries-are-added",
        len(added) == 5 and all(k[1] == "note" for k in added),
        "%d added, all at the note locus" % len(added))

    # ---- 4. the terminal verdict
    ok_a, viol, adv = V.validate([v1_2], CORPUS, assembly=True, out=lambda s: None)
    rec("v1_2-assembly-green", ok_a and not adv,
        "%d violations, %d advisories" % (len(viol), len(adv)))

    # ---- 5. MUTATIONS. Each names the check it must trip.
    def mutate(name, fn, tag, **kw):
        doc = json.load(open(v1_2, "rb"))
        fn(doc)
        p = os.path.join(tmp, "m_%s.json" % re.sub(r"[^a-z0-9]+", "_", name))
        open(p, "wb").write((json.dumps(doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
        o, v, a = V.validate([p], CORPUS, out=lambda s: None, **kw)
        hit = [x for x in (v + a) if x.startswith(tag)]
        rec(name, (not o or a) and bool(hit), "expect %s -> %s" % (tag, hit[:1]))

    def note_entry(doc):
        return next(e for e in doc["entries"] if e["target_locus"] == "note")

    # THE COVERAGE RULING, ON REAL DATA: strip every PRIMARY entry for a node that keeps a
    # note entry, and the map must stop being complete. This is the control that proves
    # apparatus cannot satisfy 82/82 -- and it fails on v0_5, where a note locus counted.
    def strip_primary_of_a_note_node(doc):
        tgt = "care-ethics"
        doc["entries"] = [e for e in doc["entries"]
                          if not (e["target_id"] == tgt and e["target_locus"] != "note")]
        doc["meta"].pop("class_counts", None)
        doc["meta"].pop("coverage_distinct_ids", None)
    mutate("note-only-node-is-not-covered", strip_primary_of_a_note_node, "coverage", terminal=True)

    mutate("declared-note-coverage-wrong",
           lambda d: d["meta"].__setitem__("note_coverage", "9/9"), "note-coverage")
    mutate("declared-variant-coverage-wrong",
           lambda d: d["meta"].__setitem__("variant_coverage", "38/39"), "variant-coverage")
    mutate("a-note-anchor-is-not-verbatim",
           lambda d: note_entry(d).__setitem__("target_anchor", "a phrase no note contains"),
           "anchor-rule")
    mutate("corpus-pin-advanced-to-the-pre-cut-corpus",
           lambda d: d["meta"].__setitem__("source_corpus_md5",
                                           "6ee1f6f31e0f012db0d58cae4f912fcb"), "meta-corpus-pin")
    mutate("class-counts-wrong",
           lambda d: d["meta"].__setitem__("class_counts", {"a": 69, "b": 29, "c": 1, "d": 40}),
           "meta-summaries")
    mutate("an-entry-carries-a-non-mapped-status",
           lambda d: note_entry(d).__setitem__("status", "queued"), "status-enum")
    mutate("a-node-is-pushed-over-its-bound", lambda d: d["entries"].extend([
        dict(note_entry(d), target_anchor=a) for a in
        ("Care ethics is a well-established feminist", "well-established feminist ethical tradition",
         "The EFIList counter-argument engages it seriously")]), "entry-cap")
    mutate("a-phase-G-entry-is-stamped-with-another-phase",
           lambda d: note_entry(d)["provenance"].__setitem__("phase", "Z"), "provenance")

    # ---- 6. THE BUILDER REFUSES when its own invariant is broken.
    #        Phase G re-stamped as Phase F would claim a locus two phases hold.
    # A whole shadow REPO, because the builder resolves the corpus from dirname(HERE).
    rrepo = os.path.join(tmp, "refuse_repo")
    work = os.path.join(rrepo, "adversarial_map_staging")
    os.makedirs(rrepo, exist_ok=True)
    shutil.copytree(HERE, work, symlinks=False,
                    ignore=shutil.ignore_patterns("__pycache__"))
    os.symlink(CORPUS, os.path.join(rrepo, os.path.basename(CORPUS)))
    g = os.path.join(work, "adv_map_phaseG_v0_1.json")
    doc = json.load(open(g, "rb"))
    doc["entries"][0]["target_locus"] = "long"
    open(g, "wb").write((json.dumps(doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    r2 = subprocess.run([sys.executable, os.path.join(work, "build_assembly_v1_2.py"),
                         "--out", os.path.join(tmp, "refuse_out")],
                        capture_output=True, text=True, cwd=work)
    blob = r2.stdout + r2.stderr
    hit = [l for l in blob.splitlines() if "PARTITION THE LOCUS" in l]
    rec("builder-refuses-a-locus-claimed-by-two-phases",
        r2.returncode != 0 and "REFUSING TO WRITE" in blob and bool(hit),
        (hit or blob.strip().splitlines() or ["(no output)"])[0][:130])

    npass = sum(1 for x in results if x["pass"])
    out = {
        "artifact": "assembly_control_v0_2.json",
        "generated_by": "adversarial_map_staging/controls_assembly_v1_2.py",
        "session": "K349", "date_operator_local": "2026-09-17",
        "pins": {"v1_0": m10, "v1_1": m11, "v1_2": m12,
                 "validator_v0_6": md5f(os.path.join(HERE, "adv_map_validator_v0_6.py")),
                 "phaseG": md5f(os.path.join(HERE, "adv_map_phaseG_v0_1.json"))},
        "superset_check": {"inherited": len(s11), "missing": len(missing),
                           "changed": len(changed), "added": len(added)},
        "results": results,
        "summary": {"controls": len(results), "passed": npass, "all_pass": npass == len(results)},
    }
    dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "assembly_control_v0_2.json")
    b = (json.dumps(out, indent=2, ensure_ascii=True) + "\n").encode("utf-8")
    open(dest, "wb").write(b)
    print(json.dumps(out["summary"], indent=1))
    print("wrote %s %s" % (dest, V.md5_bytes(b)))
    return 0 if npass == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())

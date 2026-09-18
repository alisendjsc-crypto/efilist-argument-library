#!/usr/bin/env python3
"""K351 control battery for adversarial_map_v1_3.json and the Phase G amendment.
Emits assembly_control_v0_3.json.

Three things have to be SHOWN rather than claimed.

  1. The predecessor still reproduces from its own builder (ccclxiv on an artifact), and
     v1_3 is a pure reclassification of it -- nothing added, nothing removed, exactly one
     entry changed, and the move and anchor inside that entry untouched.
  2. The amendment builder is width-of-the-ruling by construction: it refuses if the base
     blob moved, and its own assertions refuse if the move or another entry is touched.
  3. THE (b) REMAINDER HAS NOWHERE TO GO, measured on THIS builder rather than inferred
     from the last one. K349's battery proved the partition refusal on v1_2; the same
     mutation is re-run here, plus the schema half -- a (d) carrying a regen_candidate --
     which is the other wall the remainder would have to climb.

A control that cannot fail for its own reason is not a control, so every mutation names
the check it must trip and every refusal control names the line it must see.
"""
import json, os, re, shutil, subprocess, sys, tempfile, importlib.util

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
TARGET = ("care-ethics", "note")


def main():
    results = []
    tmp = tempfile.mkdtemp(prefix="k351asm_")

    def rec(name, ok, detail=""):
        # Strip the scratch root out of every detail string. K349's
        # assembly_control_v0_2.json carries a session id and a random tempdir name in
        # three of its details, so that artifact cannot be reproduced by the script its
        # own `generated_by` field names -- an inherited defect nobody met because nothing
        # had tried to reproduce a control output. Fixed here; the predecessor's bytes are
        # left alone, because they are a landed record.
        detail = str(detail).replace(tmp + os.sep, "").replace(tmp, "")
        results.append({"name": name, "pass": bool(ok), "detail": detail})
        print("%s . %s %s" % ("PASS" if ok else "FAIL", name, detail))

    v1_0 = os.path.join(HERE, "adversarial_map_v1_0.json")
    v1_1 = os.path.join(HERE, "adversarial_map_v1_1.json")
    v1_2 = os.path.join(HERE, "adversarial_map_v1_2.json")
    v1_3 = os.path.join(HERE, "adversarial_map_v1_3.json")
    pg = os.path.join(HERE, "adv_map_phaseG_v0_1.json")
    m10, m11, m12, m13 = md5f(v1_0), md5f(v1_1), md5f(v1_2), md5f(v1_3)

    # ---- 1. ccclxiv on the ARTIFACT: the predecessor's builder must still reproduce it.
    #         v1_2's builder reads adv_map_phaseG_v0_1.json FROM DISK and that file is now
    #         amended, so the run needs the base state. A git worktree would say it and
    #         costs a full checkout of a 3 MB flagship; a SYMLINK FARM whose only real file
    #         is the 12 KB base blob says the same thing for nothing.
    base_ref = "649fdbc288611fa6ea420e95055d810264301a06"
    base_pg = subprocess.run(["git", "-C", REPO, "show",
                              "%s:adversarial_map_staging/adv_map_phaseG_v0_1.json" % base_ref],
                             capture_output=True).stdout

    def farm(sub, real=(), swap=None):
        """A repo-shaped tree of symlinks. `real` names staging files to copy rather than
        link (so a control may mutate them); `swap` maps a staging filename to bytes."""
        root = os.path.join(tmp, sub)
        work = os.path.join(root, "adversarial_map_staging")
        os.makedirs(work)
        os.makedirs(os.path.join(root, "tools"))
        for n in os.listdir(HERE):
            if n == "__pycache__":
                continue
            src, dst = os.path.join(HERE, n), os.path.join(work, n)
            if swap and n in swap:
                open(dst, "wb").write(swap[n])
            elif n in real:
                shutil.copyfile(src, dst)
            else:
                os.symlink(src, dst)
        for n in os.listdir(os.path.join(REPO, "tools")):
            if n == "__pycache__":
                continue
            os.symlink(os.path.join(REPO, "tools", n), os.path.join(root, "tools", n))
        os.symlink(CORPUS, os.path.join(root, os.path.basename(CORPUS)))
        return root, work

    rroot, rwork = farm("repro", swap={"adv_map_phaseG_v0_1.json": base_pg})
    r = subprocess.run([sys.executable, os.path.join(rwork, "build_assembly_v1_2.py"),
                        "--out", os.path.join(rroot, "out")],
                       capture_output=True, text=True, cwd=rwork,
                       env=dict(os.environ, K348_REPO=rroot))
    repro = os.path.join(rroot, "out", "adversarial_map_staging", "adversarial_map_v1_2.json")
    got = md5f(repro) if os.path.exists(repro) else "(not written): " + (r.stdout + r.stderr)[-90:]
    rec("v1_2-reproduces-byte-identically-from-its-own-builder-on-its-own-inputs",
        r.returncode == 0 and os.path.exists(repro) and got == m12, "%s vs %s" % (got, m12))

    # ---- 2. the predecessors are UNMOVED by this session
    rec("v1_2-unmoved", m12 == "e4bef3cac882aa079951ba7ec1a9d11e", m12)
    rec("v1_1-unmoved", m11 == "e9e5abf820e3f7a687e2b84443883ade", m11)
    rec("v1_0-frozen-unmoved", m10 == "c4989e98b042e2f787a82df3f11ecdad", m10)

    # ---- 3. v1_3 is a PURE RECLASSIFICATION of v1_2
    d12, d13 = json.load(open(v1_2, "rb")), json.load(open(v1_3, "rb"))
    key = lambda e: (e["target_id"], e["target_locus"], e["target_anchor"])
    s12 = {key(e): e for e in d12["entries"]}
    s13 = {key(e): e for e in d13["entries"]}
    j = lambda e: json.dumps(e, sort_keys=True, ensure_ascii=False)
    missing = sorted(k for k in s12 if k not in s13)
    added = sorted(k for k in s13 if k not in s12)
    changed = sorted(k for k in s12 if k in s13 and j(s12[k]) != j(s13[k]))
    rec("nothing-added-and-nothing-removed", not missing and not added,
        "%d missing, %d added" % (len(missing), len(added)))
    rec("exactly-one-entry-changed-and-it-is-care-ethics-note",
        len(changed) == 1 and changed[0][:2] == TARGET,
        "%d changed: %s" % (len(changed), [c[:2] for c in changed]))
    if len(changed) == 1:
        a, b = s12[changed[0]], s13[changed[0]]
        rec("the-move-and-the-anchor-are-byte-identical",
            a["adversarial_move"] == b["adversarial_move"]
            and a["target_anchor"] == b["target_anchor"]
            and a["status"] == b["status"] and a["provenance"] == b["provenance"], "")
        rec("class-b-to-d-and-routing-follows-it",
            a["class"] == "b" and b["class"] == "d"
            and set(a["routing"]) == {"regen_candidate"} and set(b["routing"]) == {"residue"}
            and b["routing"]["residue"]["novel"] is True,
            "%s -> %s" % (sorted(a["routing"]), sorted(b["routing"])))
    rec("class-counts-move-by-exactly-one-b-to-d",
        d13["meta"]["class_counts"] == dict(d12["meta"]["class_counts"],
                                            b=d12["meta"]["class_counts"]["b"] - 1,
                                            d=d12["meta"]["class_counts"]["d"] + 1),
        "%s -> %s" % (d12["meta"]["class_counts"], d13["meta"]["class_counts"]))
    rec("all-three-coverage-claims-unmoved",
        (d13["meta"]["nodes_covered"], d13["meta"]["variant_coverage"], d13["meta"]["note_coverage"])
        == (d12["meta"]["nodes_covered"], d12["meta"]["variant_coverage"], d12["meta"]["note_coverage"]),
        "%d/%d primary, %s variant, %s note" % (d13["meta"]["nodes_covered"],
            d13["meta"]["nodes_total"], d13["meta"]["variant_coverage"], d13["meta"]["note_coverage"]))

    # ---- 4. THE CAP, MEASURED. The kickoff predicted care-ethics would sit AT its bound
    #         of 3 after a (b)-remainder entry landed at #long. No entry lands, so it sits
    #         at 2 of 3 and the cap is not the binding constraint -- the partition is.
    corpus = json.loads(open(CORPUS, "rb").read().decode("utf-8"))
    ce = next(o for o in corpus["objections"] if o["id"] == "care-ethics")
    nvar = len(V.node_variant_slots(ce))
    n_ce = sum(1 for e in d13["entries"] if e["target_id"] == "care-ethics")
    rec("care-ethics-sits-at-2-of-a-bound-of-3", n_ce == 2 and nvar == 0 and 3 + 3 * nvar == 3,
        "%d entries, %d variant loci, bound %d" % (n_ce, nvar, 3 + 3 * nvar))
    rec("every-entry-carries-exactly-one-routing-key",
        all(len(e["routing"]) == 1 for e in d13["entries"]),
        "%d entries" % len(d13["entries"]))

    # ---- 5. the terminal verdict
    ok_a, viol, adv = V.validate([v1_3], CORPUS, assembly=True, out=lambda s: None)
    rec("v1_3-assembly-green", ok_a and not adv,
        "%d violations, %d advisories" % (len(viol), len(adv)))

    # ---- 6. MUTATIONS on v1_3. Each names the check it must trip.
    def mutate(name, fn, tag, **kw):
        doc = json.load(open(v1_3, "rb"))
        fn(doc)
        p = os.path.join(tmp, "m_%s.json" % re.sub(r"[^a-z0-9]+", "_", name))
        open(p, "wb").write((json.dumps(doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
        o, v, a = V.validate([p], CORPUS, out=lambda s: None, **kw)
        hit = [x for x in (v + a) if x.startswith(tag)]
        rec(name, (not o or a) and bool(hit), "expect %s -> %s" % (tag, hit[:1]))

    def folded(doc):
        return next(e for e in doc["entries"]
                    if (e["target_id"], e["target_locus"]) == TARGET)

    mutate("the-folded-entry-keeps-its-old-b-routing",
           lambda d: folded(d).__setitem__(
               "routing", {"regen_candidate": {"axis_hit": ["c", "r"], "severity": "headline"}}),
           "routing-shape")
    mutate("a-d-entry-carrying-both-routings",
           lambda d: folded(d)["routing"].__setitem__(
               "regen_candidate", {"axis_hit": ["c"], "severity": "minor"}), "routing-shape")
    mutate("the-bedrock-name-is-emptied",
           lambda d: folded(d)["routing"]["residue"].__setitem__("bedrock_name", "   "),
           "routing-shape")
    mutate("novel-is-not-a-bool",
           lambda d: folded(d)["routing"]["residue"].__setitem__("novel", "yes"), "routing-shape")
    mutate("class-counts-still-say-b",
           lambda d: d["meta"].__setitem__("class_counts", {"a": 69, "b": 29, "c": 1, "d": 39}),
           "meta-summaries")
    mutate("the-folded-anchor-is-not-verbatim",
           lambda d: folded(d).__setitem__("target_anchor", "a phrase no note contains"),
           "anchor-rule")
    mutate("corpus-pin-advanced-to-the-pre-cut-corpus",
           lambda d: d["meta"].__setitem__("source_corpus_md5",
                                           "6ee1f6f31e0f012db0d58cae4f912fcb"), "meta-corpus-pin")
    mutate("declared-note-coverage-wrong",
           lambda d: d["meta"].__setitem__("note_coverage", "9/9"), "note-coverage")

    # ---- 7. THE BUILDER REFUSALS. A shadow repo, because the builder resolves the corpus
    #         from dirname(HERE).
    def shadow():
        return farm("r%d" % len(os.listdir(tmp)),
                    real=("adv_map_phaseG_v0_1.json", "build_assembly_v1_3.py"))

    def run_builder(rrepo, work, script, needle, name, out_sub="out"):
        r = subprocess.run([sys.executable, os.path.join(work, script),
                            "--out", os.path.join(rrepo, out_sub)],
                           capture_output=True, text=True, cwd=work,
                           env=dict(os.environ, K348_REPO=rrepo))
        blob = r.stdout + r.stderr
        hit = [l for l in blob.splitlines() if needle in l]
        rec(name, r.returncode != 0 and bool(hit),
            "rc=%d | %s" % (r.returncode, (hit[-1][:120] if hit
                                           else "NO LINE MATCHED %r" % needle)))

    # (a) THE (b)-REMAINDER'S WALL. Move the folded entry to #long, which Phase B2 holds
    #     since K229, and the builder must refuse. This is the measurement behind
    #     fragment_amendments.b_remainder_disposition.
    rrepo, work = shadow()
    g = os.path.join(work, "adv_map_phaseG_v0_1.json")
    doc = json.load(open(g, "rb"))
    e = next(x for x in doc["entries"] if (x["target_id"], x["target_locus"]) == TARGET)
    e["target_locus"] = "long"
    e["target_anchor"] = "Care ethics evaluates the relationship after instantiation"
    mutated = (json.dumps(doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    open(g, "wb").write(mutated)
    # The builder's AMENDED_PHASE_G_MD5 guard would abort FIRST and this control would
    # then prove the base guard a second time instead of the partition -- the K330 shape,
    # where a control aborts at an earlier gate and never reaches the one it was written
    # for. Re-pin the guard in the shadow copy so the partition is what is being tested.
    ba = os.path.join(work, "build_assembly_v1_3.py")
    bsrc = open(ba, "rb").read().decode("utf-8")
    old_pin = 'AMENDED_PHASE_G_MD5 = "%s"' % md5f(pg)
    assert bsrc.count(old_pin) == 1, "the amended-fragment pin is not unique in the builder"
    open(ba, "w", encoding="utf-8", newline="\n").write(
        bsrc.replace(old_pin, 'AMENDED_PHASE_G_MD5 = "%s"' % V.md5_bytes(mutated), 1))
    run_builder(rrepo, work, "build_assembly_v1_3.py", "PARTITION THE LOCUS",
                "a-b-remainder-entry-at-care-ethics-long-is-refused-by-the-partition")

    # (b) the builder refuses the UNAMENDED fragment -- the fold is not optional
    rrepo, work = shadow()
    open(os.path.join(work, "adv_map_phaseG_v0_1.json"), "wb").write(base_pg)
    run_builder(rrepo, work, "build_assembly_v1_3.py", "the amended Phase G fragment is",
                "the-assembly-builder-refuses-an-unamended-phase-G")

    # ---- 8. THE AMENDMENT BUILDER. Reproduces, and refuses on a moved base.
    rrepo, work = shadow()
    amend = os.path.join(rrepo, "tools", "amend_phaseG_K351.py")
    real_amend = os.path.realpath(amend)
    os.unlink(amend)
    shutil.copyfile(real_amend, amend)
    r = subprocess.run([sys.executable, amend, "--out", os.path.join(rrepo, "a1")],
                       capture_output=True, text=True, cwd=os.path.join(rrepo, "tools"),
                       env=dict(os.environ, K348_REPO=REPO))
    repro = os.path.join(rrepo, "a1", "adversarial_map_staging", "adv_map_phaseG_v0_1.json")
    rec("the-amended-fragment-reproduces-byte-identically-from-the-git-blob",
        r.returncode == 0 and os.path.exists(repro) and md5f(repro) == md5f(pg),
        "%s vs %s" % (md5f(repro) if os.path.exists(repro) else "(not written)", md5f(pg)))

    src = open(amend, "rb").read().decode("utf-8")
    for nm, old, new, needle in [
        ("a-moved-base-blob-refuses", 'BASE_MD5 = "d7cd18eb0467f38d8ecd4694776dd885"',
         'BASE_MD5 = "00000000000000000000000000000000"', "BASE GUARD"),
        ("touching-the-move-refuses",
         '    e["class"] = "d"', '    e["class"] = "d"\n    e["adversarial_move"] += " x"',
         "the adversarial_move MOVED"),
        ("touching-another-entry-refuses",
         '    e["class"] = "d"',
         '    e["class"] = "d"\n    doc["entries"][1]["grounds"] += " x"',
         "an entry other than"),
    ]:
        assert src.count(old) == 1, nm
        open(amend, "w", encoding="utf-8", newline="\n").write(src.replace(old, new, 1))
        r = subprocess.run([sys.executable, amend, "--out", os.path.join(rrepo, "a2")],
                           capture_output=True, text=True, cwd=os.path.join(rrepo, "tools"),
                           env=dict(os.environ, K348_REPO=REPO))
        blob = r.stdout + r.stderr
        hit = [l for l in blob.splitlines() if needle in l]
        rec(nm, r.returncode != 0 and bool(hit),
            "rc=%d | %s" % (r.returncode, (hit[-1][:110] if hit
                                           else "NO LINE MATCHED %r" % needle)))
    open(amend, "w", encoding="utf-8", newline="\n").write(src)

    npass = sum(1 for x in results if x["pass"])
    out = {
        "artifact": "assembly_control_v0_3.json",
        "generated_by": "adversarial_map_staging/controls_assembly_v1_3.py",
        "session": "K351", "date_operator_local": "2026-09-18",
        "pins": {"v1_0": m10, "v1_1": m11, "v1_2": m12, "v1_3": m13,
                 "validator_v0_6": md5f(os.path.join(HERE, "adv_map_validator_v0_6.py")),
                 "phaseG_amended": md5f(pg),
                 "phaseG_base_blob_ref": base_ref},
        "reclassification": {"inherited": len(s12), "missing": len(missing),
                             "added": len(added), "changed": len(changed),
                             "changed_loci": ["%s#%s" % c[:2] for c in changed]},
        "cap_measured": {"node": "care-ethics", "entries": n_ce, "variant_loci": nvar,
                         "node_bound": 3 + 3 * nvar,
                         "note": ("the kickoff predicted 3 AT THE BOUND after a (b)-remainder "
                                  "entry at #long; the partition invariant refuses that entry, "
                                  "so the node stays at 2 and the cap was never the constraint")},
        "results": results,
        "summary": {"controls": len(results), "passed": npass, "all_pass": npass == len(results)},
    }
    dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "assembly_control_v0_3.json")
    b = (json.dumps(out, indent=2, ensure_ascii=True) + "\n").encode("utf-8")
    open(dest, "wb").write(b)
    print(json.dumps(out["summary"], indent=1))
    print("wrote %s %s" % (dest, V.md5_bytes(b)))
    return 0 if npass == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())

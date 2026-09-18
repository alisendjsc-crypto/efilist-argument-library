#!/usr/bin/env python3
"""K349 final verification. Emits tools/k349_verification.json.

  REPRODUCIBILITY  every builder is run FROM ITS COMMITTED LOCATION into a scratch dir and
                   its artifact byte-compared, under TWO forced PYTHONHASHSEED values
                   (ccclxvii). A committed builder that cannot run is a fossil.
  ISOLATION        canon's change set is MEASURED, never claimed: which top-level values
                   moved, and that adversarial_map gained exactly its named subkeys.
  HELD             the three surfaces, the frozen map, v1_1 and every byte-identical
                   predecessor, re-read at close.
"""
import json, os, subprocess, sys, hashlib, tempfile, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
STG = os.path.join(REPO, "adversarial_map_staging")
md5f = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()

# (script relative to REPO, artifact relative to REPO, invocation)
#   "arg" -> the builder takes the destination path as argv[1]
#   "out" -> the builder takes --out <dir> and reads its inputs from <dir> too, so the
#            scratch tree is seeded with a copy of adversarial_map_staging
BUILDERS = [
    ("adversarial_map_staging/measure_k349.py",
     "adversarial_map_staging/measure_k349_v0_1.json", "arg"),
    ("adversarial_map_staging/build_phaseG.py",
     "adversarial_map_staging/adv_map_phaseG_v0_1.json", "arg"),
    ("adversarial_map_staging/build_design_v0_5.py",
     "adversarial_map_staging/adversarial_map_design_v0_5.md", "arg"),
    ("adversarial_map_staging/build_assembly_v1_2.py",
     "adversarial_map_staging/adversarial_map_v1_2.json", "out"),
    ("adversarial_map_staging/build_register_v0_3.py",
     "adversarial_map_staging/honest_residuals_register_v0_3.json", "out"),
    ("tools/build_canon_v38_11.py", "project_canon_v38_11.json", "out"),
]
PATCHERS = [
    ("tools/patch_validator_v0_6.py",
     "adversarial_map_staging/adv_map_validator_v0_6.py"),
    ("tools/patch_assembly_v1_2.py",
     "adversarial_map_staging/build_assembly_v1_2.py"),
]
HELD = {
    "combined.html": "72187f6cf0fccdf8e9f4ec6ca5ce009c",
    "efilist_argument_library_v4_0_0.json": "04bf6482aa0374ee92a81c1d55ec41f8",
    "efilist_argument_library_v4_0_0.jsx": "b196548b6eb39065842d62292acca89f",
    "adversarial_map_staging/adversarial_map_v1_0.json": "c4989e98b042e2f787a82df3f11ecdad",
    "adversarial_map_staging/adversarial_map_v1_1.json": "e9e5abf820e3f7a687e2b84443883ade",
    "adversarial_map_staging/adv_map_validator_v0_5.py": "713da227ec4457eaf644996ef352ff20",
    "adversarial_map_staging/adv_map_validator_v0_4.py": "d7a049ee1161d3bc5de0d3fbff96bbf9",
    "adversarial_map_staging/adversarial_map_design_v0_4.md": "4315ff24d3c40e0234586fce87fb8cfd",
    "adversarial_map_staging/honest_residuals_register_v0_2.json": "70357de7f508f8b5500442ffdf37900a",
    "adversarial_map_staging/adv_map_phaseF_v0_1.json": "1dfe418cd27bbbe5d402b3a41456324a",
    "adversarial_map_staging/adv_map_phaseR_v0_1.json": "d436ac69daa07de0b502977c71a10b74",
    "project_canon_v38_10.json": "32ee1c9f211a4fc24c55048d9e071b96",
}


def main():
    res = []
    def rec(name, ok, detail=""):
        res.append({"name": name, "pass": bool(ok), "detail": detail})
        print("%s . %s %s" % ("PASS" if ok else "FAIL", name, detail))

    # ---- HELD -------------------------------------------------------------------
    bad = [p for p, m in sorted(HELD.items()) if md5f(os.path.join(REPO, p)) != m]
    rec("held-surfaces-unmoved", not bad, "%d checked, %d moved %s" % (len(HELD), len(bad), bad))

    # ---- REPRODUCIBILITY --------------------------------------------------------
    repro = []
    for seed in ("0", "12345"):
        env = dict(os.environ, PYTHONHASHSEED=seed)
        for script_rel, art_rel, mode in BUILDERS:
            script = os.path.join(REPO, script_rel)
            want = md5f(os.path.join(REPO, art_rel))
            tmp = tempfile.mkdtemp(prefix="k349v_")
            if mode == "arg":
                dest = os.path.join(tmp, os.path.basename(art_rel))
                cmd = [sys.executable, script, dest]
            else:
                shutil.copytree(STG, os.path.join(tmp, "adversarial_map_staging"),
                                ignore=shutil.ignore_patterns("__pycache__"))
                dest = os.path.join(tmp, art_rel)
                cmd = [sys.executable, script, "--out", tmp]
            r = subprocess.run(cmd, capture_output=True, text=True,
                               cwd=os.path.dirname(script), env=env)
            got = md5f(dest) if os.path.exists(dest) else None
            ok = r.returncode == 0 and got == want
            repro.append({"artifact": os.path.basename(art_rel), "seed": seed, "ok": bool(ok),
                          "want": want, "got": got,
                          "err": ((r.stderr or "").strip().splitlines()[-1:] if not ok else [])})
            shutil.rmtree(tmp, ignore_errors=True)
    nbad = [x for x in repro if not x["ok"]]
    rec("every-builder-reproduces-its-artifact-under-two-hash-seeds", not nbad,
        "%d runs, %d failures %s" % (len(repro), len(nbad),
                                     [(x["artifact"], x["err"]) for x in nbad]))

    for patch_rel, art_rel in PATCHERS:
        script = os.path.join(REPO, patch_rel)
        tmp = tempfile.mkdtemp(prefix="k349p_")
        dest = os.path.join(tmp, os.path.basename(art_rel))
        r = subprocess.run([sys.executable, script, dest], capture_output=True, text=True,
                           cwd=os.path.dirname(script))
        ok = r.returncode == 0 and os.path.exists(dest) and \
            md5f(dest) == md5f(os.path.join(REPO, art_rel))
        rec("patcher-reproduces-%s" % os.path.basename(art_rel), ok,
            str((r.stderr or "").strip().splitlines()[-1:]) if not ok else "")
        shutil.rmtree(tmp, ignore_errors=True)

    # ---- CHANGE ISOLATION ON CANON ----------------------------------------------
    a = json.loads(open(os.path.join(REPO, "project_canon_v38_10.json"), "rb").read().decode("utf-8"))
    b = json.loads(open(os.path.join(REPO, "project_canon_v38_11.json"), "rb").read().decode("utf-8"))
    j = lambda x: json.dumps(x, sort_keys=True, ensure_ascii=False)
    moved = sorted(k for k in b if j(a.get(k)) != j(b[k]))
    rec("canon-keyset-41-unchanged", sorted(a) == sorted(b) and len(b) == 41, "%d keys" % len(b))
    # ALLOWED, not REQUIRED: `last_updated` legitimately does not move when the previous
    # canon bump ran on the same operator-local date, which K348 did. Asserting equality
    # would fail a correct canon for a calendar reason, so the gate is containment plus a
    # positive check that the date field says what this session says.
    ALLOWED = {"adversarial_map", "canon_version", "canon_version_marker",
               "keyset_delta_ledger", "last_updated", "last_updated_by_session",
               "next_recommended_session", "session_log_recent"}
    REQUIRED = {"adversarial_map", "canon_version", "canon_version_marker",
                "keyset_delta_ledger", "last_updated_by_session", "session_log_recent"}
    rec("canon-top-level-changes-are-contained", set(moved) <= ALLOWED and REQUIRED <= set(moved),
        "moved %s; unmoved-but-allowed %s" % (moved, sorted(ALLOWED - set(moved))))
    rec("canon-date-is-operator-local-today", b["last_updated"] == "2026-09-17",
        b["last_updated"])
    amA, amB = a["adversarial_map"], b["adversarial_map"]
    am_moved = sorted(k for k in amB if j(amA.get(k)) != j(amB[k]))
    am_added = sorted(set(amB) - set(amA))
    rec("adversarial_map-changes-are-exactly-10-adds-plus-next",
        len(am_added) == 10 and set(am_moved) == set(am_added) | {"next"},
        "%d added, %d moved" % (len(am_added), len(am_moved)))
    for k in ("invariants", "schemas", "hazard_map"):
        rec("canon-%s-byte-identical" % k, j(a[k]) == j(b[k]))

    npass = sum(1 for x in res if x["pass"])
    out = {"artifact": "k349_verification.json", "session": "K349",
           "date_operator_local": "2026-09-17",
           "reproducibility": repro, "canon_top_level_moved": moved,
           "adversarial_map_added": am_added, "results": res,
           "summary": {"checks": len(res), "passed": npass, "all_pass": npass == len(res)}}
    dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "k349_verification.json")
    bb = (json.dumps(out, indent=2, ensure_ascii=True) + "\n").encode("utf-8")
    open(dest, "wb").write(bb)
    print(json.dumps(out["summary"], indent=1))
    print("wrote %s %s" % (dest, hashlib.md5(bb).hexdigest()))
    return 0 if npass == len(res) else 1


if __name__ == "__main__":
    sys.exit(main())

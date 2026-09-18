#!/usr/bin/env python3
"""K351 verification. Emits tools/k351_verification.json.

Three things, and they are the three this project has learned to distrust.

  REPRODUCIBILITY. Every builder is run FROM ITS COMMITTED LOCATION into a scratch tree and
  its artifact byte-compared -- under two forced PYTHONHASHSEED values, because a seeded or
  set-ordered step is reproducible only by accident until it is shown otherwise (ccclxvii).

  CHANGE ISOLATION on canon, measured rather than claimed: which top-level values moved,
  which adversarial_map subkeys were added, and that `invariants`, `schemas` and
  `hazard_map` did not move.

  THE FENCES. The three shipped surfaces and the cross-surface gate, read at the moment the
  verification runs rather than carried from the opening report.
"""
import os, sys, json, hashlib, shutil, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K348_REPO") or os.path.dirname(HERE)
STAGE = os.path.join(REPO, "adversarial_map_staging")
md5f = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()

# (script dir, script, the artifact it writes, relative to a --out root)
BUILDS = [
    ("tools", "amend_phaseG_K351.py", "adversarial_map_staging/adv_map_phaseG_v0_1.json"),
    ("tools", "patch_assembly_v1_3.py", "adversarial_map_staging/build_assembly_v1_3.py"),
    ("tools", "patch_register_v0_4.py", "adversarial_map_staging/build_register_v0_4.py"),
    ("adversarial_map_staging", "build_assembly_v1_3.py",
     "adversarial_map_staging/adversarial_map_v1_3.json"),
    ("adversarial_map_staging", "build_register_v0_4.py",
     "adversarial_map_staging/honest_residuals_register_v0_4.json"),
    ("adversarial_map_staging", "render_register_v0_4.py",
     "adversarial_map_staging/honest_residuals_register_v0_4.md"),
    ("tools", "build_canon_v38_13.py", "project_canon_v38_13.json"),
]
SURFACES = {
    "combined.html": "72187f6cf0fccdf8e9f4ec6ca5ce009c",
    "efilist_argument_library_v4_0_0.json": "04bf6482aa0374ee92a81c1d55ec41f8",
    "efilist_argument_library_v4_0_0.jsx": "b196548b6eb39065842d62292acca89f",
}
FROZEN = {
    "adversarial_map_staging/adversarial_map_v1_0.json": "c4989e98b042e2f787a82df3f11ecdad",
    "adversarial_map_staging/adversarial_map_v1_1.json": "e9e5abf820e3f7a687e2b84443883ade",
    "adversarial_map_staging/adversarial_map_v1_2.json": "e4bef3cac882aa079951ba7ec1a9d11e",
    "adversarial_map_staging/honest_residuals_register_v0_3.json": "56a86d36e0354f00051a84ca02993fab",
    "adversarial_map_staging/build_assembly_v1_2.py": "45e711f47aad877741950dae43db929c",
    "adversarial_map_staging/build_register_v0_3.py": "98a63164315a33f63a59894e550182db",
    "adversarial_map_staging/adv_map_validator_v0_6.py": "c002e93877b09d523daf786036af7a57",
}


def main():
    checks = []

    def rec(name, ok, detail=""):
        checks.append({"name": name, "pass": bool(ok), "detail": detail})
        print("%s . %s %s" % ("PASS" if ok else "FAIL", name, detail))

    for rel, want in sorted(SURFACES.items()):
        rec("surface-unmoved:" + rel, md5f(os.path.join(REPO, rel)) == want,
            md5f(os.path.join(REPO, rel)))
    for rel, want in sorted(FROZEN.items()):
        rec("predecessor-unmoved:" + os.path.basename(rel),
            md5f(os.path.join(REPO, rel)) == want, md5f(os.path.join(REPO, rel)))

    # cwd=REPO, not HERE: the gate takes --dir defaulting to ".", so running it from
    # tools/ measures an empty directory and reports its own working directory as the
    # finding. Named here because it looked exactly like a red gate for one run.
    r = subprocess.run([sys.executable, os.path.join(HERE, "xsurface_v4_1_0.py")],
                       capture_output=True, text=True, cwd=REPO)
    rec("cross-surface-gate-green", r.returncode == 0 and "GREEN" in r.stdout,
        (r.stdout.strip().splitlines() or ["(no output)"])[-1][:90])

    # ---- reproducibility, twice, with the hash seed forced -------------------------
    runs = 0
    for seed in ("0", "12345"):
        tmp = tempfile.mkdtemp(prefix="k351v_%s_" % seed)
        for sub in ("tools", "adversarial_map_staging"):
            os.makedirs(os.path.join(tmp, sub), exist_ok=True)
        os.symlink(os.path.join(REPO, "efilist_argument_library_v4_0_0.json"),
                   os.path.join(tmp, "efilist_argument_library_v4_0_0.json"))
        for d_, script, art in BUILDS:
            env = dict(os.environ, PYTHONHASHSEED=seed, K348_REPO=REPO)
            if script in ("build_register_v0_4.py", "render_register_v0_4.py"):
                env["K348_MAP_DIR"] = os.path.join(tmp, "adversarial_map_staging")
            rr = subprocess.run([sys.executable, os.path.join(REPO, d_, script), "--out", tmp],
                                capture_output=True, text=True, cwd=os.path.join(REPO, d_),
                                env=env)
            got = os.path.join(tmp, art)
            ok = rr.returncode == 0 and os.path.exists(got) \
                and md5f(got) == md5f(os.path.join(REPO, art))
            runs += 1
            rec("reproduces[seed=%s]:%s" % (seed, script), ok,
                (md5f(got) if os.path.exists(got)
                 else "(not written) " + (rr.stdout + rr.stderr)[-80:]))
        shutil.rmtree(tmp, ignore_errors=True)

    # ---- the control artifacts must reproduce too ---------------------------------
    #      K349's assembly_control_v0_2.json cannot: it carries a session id and a random
    #      tempdir name. A control battery whose OUTPUT is not reproducible is a receipt
    #      nothing can re-derive, which is the shape this project keeps registering.
    for script, art in (("controls_assembly_v1_3.py", "assembly_control_v0_3.json"),
                        ("controls_register_v0_4.py", "register_control_v0_2.json")):
        tmpf = tempfile.mkdtemp(prefix="k351c_")
        dest = os.path.join(tmpf, art)
        rr = subprocess.run([sys.executable, os.path.join(STAGE, script), dest],
                            capture_output=True, text=True, cwd=STAGE,
                            env=dict(os.environ, K348_REPO=REPO))
        ok = rr.returncode == 0 and os.path.exists(dest) \
            and md5f(dest) == md5f(os.path.join(STAGE, art))
        rec("control-artifact-reproduces:" + art, ok,
            (md5f(dest) if os.path.exists(dest) else "(not written)"))
        shutil.rmtree(tmpf, ignore_errors=True)

    # ---- canon change isolation ----------------------------------------------------
    a = json.loads(open(os.path.join(REPO, "project_canon_v38_12.json"), "rb").read().decode("utf-8"))
    b = json.loads(open(os.path.join(REPO, "project_canon_v38_13.json"), "rb").read().decode("utf-8"))
    j = lambda x: json.dumps(x, sort_keys=True, ensure_ascii=False)
    rec("canon-keyset-held-at-41", list(a) == list(b) and len(b) == 41, "%d" % len(b))
    moved = sorted(k for k in b if j(a.get(k)) != j(b[k]))
    ALLOWED = ["adversarial_map", "canon_version", "canon_version_marker", "keyset_delta_ledger",
               "last_updated_by_session", "next_recommended_session", "session_log_recent",
               "terminal_stability_marker"]
    rec("canon-only-the-allowed-top-level-values-moved", moved == ALLOWED, str(moved))
    for k in ("invariants", "schemas", "hazard_map"):
        rec("canon-%s-byte-identical" % k, j(a[k]) == j(b[k]), "")
    am_new = sorted(set(b["adversarial_map"]) - set(a["adversarial_map"]))
    am_moved = sorted(k for k in a["adversarial_map"]
                      if j(a["adversarial_map"][k]) != j(b["adversarial_map"].get(k)))
    rec("canon-adversarial_map-gains-exactly-five-subkeys", len(am_new) == 5, str(am_new))
    rec("canon-adversarial_map-changes-exactly-three-existing",
        am_moved == ["HR_15_ratification_K350", "care_ethics_supersession_RATIFIED_K350", "next"],
        str(am_moved))
    hr_new = sorted(set(b["terminal_stability_marker"]["honest_residuals"])
                    - set(a["terminal_stability_marker"]["honest_residuals"]))
    tsm_moved = sorted(k for k in a["terminal_stability_marker"]
                       if j(a["terminal_stability_marker"][k])
                       != j(b["terminal_stability_marker"].get(k)))
    rec("canon-honest_residuals-gains-exactly-HR-15", hr_new == ["currency_of_obligation"]
        and tsm_moved == ["honest_residuals"], "%s / %s" % (hr_new, tsm_moved))
    rec("canon-session-log-gains-exactly-one-entry",
        len(b["session_log_recent"]) == len(a["session_log_recent"]) + 1
        and b["session_log_recent"][:-1] == a["session_log_recent"],
        "%d -> %d" % (len(a["session_log_recent"]), len(b["session_log_recent"])))

    npass = sum(1 for c in checks if c["pass"])
    out = {"artifact": "k351_verification.json", "generated_by": "tools/verify_k351.py",
           "session": "K351", "date_operator_local": "2026-09-18",
           "reproducibility_runs": runs,
           "pins": {os.path.basename(a_): md5f(os.path.join(REPO, a_))
                    for _d, _s, a_ in BUILDS},
           "checks": checks,
           "summary": {"checks": len(checks), "passed": npass, "all_pass": npass == len(checks)}}
    dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "k351_verification.json")
    bb = (json.dumps(out, indent=2, ensure_ascii=True) + "\n").encode("utf-8")
    open(dest, "wb").write(bb)
    print(json.dumps(out["summary"], indent=1))
    print("wrote %s %s" % (dest, hashlib.md5(bb).hexdigest()))
    return 0 if npass == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())

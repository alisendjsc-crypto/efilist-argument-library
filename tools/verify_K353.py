#!/usr/bin/env python3
"""verify_K353.py -- one verifier for the whole K353 cut, and the source of every constant
the operator blocks quote.

It does four things and nothing else:
  1. REPRODUCTION. Runs each generator FROM ITS COMMITTED LOCATION into a scratch tree, twice
     under two forced PYTHONHASHSEED values, and byte-compares the result against what is on
     disk. A generator that cannot reproduce its own artifact has not been verified, it has
     been trusted.
  2. HELD. Asserts the flagship, corpus, jsx, all four maps, the register, the validator and
     the designs are byte-identical git-to-git, and runs the cross-surface gate.
  3. CONTROLS. Re-runs the wing control battery and requires zero failures.
  4. PINS. Emits tools/k353_pins.json binding every constant the handoff blocks will carry, so
     the block emitter can assert each one against a value measured THIS session rather than
     typed (ccclxii).

Repo-relative. Runs on the operator VM; the FUNCTIONAL gate does not and is not run here.
"""
import io, os, sys, json, hashlib, subprocess, tempfile, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
STG = os.path.join(REPO, "adversarial_map_staging")

fails, log = [], []
def chk(name, cond, got=""):
    log.append({"check": name, "ok": bool(cond), "detail": str(got)[:300]})
    print(("  ok    " if cond else "  FAIL  ") + name + (("   " + str(got)[:200]) if not cond else ""))
    if not cond: fails.append(name)

def md5f(p): return hashlib.md5(io.open(p, "rb").read()).hexdigest()
def blob(path):
    r = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + path], capture_output=True)
    return hashlib.md5(r.stdout).hexdigest() if r.returncode == 0 else None

# ---------------------------------------------------------------- 1 reproduction
# (script, argv-out-flag, repo-relative artifact, cwd)
GENS = [
    ("adversarial_map_staging/render_wing_v0_1.py", "--out", "adversarial/index.html", STG),
    ("adversarial_map_staging/render_wing_v0_1.py", "--out", "adversarial/index.html", REPO),
    ("tools/frontdoor_K353.py", "--out", "libraries/index.html", HERE),
    ("tools/frontdoor_K353.py", "--out", "libraries/index.html", REPO),
]

def main():
    print("verify_K353 -- repo %s" % REPO)
    print("REPRODUCTION (from committed locations, two forced PYTHONHASHSEED values)")
    runs = 0
    for script, flag, artifact, cwd in GENS:
        want = md5f(os.path.join(REPO, artifact))
        for seed in ("0", "1"):
            with tempfile.TemporaryDirectory() as td:
                out = os.path.join(td, os.path.basename(artifact))
                env = dict(os.environ, PYTHONHASHSEED=seed)
                r = subprocess.run([sys.executable, os.path.join(REPO, script), flag, out],
                                   cwd=cwd, env=env, capture_output=True, text=True)
                got = md5f(out) if r.returncode == 0 and os.path.exists(out) else (r.stderr or r.stdout)[-160:]
            runs += 1
            chk("%-42s seed=%s cwd=%-9s" % (os.path.basename(script), seed,
                                            "staging" if cwd == STG else ("tools" if cwd == HERE else "root")),
                got == want, got)
    # the canon builder emits by NAME into --out <dir>
    want_canon = md5f(os.path.join(REPO, "project_canon_v38_15.json"))
    for seed in ("0", "1"):
        with tempfile.TemporaryDirectory() as td:
            env = dict(os.environ, PYTHONHASHSEED=seed)
            r = subprocess.run([sys.executable, os.path.join(REPO, "tools/build_canon_v38_15.py"),
                                "--out", td], cwd=HERE, env=env, capture_output=True, text=True)
            p = os.path.join(td, "project_canon_v38_15.json")
            got = md5f(p) if r.returncode == 0 and os.path.exists(p) else (r.stderr or r.stdout)[-160:]
        runs += 1
        chk("build_canon_v38_15.py                      seed=%s cwd=tools    " % seed,
            got == want_canon, got)
    chk("every generator reproduced, %d runs" % runs, not fails)

    # ---------------------------------------------------------------- 2 held
    print("HELD (git-to-git; a worktree md5 is not evidence about a commit)")
    HELD = {
        "combined.html": "f095c0ce0e5a1d796d57fa5a5dd62f7d",
        "efilist_argument_library_v4_0_0.json": "04bf6482aa0374ee92a81c1d55ec41f8",
        "efilist_argument_library_v4_0_0.jsx": "b196548b6eb39065842d62292acca89f",
        "adversarial_map_staging/adversarial_map_v1_0.json": "c4989e98b042e2f787a82df3f11ecdad",
        "adversarial_map_staging/adversarial_map_v1_1.json": "e9e5abf820e3f7a687e2b84443883ade",
        "adversarial_map_staging/adversarial_map_v1_2.json": "e4bef3cac882aa079951ba7ec1a9d11e",
        "adversarial_map_staging/adversarial_map_v1_3.json": "681827419df72a16a7c6fe70df8fe77f",
        "adversarial_map_staging/honest_residuals_register_v0_4.json": "d067729fafb51926bc9e845209417886",
        "adversarial_map_staging/adv_map_validator_v0_6.py": "c002e93877b09d523daf786036af7a57",
        "adversarial_map_staging/adversarial_map_design_v0_5.md": "ab9569122de23de82db2ab5600d86d9e",
        "adversarial_map_staging/adv_map_phaseG_v0_1.json": "571cd47305612068651f13ca049557c2",
        "project_canon_v38_14.json": "0eb13633ab88087d5f882f94bb6edfc9",
    }
    for p, h in sorted(HELD.items()):
        b, w = blob(p), md5f(os.path.join(REPO, p))
        chk("HELD %-58s" % p, b == h and w == h, "blob %s worktree %s" % (b, w))
    r = subprocess.run([sys.executable, os.path.join(REPO, "tools/xsurface_v4_1_0.py")],
                       cwd=REPO, capture_output=True, text=True)
    chk("cross-surface gate GREEN at 6cd132ee5b8c7ca78ad0e095806f1c93",
        r.returncode == 0 and "6cd132ee5b8c7ca78ad0e095806f1c93" in r.stdout
        and "X-SURFACE GATE: GREEN" in r.stdout, r.stdout[-200:])

    # ---------------------------------------------------------------- 3 controls
    print("CONTROLS")
    r = subprocess.run([sys.executable, os.path.join(STG, "controls_wing_v0_1.py")],
                       cwd=REPO, capture_output=True, text=True)
    chk("wing control battery, zero failures", r.returncode == 0, r.stdout[-200:])
    cj = json.load(io.open(os.path.join(STG, "wing_control_v0_1.json"), encoding="utf-8"))
    chk("control artifact records its own result", cj["failed"] == 0 and cj["checks"] >= 50,
        "%d checks / %d failed" % (cj["checks"], cj["failed"]))

    # ---------------------------------------------------------------- 4 pins
    NEW = ["adversarial/index.html", "adversarial_map_staging/render_wing_v0_1.py",
           "adversarial_map_staging/controls_wing_v0_1.py",
           "adversarial_map_staging/wing_control_v0_1.json",
           "tools/frontdoor_K353.py", "tools/build_canon_v38_15.py", "tools/verify_K353.py",
           "tools/k353_wing_functional_gate.py", "tools/k353_wing_functional_control_v0_1.json",
           "project_canon_v38_15.json"]
    MOD = ["libraries/index.html"]
    pins = {"held": HELD, "new": {}, "modified": {}, "removed": ["project_canon_v38_14.json"]}
    for p in NEW:
        fp = os.path.join(REPO, p)
        if os.path.exists(fp):
            pins["new"][p] = {"md5": md5f(fp), "bytes": os.path.getsize(fp)}
        else:
            chk("NEW file present: %s" % p, False, "absent")
    for p in MOD:
        fp = os.path.join(REPO, p)
        pins["modified"][p] = {"md5": md5f(fp), "bytes": os.path.getsize(fp),
                               "base_md5": blob(p), "base_bytes": None}
    pins["staged_expected"] = sorted(list(pins["new"]) + MOD + ["project_canon_v38_14.json"])
    pins["head_at_measure"] = subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD"],
                                             capture_output=True, text=True).stdout.strip()
    io.open(os.path.join(HERE, "k353_pins.json"), "w", encoding="utf-8", newline="\n").write(
        json.dumps(pins, indent=1, sort_keys=True) + "\n")
    print("\n  pins -> tools/k353_pins.json   (%d new, %d modified, %d held)"
          % (len(pins["new"]), len(pins["modified"]), len(pins["held"])))

    io.open(os.path.join(HERE, "k353_verification.json"), "w", encoding="utf-8", newline="\n").write(
        json.dumps({"checks": len(log), "failed": len(fails), "failures": fails, "results": log},
                   indent=1, sort_keys=True) + "\n")
    print("  %d checks, %d failed -> tools/k353_verification.json" % (len(log), len(fails)))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()

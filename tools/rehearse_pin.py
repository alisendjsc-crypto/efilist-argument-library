#!/usr/bin/env python3
"""rehearse_pin.py -- rehearse the corpus pin move before trusting the instruments (L5, 2026-09-26, R0150 ph. 1).

R0150 phase 1: "Rehearse the pin before trusting it. Work in a scratch clone and edit one queued sentence on
all three surfaces. Every gate must stay GREEN there. The unpinned version of at least one gate must go RED,
which shows the pin is load-bearing. Run the unmutated control first."

This edits EVERY queued sentence, not one: each sentence the newest pin-move queue block in canon names is
replaced by a placeholder on all three surfaces (corpus JSON, JSX, site/combined.html), in the JSON string
encoding all three share. That is the strongest edit the pin can make: every anchor and every quote inside a
repaired sentence breaks at once.

In a scratch clone of this repository, carrying the working tree's tracked changes and new files:
  C0  unmutated: the gate battery GREEN, every instrument run, every output hashed.
  C1  edited corpus: xsurface GREEN on the edited surfaces (they agree), the gate battery GREEN, and every
      instrument's output byte-identical to C0's. Nothing the records say moved.
  C2  edited corpus with the instruments as they were at BASE (before L5 pinned them): at least one gate RED.
  C3  the three lineage builders (maps v1_1..v1_3), which must stay byte-identical, run through
      tools/pinned_farm.py on the edited corpus: each reproduces its committed map.
  SWb the sweep below with the instruments at BASE: what the edit did before L5 (a record, not a verdict).
  SW  every tracked script that names the corpus, run with no arguments in C0's state and C1's: the outcome
      (exit status, tracked files it changed, files it added) must be the same in both, except for the lineage
      builders (C3 covers them) and scripts that already did not reproduce unmutated (listed, not excused
      silently: each is named in the record).

  python3 tools/rehearse_pin.py            # rehearse; print; write nothing in the repo
  python3 tools/rehearse_pin.py --emit     # also write tools/pin_rehearsal_v0_1.json
  python3 tools/rehearse_pin.py --check    # exit 1 unless the committed record equals a fresh run

Deterministic: outputs are hashed, never quoted; no scratch path, time or scratch commit enters the record.

HOUSEKEEPING (added the same day, after it bit): every subprocess runs with TMPDIR inside this run's scratch, so the
older instruments' leaked scratch directories (k349asm_, k351asm_, k346ctl_ ...) go when the scratch goes; and a
swept script that times out is killed with its whole process group. The first run of this tool swept itself, and the
timeout killed only the direct child: its grandchildren kept rehearsing, recursively, and filled the shared /tmp.
"""
import hashlib, io, json, os, re, shutil, signal, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
RECORD = os.path.join(HERE, "pin_rehearsal_v0_1.json")
BASE = "09289dd2c2f8b730fa7df73a84e349f8ad53983d"   # efilist HEAD when L5 opened: the instruments unpinned
SURFACES = ["efilist_argument_library_v4_0_0.json", "efilist_argument_library_v4_0_0.jsx", "site/combined.html"]
S, R = "adversarial_map_staging", "adversarial_map_staging/r1"

GATES = [
    ("xsurface", ["tools/xsurface_v4_1_0.py"]),
    ("sidecars", ["tools/build_map_sidecars.py", "--check"]),
    ("rulings_gate", [R + "/r1_rulings_gate.py"]),
    ("quote_check_rulings", [R + "/r1_quote_check.py", "--rulings"]),
    ("quote_check_selftest", [R + "/r1_quote_check.py", "--self-test"]),
    ("collision_v0_2", [R + "/r1_collision_list.py"]),
    ("collision_v0_1", [R + "/r1_collision_list.py", "--rule", "v0_1"]),
    ("controls_assembly_v1_4", [S + "/controls_assembly_v1_4.py", "--check"]),
    ("controls_register_v0_5", [S + "/controls_register_v0_5.py", "--check"]),
    ("l4_knock_on", [R + "/l4_knock_on.py", "--check"]),
    ("judgments_gate", [R + "/r1_judgments_gate.py"]),
    ("controls_v1_5", [S + "/controls_v1_5.py", "--check"]),
    ("v1_5_judgments_gate", [R + "/r1_v1_5_judgments_gate.py"]),
    ("icons", ["tools/icons_regen_check.py"]),
    ("controls_v1_6", [S + "/controls_v1_6.py", "--check"]),
    ("l4c_knock_on", [R + "/l4c_knock_on.py", "--check"]),
    ("l4c_knock_on_selftest", [R + "/l4c_knock_on.py", "--self-test"]),
    ("v1_6_judgments_gate", [R + "/r1_v1_6_judgments_gate.py"]),
    ("v1_6_reading", [R + "/r1_v1_6_reading.py", "--check"]),
]
# self-tests whose emitted control record must equal the committed one (emitted under the same basename)
EMITS = [
    ("rulings_selftest", R + "/r1_rulings_gate.py", R + "/r1_rulings_gate_control_v0_3.json"),
    ("judgments_selftest", R + "/r1_judgments_gate.py", R + "/r1_judgments_gate_control_v0_5.json"),
    ("v1_5_judgments_selftest", R + "/r1_v1_5_judgments_gate.py", R + "/r1_v1_5_judgments_gate_control_v0_3.json"),
    ("v1_6_judgments_selftest", R + "/r1_v1_6_judgments_gate.py", R + "/r1_v1_6_judgments_gate_control_v0_1.json"),
]
# instruments that write under --out; their output trees are hashed
OUTS = [
    ("draft_dossiers", [R + "/r1_draft_dossiers.py", "--out", "{o}"]),
    ("knock_on_dossiers", [R + "/r1_knock_on_dossiers.py", "--out", "{o}"]),
    ("r1_dossiers_all", [R + "/r1_dossiers.py", "--out", "{o}", "--all"]),
    ("build_v1_6", [S + "/build_assembly_v1_6.py", "--out", "{o}"]),
    ("render_wing", [S + "/render_wing_v0_1.py", "--out", "{o}/index.html"]),
]
LINEAGE = [("build_assembly_v1_1.py", "adversarial_map_v1_1.json"),
           ("build_assembly_v1_3.py", "adversarial_map_v1_3.json")]
SWEEP_SKIP = {"tools/build_k354_pins.py": "names a Cowork /sessions path",
              "tools/rehearse_pin.py": "this file",
              "tools/build_canon_v38_30.py": "reads the record this file writes"}
LINEAGE_BUILDERS = {S + "/" + b for b, _ in LINEAGE} | {S + "/build_assembly_v1_2.py"}


def md5b(b):
    return hashlib.md5(b).hexdigest()


ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")


def sh(cmd, cwd, **kw):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=ENV, **kw)


def tree_md5(d):
    h = hashlib.md5()
    for root, dirs, fs in os.walk(d):
        dirs.sort()
        for f in sorted(fs):
            p = os.path.join(root, f)
            h.update(os.path.relpath(p, d).encode()); h.update(md5b(open(p, "rb").read()).encode())
    return h.hexdigest()


def queue_sentences(repo):
    canons = sorted(f for f in os.listdir(repo) if re.match(r"project_canon_v38_\d+\.json$", f))
    assert len(canons) == 1, canons
    am = json.load(open(os.path.join(repo, canons[0]), encoding="utf-8"))["adversarial_map"]
    blocks = [k for k in am if k.startswith("pin_move_queue_")]
    newest = blocks[-1]   # canon keeps insertion order; the newest block of the kind is the last
    out = []
    for r in am[newest]["rows"]:
        for i, s in enumerate(r.get("sentences") or [r["sentence"]]):
            out.append(("%s%s" % (r["id"], "" if i == 0 else "." + str(i + 1)), s))
    return newest, out


def edit_surfaces(clone, sents):
    enc = lambda s: json.dumps(s, ensure_ascii=False)[1:-1]
    for f in SURFACES:
        p = os.path.join(clone, f)
        t = io.open(p, encoding="utf-8", newline="").read()
        for pid, s in sents:
            new = "Rehearsal replacement for %s." % pid
            assert t.count(enc(s)) == 1, "%s: %s occurs %d times" % (f, pid, t.count(enc(s)))
            t = t.replace(enc(s), enc(new))
        io.open(p, "w", encoding="utf-8", newline="").write(t)


def battery(clone):
    res = {}
    for name, args in GATES:
        r = sh([sys.executable] + args, clone)
        res[name] = r.returncode
    return res


def emits(clone, scratch):
    res = {}
    for name, gate, ctl in EMITS:
        d = tempfile.mkdtemp(dir=scratch)
        p = os.path.join(d, os.path.basename(ctl))
        r = sh([sys.executable, gate, "--self-test", "--emit", p], clone)
        same = os.path.exists(p) and open(p, "rb").read() == open(os.path.join(clone, ctl), "rb").read()
        res[name] = {"rc": r.returncode, "reproduces_committed_control": same}
    return res


def outs(clone, scratch):
    res = {}
    for name, args in OUTS:
        d = tempfile.mkdtemp(dir=scratch)
        r = sh([sys.executable] + [a.replace("{o}", d) for a in args], clone)
        res[name] = {"rc": r.returncode, "tree_md5": tree_md5(d)}
    return res


def lineage(clone):
    res = {}
    for builder, out in LINEAGE:
        before = md5b(open(os.path.join(clone, S, out), "rb").read())
        r = sh([sys.executable, "tools/pinned_farm.py", S + "/" + builder], clone)
        after = md5b(open(os.path.join(clone, S, out), "rb").read())
        res[builder] = {"rc": r.returncode, "reproduces": before == after, "map_md5": after}
        sh(["git", "checkout", "--", S + "/" + out], clone)
    return res


def reset(clone, edit=None):
    sh(["git", "checkout", "--", "."], clone); sh(["git", "clean", "-fdq"], clone)
    if edit:
        edit_surfaces(clone, edit)


def sweep(clone, edit=None):
    files = sorted(l for l in sh(["git", "ls-files", "*.py"], clone).stdout.split()
                   if "efilist_argument_library_v4_0_0" in open(os.path.join(clone, l), encoding="utf-8").read())
    res = {}
    for f in files:
        if f in SWEEP_SKIP:
            continue
        reset(clone, edit)
        p = subprocess.Popen([sys.executable, f], cwd=clone, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             stdin=subprocess.DEVNULL, env=ENV, start_new_session=True)
        try:
            rc = p.wait(timeout=300)
        except subprocess.TimeoutExpired:
            os.killpg(p.pid, signal.SIGKILL)   # the whole group: a timeout must not orphan grandchildren
            p.wait()
            rc = "timeout"
        st = sh(["git", "status", "--porcelain"], clone).stdout.splitlines()
        changed = sorted(l[3:] for l in st if l[:2] == " M" and l[3:] not in SURFACES)
        added = sorted(l[3:] for l in st if l[:2] == "??")
        res[f] = {"rc": rc, "changed": changed, "added": added}
    reset(clone)
    return res


def rehearse():
    scratch = tempfile.mkdtemp(prefix="rehearse_pin_")
    os.makedirs(os.path.join(scratch, "tmp"))
    ENV["TMPDIR"] = os.path.join(scratch, "tmp")
    try:
        clone = os.path.join(scratch, "clone")
        assert sh(["git", "clone", "--quiet", "--no-hardlinks", REPO, clone], scratch).returncode == 0
        # carry the working tree: tracked changes and new, unignored files; commit them in the clone only
        gone = sorted(set(sh(["git", "diff", "--name-only", "--no-renames", "--diff-filter=D", "HEAD"], REPO).stdout.split()))
        overlay = sorted(set(sh(["git", "ls-files", "-m", "-o", "--exclude-standard"], REPO).stdout.split()) - set(gone))
        for f in overlay:
            dst = os.path.join(clone, f)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(os.path.join(REPO, f), dst)
        for f in gone:
            sh(["git", "rm", "-q", "--", f], clone)
        if overlay or gone:
            sh(["git", "add", "--"] + overlay, clone)
            sh(["git", "-c", "user.name=rehearsal", "-c", "user.email=rehearsal@invalid", "commit", "-qm", "overlay"], clone)
        block, sents = queue_sentences(clone)
        rec = {"queue_block": block, "sentences": [p for p, _ in sents], "base_commit": BASE}

        o0 = outs(clone, scratch)
        rec["C0_unmutated"] = {"gates": battery(clone), "self_tests": emits(clone, scratch)}
        edit_surfaces(clone, sents)
        rec["edited_surfaces_md5"] = {f: md5b(open(os.path.join(clone, f), "rb").read()) for f in SURFACES}
        o1 = outs(clone, scratch)
        rec["C1_edited_pinned"] = {"gates": battery(clone), "self_tests": emits(clone, scratch)}
        # outputs are compared, not recorded: r1_dossiers names the canon file in its header, so a raw hash
        # would tie this record to one canon version
        rec["outputs_C0_vs_C1"] = {k: {"rc_unmutated": o0[k]["rc"], "rc_edited": o1[k]["rc"],
                                       "identical": o0[k]["tree_md5"] == o1[k]["tree_md5"]} for k in o0}
        rec["C3_lineage_via_farm"] = lineage(clone)
        # C2: the same edited corpus, with every file L5 changed put back as it was at BASE
        # L5's instruments only: other lanes' commits since BASE (the design lane's tools) are not what is tested
        moved = [l for l in sh(["git", "diff", "--name-only", BASE, "HEAD"], clone).stdout.split()
                 if l.startswith(S + "/") and l.endswith(".py")
                 and sh(["git", "cat-file", "-e", "%s:%s" % (BASE, l)], clone).returncode == 0]
        sh(["git", "checkout", BASE, "--"] + moved, clone)
        rec["C2_edited_unpinned"] = {"instruments_at_base": moved, "gates": battery(clone)}
        # the same sweep as SW below, with the instruments as they were at BASE: what the edit did before L5
        b0, b1 = sweep(clone), sweep(clone, sents)
        rec["SW_sweep_base"] = {f: {"unmutated": b0[f], "edited": b1[f], "same": b0[f] == b1[f]} for f in b0}
        sh(["git", "checkout", "HEAD", "--"] + moved, clone)
        sh(["git", "checkout", "--"] + SURFACES, clone)

        sw0 = sweep(clone)
        sw1 = sweep(clone, sents)
        rec["SW_sweep"] = {f: {"unmutated": sw0[f], "edited": sw1[f], "same": sw0[f] == sw1[f]} for f in sw0}
        rec["SW_skipped"] = {f: why for f, why in sorted(SWEEP_SKIP.items())
                             if os.path.exists(os.path.join(clone, f))}

        c0, c1, c2 = rec["C0_unmutated"], rec["C1_edited_pinned"], rec["C2_edited_unpinned"]
        red_unpinned = sorted(k for k, v in c2["gates"].items() if v != 0)
        rec["verdict"] = {
            "C0_all_gates_green": all(v == 0 for v in c0["gates"].values()),
            "C0_self_tests_reproduce": all(v["rc"] == 0 and v["reproduces_committed_control"] for v in c0["self_tests"].values()),
            "C1_all_gates_green": all(v == 0 for v in c1["gates"].values()),
            "C1_self_tests_reproduce": all(v["rc"] == 0 and v["reproduces_committed_control"] for v in c1["self_tests"].values()),
            "C1_outputs_identical_to_C0": all(x["identical"] for x in rec["outputs_C0_vs_C1"].values()),
            "C1_outputs_all_rc0": all(x["rc_unmutated"] == 0 and x["rc_edited"] == 0 for x in rec["outputs_C0_vs_C1"].values()),
            "C2_red_with_unpinned_instruments": red_unpinned,
            "C3_lineage_reproduces": all(v["rc"] == 0 and v["reproduces"] for v in rec["C3_lineage_via_farm"].values()),
            "SW_same_outcome_edited": sorted(f for f, v in rec["SW_sweep"].items() if v["same"]),
            # expected to differ: the lineage builders read the working corpus by design (C3 covers them), and a
            # script that did not reproduce unmutated (exit status non-zero, or a tracked file changed) proves nothing
            "SW_differs_lineage": sorted(f for f, v in rec["SW_sweep"].items() if not v["same"] and f in LINEAGE_BUILDERS),
            "SW_differs_not_reproducing_unmutated": sorted(
                f for f, v in rec["SW_sweep"].items() if not v["same"] and f not in LINEAGE_BUILDERS
                and (v["unmutated"]["rc"] != 0 or v["unmutated"]["changed"])),
            "SW_differs_unexplained": sorted(
                f for f, v in rec["SW_sweep"].items() if not v["same"] and f not in LINEAGE_BUILDERS
                and v["unmutated"]["rc"] == 0 and not v["unmutated"]["changed"]),
        }
        v = rec["verdict"]
        v["GREEN"] = bool(v["C0_all_gates_green"] and v["C0_self_tests_reproduce"] and v["C1_all_gates_green"]
                          and v["C1_self_tests_reproduce"] and v["C1_outputs_identical_to_C0"] and v["C1_outputs_all_rc0"]
                          and v["C2_red_with_unpinned_instruments"] and v["C3_lineage_reproduces"]
                          and not v["SW_differs_unexplained"])
        return rec
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def main():
    rec = rehearse()
    out = (json.dumps(rec, indent=1, ensure_ascii=False, sort_keys=False) + "\n").encode("utf-8")
    v = rec["verdict"]
    for k, x in v.items():
        print("  %-38s %s" % (k, x if not isinstance(x, list) or len(x) < 8 else "%d files" % len(x)))
    if "--emit" in sys.argv or "--out" in sys.argv:
        dest = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else RECORD
        open(dest, "wb").write(out)
        print("wrote %s  %s" % (dest, md5b(out)))
    if "--check" in sys.argv:
        same = os.path.exists(RECORD) and open(RECORD, "rb").read() == out
        print("REHEARSAL RECORD: %s" % ("matches the committed record" if same else "DIFFERS from the committed record"))
        sys.exit(0 if same and v["GREEN"] else 1)
    print("PIN REHEARSAL: %s" % ("GREEN" if v["GREEN"] else "RED"))
    sys.exit(0 if v["GREEN"] else 1)


if __name__ == "__main__":
    main()

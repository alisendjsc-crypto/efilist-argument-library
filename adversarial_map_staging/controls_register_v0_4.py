#!/usr/bin/env python3
"""K351 controls for honest_residuals_register_v0_4.json. Emits register_control_v0_2.json.

Two claims and four guards.

The CLAIMS are that adding a bedrock added exactly one bedrock -- HR-15 is new, HR-06
gains one relation, and every other bedrock, every other tributary and every other
tributary COUNT are unchanged -- and that HR-15's birth certificate is where the
ratification put it.

The GUARDS are what make the declaration mean anything, and each must refuse for its own
reason: an undeclared adjacency, a shipped bedrock_name the map does not recognise, a
second birth certificate, and a bedrock that drifted from v0_3 without being declared.

Symlink farms rather than copytree: the repo carries a 3 MB flagship and none of these
controls reads it.
"""
import json, os, shutil, subprocess, sys, tempfile, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CORPUS = os.path.join(REPO, "efilist_argument_library_v4_0_0.json")
md5f = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()


def main():
    results = []
    tmp = tempfile.mkdtemp(prefix="k351reg_")

    def rec(name, ok, detail=""):
        results.append({"name": name, "pass": bool(ok), "detail": detail})
        print("%s . %s %s" % ("PASS" if ok else "FAIL", name, detail))

    def farm(sub, real=()):
        root = os.path.join(tmp, sub)
        work = os.path.join(root, "adversarial_map_staging")
        os.makedirs(work)
        for n in os.listdir(HERE):
            if n == "__pycache__":
                continue
            src, dst = os.path.join(HERE, n), os.path.join(work, n)
            (shutil.copyfile if n in real else os.symlink)(src, dst)
        os.symlink(CORPUS, os.path.join(root, os.path.basename(CORPUS)))
        return root, work

    p3 = os.path.join(HERE, "honest_residuals_register_v0_3.json")
    p4 = os.path.join(HERE, "honest_residuals_register_v0_4.json")
    v3, v4 = json.load(open(p3, "rb")), json.load(open(p4, "rb"))

    # ---- 1. ccclxiv: v0_3 still reproduces from its own builder, on its own source
    root, work = farm("repro")
    r = subprocess.run([sys.executable, os.path.join(work, "build_register_v0_3.py"),
                        "--out", root], capture_output=True, text=True, cwd=work,
                       env=dict(os.environ, K348_REPO=root,
                                K348_MAP_DIR=os.path.join(HERE)))
    repro = os.path.join(root, "adversarial_map_staging", "honest_residuals_register_v0_3.json")
    got = md5f(repro) if os.path.exists(repro) else "(not written): " + (r.stdout + r.stderr)[-90:]
    rec("v0_3-reproduces-byte-identically-from-its-own-builder", got == md5f(p3),
        "%s vs %s" % (got, md5f(p3)))
    rec("v0_3-unmoved", md5f(p3) == "56a86d36e0354f00051a84ca02993fab", md5f(p3))

    b3 = {b["bedrock_id"]: b for b in v3["bedrocks"]}
    b4 = {b["bedrock_id"]: b for b in v4["bedrocks"]}
    rec("bedrock-count-14-to-15", len(b3) == 14 and len(b4) == 15,
        "%d -> %d" % (len(b3), len(b4)))
    rec("exactly-HR-15-is-new", sorted(set(b4) - set(b3)) == ["HR-15"] and not (set(b3) - set(b4)),
        "added %s, lost %s" % (sorted(set(b4) - set(b3)), sorted(set(b3) - set(b4))))

    j = lambda x: json.dumps(x, sort_keys=True, ensure_ascii=False)
    drift = [i for i in b4 if i in b3 and i != "HR-06" and j(b3[i]) != j(b4[i])]
    rec("every-other-bedrock-byte-identical-to-v0_3", not drift, "drifted: %s" % drift)

    a6 = [r_ for r_ in b4["HR-06"]["relations"] if r_ not in b3["HR-06"]["relations"]]
    l6 = [r_ for r_ in b3["HR-06"]["relations"] if r_ not in b4["HR-06"]["relations"]]
    rec("HR-06-gains-exactly-depends_on-HR-15",
        len(a6) == 1 and not l6 and a6[0]["kind"] == "depends_on" and a6[0]["to"] == "HR-15",
        "+%d/-%d" % (len(a6), len(l6)))
    rec("HR-06-changed-nothing-but-its-relations",
        j(dict(b3["HR-06"], relations=None)) == j(dict(b4["HR-06"], relations=None)), "")

    counts_moved = {i: (b3[i]["tributary_count"], b4[i]["tributary_count"])
                    for i in b4 if i in b3 and b3[i]["tributary_count"] != b4[i]["tributary_count"]}
    rec("no-bedrock-changed-tributary-count", not counts_moved, str(counts_moved))

    h15 = b4["HR-15"]
    rec("HR-15-birth-certificate-is-care-ethics-note-phase-G",
        h15["birth_certificate"] == {"phase": "G", "node": "care-ethics", "locus": "note"}
        and h15["tributary_count"] == 1 and h15["registered_in"] == "this-program"
        and h15["alias"] == "rival-occupant",
        json.dumps(h15["birth_certificate"]))
    rec("HR-15-facet-is-the-one-canon-names",
        [f["facet_id"] for f in h15["facets"]] == ["unchosen-relations-bind-without-authorization"],
        str([f["facet_id"] for f in h15["facets"]]))
    rec("HR-15-declares-sibling_of-HR-03",
        [(r_["kind"], r_["to"]) for r_ in h15["relations"]] == [("sibling_of", "HR-03")], "")
    rec("residue-entry-count-39-to-40",
        v3["meta"]["residue_entries"] == 39 and v4["meta"]["residue_entries"] == 40,
        "%d -> %d" % (v3["meta"]["residue_entries"], v4["meta"]["residue_entries"]))
    und = [a for a in v4["audit"] if a["severity"] == "undeclared-adjacency"]
    rec("no-undeclared-adjacency", not und, "%d" % len(und))

    # ---- the REFUSAL controls -------------------------------------------------------
    def run_mutated(name, needle, edit_builder=None, edit_fragment=None):
        root, work = farm("g%d" % len(os.listdir(tmp)),
                          real=("build_register_v0_4.py", "adv_map_phaseG_v0_1.json",
                                "adversarial_map_v1_3.json"))
        if edit_builder:
            p = os.path.join(work, "build_register_v0_4.py")
            src = open(p, "rb").read().decode("utf-8")
            new = edit_builder(src)
            assert new != src, "%s: the builder edit changed nothing" % name
            open(p, "w", encoding="utf-8", newline="\n").write(new)
        if edit_fragment:
            p = os.path.join(work, "adversarial_map_v1_3.json")
            d = json.loads(open(p, "rb").read().decode("utf-8"))
            edit_fragment(d)
            open(p, "wb").write((json.dumps(d, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
        r = subprocess.run([sys.executable, os.path.join(work, "build_register_v0_4.py"),
                            "--out", root], capture_output=True, text=True, cwd=work,
                           env=dict(os.environ, K348_REPO=root))
        blob = r.stdout + r.stderr
        hit = [l for l in blob.splitlines() if needle in l]
        rec(name, r.returncode != 0 and bool(hit),
            "rc=%d | %s" % (r.returncode, (hit[-1][:120] if hit
                                           else "NO LINE MATCHED %r" % needle)))

    run_mutated("an-undeclared-adjacency-refuses", "UNDECLARED ADJACENCY",
                edit_builder=lambda s: s.replace('RELATIONS["HR-15"] = [',
                                                 'RELATIONS["HR-15"] = []\n_UNUSED = [', 1))
    run_mutated("a-kind-outside-the-ratified-vocabulary-refuses", "not in the ratified vocabulary",
                edit_builder=lambda s: s.replace('    ("sibling_of", "HR-03",',
                                                 '    ("resembles", "HR-03",', 1))
    run_mutated("a-shipped-bedrock_name-the-map-does-not-recognise-refuses", "UNMAPPED bedrock_name",
                edit_builder=lambda s: s.replace(
                    'HR15_NAME = "HR-15 -- currency of obligation: consent versus constitutive relation"',
                    'HR15_NAME = "HR-15 -- a name the fragment does not ship"', 1))
    run_mutated("a-second-birth-certificate-refuses", "novel=true entries",
                edit_builder=lambda s: s.replace(
                    'BEDROCK_MAP[HR15_NAME] = ("HR-15", "unchosen-relations-bind-without-authorization")',
                    'BEDROCK_MAP[HR15_NAME] = ("HR-15", "unchosen-relations-bind-without-authorization")\n'
                    'BEDROCK_MAP[HR14_NAME] = ("HR-15", "borrowed")', 1))
    # HR-14 rather than an A-E bedrock on purpose: the inherited v0_1 gate skips HR-14 and
    # HR-15 (neither is in v0_1), so drifting HR-14 reaches the v0_3 gate instead of
    # aborting at the earlier one. A control that trips a gate other than the one it names
    # proves the wrong thing -- the K330 shape, and it cost this battery one run.
    run_mutated("a-bedrock-that-drifts-from-v0_3-refuses", "parity with v0_3",
                edit_builder=lambda s: s.replace(
                    'RELATIONS = {k: list(v) for k, v in R.RELATIONS.items()}',
                    'BEDROCKS["HR-14"]["gloss"] = BEDROCKS["HR-14"]["gloss"] + " drift"\n'
                    'RELATIONS = {k: list(v) for k, v in R.RELATIONS.items()}', 1))

    npass = sum(1 for x in results if x["pass"])
    out = {"artifact": "register_control_v0_2.json",
           "generated_by": "adversarial_map_staging/controls_register_v0_4.py",
           "session": "K351", "date_operator_local": "2026-09-18",
           "pins": {"v0_3": md5f(p3), "v0_4": md5f(p4),
                    "assembly_v1_3": md5f(os.path.join(HERE, "adversarial_map_v1_3.json"))},
           "delta": {"bedrocks": [len(b3), len(b4)],
                     "residue_entries": [v3["meta"]["residue_entries"],
                                         v4["meta"]["residue_entries"]],
                     "new": sorted(set(b4) - set(b3)),
                     "relations_added": [(r_["kind"], r_["to"]) for r_ in a6]},
           "results": results,
           "summary": {"controls": len(results), "passed": npass,
                       "all_pass": npass == len(results)}}
    dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "register_control_v0_2.json")
    b = (json.dumps(out, indent=2, ensure_ascii=True) + "\n").encode("utf-8")
    open(dest, "wb").write(b)
    print(json.dumps(out["summary"], indent=1))
    print("wrote %s %s" % (dest, hashlib.md5(b).hexdigest()))
    return 0 if npass == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())

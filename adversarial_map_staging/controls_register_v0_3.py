#!/usr/bin/env python3
"""K349 controls for honest_residuals_register_v0_3.json. Emits register_control_v0_1.json.

Two things must be shown, not asserted: that ratifying a fifth relation kind did not move
any bedrock (Phase G yields no (d), so the register's content is expected to be v0_2's),
and that the two guards which make the declaration mean anything still refuse -- an
undeclared adjacency, and a kind outside the ratified vocabulary.
"""
import json, os, re, shutil, subprocess, sys, tempfile, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
md5f = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()


def main():
    results = []
    def rec(name, ok, detail=""):
        results.append({"name": name, "pass": bool(ok), "detail": detail})
        print("%s . %s %s" % ("PASS" if ok else "FAIL", name, detail))

    v2 = json.load(open(os.path.join(HERE, "honest_residuals_register_v0_2.json"), "rb"))
    v3 = json.load(open(os.path.join(HERE, "honest_residuals_register_v0_3.json"), "rb"))

    def bedrocks(d):
        for k in ("bedrocks", "register", "entries"):
            if isinstance(d.get(k), list):
                return d[k]
        return []
    b2, b3 = bedrocks(v2), bedrocks(v3)
    rec("bedrock-count-unchanged", len(b2) == len(b3) and len(b3) == 14,
        "%d -> %d" % (len(b2), len(b3)))

    # every bedrock identical EXCEPT HR-14, which gains exactly one relation
    def strip(b):
        c = json.loads(json.dumps(b))
        c.pop("relations", None)
        return json.dumps(c, sort_keys=True)
    m2 = {b["bedrock_id"]: b for b in b2}
    m3 = {b["bedrock_id"]: b for b in b3}
    same = [i for i in m3 if i in m2 and strip(m2[i]) == strip(m3[i])]
    rec("every-bedrock-identical-apart-from-relations", len(same) == len(m3),
        "%d of %d" % (len(same), len(m3)))
    r2 = {r["kind"] + ">" + r["to"] for r in m2["HR-14"].get("relations", [])}
    r3 = {r["kind"] + ">" + r["to"] for r in m3["HR-14"].get("relations", [])}
    rec("HR-14-gains-exactly-the-conditions-relation",
        r3 - r2 == {"conditions>HR-11"} and not (r2 - r3), "added %s" % sorted(r3 - r2))
    others = [i for i in m3 if i != "HR-14"
              and json.dumps(m3[i].get("relations"), sort_keys=True)
              != json.dumps(m2.get(i, {}).get("relations"), sort_keys=True)]
    rec("no-other-bedrock-changed-relations", not others, str(others))

    # tributary parity: (d) count and every tributary node
    def tribs(d):
        return sorted((b["bedrock_id"], f.get("name"), str(t.get("node")), str(t.get("phase")))
                      for b in bedrocks(d) for f in b.get("facets", [])
                      for t in f.get("tributaries", []))
    rec("tributaries-identical", tribs(v2) == tribs(v3),
        "%d tributaries" % len(tribs(v3)))

    # ---- the two REFUSAL controls ----------------------------------------------
    tmp = tempfile.mkdtemp(prefix="k349reg_")
    rrepo = os.path.join(tmp, "repo")
    work = os.path.join(rrepo, "adversarial_map_staging")
    os.makedirs(rrepo, exist_ok=True)
    shutil.copytree(HERE, work, ignore=shutil.ignore_patterns("__pycache__"))
    os.symlink(os.path.join(REPO, "efilist_argument_library_v4_0_0.json"),
               os.path.join(rrepo, "efilist_argument_library_v4_0_0.json"))
    builder = os.path.join(work, "build_register_v0_3.py")
    orig = open(builder, "rb").read().decode("utf-8")

    # MAP_DIR is derived from OUT_DIR in this builder, so the throwaway tree is both the
    # source and the destination -- pointing --out elsewhere makes it look for its own
    # inputs there and fail for the harness's reason instead of the guard's.
    def run_with(src, name, needle):
        open(builder, "w", encoding="utf-8", newline="\n").write(src)
        r = subprocess.run([sys.executable, builder, "--out", rrepo],
                           capture_output=True, text=True, cwd=work)
        blob = r.stdout + r.stderr
        hit = [l for l in blob.splitlines() if needle in l]
        rec(name, r.returncode != 0 and bool(hit),
            "rc=%d | %s" % (r.returncode,
                            (hit[-1][:120] if hit else "NO LINE MATCHED %r" % needle)))

    # (a) a kind outside the ratified vocabulary
    bad_kind = orig.replace('("conditions", "HR-11",', '("modulates", "HR-11",', 1)
    assert bad_kind != orig
    run_with(bad_kind, "a-kind-outside-the-ratified-vocabulary-refuses",
             "not in the ratified vocabulary")

    # (b) an undeclared adjacency still refuses -- remove a DECLARED relation that the
    #     mechanical signals also derive, so the audit's undeclared-adjacency guard fires.
    undecl = re.sub(r'RELATIONS\["HR-14"\] = \[',
                    'RELATIONS["HR-14"] = []\n_UNUSED = [', orig, count=1)
    assert undecl != orig
    run_with(undecl, "an-undeclared-adjacency-still-refuses", "UNDECLARED ADJACENCY")

    open(builder, "w", encoding="utf-8", newline="\n").write(orig)

    npass = sum(1 for x in results if x["pass"])
    out = {"artifact": "register_control_v0_1.json",
           "generated_by": "adversarial_map_staging/controls_register_v0_3.py",
           "session": "K349", "date_operator_local": "2026-09-17",
           "pins": {"v0_2": md5f(os.path.join(HERE, "honest_residuals_register_v0_2.json")),
                    "v0_3": md5f(os.path.join(HERE, "honest_residuals_register_v0_3.json"))},
           "results": results,
           "summary": {"controls": len(results), "passed": npass,
                       "all_pass": npass == len(results)}}
    dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "register_control_v0_1.json")
    b = (json.dumps(out, indent=2, ensure_ascii=True) + "\n").encode("utf-8")
    open(dest, "wb").write(b)
    print(json.dumps(out["summary"], indent=1))
    print("wrote %s %s" % (dest, hashlib.md5(b).hexdigest()))
    return 0 if npass == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())

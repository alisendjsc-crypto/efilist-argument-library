#!/usr/bin/env python3
"""project_canon_v38_17.json -- MINOR. L1: the flagship's first two mega-literal sidecars, pinned.

ccclxiv FIRST: v38_16 is round-tripped at the serialization this file emits BEFORE anything is derived.

MINOR by the canon's own ledger convention ("keyset moves BY DESIGN; proof = this ledger +
invariants-md5 guard + subtree-unchanged assertion"), on the v38_1 precedent, which added the
top-level `adversarial_map` block the same way (keyset 40 -> 41). This adds `flagship_sidecars`
(41 -> 42). Asserted, not claimed: `invariants`, `schemas` and `hazard_map` byte-identical, and
every top-level key this build does not name byte-identical too.

Every hash and count it records is COMPUTED here from the files on disk -- the sidecars, the
generator, the gate, the controls, the flagship -- never typed (ccclxii).

Repo-relative.  --out <dir> to emit elsewhere.
"""
import hashlib, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_map_sidecars as B

OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "project_canon_v38_16.json")
OUT = os.path.join(OUT_DIR, "project_canon_v38_17.json")
SRC_MD5 = "d514a6a8e0ebaabe8441fe275b2ab6a2"
DUMP = dict(indent=2, ensure_ascii=False)
SESSION = "L1_map_sidecars"
DATE = "2026-09-25"
TOUCHED = {"canon_version", "canon_version_marker", "last_updated", "last_updated_by_session",
           "next_recommended_session", "keyset_delta_ledger", "session_log_recent", "flagship_sidecars"}


def f(rel):
    b = open(os.path.join(REPO, rel), "rb").read()
    return {"md5": hashlib.md5(b).hexdigest(), "bytes": len(b)}


def literals(s):
    """Every top-level `var|const|let NAME = [..]|{..}` of 5,000 B or more, JS quoting honoured."""
    out = []
    for m in re.finditer(r"(?:^|\n)\s*(?:var|const|let)\s+([A-Za-z_$][\w$]*)\s*=\s*([\[{])", s):
        i = st = m.end() - 1; depth = 0; q = None; esc = False
        while i < len(s):
            ch = s[i]
            if q:
                if esc: esc = False
                elif ch == "\\": esc = True
                elif ch == q: q = None
            elif ch in "\"'`": q = ch
            elif ch in "[{": depth += 1
            elif ch in "]}":
                depth -= 1
                if depth == 0: break
            i += 1
        lit = s[st:i + 1]
        n = len(lit.encode("utf-8"))
        if n >= 5000:
            try: json.loads(lit); kind = "JSON"
            except ValueError: kind = "JavaScript, not JSON"
            out.append((m.group(1), n, kind))
    return sorted(out, key=lambda r: -r[1])


def main():
    raw = open(SRC, "rb").read()
    got = hashlib.md5(raw).hexdigest()
    assert got == SRC_MD5, "BASE GUARD: project_canon_v38_16.json is %s" % got
    d = json.loads(raw.decode("utf-8"))
    assert (json.dumps(d, **DUMP) + "\n").encode("utf-8") == raw, \
        "ccclxiv: v38_16 does not round-trip at this serialization -- do not derive from it"
    before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in d.items()}
    keys_before = list(d)
    assert "flagship_sidecars" not in d

    # ---------------------------------------------------------------- measured, not typed
    s = B.read_flagship(REPO)
    emitted = B.build(s)
    for rel, b in emitted.items():
        assert open(os.path.join(REPO, rel), "rb").read() == b, \
            "%s on disk is not what build_map_sidecars.py emits -- run it first" % rel
    mgd = json.loads(emitted[B.MGD_OUT])
    m1 = json.loads(emitted[B.M1_OUT])
    flag = f(B.FLAGSHIP)
    pin_record = "%s / %d (v4.1.2)" % (flag["md5"], flag["bytes"])
    assert pin_record in d["keyset_delta_ledger"]["v38_16_K354"], \
        "the flagship on disk is not the v4.1.2 pin v38_16 records"
    ctl = json.load(io.open(os.path.join(HERE, "l1_sidecar_control_v0_1.json"), encoding="utf-8"))
    assert ctl["summary"] == "%d of %d as expected" % (len(ctl["controls"]), len(ctl["controls"])), ctl["summary"]
    assert ctl["gate"]["md5"] == f("tools/xsurface_v4_1_0.py")["md5"], "controls ran against another gate"
    corpus = json.load(io.open(os.path.join(REPO, "efilist_argument_library_v4_0_0.json"), encoding="utf-8"))
    rwe_equal = B.canon_md5(B.literal(s, "REAL_WORLD_EXAMPLES")) == B.canon_md5(corpus["realWorldExamples"])
    dep = B.literal(s, "DEP_GRAPH_DATA")
    dep_equal = B.canon_md5(dep) == B.canon_md5(corpus["dependencyGraph"])
    raw_differs = [n["entryId"] for n in mgd["data"]["nodes"] if n["type"] == "objection"
                   and n["mechanism_raw"] != {o["id"]: o["psychMechanism"]
                                              for o in corpus["objections"]}[n["entryId"]]]
    lits = literals(s)
    cov = m1["coverage"]

    # ---------------------------------------------------------------- the new block
    d["flagship_sidecars"] = {
        "block_kind": "flagship_sidecars",
        "registered_by_session": SESSION + " (" + DATE + "), the library seat's first Code session",
        "ruling": ("Standing ruling 1 of 2026-09-18, in the umbrella memory's words: 'No assembler for "
                   "combined.html. Extend the cross-surface gate to every mega-literal without a second "
                   "copy; create sidecar data files as the reference and pin their md5 in canon.'"),
        "requested_by": ("Relay R0057 (argue S38, 2026-09-24): a Map 1 export the card game can vendor, "
                         "with stable ids matching the corpus, a version field and a file md5 to pin."),
        "what_a_sidecar_is": (
            "A pure function of site/combined.html, written by tools/build_map_sidecars.py. `data` is the "
            "literal as the flagship carries it; every other field is derived from the flagship, the Map "
            "1 caveats included. A pin move that leaves the literal and Map 1's methodology panel alone "
            "leaves the sidecar byte-identical; one that touches them turns the gate RED until the "
            "generator is re-run and this pin moves with it."),
        "pins": {
            B.MGD_OUT: dict(f(B.MGD_OUT), literal="MAP_GRAPH_DATA", data_md5=mgd["data_md5"],
                            version=mgd["version"]),
            B.M1_OUT: dict(f(B.M1_OUT), literal="MAP1_TRANSITIONS", data_md5=m1["data_md5"],
                           version=m1["version"]),
        },
        "extracted_from": dict(file=B.FLAGSHIP, pin="v4.1.2", **flag),
        "generator": dict(path="tools/build_map_sidecars.py", **f("tools/build_map_sidecars.py")),
        "gate": dict(path="tools/xsurface_v4_1_0.py", **f("tools/xsurface_v4_1_0.py"),
                     checks=("Per sidecar: data equals the flagship's literal under the gate's own "
                             "canonical md5; data_md5 describes its own data; the file is byte for byte "
                             "what the generator emits from the flagship under test; the file matches "
                             "this pin. Extended in place: its first three checks and their output are "
                             "unchanged.")),
        "controls": dict(path="tools/l1_sidecar_controls.py", artifact="tools/l1_sidecar_control_v0_1.json",
                         **f("tools/l1_sidecar_control_v0_1.json"), summary=ctl["summary"]),
        "primary_mechanism": (
            "UNRULED. No link in MAP_GRAPH_DATA is marked primary and %d of the %d objections link to more "
            "than one mechanism, so the sidecar emits the links as they stand and no primary. A rule for "
            "choosing one is Josiah's, asked at L1." % (mgd["summary"]["objections_with_several_mechanisms"],
                                                        mgd["summary"]["objections"])),
        "map1_coverage": (
            "%d of %d objections are Map 1 sources. Absent: %s. Never a target: %s. Reported, not authored."
            % (cov["sources"], cov["objections"], ", ".join(cov["absent_as_source"]),
               ", ".join(cov["never_a_target"]))),
        "findings_logged_not_repaired": {
            "mechanism_raw_diverges": (
                "The Mechanism Web's objection nodes carry a `mechanism_raw` text that differs from the "
                "corpus's psychMechanism on %d of %d nodes: %s. %d of them are among Map 1's %d absent "
                "sources, which bears on K345a's shared-generation-boundary hypothesis. Repairing served "
                "text is a pin move." % (len(raw_differs), mgd["summary"]["objections"], ", ".join(raw_differs),
                                         len(set(raw_differs) & set(cov["absent_as_source"])),
                                         len(cov["absent_as_source"]))),
            "overrides_15_and_10": (
                "Map 1's START HERE caveat speaks of '15 canonical sophisticate overrides'; the data marks "
                "%d sophisticate edges canonical_override true. The panel's own KNOWN LIMITATIONS, item 2, "
                "reconciles the two, and the sidecar carries both texts. A reader of the first alone is "
                "misled; rewording it is a pin move."
                % sum(1 for v in m1["data"].values() for e in v["sophisticate"]
                      if e.get("canonical_override") is True)),
        },
        "ruling_1_scope_remaining": {
            "method": "Every top-level literal of 5,000 B or more in the flagship, measured by this builder.",
            "covered": ("OBJECTIONS by the corpus JSON and the JSX (the gate's first three checks); "
                        "MAP_GRAPH_DATA and MAP1_TRANSITIONS by these sidecars."),
            "not_yet": {name: "%d B, %s" % (n, kind) for name, n, kind in lits
                        if name not in ("OBJECTIONS", "MAP_GRAPH_DATA", "MAP1_TRANSITIONS")},
            "second_copies_already_present": (
                "REAL_WORLD_EXAMPLES %s the corpus's realWorldExamples under the canonical md5, so it "
                "needs a gate check rather than a sidecar. DEP_GRAPH_DATA %s the corpus's "
                "dependencyGraph (same %d nodes and %d links, but the corpus's nodes carry more fields), "
                "so it needs a declared projection or a sidecar."
                % ("EQUALS" if rwe_equal else "does NOT equal",
                   "EQUALS" if dep_equal else "does NOT equal",
                   len(dep["nodes"]), len(dep["links"]))),
        },
    }

    d["canon_version"] = "38.17"
    d["canon_version_marker"] = "v38.17"
    d["last_updated"] = DATE
    d["last_updated_by_session"] = SESSION

    d["next_recommended_session"]["precondition_L1"] = (
        "Before any R1 work: Josiah's answer on the Adversarial Map's audience status, asked at L1. His "
        "words, as the umbrella memory records them: the Map 'was meant as a transparent stance to the "
        "actual legitimacy of the philosophy of antinatalism itself ... a mirror library to object to "
        "even my OWN beliefs'. /adversarial/ is live, and R1 decides what it shows, so what he meant "
        "comes first.")

    d["keyset_delta_ledger"]["v38_17_L1"] = (
        "MINOR. One top-level addition, flagship_sidecars (keyset 41 -> 42, on the v38_1 precedent and the "
        "ledger's own convention: keyset moves by design, proved by this note, the invariants guard and "
        "a subtree-unchanged assertion over every other top-level key). Canon-meta version fields; one "
        "addition inside next_recommended_session (precondition_L1); this note; one session_log_recent "
        "append. NO PIN: combined.html " + pin_record + " HELD, corpus and jsx HELD, xsurface's objection "
        "canon unchanged. invariants, schemas and hazard_map asserted byte-identical. CORRECTED FORWARD: "
        "v38_16 left canon_version at 38.15 and canon_version_marker at v38.15 -- K354's builder dropped "
        "the lines K351-K353 carried -- and both read 38.17 here. v38_16's own bytes are not edited.")

    d["session_log_recent"].append(
        "L1_map_sidecars (" + DATE + ", the library seat's first Code session; answers relay R0057 from "
        "argue S38 under standing ruling 1; NO PIN): THE FIRST TWO MEGA-LITERAL SIDECARS. "
        "tools/build_map_sidecars.py writes sidecars/map_graph_data.json (" + mgd["data_md5"] + " data; "
        "%d objections, %d mechanisms, %d links) and sidecars/map1_transitions.json (" % (
            mgd["summary"]["objections"], mgd["summary"]["mechanisms"], mgd["summary"]["links"])
        + m1["data_md5"] + " data; %d sources, %d edges over %s) from the flagship's own literals, never "
        "retyped, with Map 1's caveats lifted from its methodology panel. No primary mechanism is "
        "emitted: none is marked, and %d objections carry several. tools/xsurface_v4_1_0.py extended in "
        "place to gate both, and tools/l1_sidecar_controls.py proves it: %s, the unmutated control first. "
        "Both file md5s pinned in the new flagship_sidecars block. Also landed by bytes: "
        "icons/gen_icons.py, which all seven served favicons name and no repo had tracked; it regenerates "
        "all seven byte for byte." % (cov["sources"], m1["edge_counts"]["total"], ", ".join(m1["modes"]),
                                      mgd["summary"]["objections_with_several_mechanisms"], ctl["summary"]))

    out = (json.dumps(d, **DUMP) + "\n").encode("utf-8")

    assert list(d)[:len(keys_before)] == keys_before and list(d)[len(keys_before):] == ["flagship_sidecars"], \
        "top-level keyset moved other than by the one declared addition"
    assert len(d) == 42, "keyset is %d, expected 42" % len(d)
    for k in keys_before:
        if k not in TOUCHED:
            assert json.dumps(d[k], sort_keys=True, ensure_ascii=False) == before[k], "%s moved" % k
    nrs = json.loads(before["next_recommended_session"])
    assert {k: v for k, v in d["next_recommended_session"].items() if k != "precondition_L1"} == nrs, \
        "next_recommended_session changed beyond its one addition"
    assert json.loads(out.decode("utf-8")) == d, "emitted bytes do not round-trip"

    open(OUT, "wb").write(out)
    print("project_canon_v38_17.json  %s / %d" % (hashlib.md5(out).hexdigest(), len(out)))
    print("  keyset 41 -> 42 (flagship_sidecars); every other untouched key byte-identical")
    for rel, p in d["flagship_sidecars"]["pins"].items():
        print("  pin %-34s %s / %d" % (rel, p["md5"], p["bytes"]))


if __name__ == "__main__":
    main()

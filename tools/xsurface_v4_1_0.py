#!/usr/bin/env python3
"""xsurface_v4_1_0.py -- THE CORPUS-VS-FLAGSHIP GATE. Built at K344 because the v4.1.0
execution order is right that no gate anywhere cross-checks corpus text against the
flagship, and a missed surface ships a corpus and a served page that disagree with
nothing to say so.

There is NO BUILD STEP. combined.html is a hand-assembled superset carrying
REBUTTAL_STRENGTH, which the JSX does not, and nothing regenerates any surface from any
other. The three shipped copies of the 82 objections are kept in step by hand, which is
exactly why this needs to be mechanical.

Method: bracket-balance extraction of the `const OBJECTIONS = [...]` literal from
combined.html and from the JSX (string-aware, so a bracket inside a string cannot close
the literal), json.loads each, and compare all three against the corpus file's
`objections` by a canonical serialization md5. One hash, three surfaces. This is the K330
data-literal extraction method generalised from "did the literal move" to "do the surfaces
agree".

  python3 tools/xsurface_v4_1_0.py                # gate the tracked surfaces
  python3 tools/xsurface_v4_1_0.py --dir k344_drop  # gate a candidate set
  python3 tools/xsurface_v4_1_0.py --dir k344_drop --against .   # and diff the two

EXTENDED AT L1 (2026-09-25) under standing ruling 1 (2026-09-18): the mega-literals with no second
copy get sidecar data files as the reference, md5-pinned in canon, and this gate checks them too.
Two so far, MAP_GRAPH_DATA and MAP1_TRANSITIONS, in sidecars/. Each must (1) carry `data` equal to
the flagship's literal under the same canonical md5, (2) describe its own data truly, (3) be byte
for byte what tools/build_map_sidecars.py emits from the flagship under test, and (4) match the pin
in the one project_canon_v*.json. A sidecar or canon absent from --dir resolves to the repo's own
copy, so a candidate flagship dropped alone is still gated against the committed sidecars; the
resolved path is printed either way. --against compares OBJECTIONS only, as before.
"""
import argparse, glob, hashlib, io, json, os, re, sys

JSONF = "efilist_argument_library_v4_0_0.json"
JSXF  = "efilist_argument_library_v4_0_0.jsx"
HTMLF = "combined.html"


def balance(s, start):
    """Return the balanced [..] / {..} beginning at `start`, ignoring brackets in strings."""
    depth = 0; i = start; instr = False; esc = False
    while i < len(s):
        ch = s[i]
        if instr:
            if esc:            esc = False
            elif ch == "\\":   esc = True
            elif ch == '"':    instr = False
        else:
            if ch == '"':      instr = True
            elif ch in "[{":   depth += 1
            elif ch in "]}":
                depth -= 1
                if depth == 0:
                    return s[start:i + 1]
        i += 1
    return None


def extract(path, name="OBJECTIONS"):
    s = io.open(path, encoding="utf-8", newline="").read()
    m = re.search(r"const\s+%s\s*=\s*" % name, s)
    if not m:
        raise SystemExit("ABORT: no `const %s =` in %s" % (name, path))
    if s.count("const %s =" % name) != 1:
        raise SystemExit("ABORT: `const %s =` occurs %d times in %s, expected 1"
                         % (name, s.count("const %s =" % name), path))
    start = s.index("[", m.end())
    lit = balance(s, start)
    if lit is None:
        raise SystemExit("ABORT: %s literal in %s never closes" % (name, path))
    return json.loads(lit)


def canon(objs):
    return hashlib.md5(json.dumps(objs, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def html_path(d):
    """combined.html is served from site/ since WI-K360 (2026-09-20); an older baseline (--against) has it at the root."""
    p = os.path.join(d, "site", HTMLF)
    return p if os.path.isfile(p) else os.path.join(d, HTMLF)


def surfaces(d):
    return {
        JSONF: json.load(io.open(os.path.join(d, JSONF), encoding="utf-8"))["objections"],
        JSXF:  extract(os.path.join(d, JSXF)),
        HTMLF: extract(html_path(d)),
    }


def leaves(x, path=()):
    if isinstance(x, dict):
        for k, v in x.items(): yield from leaves(v, path + (k,))
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from leaves(v, path + (i,))
    else:
        yield path, x


ap = argparse.ArgumentParser()
ap.add_argument("--dir", default=".")
ap.add_argument("--against", default=None)
a = ap.parse_args()

fail = 0
def chk(name, cond, got=""):
    global fail
    print(("  ok   " if cond else "  FAIL ") + name + (("  " + got) if got and not cond else ""))
    if not cond: fail += 1

print("CROSS-SURFACE GATE -- %s" % os.path.abspath(a.dir))
S = surfaces(a.dir)
H = {p: canon(v) for p, v in S.items()}
for p, h in H.items():
    print("  %-38s %3d objections  canon %s" % (p, len(S[p]), h))
chk("all three surfaces carry 82 objections", all(len(v) == 82 for v in S.values()),
    repr({p: len(v) for p, v in S.items()}))
chk("all three surfaces AGREE, byte-for-byte after canonicalization", len(set(H.values())) == 1,
    repr(H))
ids = [tuple(o["id"] for o in v) for v in S.values()]
chk("id order identical across surfaces", len(set(ids)) == 1)

# ---------------------------------------------------------------- the mega-literal sidecars (L1)
SIDECARS = (("MAP_GRAPH_DATA", "sidecars/map_graph_data.json"),
            ("MAP1_TRANSITIONS", "sidecars/map1_transitions.json"))
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def extract_var(path, name):
    """The one `var NAME = {..}` literal, bracket-balanced as above."""
    s = io.open(path, encoding="utf-8", newline="").read()
    if s.count("var %s =" % name) != 1:
        raise SystemExit("ABORT: `var %s =` occurs %d times in %s, expected 1"
                         % (name, s.count("var %s =" % name), path))
    m = re.search(r"var\s+%s\s*=\s*" % name, s)
    lit = balance(s, m.end()) if s[m.end()] in "[{" else None
    if lit is None:
        raise SystemExit("ABORT: %s literal in %s is not a closed [..] or {..}" % (name, path))
    return json.loads(lit)


def resolve(d, rel):
    p = os.path.join(d, rel)
    return p if os.path.exists(p) else os.path.join(REPO, rel)


def canon_file(d):
    for root in (d, REPO):
        found = glob.glob(os.path.join(root, "project_canon_v*.json"))
        if found:
            return found
    return []


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_map_sidecars

print("\n  --- sidecars (standing ruling 1) ---")
HP = html_path(a.dir)
emitted = build_map_sidecars.build(io.open(HP, encoding="utf-8", newline="").read())
cf = canon_file(a.dir)
chk("exactly one project_canon_v*.json", len(cf) == 1, repr(cf))
pins = json.load(io.open(cf[0], encoding="utf-8")).get("flagship_sidecars", {}).get("pins", {}) if len(cf) == 1 else {}
print("  canon    %s" % (cf[0] if len(cf) == 1 else "?"))
for name, rel in SIDECARS:
    p = resolve(a.dir, rel)
    print("  sidecar  %s" % p)
    if not os.path.isfile(p):
        chk("%s exists" % rel, False, p)
        continue
    raw = open(p, "rb").read()
    sc = json.loads(raw.decode("utf-8"))
    hl, hs = canon(extract_var(HP, name)), canon(sc.get("data"))
    print("  %-38s %-17s canon %s" % (rel, name, hs))
    chk("%s data == the flagship's %s" % (rel, name), hs == hl, "flagship %s" % hl)
    chk("%s data_md5 describes its own data" % rel, sc.get("data_md5") == hs, repr(sc.get("data_md5")))
    chk("%s is byte for byte what build_map_sidecars.py emits from this flagship" % rel,
        raw == emitted[rel], "file %d B, emitted %d B" % (len(raw), len(emitted[rel])))
    pin, md5 = pins.get(rel, {}), hashlib.md5(raw).hexdigest()
    chk("%s == its canon pin" % rel, (md5, len(raw)) == (pin.get("md5"), pin.get("bytes")),
        "file %s / %d, pin %s / %s" % (md5, len(raw), pin.get("md5"), pin.get("bytes")))

if a.against:
    print("\n  --- against %s ---" % os.path.abspath(a.against))
    B = surfaces(a.against)
    HB = {p: canon(v) for p, v in B.items()}
    chk("baseline's three surfaces also agree", len(set(HB.values())) == 1, repr(HB))
    bl, nl = dict(leaves(B[JSONF])), dict(leaves(S[JSONF]))
    chk("no leaf added or removed", set(bl) == set(nl))
    moved = sorted(k for k in bl if bl[k] != nl.get(k))
    print("  moved leaves (%d):" % len(moved))
    byid = {o["id"]: i for i, o in enumerate(B[JSONF])}
    rev = {i: n for n, i in byid.items()}
    for k in moved:
        print("      %s#%s" % (rev.get(k[0], k[0]), "/".join(str(x) for x in k[1:])))
    # and the SAME leaves moved on every surface, which is the real cross-surface claim
    for p in (JSXF, HTMLF):
        mp = sorted(k for k, v in leaves(B[p]) if dict(leaves(S[p])).get(k) != v)
        chk("%s moved exactly the same leaves as the corpus" % p, mp == moved, repr(mp[:6]))

print("\nX-SURFACE GATE: " + ("RED -- %d failure(s)" % fail if fail else "GREEN"))
sys.exit(1 if fail else 0)

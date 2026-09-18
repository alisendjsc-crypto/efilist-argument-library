#!/usr/bin/env python3
"""K351: derive build_register_v0_4.py from build_register_v0_3.py by ANCHORED patches.

build_register_v0_3.py stays byte-identical on disk so honest_residuals_register_v0_3.json
remains reproducible from its own builder. Every anchor is asserted to occur EXACTLY once.
Binary read, explicit UTF-8 (ccclx).
"""
import os, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K348_REPO") or os.path.dirname(HERE)
SRC = os.path.join(REPO, "adversarial_map_staging", "build_register_v0_3.py")
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "build_register_v0_4.py")
BASE_MD5 = "98a63164315a33f63a59894e550182db"

PATCHES = []
def P(tag, old, new):
    PATCHES.append((tag, old, new))

P("header",
'''"""honest_residuals_register_v0_3.json -- the FIFTH RELATION KIND (K349).''',
'''"""honest_residuals_register_v0_4.json -- HR-15, the fifteenth bedrock (K351).

WHAT CHANGES FROM v0_3, which stays byte-identical on disk:
  i.   THE SOURCE is adversarial_map_v1_3.json, which carries the HR-15 fold.
  ii.  HR-15 -- currency of obligation: consent versus constitutive relation. Ratified by
       Josiah at K350 on the STRUCTURAL ground, not the scatter one: routing it into HR-06
       would give HR-06 a tributary that dissolves HR-06's own question, which is a
       reductio rather than a preference. Name, gloss, alias and facet are taken from
       canon's HR_15_ratification_K350 rather than rewritten.
  iii. TWO RELATIONS, both already written in canon and both inside the ratified
       vocabulary, so the v0_3 allowlist passes without extension: HR-06 depends_on HR-15,
       and HR-15 sibling_of HR-03.
  iv.  A SECOND PARITY GATE, against the IMMEDIATE predecessor. v0_3 checks parity against
       v0_1 restricted to the phases v0_1 read, which cannot see a change confined to the
       later phases. v0_4 adds a field-for-field check against v0_3 with exactly two
       declared exceptions -- HR-15 is new, and HR-06 gains one relation -- so every other
       bedrock's tributary count and every other field are asserted UNCHANGED rather than
       claimed to be.

--- the v0_3 header follows, unchanged ---------------------------------------------
honest_residuals_register_v0_3.json -- the FIFTH RELATION KIND (K349).''')

P("assembly-src",
'''ASSEMBLY = os.path.join(MAP_DIR, "adversarial_map_v1_2.json")
V0_2_REGISTER = os.path.join(MAP_DIR, "honest_residuals_register_v0_2.json")
V0_1 = os.path.join(STAGE, "honest_residuals_register_v0_1.json")''',
'''ASSEMBLY = os.path.join(MAP_DIR, "adversarial_map_v1_3.json")
V0_2_REGISTER = os.path.join(MAP_DIR, "honest_residuals_register_v0_2.json")
V0_1 = os.path.join(STAGE, "honest_residuals_register_v0_1.json")
V0_3 = os.path.join(STAGE, "honest_residuals_register_v0_3.json")
V0_3_MD5 = "56a86d36e0354f00051a84ca02993fab"
# The two places v0_4 is ALLOWED to differ from v0_3. Anything else refuses the write.
V0_3_EXCEPTIONS = {"HR-15": "new bedrock, ratified K350",
                   "HR-06": "gains depends_on HR-15"}''')

P("out-path",
'''OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "honest_residuals_register_v0_3.json")''',
'''OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "honest_residuals_register_v0_4.json")''')

P("bedrock-map",
'''BEDROCK_MAP = dict(R.BEDROCK_MAP)
BEDROCK_MAP[HR14_NAME] = ("HR-14", "terminus-held-open")''',
'''# The shipped bedrock_name, EXACTLY as adv_map_phaseG_v0_1.json ships it. Keyed on the
# string so a fragment edit breaks this build loudly rather than silently remapping. It
# carries the id, which the pre-map names do not: those were written by fragment authors
# who did not know the id, and this one by the ruling that assigned it.
HR15_NAME = "HR-15 -- currency of obligation: consent versus constitutive relation"

BEDROCK_MAP = dict(R.BEDROCK_MAP)
BEDROCK_MAP[HR14_NAME] = ("HR-14", "terminus-held-open")
BEDROCK_MAP[HR15_NAME] = ("HR-15", "unchosen-relations-bind-without-authorization")''')

P("bedrocks",
'''BEDROCKS["HR-05"]["registered_in"] = (
    "canon:terminal_stability_marker.honest_residuals.comparative_vs_non_comparative_harm")''',
'''BEDROCKS["HR-05"]["registered_in"] = (
    "canon:terminal_stability_marker.honest_residuals.comparative_vs_non_comparative_harm")
# K351. Gloss VERBATIM from canon:adversarial_map.HR_15_ratification_K350.gloss -- it is
# ratified text and is quoted, not rewritten. Alias and facet likewise.
BEDROCKS["HR-15"] = dict(
    name="Currency of obligation: consent versus constitutive relation",
    gloss=("Whether obligation is denominated in authorization by the obligated party, or "
           "constituted by the relation the parties stand in. The corpus's consent architecture "
           "presupposes the first; a developed relational ethics denies it, and nothing in-corpus "
           "derives either."),
    registered_in="this-program", alias="rival-occupant")''')

P("relations",
'''RELATIONS = {k: list(v) for k, v in R.RELATIONS.items()}''',
'''RELATIONS = {k: list(v) for k, v in R.RELATIONS.items()}
# K351, Josiah at K350. Both notes are canon's, quoted rather than paraphrased, and both
# kinds are already in the ratified vocabulary, so the allowlist passes without extension.
RELATIONS["HR-06"] = RELATIONS["HR-06"] + [
    ("depends_on", "HR-15",
     "HR-15: HR-06 asks whether unauthorized imposition wrongs absent harm, which presupposes "
     "that authorization is the currency. Resolve HR-15 in care ethics' favour and HR-06's "
     "question does not arise; resolve it against and HR-06 is untouched. Same declared shape as "
     "HR-05 depends_on HR-03.")]
RELATIONS["HR-15"] = [
    ("sibling_of", "HR-03",
     "HR-03: both concern where the moral primitive is seated, neither derives the other. HR-03 "
     "is the seat of STANDING (what bears value); HR-15 is the currency of OBLIGATION (what makes "
     "a demand binding). They come apart both ways -- a relational holist can hold consent is the "
     "currency for impositions on individuals, and a natural-duties theorist denies "
     "consent-as-currency with no relational axiology at all.")]''')

P("parity-v0_1-exemptions",
'''    prev = json.loads(open(V0_1, "rb").read().decode("utf-8"))
    prev_b = {b["bedrock_id"]: b for b in prev["bedrocks"]}
    MOVED = {("HR-05", "registered_in")}''',
'''    prev = json.loads(open(V0_1, "rb").read().decode("utf-8"))
    prev_b = {b["bedrock_id"]: b for b in prev["bedrocks"]}
    # K351: HR-06 gains depends_on HR-15, so its relations list legitimately differs from
    # v0_1's. Declared here as a MOVE rather than silently exempted, exactly as
    # HR-05.registered_in was at K349; the v0_3 gate added below checks the delta is
    # precisely the one relation.
    MOVED = {("HR-05", "registered_in"), ("HR-06", "relations")}''')

P("parity-v0_1-skip-new",
'''        if bid == "HR-14":
            continue''',
'''        if bid in ("HR-14", "HR-15"):
            continue''')

P("parity-v0_3-gate",
'''    if parity_diffs:
        print("REFUSING TO WRITE -- parity with v0_1 broke in %d place(s):" % len(parity_diffs))
        for d in parity_diffs:
            print("  " + d)
        return 1''',
'''    if parity_diffs:
        print("REFUSING TO WRITE -- parity with v0_1 broke in %d place(s):" % len(parity_diffs))
        for d in parity_diffs:
            print("  " + d)
        return 1

    # ---- 5b (K351): PARITY AGAINST THE IMMEDIATE PREDECESSOR --------------------
    # The v0_1 gate above is restricted to the phases v0_1 read, so it is structurally
    # blind to anything confined to R/F/G. This one compares v0_4 to v0_3 field for
    # field and admits exactly the two declared exceptions.
    v3raw = open(V0_3, "rb").read()
    assert V.md5_bytes(v3raw) == V0_3_MD5, "BASE GUARD: v0_3 is %s" % V.md5_bytes(v3raw)
    v3 = json.loads(v3raw.decode("utf-8"))
    v3b = {b["bedrock_id"]: b for b in v3["bedrocks"]}
    pred_diffs, pred_ok = [], []
    for b in bedrocks:
        bid = b["bedrock_id"]
        if bid in V0_3_EXCEPTIONS:
            continue
        p = v3b.get(bid)
        if p is None:
            pred_diffs.append("%s is new but is not a declared exception" % bid)
            continue
        if json.dumps(b, sort_keys=True) != json.dumps(p, sort_keys=True):
            pred_diffs.append("%s differs from v0_3 and is not a declared exception" % bid)
        else:
            pred_ok.append(bid)
    for bid in v3b:
        if bid not in {x["bedrock_id"] for x in bedrocks}:
            pred_diffs.append("%s is in v0_3 and absent here" % bid)
    # HR-06 must gain EXACTLY the one relation and change in no other way.
    h6 = next(b for b in bedrocks if b["bedrock_id"] == "HR-06")
    p6 = v3b["HR-06"]
    if json.dumps(dict(h6, relations=None), sort_keys=True) \\
            != json.dumps(dict(p6, relations=None), sort_keys=True):
        pred_diffs.append("HR-06 changed outside its relations list")
    added6 = [r for r in h6["relations"] if r not in p6["relations"]]
    lost6 = [r for r in p6["relations"] if r not in h6["relations"]]
    if len(added6) != 1 or added6[0]["kind"] != "depends_on" or added6[0]["to"] != "HR-15" or lost6:
        pred_diffs.append("HR-06 relations delta is %d added / %d lost, expected exactly "
                          "depends_on HR-15" % (len(added6), len(lost6)))
    if pred_diffs:
        print("REFUSING TO WRITE -- parity with v0_3 broke in %d place(s):" % len(pred_diffs))
        for d in pred_diffs:
            print("  " + d)
        return 1''')

P("artifact-name",
'''        artifact="honest_residuals_register_v0_3.json",''',
'''        artifact="honest_residuals_register_v0_4.json",''')

P("changes-list",
'''            "an adjacency the ratified four-kind vocabulary cannot express is recorded in the audit "
            "rather than declared as a relation that would misdescribe it",
        ],''',
'''            "an adjacency the ratified four-kind vocabulary cannot express is recorded in the audit "
            "rather than declared as a relation that would misdescribe it",
            "K351: HR-15 added -- currency of obligation, consent versus constitutive relation. "
            "Ratified by Josiah at K350 on the structural ground: routing it into HR-06 would give "
            "HR-06 a tributary that dissolves HR-06's own question. Birth certificate "
            "care-ethics#note, which the same ratification reclassified (b) -> (d)",
            "K351: HR-06 gains depends_on HR-15, and HR-15 declares sibling_of HR-03. Both kinds "
            "were already in the ratified vocabulary, so no extension was needed",
        ],
        parity_with_v0_3=("Every bedrock except HR-15 and HR-06 is byte-identical to v0_3 field "
                          "for field, asserted before the write rather than claimed after it: %d "
                          "of %d checked and unchanged. HR-15 is new; HR-06 gains exactly one "
                          "relation and changes in no other way. The v0_1 gate above is restricted "
                          "to the phases v0_1 read and is structurally blind to a change confined "
                          "to R/F/G, which is why this second gate exists."
                          % (len(pred_ok), len(BEDROCKS))),
        predecessor=dict(artifact="honest_residuals_register_v0_3.json", md5=V0_3_MD5,
                         note="stays byte-identical on disk; v0_4 supersedes it, it is not edited"),''')


def main():
    raw = open(SRC, "rb").read()
    got = hashlib.md5(raw).hexdigest()
    assert got == BASE_MD5, "BASE GUARD: build_register_v0_3.py is %s" % got
    src = raw.decode("utf-8")
    for tag, old, new in PATCHES:
        n = src.count(old)
        assert n == 1, "anchor %r occurs %d times, expected exactly 1" % (tag, n)
        src = src.replace(old, new, 1)
    for tag, old, new in PATCHES:
        assert src.count(new) == 1, "patched text %r is not unique in the result" % tag
    out = src.encode("utf-8")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "wb").write(out)
    compile(src, OUT, "exec")
    print("WROTE %s  %d B  md5 %s" % (OUT, len(out), hashlib.md5(out).hexdigest()))
    print("  %d anchored patches, each unique before and after; compiles clean" % len(PATCHES))
    return 0


if __name__ == "__main__":
    sys.exit(main())

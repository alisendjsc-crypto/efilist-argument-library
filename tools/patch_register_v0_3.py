#!/usr/bin/env python3
"""K349: derive build_register_v0_3.py and render_register_v0_3.py by ANCHORED patches.

v0_2's builder and renderer stay byte-identical: canon pins the v0_2 artifact and its
receipt names them. The only substantive change is Josiah's K349 ratification of a FIFTH
relation kind, `conditions`, with HR-14+HR-11 as its first instance -- plus the vocabulary
becoming an ENFORCED allowlist rather than a comment, which is the cccli discipline applied
to the one rule in this file that had only ever asked for compliance at write time.
"""
import os, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
STG = os.path.join(REPO, "adversarial_map_staging")

B_SRC = os.path.join(STG, "build_register_v0_2.py")
R_SRC = os.path.join(STG, "render_register_v0_2.py")

BP, RP = [], []
def P(lst, tag, old, new):
    lst.append((tag, old, new))

# ---------------- builder ----------------------------------------------------------
P(BP, "header",
'''"""honest_residuals_register_v0_2.json -- derived FROM THE ASSEMBLY (K348).''',
'''"""honest_residuals_register_v0_3.json -- the FIFTH RELATION KIND (K349).

WHAT CHANGES FROM v0_2, which stays byte-identical on disk:
  i.   THE SOURCE is adversarial_map_v1_2.json. Phase G yields NO (d), so the bedrock set
       and every tributary are expected to come back unchanged -- and the parity gate
       asserts that rather than the receipt claiming it.
  ii.  `conditions` JOINS THE RELATION VOCABULARY (Josiah, K349). v0_2 recorded
       HR-14+HR-11 in the AUDIT because the ratified four kinds could not state it:
       HR-11's resolution neither creates nor dissolves HR-14's question, it changes its
       FORCE. The gap is now closed by ratification and declared as a relation.
  iii. THE VOCABULARY IS ENFORCED. In v0_2 the five-line comment above RELATIONS was the
       only thing keeping a kind inside the vocabulary; nothing checked. It is an
       allowlist now, so a mistyped or invented kind refuses the write (cccli: a rule that
       asks a writer to comply at write time is violated the first time someone does not).

--- the v0_2 header follows, unchanged ---------------------------------------------
honest_residuals_register_v0_2.json -- derived FROM THE ASSEMBLY (K348).''')

P(BP, "out",
'''OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "honest_residuals_register_v0_2.json")''',
'''OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "honest_residuals_register_v0_3.json")''')

P(BP, "assembly",
'''ASSEMBLY = os.path.join(MAP_DIR, "adversarial_map_v1_1.json")''',
'''ASSEMBLY = os.path.join(MAP_DIR, "adversarial_map_v1_2.json")
V0_2_REGISTER = os.path.join(MAP_DIR, "honest_residuals_register_v0_2.json")''')

P(BP, "phase-order",
'''PHASE_ORDER = ["A", "B1", "B2", "C", "D", "E", "R", "F"]''',
'''PHASE_ORDER = ["A", "B1", "B2", "C", "D", "E", "R", "F", "G"]''')

P(BP, "relations-hr14",
'''RELATIONS = {k: list(v) for k, v in R.RELATIONS.items()}
RELATIONS["HR-14"] = [''',
'''# K349 RATIFICATION (Josiah). The fifth kind, and the definition it was ratified under:
#   conditions : A's resolution changes the FORCE of B's open question without creating
#                or dissolving it. B stays askable either way; what moves is how much
#                turns on the answer.
# ENFORCED from here, not merely documented -- see the allowlist check in main().
RELATION_KINDS = ("depends_on", "stronger_than", "sibling_of", "independent_of", "conditions")

RELATIONS = {k: list(v) for k, v in R.RELATIONS.items()}
RELATIONS["HR-14"] = [
    ("conditions", "HR-11",
     "K349, Josiah: the first instance of the fifth kind. HR-11 is the epistemic authority of "
     "the anti-extinction intuition against its evolutionary debunking. If the debunking "
     "succeeds, HR-14's question -- whether the positive-eliminationist charge is answered "
     "anywhere in the corpus -- stays exactly as open, but far less turns on it, because the "
     "intuition generating the charge's rhetorical force loses its standing. If the debunking "
     "fails, HR-14's openness is a live scandal rather than a curiosity. Neither bedrock "
     "entails the other and both arise independently, so none of the four ratified kinds "
     "states it; what moves is FORCE, not existence."),''')

P(BP, "vocab-gap",
'''VOCABULARY_GAP = dict(
    pair="HR-14+HR-11",
    detected_by="neither signal -- found by hand, as HR-04+HR-07 was",''',
'''VOCABULARY_GAP = dict(
    pair="HR-14+HR-11",
    status="CLOSED at K349 by ratification; declared as a `conditions` relation on HR-14",
    detected_by="neither signal -- found by hand, as HR-04+HR-07 was",''')

P(BP, "audit-severity",
'''    audit.append(dict(severity="adjacency-vocabulary-gap", bedrock_id=VOCABULARY_GAP["pair"],
                      detail=VOCABULARY_GAP["detail"]))''',
'''    # The gap is closed, so the audit records the RESOLUTION rather than the gap. Kept as an
    # audit line rather than deleted: what the register used to be unable to say is a record.
    audit.append(dict(severity="adjacency-vocabulary-gap-CLOSED",
                      bedrock_id=VOCABULARY_GAP["pair"],
                      detail=("RESOLVED at K349: Josiah ratified a fifth relation kind, "
                              "`conditions`, and HR-14+HR-11 is declared under it. The v0_2 "
                              "statement of the gap is preserved verbatim below. "
                              + VOCABULARY_GAP["detail"])))
    # THE VOCABULARY IS A GATE NOW, NOT A COMMENT.
    for _bid, _rels in sorted(RELATIONS.items()):
        for _k, _o, _n in _rels:
            if _k not in RELATION_KINDS:
                fail.append("%s declares relation kind %r, which is not in the ratified "
                            "vocabulary %s" % (_bid, _k, list(RELATION_KINDS)))''')

P(BP, "artifact-name",
'''        artifact="honest_residuals_register_v0_2.json",''',
'''        artifact="honest_residuals_register_v0_3.json",''')

P(BP, "source-line",
'''            "SOURCE: this file derives from adversarial_map_v1_1.json, which asserts every one of ''',
'''            "SOURCE: this file derives from adversarial_map_v1_2.json, which asserts every one of ''')

P(BP, "provenance-line",
'''            "source is adversarial_map_v1_1.json rather than six fragment files",''',
'''            "source is adversarial_map_v1_2.json rather than six fragment files",''')

P(BP, "adjacency-note",
'''            vocabulary_gap=VOCABULARY_GAP,''',
'''            vocabulary_gap=VOCABULARY_GAP,
            ratified_kinds=list(RELATION_KINDS),
            fifth_kind=dict(
                kind="conditions", ratified="Josiah, K349",
                definition=("A conditions B: A's resolution changes the FORCE of B's open "
                            "question without creating or dissolving it. B stays askable "
                            "either way; what moves is how much turns on the answer."),
                first_instance="HR-14 conditions HR-11",
                enforced=("The vocabulary is an allowlist checked before the write, not the "
                          "comment it was in v0_2. A kind outside it refuses the build.")),''')

# ---------------- renderer ---------------------------------------------------------
P(RP, "r-src",
'''honest_residuals_register_v0_2.json''',
'''honest_residuals_register_v0_3.json''')


P(BP, "undeclared-adjacency-refuses",
'''    undeclared = sorted(set(cands) - declared)
    for pair in undeclared:
        audit.append(dict(severity="undeclared-adjacency", bedrock_id="%s+%s" % pair,
            detail=("%s and %s are adjacent by evidence (%s) but neither declares a relation."
                    % (pair[0], pair[1], "; ".join(sorted(cands[pair]))))))''',
'''    undeclared = sorted(set(cands) - declared)
    for pair in undeclared:
        _d = ("%s and %s are adjacent by evidence (%s) but neither declares a relation."
              % (pair[0], pair[1], "; ".join(sorted(cands[pair]))))
        audit.append(dict(severity="undeclared-adjacency", bedrock_id="%s+%s" % pair, detail=_d))
        # K349: build_register.py's own comment says "the audit below REFUSES TO WRITE if any
        # mechanically-derived adjacency candidate is undeclared." It did not -- it appended an
        # audit line and wrote anyway. The claim was made when the set was empty and stayed true
        # by luck rather than by construction, which is cccli in its purest form: a compliance
        # rule that has never been the gate it says it is. It is the gate now. Blast radius
        # measured before promoting it: 7 derived candidates, 7 declared, ZERO undeclared, so
        # no shipped register state changes and the only thing that moves is what happens to
        # the NEXT undeclared pair.
        fail.append("UNDECLARED ADJACENCY: " + _d)''')


def apply(src, patches, dest, label):
    raw = open(src, "rb").read()
    base = hashlib.md5(raw).hexdigest()
    txt = raw.decode("utf-8")
    for tag, old, new in patches:
        n = txt.count(old)
        assert n == 1, "%s: anchor %r occurs %d times, expected exactly 1" % (label, tag, n)
        txt = txt.replace(old, new, 1)
    out = txt.encode("utf-8")
    open(dest, "wb").write(out)
    print("  %s: base %s -> %s  %s  %d B" % (label, base, os.path.basename(dest),
                                             hashlib.md5(out).hexdigest(), len(out)))
    assert hashlib.md5(open(src, "rb").read()).hexdigest() == base, "%s mutated" % label
    return base


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else STG
    apply(B_SRC, BP, os.path.join(outdir, "build_register_v0_3.py"), "build_register_v0_2.py")
    n = open(R_SRC, "rb").read().decode("utf-8").count("honest_residuals_register_v0_2.json")
    print("  renderer references to the v0_2 artifact: %d" % n)
    raw = open(R_SRC, "rb").read().decode("utf-8")
    raw = raw.replace("honest_residuals_register_v0_2.json", "honest_residuals_register_v0_3.json")
    raw = raw.replace("honest_residuals_register_v0_2.md", "honest_residuals_register_v0_3.md")
    out = raw.encode("utf-8")
    open(os.path.join(outdir, "render_register_v0_3.py"), "wb").write(out)
    print("  render_register_v0_3.py  %s  %d B" % (hashlib.md5(out).hexdigest(), len(out)))


if __name__ == "__main__":
    main()

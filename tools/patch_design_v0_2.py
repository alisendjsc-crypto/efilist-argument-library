"""K345: derive adversarial_map_design_v0_2.md from v0_1 by explicit patch.
v0_1 is NEVER mutated -- canon pins it and the Phase A-E receipts cite it.
Run: python tools/patch_design_v0_2.py [--out <dir>]"""
import sys, os, hashlib
_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(_HERE)
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC = os.path.join(REPO, "adversarial_map_staging", "adversarial_map_design_v0_1.md")
APPEND = os.path.join(_HERE, "k345_design_v0_2_section9.md")
raw = open(SRC, "rb").read()
assert hashlib.md5(raw).hexdigest() == "49514ec9d631c3fbdf2cbf227923dd1b", "BASE GUARD FAIL"
t = raw.decode("utf-8")
assert "\r" not in t, "CR in source"
P = [
 ("header",
  "# Adversarial Objection/Rebuttal Map — Design v0.1\n*(Library seat, 2026-07-11 · answers `adversarial_map_commission_relay_v1.md` · Exchange 151 candidate · DESIGN ONLY — zero map entries authored here)*",
  "# Adversarial Objection/Rebuttal Map — Design v0.2\n*(v0.1: library seat, 2026-07-11 · answers `adversarial_map_commission_relay_v1.md` · Exchange 151 · DESIGN ONLY.*\n*v0.2: wuld.ink Cowork, K345, 2026-09-17 — §9 added, amending §1 and §2 per the LOCI ruling. §0–§8 are v0.1 verbatim;*\n*`adversarial_map_design_v0_1.md` stays on disk byte-identical as the record canon pins.)*"),
 ("schema-locus",
  '  "target_locus": "short|medium|long|diagnosis",',
  '  "target_locus": "short|medium|long|diagnosis|archetypeVariants.<slot>",   // <slot>: sophisticate|defender|drifter|blended -- see S9'),
 ("coverage-contract",
  "**Coverage contract:** every node gets ≥1 entry — a confident (a) or (d) is itself the routing datum. Cap 3 entries/node; the contract is the *strongest* continuation, not all continuations.",
  "**Coverage contract:** every node gets ≥1 entry — a confident (a) or (d) is itself the routing datum. Cap 3 entries/node; the contract is the *strongest* continuation, not all continuations.\n\n> **Amended K345 (§9):** the cap's unit is now the **locus**, not the node — ≤3 per `(target_id, target_locus)`, with a node-level bound of `3 + (variant loci on that node)` so a node without variants keeps the ratified 3 exactly. And `coverage` is now two claims: `coverage` over the primary ladder, `variant_coverage` over `archetypeVariants`. **Read §9 before authoring against this section.**"),
 ("anchor-rule",
  "1. **Anchor rule** — no entry without `target_anchor`; the move must engage a clause we actually shipped, killing mechanism-generic counters.",
  "1. **Anchor rule** — no entry without `target_anchor`; the move must engage a clause we actually shipped, killing mechanism-generic counters. *(K345: \"shipped\" means rendered to a reader. `archetypeVariants` and `note` render; `objectionSubforms` does not — §9.2, §9.4.)*"),
]
for name, o, n in P:
    assert t.count(o) == 1, "PATCH %r matched %d (want 1)" % (name, t.count(o))
    t = t.replace(o, n)
    print("  applied: %s" % name)
t = t.rstrip("\n") + "\n" + open(APPEND, encoding="utf-8").read()
dest = os.path.join(OUT, "adversarial_map_staging", "adversarial_map_design_v0_2.md")
b = t.encode("utf-8")
open(dest, "wb").write(b)
print("\nWROTE %s\n  bytes %d  md5 %s" % (dest, len(b), hashlib.md5(b).hexdigest()))

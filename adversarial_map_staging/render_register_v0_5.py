#!/usr/bin/env python3
"""Render honest_residuals_register_v0_5.json as its readable companion (L4).

Derived from render_register_v0_4.py, which stays byte-identical because it renders v0_4 and
v0_4's bytes do not move. The shape of the document is unchanged. What moves: the paths and the
version strings; a section for what moved from v0.4, including the tributaries L4 reclassified
and the three relations it declared; and each reclassified tributary is marked in the listing,
so a reader can tell a (d) a phase authored from an R1 FAILS a drafting pass reclassified.
"""
import os, sys, json

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K348_REPO") or os.path.dirname(_HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC_DIR = os.environ.get("K348_MAP_DIR") or os.path.join(OUT_DIR, "adversarial_map_staging")
SRC = os.path.join(SRC_DIR, "honest_residuals_register_v0_5.json")
OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "honest_residuals_register_v0_5.md")

d = json.loads(open(SRC, "rb").read().decode("utf-8"))
m = d["meta"]
L = []
w = L.append
w("# Honest-Residuals Register v0.5")
w("")
w("**Status: WORKING, and derived from a drafted assembly.** %d honest-residue (d) entries "
  "consolidated from `%s` (%s), which carries L4's drafts of R1's FAILS. A seat that did not draft "
  "them judges them (K258); that judgment is recorded in canon, not here."
  % (m["residue_entries"], m["source"]["artifact"], m["source"]["md5"][:8]))
w("Contributing phases (by authorship): %s. Contributing nothing: %s."
  % (", ".join("%s (%d)" % (k, v) for k, v in sorted(m["phases_contributing"].items())),
     ", ".join(m["phases_with_no_residue"]) or "none"))
w("Source corpus `%s` / 82 nodes. Rebuild: `python3 build_register_v0_5.py`." % m["source_corpus_md5"][:8])
w("")
w("**Library-internal.** No corpus, ledger, index or `/combined` byte moves from this artifact.")
w("")
w("---")
w("")
w("## What moved from v0.4")
w("")
for c in m["changes_from_v0_4"]:
    w("- %s" % c)
w("")
w(m["reclassified_at_L4"]["note"])
w("")
w("### Parity")
w("")
w(m["parity_with_v0_4"])
w("")
w("## What moved from v0.1 (carried from v0.4)")
w("")
for c in m["changes_from_v0_1"]:
    w("- %s" % c)
w("")
w("### The corpus span, ruled")
w("")
w(m["corpus_span_ruling"])
w("")
w("---")
w("")
w("## Audit")
w("")
if not d["audit"]:
    w("_No findings._")
for a in d["audit"]:
    w("- **[%s] `%s`** — %s" % (a["severity"], a["bedrock_id"], a["detail"]))
w("")
w("### Adjacency")
w("")
adj = m["adjacency"]
w("%d candidates derived from the two signals, %d relations declared, %d declared beyond what "
  "the signals detect; %d added at L4 (%s)." % (adj["candidates_derived"], adj["declared_relations"],
                                                len(adj["declared_but_undetected"]), len(adj["added_at_L4"]),
                                                ", ".join(adj["added_at_L4"])))
w("")
w(adj["note"])
w("")
w("**Vocabulary gap — `%s`:** %s" % (adj["vocabulary_gap"]["pair"], adj["vocabulary_gap"]["detail"]))
w("")
w("---")
w("")
w("## Bedrocks")
w("")
w("A tributary marked `→L4` is an R1 FAILS that L4 reclassified (a) → (d); its phase is the "
  "phase that authored the move.")
w("")
for b in d["bedrocks"]:
    w("### %s — %s" % (b["bedrock_id"], b["name"]))
    w("")
    if b["alias"]:
        w("*Alias:* `%s`" % b["alias"])
        w("")
    w(b["gloss"])
    w("")
    w("*Registered in:* `%s`" % b["registered_in"])
    if b["birth_certificate"]:
        bc = b["birth_certificate"]
        w("  ·  *Birth certificate:* `%s#%s` (phase %s)" % (bc["node"], bc["locus"], bc["phase"]))
    w("")
    if b.get("relations"):
        w("**Relations:**")
        w("")
        for r in b["relations"]:
            w("- `%s` → `%s` — %s" % (r["kind"], r["to"], r["note"]))
        w("")
    w("**Tributaries (%d across %d facet%s):**"
      % (b["tributary_count"], b["facet_count"], "" if b["facet_count"] == 1 else "s"))
    w("")
    for f in b["facets"]:
        w("- **%s** — %s" % (f["facet_id"], ", ".join(
            "`%s` (%s%s)" % (t["node"] if t["locus"] == "long" else "%s#%s" % (t["node"], t["locus"]),
                             t["phase"], "→L4" if "reclassified" in t else "")
            for t in f["tributaries"])))
    w("")
out = "\n".join(L) + "\n"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8", newline="\n").write(out)
print("rendered %s  %d B" % (OUT, len(out.encode("utf-8"))))

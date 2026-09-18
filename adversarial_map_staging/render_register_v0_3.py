#!/usr/bin/env python3
"""Render honest_residuals_register_v0_3.json as its readable companion.

Derived from render_register.py, which stays byte-identical because it renders v0_1 and
v0_1's bytes do not move. The shape of the document is unchanged; what changed is the
source block (v0_2 derives from one assembly, not six fragments) and the corpus note.
"""
import os, sys, json

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K348_REPO") or os.path.dirname(_HERE)
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
SRC_DIR = os.environ.get("K348_MAP_DIR") or os.path.join(OUT_DIR, "adversarial_map_staging")
SRC = os.path.join(SRC_DIR, "honest_residuals_register_v0_3.json")
OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "honest_residuals_register_v0_3.md")

d = json.loads(open(SRC, "rb").read().decode("utf-8"))
m = d["meta"]
L = []
w = L.append
w("# Honest-Residuals Register v0.2")
w("")
w("**Status: WORKING, and derived from a terminal artifact.** %d honest-residue (d) entries "
  "consolidated from `%s` (%s), which is the successor assembly."
  % (m["residue_entries"], m["source"]["artifact"], m["source"]["md5"][:8]))
w("Contributing phases: %s. Contributing nothing: %s."
  % (", ".join("%s (%d)" % (k, v) for k, v in sorted(m["phases_contributing"].items())),
     ", ".join(m["phases_with_no_residue"]) or "none"))
w("Source corpus `%s` / 82 nodes. Rebuild: `python3 build_register_v0_2.py`." % m["source_corpus_md5"][:8])
w("")
w("**Library-internal.** No corpus, ledger, index or `/combined` byte moves from this artifact.")
w("")
w("---")
w("")
w("## What moved from v0.1")
w("")
for c in m["changes_from_v0_1"]:
    w("- %s" % c)
w("")
w("### The corpus span, ruled")
w("")
w(m["corpus_span_ruling"])
w("")
w("### Parity")
w("")
w(m["parity_with_v0_1"])
if m.get("parity_reordered_only"):
    w("")
    w("Re-sequenced (content identical): %s." % ", ".join("`%s`" % b for b in m["parity_reordered_only"]))
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
  "the signals detect." % (adj["candidates_derived"], adj["declared_relations"],
                           len(adj["declared_but_undetected"])))
w("")
w(adj["note"])
w("")
w("**Vocabulary gap — `%s`:** %s" % (adj["vocabulary_gap"]["pair"], adj["vocabulary_gap"]["detail"]))
w("")
w("---")
w("")
w("## Bedrocks")
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
            w("- `%s` \u2192 `%s` \u2014 %s" % (r["kind"], r["to"], r["note"]))
        w("")
    w("**Tributaries (%d across %d facet%s):**"
      % (b["tributary_count"], b["facet_count"], "" if b["facet_count"] == 1 else "s"))
    w("")
    for f in b["facets"]:
        w("- **%s** — %s" % (f["facet_id"],
                             ", ".join("`%s` (%s)" % (t["node"], t["phase"]) for t in f["tributaries"])))
    w("")
out = "\n".join(L) + "\n"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8", newline="\n").write(out)
print("rendered %s  %d B" % (OUT, len(out.encode("utf-8"))))

#!/usr/bin/env python3
"""Build adversarial_map_v1_0.json -- the terminal assembly.

Design doc, terminal deliverables: fragments partition the 82, id-preferring dedupe,
class-count summary into canon, the (b)/(c) queue extracted as a v-cut scoping input,
(d)-novel items appended to the honest-residuals register. The last two ship as their own
artifacts beside this one; this file is the mapped-complete union.

Q3: v1_0 is the MAPPED-COMPLETE, PRE-TRIAGE state. Every entry carries status "mapped";
the lifecycle (queued -> ratified -> landed | rejected) lives in canon, never here.
"""
import json, hashlib, collections, sys

CORPUS = "../efilist_argument_library_v4_0_0.json"
PHASES = [("A","adv_map_phaseA_v0_1.json"), ("B1","adv_map_phaseB1_v0_1.json"),
          ("B2","adv_map_phaseB2_v0_1.json"), ("C","adv_map_phaseC_v0_1.json"),
          ("D","adv_map_phaseD_v0_1.json"), ("E","adv_map_phaseE_v0_1.json")]
OUT = "adversarial_map_v1_0.json"


def main():
    craw = open(CORPUS, "rb").read()
    corpus = json.loads(craw.decode("utf-8"))
    ids = [o["id"] for o in corpus["objections"]]
    idset = set(ids)
    order = {i: n for n, i in enumerate(ids)}
    fail, entries, frag = [], [], {}

    for ph, f in PHASES:
        raw = open(f, "rb").read()
        doc = json.loads(raw.decode("utf-8"))
        frag[ph] = {"file": f, "md5": hashlib.md5(raw).hexdigest(), "entries": len(doc["entries"]),
                    "amended": bool(doc["meta"].get("amended"))}
        for e in doc["entries"]:
            pv = e.get("provenance", {})
            if pv.get("phase") != ph:
                fail.append("%s carries an entry stamped phase %r" % (f, pv.get("phase")))
            entries.append(e)

    # PARTITION, not merge: no id may be claimed by two phases, and id x anchor stays unique.
    by_phase = collections.defaultdict(set)
    for e in entries:
        by_phase[e["provenance"]["phase"]].add(e["target_id"])
    seen = {}
    for ph, s in by_phase.items():
        for i in s:
            if i in seen:
                fail.append("node %s claimed by both %s and %s - fragments must PARTITION" % (i, seen[i], ph))
            seen[i] = ph
    pairs = collections.Counter((e["target_id"], e["target_anchor"]) for e in entries)
    for k, n in pairs.items():
        if n > 1:
            fail.append("duplicate id x anchor: %r" % (k,))
    per_id = collections.Counter(e["target_id"] for e in entries)
    for i, n in per_id.items():
        if n > 3:
            fail.append("%s has %d entries (cap 3)" % (i, n))
    missing = sorted(idset - set(per_id))
    if missing:
        fail.append("NOT mapped-complete: %d ids uncovered: %s" % (len(missing), missing[:6]))
    extra = sorted(set(per_id) - idset)
    if extra:
        fail.append("entries target %d ids not in the corpus: %s" % (len(extra), extra[:6]))
    if any(e.get("status") != "mapped" for e in entries):
        fail.append("an entry carries a status other than 'mapped'; the lifecycle lives in canon")

    if fail:
        print("REFUSING TO WRITE -- %d failure(s):" % len(fail))
        for f_ in fail: print("  " + f_)
        return 1

    # id-preferring dedupe (scholar pattern): corpus order, then phase, then anchor.
    entries.sort(key=lambda e: (order[e["target_id"]], e["provenance"]["phase"], e["target_anchor"]))

    cc = collections.Counter(e["class"] for e in entries)
    per_phase = {ph: dict(collections.Counter(
        e["class"] for e in entries if e["provenance"]["phase"] == ph)) for ph, _ in PHASES}
    tiers = {o["id"]: o["tier"] for o in corpus["objections"]}
    per_tier = {}
    for t in sorted(set(tiers.values())):
        n = [e for e in entries if tiers[e["target_id"]] == t]
        per_tier["T%d" % t] = {"nodes": len(set(e["target_id"] for e in n)), "entries": len(n),
                               **dict(collections.Counter(e["class"] for e in n))}
    loci = dict(collections.Counter(e["target_locus"] for e in entries))
    odig = hashlib.md5(json.dumps(corpus["objections"], indent=2, ensure_ascii=False,
                                  sort_keys=True).encode("utf-8") + b"\n").hexdigest()

    doc = {"meta": {
      "artifact": "adversarial_map_v1_0.json",
      "state": ("MAPPED-COMPLETE, PRE-TRIAGE (ratification Q3). Every entry carries status "
        "'mapped'. The lifecycle mapped -> queued -> ratified -> landed | rejected lives in "
        "project_canon, never in this artifact."),
      "assembled": "2026-09-17, wuld.ink Cowork, K339",
      "source_corpus": "efilist_argument_library_v4_0_0.json",
      "source_corpus_md5": hashlib.md5(craw).hexdigest(),
      "source_corpus_objections_md5": odig,
      "nodes_covered": len(per_id), "nodes_total": len(ids), "entries": len(entries),
      "class_counts": {k: cc[k] for k in ("a", "b", "c", "d")},
      "per_phase": per_phase, "per_tier": per_tier, "locus_distribution": loci,
      "fragments": frag,
      "validation": ("validator v0_2 under --assembly: 21 checks, 0 violations, 0 advisories. "
        "--assembly promotes every advisory to hard, which is why the Phase A em-dashes and the "
        "B1 carry-forward routes had to be discharged rather than displayed before this file "
        "could exist."),
      "locus_discipline": ("Author against the deepest locus that addresses the objection, or "
        "state in the grounds why a shallower one was chosen (hazard ccclxi / ledger class C8). "
        "The anchor rule permits any locus and is silent on depth; practice settled on `long`, "
        "and the distribution above is the evidence."),
      "fences": ("Nothing here authorizes a byte. (b) and (c) yields are intake candidates routing "
        "through staging -> cold-grade -> assembly inside a declared content cut; see "
        "adversarial_map_regen_queue_v0_1.json. (d) termini route to "
        "honest_residuals_register_v0_1.json."),
      "siblings": {"queue": "adversarial_map_regen_queue_v0_1.json",
                   "register": "honest_residuals_register_v0_1.json",
                   "rulings": "adversarial_map_assembly_rulings_v0_1.json",
                   "ledger": "process_ledger_v0_1.md"}},
      "entries": entries}

    out = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = out.encode("utf-8")
    print("WROTE %s  %d B  md5 %s" % (OUT, len(b), hashlib.md5(b).hexdigest()))
    print("  %d/%d nodes, %d entries, classes %s" % (len(per_id), len(ids), len(entries), doc["meta"]["class_counts"]))
    print("  per tier: %s" % json.dumps(per_tier))
    print("  loci    : %s" % loci)
    return 0


if __name__ == "__main__":
    sys.exit(main())

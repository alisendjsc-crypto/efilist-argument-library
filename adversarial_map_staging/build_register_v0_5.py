#!/usr/bin/env python3
"""honest_residuals_register_v0_5.json -- the (d)s L4 drafted, consolidated (L4, 2026-09-25).

WHAT CHANGES FROM v0_4, which stays byte-identical on disk:
  i.   THE SOURCE is adversarial_map_v1_4.json. Its 35 new (d)s are R1 FAILS reclassified by the
       drafting pass, so they are TRIBUTARIES OF BEDROCK ALREADY REGISTERED. No bedrock is added:
       the class law forced none, and the build refuses if a new bedrock_id appears.
  ii.  ONE FACET PER TRIBUTARY, AS REGISTERED, BY LOOKUP. Each amended (d) names in
       provenance.amended.bedrock_from the registered (d) its line reaches; its facet is that
       tributary's facet in v0_4, and the build asserts the shipped bedrock_name resolves to the
       same bedrock through BEDROCK_MAP. No facet id is minted.
  iii. A RECLASSIFIED TRIBUTARY IS DATED BY ITS RECLASSIFICATION, NOT ITS AUTHORSHIP. Its `phase`
       stays the phase that authored the move, and it carries `reclassified`. The birth-order check
       reads an amended tributary as adjudicated at L4, after G: an (a) authored in Phase A and
       reclassified onto HR-14 at L4 does not precede HR-14's Phase F birth certificate, and a
       check that said it did would refuse a true register.
  iv.  THREE RELATIONS, because three pairs now share a tributary node and the adjacency gate
       refuses an undeclared pair. All three kinds are in the ratified vocabulary. They are the
       drafting seat's, and the judge reads them with the drafts:
         HR-11 conditions HR-02      red-button-repugnant carries both
         HR-12 independent_of HR-10  moral-particularism carries both
         HR-14 independent_of HR-05  imposing-values carries both
  v.   PARITY AGAINST v0_4, field for field: every v0_4 bedrock keeps its name, alias, gloss,
       registration and birth certificate; its relations gain exactly the declared three and lose
       none; every v0_4 tributary is present unchanged on its v0_4 facet; the only new tributaries
       are the amended (d)s, each on the facet its draft names. The v0_1 and v0_3 gates hold by
       transitivity: v0_4 held them and no tributary they read has moved.

Imports build_register_v0_4.py (md5-guarded) for BEDROCK_MAP, FACET_BY_NODE, BEDROCKS and
RELATIONS rather than restating them. Repo-relative. --out <dir> to emit elsewhere.
"""
import os, sys, json, collections, itertools, re as _re, importlib.util

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K348_REPO") or os.path.dirname(_HERE)
STAGE = os.path.join(REPO, "adversarial_map_staging")
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
MAP_DIR = os.environ.get("K348_MAP_DIR") or os.path.join(OUT_DIR, "adversarial_map_staging")
OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "honest_residuals_register_v0_5.json")

sys.path.insert(0, STAGE)
import adv_map_validator_v0_6 as V   # noqa: E402

V0_4_BUILDER_MD5 = "705d8a437d921993d94c72a85b455379"
V0_4 = os.path.join(STAGE, "honest_residuals_register_v0_4.json")
V0_4_MD5 = "d067729fafb51926bc9e845209417886"
ASSEMBLY = os.path.join(MAP_DIR, "adversarial_map_v1_4.json")

_bp = os.path.join(STAGE, "build_register_v0_4.py")
_md5_builder = V.md5_bytes(open(_bp, "rb").read())
_spec = importlib.util.spec_from_file_location("build_register_v0_4", _bp)
W = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(W)

BEDROCK_MAP = dict(W.BEDROCK_MAP)
FACET_BY_NODE = dict(W.FACET_BY_NODE)
BEDROCKS = {k: dict(v) for k, v in W.BEDROCKS.items()}
RELATION_KINDS = W.RELATION_KINDS
RELATIONS = {k: list(v) for k, v in W.RELATIONS.items()}
ADDED_RELATIONS = {
    "HR-11": ("conditions", "HR-02",
              "L4, drafted: co-located at red-button-repugnant, where #44 reaches HR-11 and the (d) at "
              "#medium, with #45 and #47, sits on HR-02's intrinsic-value-of-existence facet. That (d) "
              "states the dispute HR-11 names -- 'The firmware genealogy cannot break the tie' -- and "
              "HR-11's own tributary cross-refers to this node's Moorean retreat, so the pair was "
              "adjacent before any signal could see it. HR-11's resolution changes the FORCE of HR-02's "
              "open question through that facet without creating or dissolving it: if the debunking "
              "succeeds, the staked value of existence loses the intuition that makes it more than a "
              "stake, and the question whether the positive-states rebuttals survive rejecting the "
              "asymmetry stays askable either way. Same shape as HR-14 conditions HR-11."),
    "HR-12": ("independent_of", "HR-10",
              "L4, drafted: co-located at moral-particularism, where the Phase A (d) is HR-10 and #61 "
              "reaches HR-12 through contractualism-scanlon. HR-10 refuses invariant verdicts as such; "
              "HR-12 asks which standpoint, prospects or outcomes, contractualist justification is "
              "indexed to. The particularist's refusal arises whichever index wins, and the index "
              "question arises inside contractualism with no particularism at all. Sharing a node is "
              "a fact about where #61 surfaced, not about what either bedrock claims."),
    "HR-14": ("independent_of", "HR-05",
              "L4, drafted: co-located at imposing-values, whose #short takes the creation symmetry "
              "(#13, HR-05) and whose #medium the terminal-outcome clause (#12, HR-14). HR-05 asks "
              "whether creation can wrong a being with no worse-off baseline; HR-14 concerns beings "
              "who already exist and have baselines. Neither resolution touches the other's question, "
              "the same ground on which HR-14 is already declared independent_of HR-03."),
}
for _bid, _rel in ADDED_RELATIONS.items():
    RELATIONS[_bid] = RELATIONS.get(_bid, []) + [_rel]

ORDER = list(W.PHASE_ORDER) + ["L4"]


def main():
    fail, audit = [], []
    assert _md5_builder == V0_4_BUILDER_MD5, "BASE GUARD: build_register_v0_4.py moved (%s)" % _md5_builder
    assert W._md5_builder == W.BASE_BUILDER_MD5, "BASE GUARD: build_register.py moved"
    v4raw = open(V0_4, "rb").read()
    assert V.md5_bytes(v4raw) == V0_4_MD5, "BASE GUARD: register v0_4 is %s" % V.md5_bytes(v4raw)
    v4 = json.loads(v4raw.decode("utf-8"))
    v4b = {b["bedrock_id"]: b for b in v4["bedrocks"]}
    v4row = {}
    for b in v4["bedrocks"]:
        for f in b["facets"]:
            for t in f["tributaries"]:
                v4row[(t["node"], t["locus"], t["anchor"])] = (b["bedrock_id"], f["facet_id"])

    araw = open(ASSEMBLY, "rb").read()
    amap = json.loads(araw.decode("utf-8"))
    ameta = amap["meta"]
    d_at = collections.defaultdict(list)
    for e in amap["entries"]:
        if e["class"] == "d" and "amended" not in e["provenance"]:
            d_at["%s#%s" % (e["target_id"], e["target_locus"])].append(e)

    rows = []
    for e in amap["entries"]:
        if e["class"] != "d":
            continue
        r = e["routing"]["residue"]
        key = r["bedrock_name"]
        if key not in BEDROCK_MAP:
            fail.append("UNMAPPED bedrock_name at %s/%s: %r" % (e["provenance"]["phase"], e["target_id"], key))
            continue
        bid, facet = BEDROCK_MAP[key]
        facet = FACET_BY_NODE.get((bid, e["target_id"]), facet)
        am = e["provenance"].get("amended")
        row = dict(bedrock_id=bid, facet=facet, phase=e["provenance"]["phase"],
                   node=e["target_id"], locus=e["target_locus"], anchor=e["target_anchor"],
                   novel=r["novel"], shipped_bedrock_name=key, terminus_routing=r["terminus_routing"],
                   adjudicated="L4" if am else e["provenance"]["phase"])
        if am:
            src = d_at.get(am["bedrock_from"], [])
            if len(src) != 1:
                fail.append("%s#%s: bedrock_from %s names %d registered (d)s"
                            % (e["target_id"], e["target_locus"], am["bedrock_from"], len(src)))
                continue
            got = v4row.get((src[0]["target_id"], src[0]["target_locus"], src[0]["target_anchor"]))
            if got is None or got[0] != bid:
                fail.append("%s#%s: its bedrock_name resolves to %s but bedrock_from sits on %s"
                            % (e["target_id"], e["target_locus"], bid, got))
                continue
            row["facet"] = got[1]
            if r["novel"]:
                fail.append("%s#%s: a reclassified tributary claims novel=true" % (e["target_id"], e["target_locus"]))
            row["reclassified"] = ("from (a) at L4 under the R1 standard, row %s; through %s"
                                   % (am["r1_row"], am["bedrock_from"]))
        rows.append(row)
    for (bid, node) in FACET_BY_NODE:
        if not any(r["bedrock_id"] == bid and r["node"] == node for r in rows):
            fail.append("FACET_BY_NODE names (%s, %s) but no tributary matches it" % (bid, node))
    new_bids = sorted(set(r["bedrock_id"] for r in rows) - set(BEDROCKS))
    if new_bids:
        fail.append("a bedrock appears that is not registered: %s (L4 adds none)" % new_bids)

    by_id = collections.defaultdict(list)
    for r in rows:
        by_id[r["bedrock_id"]].append(r)

    # ---- adjacency: the same two signals as v0_4, and the same refusal
    alias = {}
    for bid, meta in BEDROCKS.items():
        keys = [meta["name"].lower()]
        if meta["alias"]:
            keys += [a.strip().lower() for a in _re.split(r"[/]", meta["alias"])]
        alias[bid] = keys
    cands = collections.defaultdict(set)
    for r in rows:
        low = r["terminus_routing"].lower()
        for other, keys in alias.items():
            if other == r["bedrock_id"]:
                continue
            if other.lower() in low or any(k in low or k.replace(" ", "-") in low for k in keys):
                cands[tuple(sorted((r["bedrock_id"], other)))].add(
                    "terminus at %s/%s names %s" % (r["phase"], r["node"], other))
    bynode = collections.defaultdict(set)
    for r in rows:
        bynode[r["node"]].add(r["bedrock_id"])
    for node, bids in bynode.items():
        if len(bids) > 1:
            for a, b_ in itertools.combinations(sorted(bids), 2):
                cands[(a, b_)].add("shared tributary node %s" % node)
    declared = set()
    for bid, rels in RELATIONS.items():
        for _kind, other, _note in rels:
            declared.add(tuple(sorted((bid, other))))
            if other not in BEDROCKS:
                fail.append("%s declares a relation to unknown bedrock %s" % (bid, other))
    for bid in BEDROCKS:
        if bid not in RELATIONS:
            fail.append("%s declares no relations list; an empty list must be explicit" % bid)
    for pair in sorted(set(cands) - declared):
        fail.append("UNDECLARED ADJACENCY: %s and %s (%s)" % (pair[0], pair[1], "; ".join(sorted(cands[pair]))))
    hand_only = sorted(declared - set(cands))
    new_pairs = sorted(tuple(sorted((b, rel[1]))) for b, rel in ADDED_RELATIONS.items())
    for pair in new_pairs:
        if pair not in cands:
            fail.append("added relation %s+%s is not detected by either signal; it was added to "
                        "discharge a detected pair" % pair)
    for _bid, _rels in sorted(RELATIONS.items()):
        for _k, _o, _n in _rels:
            if _k not in RELATION_KINDS:
                fail.append("%s declares relation kind %r, not in the ratified vocabulary" % (_bid, _k))

    # ---- birth certificates, dated by adjudication
    for bid, rs in sorted(by_id.items()):
        meta = BEDROCKS.get(bid)
        if meta is None:
            continue   # already refused above: a bedrock that is not registered
        births = [r for r in rs if r["novel"]]
        if meta["registered_in"] == "this-program":
            if len(births) != 1:
                fail.append("%s claims this-program registration but has %d novel=true entries" % (bid, len(births)))
            else:
                b = births[0]
                earlier = [r for r in rs if ORDER.index(r["adjudicated"]) < ORDER.index(b["adjudicated"])]
                if earlier:
                    fail.append("%s birth certificate is %s/%s but %d tributary/ies were adjudicated before it"
                                % (bid, b["phase"], b["node"], len(earlier)))
        elif births:
            audit.append(dict(severity="novel-flag-collision", bedrock_id=bid,
                detail=("%s was registered before this program (%s) but %d fragment entry/ies "
                        "flag it novel=true: %s. A bedrock has one birth certificate.")
                       % (bid, meta["registered_in"], len(births), [(r["phase"], r["node"]) for r in births])))
    audit.append(dict(severity="adjacency-vocabulary-gap-CLOSED", bedrock_id=W.VOCABULARY_GAP["pair"],
                      detail=("RESOLVED at K349: Josiah ratified a fifth relation kind, `conditions`, and "
                              "HR-14+HR-11 is declared under it. The v0_2 statement of the gap is preserved "
                              "verbatim below. " + W.VOCABULARY_GAP["detail"])))
    audit.append(dict(severity="relations-drafted-L4", bedrock_id="HR-11+HR-02, HR-12+HR-10, HR-14+HR-05",
                      detail=("Three relations are declared because three pairs came to share a tributary "
                              "node when L4 reclassified R1's FAILS, and the adjacency gate refuses an "
                              "undeclared pair. They are the drafting seat's, inside the ratified vocabulary, "
                              "and are judged with the drafts (K258).")))

    if fail:
        print("REFUSING TO WRITE -- %d invariant failure(s):" % len(fail))
        for f in fail:
            print("  " + f)
        return 1

    bedrocks = []
    for bid in sorted(BEDROCKS):
        rs = by_id.get(bid, [])
        facets = collections.defaultdict(list)
        for r in rs:
            t = dict(phase=r["phase"], node=r["node"], locus=r["locus"], anchor=r["anchor"],
                     novel=r["novel"], terminus_routing=r["terminus_routing"])
            if "reclassified" in r:
                t["reclassified"] = r["reclassified"]
            facets[r["facet"]].append(t)
        births = [r for r in rs if r["novel"]]
        bedrocks.append(dict(
            bedrock_id=bid, name=BEDROCKS[bid]["name"], alias=BEDROCKS[bid]["alias"],
            gloss=BEDROCKS[bid]["gloss"], registered_in=BEDROCKS[bid]["registered_in"],
            birth_certificate=(dict(phase=births[0]["phase"], node=births[0]["node"],
                                    locus=births[0]["locus"]) if len(births) == 1 else None),
            tributary_count=len(rs), facet_count=len(facets),
            relations=[dict(kind=k, to=o, note=n) for k, o, n in RELATIONS.get(bid, [])],
            facets=[dict(facet_id=k, tributaries=v) for k, v in sorted(facets.items())]))

    # ---- parity against v0_4, field for field
    diffs, unchanged = [], []
    def strip(t):
        return {k: v for k, v in t.items() if k != "reclassified"}
    for b in bedrocks:
        bid = b["bedrock_id"]
        p = v4b.get(bid)
        if p is None:
            diffs.append("%s is not in v0_4" % bid)
            continue
        for k in ("name", "alias", "gloss", "registered_in", "birth_certificate"):
            if b[k] != p[k]:
                diffs.append("%s.%s differs from v0_4" % (bid, k))
        want_rel = list(p["relations"])
        if bid in ADDED_RELATIONS:
            k, o, n = ADDED_RELATIONS[bid]
            want_rel.append(dict(kind=k, to=o, note=n))
        if b["relations"] != want_rel:
            diffs.append("%s relations are not v0_4's plus exactly the declared additions" % bid)
        mine = {f["facet_id"]: f["tributaries"] for f in b["facets"]}
        for f in p["facets"]:
            olds = [t for t in mine.get(f["facet_id"], []) if "reclassified" not in t]
            if olds != f["tributaries"]:
                diffs.append("%s facet %s: its v0_4 tributaries moved" % (bid, f["facet_id"]))
        if set(mine) - set(f["facet_id"] for f in p["facets"]):
            diffs.append("%s gains a facet id: %s" % (bid, sorted(set(mine) - set(f["facet_id"] for f in p["facets"]))))
        added = sum(1 for ts in mine.values() for t in ts if "reclassified" in t)
        if b["tributary_count"] != len([t for f in p["facets"] for t in f["tributaries"]]) + added:
            diffs.append("%s tributary arithmetic does not close" % bid)
        if json.dumps(b, sort_keys=True) == json.dumps(p, sort_keys=True):
            unchanged.append(bid)
    amended_d = [e for e in amap["entries"] if e["class"] == "d" and "amended" in e["provenance"]]
    reclassified = [t for b in bedrocks for f in b["facets"] for t in f["tributaries"] if "reclassified" in t]
    if len(reclassified) != len(amended_d):
        diffs.append("%d reclassified tributaries for %d amended (d)s" % (len(reclassified), len(amended_d)))
    if diffs:
        print("REFUSING TO WRITE -- parity with v0_4 broke in %d place(s):" % len(diffs))
        for x in diffs:
            print("  " + x)
        return 1

    per_bid = dict(sorted(collections.Counter(
        r["bedrock_id"] for r in rows if r["adjudicated"] == "L4").items()))
    m4 = v4["meta"]
    doc = dict(meta=dict(
        artifact="honest_residuals_register_v0_5.json",
        supersedes=m4["supersedes"],
        status=("WORKING, and derived from a DRAFTED assembly. adversarial_map_v1_4.json carries L4's "
                "drafts of R1's FAILS; a seat that did not draft them judges them (K258), and whether "
                "they are judged is recorded in canon, not here. Every (d) in that assembly is "
                "consolidated here."),
        purpose=m4["purpose"],
        source=dict(artifact=ameta["artifact"], md5=V.md5_bytes(araw), entries=ameta["entries"]),
        source_corpus=ameta["source_corpus"],
        source_corpus_md5=ameta["source_corpus_md5"],
        source_corpus_objections_md5=ameta["source_corpus_objections_md5"],
        corpus_span_ruling=m4["corpus_span_ruling"],
        residue_entries=len(rows), bedrocks=len(BEDROCKS),
        distinct_shipped_bedrock_names=len(set(r["shipped_bedrock_name"] for r in rows)),
        phases_contributing=dict(collections.Counter(r["phase"] for r in rows)),
        phases_with_no_residue=[p for p in W.PHASE_ORDER if not any(r["phase"] == p for r in rows)],
        reclassified_at_L4=dict(count=len(reclassified), by_bedrock=per_bid,
                                note=("Tributaries whose (d) is L4's reclassification of an R1 FAILS. "
                                      "`phase` is the phase that authored the move; `reclassified` names "
                                      "the R1 row and the registered (d) the line reaches. No bedrock and "
                                      "no facet id is added.")),
        pre_map_registrations=m4["pre_map_registrations"],
        this_program_registrations=m4["this_program_registrations"],
        changes_from_v0_4=[
            "source is adversarial_map_v1_4.json, which carries L4's drafts of R1's 45 FAILS",
            "%d tributaries added, each an R1 FAILS reclassified (a) -> (d) onto registered bedrock "
            "and filed on the facet of the registered (d) it reaches: %s"
            % (len(reclassified), ", ".join("%s %d" % kv for kv in per_bid.items())),
            "no bedrock added and no facet id minted; the class law forced none",
            "HR-11 conditions HR-02, HR-12 independent_of HR-10 and HR-14 independent_of HR-05 "
            "declared, because the new tributaries made each pair share a node; drafted by L4",
            "the birth-order check reads a reclassified tributary as adjudicated at L4, after G",
        ],
        changes_from_v0_1=m4["changes_from_v0_1"],
        parity_with_v0_4=("Field for field, asserted before the write: every v0_4 bedrock keeps its "
                          "name, alias, gloss, registration and birth certificate; relations gain "
                          "exactly the three declared and lose none; every v0_4 tributary stands "
                          "unchanged on its v0_4 facet; the only additions are the %d reclassified "
                          "tributaries. %d of %d bedrocks are byte-identical to v0_4. The v0_1 and "
                          "v0_3 parity gates hold by transitivity: v0_4 held them, and no tributary "
                          "they read has moved." % (len(reclassified), len(unchanged), len(BEDROCKS))),
        predecessor=dict(artifact="honest_residuals_register_v0_4.json", md5=V0_4_MD5,
                         note="stays byte-identical on disk; v0_5 supersedes it, it is not edited"),
        adjacency=dict(
            candidates_derived=len(cands), declared_relations=len(declared),
            detected_and_declared=sorted("%s+%s" % p for p in sorted(set(cands) & declared)),
            declared_but_undetected=sorted("%s+%s" % p for p in hand_only),
            added_at_L4=["%s+%s" % p for p in new_pairs],
            vocabulary_gap=W.VOCABULARY_GAP,
            ratified_kinds=list(RELATION_KINDS),
            fifth_kind=m4["adjacency"]["fifth_kind"],
            note=m4["adjacency"]["note"]),
        fences="LIBRARY-INTERNAL. No corpus, ledger, index or combined byte moves from this artifact."),
        audit=audit, bedrocks=bedrocks)

    out = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    bb = out.encode("utf-8")
    print("WROTE %s  %d B  md5 %s" % (OUT, len(bb), V.md5_bytes(bb)))
    print("  %d (d) entries -> %d bedrocks; %d reclassified at L4: %s"
          % (len(rows), len(BEDROCKS), len(reclassified), json.dumps(per_bid)))
    print("  adjacency: %d candidates, %d declared, %d added at L4" % (len(cands), len(declared), len(new_pairs)))
    print("  parity with v0_4: HELD (%d of %d bedrocks byte-identical)" % (len(unchanged), len(BEDROCKS)))
    for b in bedrocks:
        print("  %-6s %-2d trib / %d facet  %s" % (b["bedrock_id"], b["tributary_count"], b["facet_count"], b["name"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

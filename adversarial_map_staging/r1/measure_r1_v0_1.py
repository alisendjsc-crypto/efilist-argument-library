#!/usr/bin/env python3
"""R1 instrument -- make R1 decidable, not decide it.

R1 (project_canon_v38_16.json L3917): "OPEN -- Josiah + library seat.
Strongest-vs-repairable. SCOPE CORRECTED at K350: blocks (a) only."
Question (canon L4067): "whether a continuation was authored at full force or
at the most repairable reading of our text".

For every class-(a) entry in adversarial_map_v1_3.json this emits: node id,
tier, move verbatim, anchor verbatim, answering locus, the claim a card would
make under a strength label, and instrument readings (anchor presence, lexical
overlap between the move and its answering locus, the answering sentences with
the highest overlap, strength/repair lexical signals).  Then the per-tier class
mix against the phases A-E base rate, K346 method (design v0_5 s10.4; K348
two-sided exact binomial; seeded sorted-pool permutation null, ccclxvii).

NOTHING HERE IS A RULING.  Every number is an instrument reading (K346: "a
class distribution that departs from its own base rate is an instrument
reading before it is a finding").  Josiah rules; the JSON carries a `ruling`
slot per entry, null until he does.

Repo-relative; reproducible under any PYTHONHASHSEED.  Code seat session 2.
"""
import collections
import datetime
import hashlib
import json
import math
import os
import random
import re

HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = os.path.dirname(HERE)
ROOT = os.path.dirname(STAGE)
MAP = os.path.join(STAGE, "adversarial_map_v1_3.json")
CORPUS = os.path.join(ROOT, "efilist_argument_library_v4_0_0.json")
OUT_STEM = "R1_evidence_2026-09-19"          # name as commissioned in the session-2 kickoff

# --- the K346/K348 constants, verbatim from controls_phaseF.py / measure_k348_v0_1.py
AE_V1_0 = {"a": 39, "b": 21, "c": 1, "d": 32}   # frozen v1_0, 93 entries -- the ruled base rate
SEED = 20260918
N_PERM = 20000
AE_PHASES = ("A", "B1", "B2", "C", "D", "E")

STOP = set("""a an the and or but if then than that this these those of to in on at by for
with from as is are was were be been being it its not no nor so such which who whom
whose what when where why how do does did done has have had having can could would should
may might must will shall into onto over under out up down off about above below between
own same too very just also only any all each both few more most other some our ours we us
you your yours they them their theirs he him his she her hers i me my mine one ones there
here because while whether either neither since until against without within through
during before after again further once doing""".split())


def md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def words(s):
    return re.findall(r"[A-Za-z][A-Za-z'-]*", s)


def content(s):
    out = set()
    for w in words(s):
        w = w.lower().strip("'-")
        if len(w) < 3 or w in STOP:
            continue
        if len(w) > 4 and w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
        out.add(w)
    return out


def sentences(s):
    return [x.strip() for x in re.split(r"(?<=[.!?])\s+", s) if x.strip()]


def C(n, r):
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))


def two_sided(k, n, p):
    """K348's exact two-sided binomial: sum of pmf mass <= pmf(observed)."""
    pmf = [C(n, i) * (p ** i) * ((1 - p) ** (n - i)) for i in range(n + 1)]
    return sum(q for q in pmf if q <= pmf[k] + 1e-15)


def locus_text(node, locus):
    if locus in ("short", "medium", "long"):
        return node["responses"].get(locus) or ""
    if locus.startswith("archetypeVariants."):
        return (node["responses"].get("archetypeVariants") or {}).get(locus.split(".", 1)[1]) or ""
    return node.get(locus) or ""      # diagnosis, note


STRENGTH_SIG = ["at strength", "strongest", "best reading", "steelman", "charitab",
                "met directly", "meets it directly", "at full force", "full strength"]
REPAIR_SIG = ["clause", "sentence", "wording", "phrasing", "the word ", "misstat", "overstat",
              "fixable", "repair", "regen", "rewrite", "one line", "the number", "statistic"]


def sig(text, pats):
    t = text.lower()
    return sorted({p.strip() for p in pats if p in t})


def med(xs):
    xs = sorted(xs)
    return xs[len(xs) // 2] if xs else None


def main():
    map_raw = open(MAP, "rb").read()
    corpus_raw = open(CORPUS, "rb").read()
    m = json.loads(map_raw.decode("utf-8"))
    c = json.loads(corpus_raw.decode("utf-8"))
    assert m["meta"]["source_corpus_md5"] == md5_bytes(corpus_raw), "corpus md5 != map.meta.source_corpus_md5"
    nodes = {n["id"]: n for n in c["objections"]}
    E = m["entries"]
    A = [e for e in E if e["class"] == "a"]
    assert len(A) == 69, len(A)

    # ------------------------------------------------------------------ per-entry
    rows = []
    for e in A:
        node = nodes[e["target_id"]]
        tier = "T%s" % node["tier"]
        ltxt = locus_text(node, e["target_locus"])
        move_c = content(e["adversarial_move"])
        answers = []
        for ref in e["routing"]["answered_by"]:
            nid, _, loc = ref.partition("#")
            atxt = locus_text(nodes[nid], loc) if nid in nodes else ""
            a_c = content(atxt)
            ov = (len(move_c & a_c) / len(move_c)) if move_c else 0.0
            scored = []
            for i, s in enumerate(sentences(atxt)):
                scored.append((len(move_c & content(s)), -i, s))
            scored.sort(reverse=True)
            top = [{"overlap_words": k, "sentence": s[:420]} for k, _, s in scored[:2] if k > 0]
            answers.append({
                "ref": ref, "same_node": nid == e["target_id"], "locus": loc,
                "locus_words": len(words(atxt)),
                "move_overlap": round(ov, 3),
                "overlap_terms": sorted(move_c & a_c)[:12],
                "top_sentences": top,
            })
        card = ('%s#%s -- the strongest objection here is: "%s" -- WE ANSWER THIS at %s.'
                % (e["target_id"], e["target_locus"], e["adversarial_move"],
                   ", ".join(e["routing"]["answered_by"])))
        rows.append({
            "n": len(rows) + 1,
            "target_id": e["target_id"], "tier": tier, "category": node.get("category"),
            "target_locus": e["target_locus"],
            "phase": e["provenance"]["phase"], "seat": e["provenance"]["seat"], "date": e["provenance"]["date"],
            "adversarial_move": e["adversarial_move"],
            "move_words": len(words(e["adversarial_move"])),
            "target_anchor": e["target_anchor"],
            "anchor_words": len(words(e["target_anchor"])),
            "anchor_found_in_locus": e["target_anchor"] in ltxt,
            "locus_words": len(words(ltxt)),
            "answered_by": e["routing"]["answered_by"],
            "answered_by_any_same_node": any(a["same_node"] for a in answers),
            "answered_by_max_overlap": max([a["move_overlap"] for a in answers] or [0.0]),
            "answers": answers,
            "grounds": e["grounds"],
            "strength_signals": sig(e["adversarial_move"] + " " + e["grounds"], STRENGTH_SIG),
            "repair_signals": sig(e["adversarial_move"] + " " + e["grounds"], REPAIR_SIG),
            "card_claim_strength_label": card,
            "R1_question": ("Is the move the strongest continuation a maximally competent hostile "
                            "interlocutor deploys against %s#%s as a reader meets it, and does %s answer "
                            "THAT form rather than a more repairable reading?"
                            % (e["target_id"], e["target_locus"], ", ".join(e["routing"]["answered_by"]))),
            "ruling": None,
        })

    # ------------------------------------------------------------------ class mix, K346 method
    def mix(entries):
        cc = collections.Counter(x["class"] for x in entries)
        n = len(entries)
        return {"n": n, "counts": {k: cc.get(k, 0) for k in "abcd"},
                "a_share": round(cc["a"] / n, 4) if n else None,
                "b_share": round(cc["b"] / n, 4) if n else None,
                "d_share": round(cc["d"] / n, 4) if n else None,
                "a_or_d": cc["a"] + cc["d"]}

    base_n = sum(AE_V1_0.values())
    p_ad = (AE_V1_0["a"] + AE_V1_0["d"]) / base_n
    p_a = AE_V1_0["a"] / base_n
    p_b = AE_V1_0["b"] / base_n
    AE_entries = [x for x in E if x["provenance"]["phase"] in AE_PHASES]
    ae13 = mix(AE_entries)
    p_ad_13 = ae13["a_or_d"] / ae13["n"]

    def tests(mx):
        n = mx["n"]
        cnt = mx["counts"]
        return {
            "p_a_or_d_vs_v1_0_base": round(two_sided(mx["a_or_d"], n, p_ad), 4),
            "p_a_or_d_vs_v1_3_AE": round(two_sided(mx["a_or_d"], n, p_ad_13), 4),
            "p_a_vs_base": round(two_sided(cnt["a"], n, p_a), 4),
            "p_b_vs_base": round(two_sided(cnt["b"], n, p_b), 4),
        }

    def tier_of(x):
        return "T%s" % nodes[x["target_id"]]["tier"]

    per_tier = {}
    for scope_name, pool in (("all_phases", E), ("A_to_E_only", AE_entries)):
        d = {}
        for t in ("T1", "T2", "T3", "T4", "T5"):
            sub = [x for x in pool if tier_of(x) == t]
            mx = mix(sub)
            mx.update(tests(mx))
            a_rows = [r for r in rows if r["tier"] == t and (scope_name == "all_phases" or r["phase"] in AE_PHASES)]
            mx["a_entries"] = len(a_rows)
            if a_rows:
                mx["a_median_move_words"] = med([r["move_words"] for r in a_rows])
                mx["a_median_anchor_words"] = med([r["anchor_words"] for r in a_rows])
                mx["a_same_node_share"] = round(sum(r["answered_by_any_same_node"] for r in a_rows) / len(a_rows), 3)
                mx["a_median_max_overlap"] = med([r["answered_by_max_overlap"] for r in a_rows])
                mx["a_answering_depth"] = dict(collections.Counter(a["locus"] for r in a_rows for a in r["answers"]))
            d[t] = mx
        per_tier[scope_name] = d

    # permutation null: is a-share heterogeneous across tiers?  statistic = max |tier a-share - pooled|
    def perm(pool):
        pool = sorted(pool, key=lambda x: (x["target_id"], x["target_locus"], x["provenance"]["phase"]))  # ccclxvii
        labels = [x["class"] for x in pool]
        groups = [tier_of(x) for x in pool]
        gidx = {g: [i for i, gg in enumerate(groups) if gg == g] for g in sorted(set(groups))}

        def stat(lbls):
            pooled = sum(1 for l in lbls if l == "a") / len(lbls)
            return max(abs(sum(1 for i in idx if lbls[i] == "a") / len(idx) - pooled) for idx in gidx.values())

        obs = stat(labels)
        rng = random.Random(SEED)
        ge = 0
        lb = list(labels)
        for _ in range(N_PERM):
            rng.shuffle(lb)
            if stat(lb) >= obs - 1e-12:
                ge += 1
        return {"statistic": "max |tier a-share - pooled a-share|", "observed": round(obs, 4),
                "N": N_PERM, "seed": SEED, "p": round(ge / N_PERM, 4)}

    perm_all = perm(E)
    perm_ae = perm(AE_entries)

    # by phase, replicating K348's published numbers as the implementation check
    by_phase = {}
    for ph in sorted({x["provenance"]["phase"] for x in E}):
        mx = mix([x for x in E if x["provenance"]["phase"] == ph])
        mx.update(tests(mx))
        by_phase[ph] = mx
    k348_check = {
        "union_105_of_133_expect_0.5408": round(two_sided(105, 133, p_ad), 4),
        "new_34_of_43_expect_0.8575": round(two_sided(34, 43, p_ad), 4),
        "phaseF_zero_of_38_expect_1.62e-24": "%.3g" % ((1 - p_ad) ** 38),
    }

    move_len = {}
    for scope_name, pool in (("all_phases", E), ("A_to_E_only", AE_entries)):
        move_len[scope_name] = {k: med([len(words(x["adversarial_move"])) for x in pool if x["class"] == k]) for k in "abd"}

    ovs = sorted(r["answered_by_max_overlap"] for r in rows)
    a_readings = {
        "n": len(rows),
        "anchor_found_in_locus": sum(r["anchor_found_in_locus"] for r in rows),
        "by_phase": dict(collections.Counter(r["phase"] for r in rows)),
        "authored_pre_K346_ruling_A_to_E": sum(r["phase"] in AE_PHASES for r in rows),
        "authored_under_K346_ruling_F_G_R": sum(r["phase"] not in AE_PHASES for r in rows),
        "by_tier": dict(collections.Counter(r["tier"] for r in rows)),
        "by_locus": dict(collections.Counter(r["target_locus"].split(".")[0] for r in rows)),
        "answering_depth": dict(collections.Counter(a["locus"] for r in rows for a in r["answers"])),
        "answered_by_any_same_node": sum(r["answered_by_any_same_node"] for r in rows),
        "answered_by_cross_node_only": sum(not r["answered_by_any_same_node"] for r in rows),
        "median_move_words": med([r["move_words"] for r in rows]),
        "median_anchor_words": med([r["anchor_words"] for r in rows]),
        "overlap_quartiles": [ovs[int(q * (len(ovs) - 1))] for q in (0.0, 0.25, 0.5, 0.75, 1.0)],
        "entries_with_strength_signal": sum(bool(r["strength_signals"]) for r in rows),
        "entries_with_repair_signal": sum(bool(r["repair_signals"]) for r in rows),
        "lowest_overlap_10": [[r["n"], "%s#%s" % (r["target_id"], r["target_locus"]), r["answered_by_max_overlap"]]
                              for r in sorted(rows, key=lambda r: r["answered_by_max_overlap"])[:10]],
    }

    out = {
        "artifact": OUT_STEM + ".json",
        "state": "UNRULED. Instrument readings for R1; no entry's class, routing or shippability changes here. "
                 "Josiah + library seat rule R1; record rulings forward in the `ruling` slots, never by editing readings.",
        "generated": datetime.date.today().isoformat() + " (America/Phoenix; filename as commissioned)",
        "seat": "Code seat, session 2 (2026-09-18 kickoff step 6)",
        "R1_verbatim": {
            "canon_L3917": "OPEN -- Josiah + library seat. Strongest-vs-repairable. SCOPE CORRECTED at K350: blocks (a) only.",
            "canon_L4067": "whether a continuation was authored at full force or at the most repairable reading of our text is R1, still open, so a card saying WE ANSWER THIS would claim more than the map has established, while a card saying THIS LINE TERMINATES HERE would not.",
            "canon_L3449_K346_criterion": "STRONGEST. An entry names the strongest continuation a maximally competent hostile interlocutor deploys against our text as written, per design section 0. The most-repairable-defect reading is REJECTED.",
            "canon_L3428_K345_finding": "the entry taken was consistently the REPAIRABLE-DEFECT move (a clause with a fixable error, routable as a (b) regen candidate) rather than the STRONGEST-ATTACK move the design's section 0 contract actually asks for.",
            "design_v0_5_s10_4_rule": "Strongest means strongest against the text as a reader meets it -- the whole locus, including everything it inherits from its node -- never strongest against the locus's distinctive content.",
            "R2_canon_L3918": "OPEN -- Josiah + library seat. May a (b) be reader-facing, and under what label.",
        },
        "inputs": {"map": os.path.basename(MAP), "map_md5": md5_bytes(map_raw), "map_bytes": len(map_raw),
                   "corpus": os.path.basename(CORPUS), "corpus_md5": md5_bytes(corpus_raw)},
        "method": {
            "base_rate": {"source": "frozen v1_0 phases A-E (controls_phaseF.py / measure_k348_v0_1.py)",
                          "counts": AE_V1_0, "n": base_n, "p_a_or_d": round(p_ad, 4), "p_a": round(p_a, 4), "p_b": round(p_b, 4)},
            "v1_3_A_to_E": {"counts": ae13["counts"], "n": ae13["n"], "p_a_or_d": round(p_ad_13, 4),
                            "why_different": "v1_3 supersedes three Phase E (b) entries whose anchors the v4.1.0 cut destroyed (map.meta.supersedes)."},
            "binomial": "K348 exact two-sided: sum of pmf mass <= pmf(observed)",
            "permutation": "class labels shuffled across entries, sorted pool, seed %d, N=%d (ccclxvii)" % (SEED, N_PERM),
            "overlap": "fraction of the move's content words (stopword-filtered, crude de-pluralised) present in the answering locus text; a lexical proxy, NOT a judgement of whether the locus answers the strongest form",
            "implementation_check_vs_K348": k348_check,
        },
        "a_set_readings": a_readings,
        "move_words_median_by_class": move_len,
        "per_tier": per_tier,
        "tier_heterogeneity_permutation": {"all_phases": perm_all, "A_to_E_only": perm_ae},
        "by_phase": by_phase,
        "entries": rows,
    }
    jpath = os.path.join(HERE, OUT_STEM + ".json")
    with open(jpath, "wb") as f:
        f.write((json.dumps(out, indent=2, ensure_ascii=True) + "\n").encode("utf-8"))

    # ------------------------------------------------------------------ markdown
    L = []
    w = L.append
    w("# R1 evidence -- the (a) surface, laid out for ruling")
    w("")
    w("**UNRULED.** Instrument readings only. Nothing here changes an entry's class, routing or shippability. "
      "R1 is Josiah's and the library seat's; this file exists so that ruling is an hour's reading, not a fifth deferral. "
      "Corrections go forward: record rulings in the JSON `ruling` slots, never by editing a reading.")
    w("")
    w("Generated %s by the Code seat (session 2). Builder: `adversarial_map_staging/r1/measure_r1_v0_1.py`. "
      "Inputs: `%s` (md5 `%s`, %d B) over corpus `%s` (md5 `%s`)."
      % (out["generated"], out["inputs"]["map"], out["inputs"]["map_md5"], out["inputs"]["map_bytes"],
         out["inputs"]["corpus"], out["inputs"]["corpus_md5"]))
    w("")
    w("## 0. What R1 is, verbatim")
    w("")
    for k, v in out["R1_verbatim"].items():
        w("- `%s`: %s" % (k, v))
    w("")
    w("**The question each entry puts to the ruler:** is the move the strongest continuation against the locus *as a reader meets it* "
      "(design v0_5 s10.4), and does the answering locus answer *that* -- or a more repairable reading? "
      "If yes for an entry, a card over it may say WE ANSWER THIS. If no, the card overclaims (canon L4067). "
      "R1 is scoped to (a) only (K350); (d) ships under a terminus label regardless.")
    w("")
    w("## 1. Readings over the whole (a) set (n=%d)" % len(rows))
    w("")
    ar = a_readings
    w("| reading | value |")
    w("|---|---|")
    w("| anchors found verbatim in their locus | %d / %d |" % (ar["anchor_found_in_locus"], ar["n"]))
    w("| by phase | %s |" % json.dumps(ar["by_phase"]))
    w("| authored BEFORE the K346 STRONGEST ruling (phases A-E) / under it (F, G, R) | %d / %d |" % (ar["authored_pre_K346_ruling_A_to_E"], ar["authored_under_K346_ruling_F_G_R"]))
    w("| by tier | %s |" % json.dumps(ar["by_tier"]))
    w("| by target locus | %s |" % json.dumps(ar["by_locus"]))
    w("| answering-locus depth (all answered_by refs) | %s |" % json.dumps(ar["answering_depth"]))
    w("| answered at least partly by the same node / cross-node only | %d / %d |" % (ar["answered_by_any_same_node"], ar["answered_by_cross_node_only"]))
    w("| median move words / median anchor words | %s / %s |" % (ar["median_move_words"], ar["median_anchor_words"]))
    w("| move-to-answer lexical overlap: min / Q1 / median / Q3 / max | %s |" % " / ".join("%.2f" % q for q in ar["overlap_quartiles"]))
    w("| entries whose move or grounds carry a strength signal / a repair signal | %d / %d |" % (ar["entries_with_strength_signal"], ar["entries_with_repair_signal"]))
    w("| median move words by class, all phases (K346 on v1_0: d 119 > b 103 > a 51) | a %s, b %s, d %s |" % (move_len["all_phases"]["a"], move_len["all_phases"]["b"], move_len["all_phases"]["d"]))
    w("| median move words by class, A-E only | a %s, b %s, d %s |" % (move_len["A_to_E_only"]["a"], move_len["A_to_E_only"]["b"], move_len["A_to_E_only"]["d"]))
    w("")
    w("Ten (a) entries with the lowest move-to-answer overlap (a place to start reading, not a verdict): "
      + ", ".join("#%d %s (%.2f)" % tuple(t) for t in ar["lowest_overlap_10"]))
    w("")
    w("## 2. Per-tier class mix vs the A-E base rate (K346 method)")
    w("")
    w("Base rate: frozen v1_0 phases A-E %s, n=%d, P(a or d)=%.4f, P(a)=%.4f, P(b)=%.4f. v1_3's own A-E is %s, n=%d, P(a or d)=%.4f (three Phase E (b) superseded by Phase R). "
      "p-values are K348's exact two-sided binomial. Implementation check against K348's published numbers: %s."
      % (json.dumps(AE_V1_0), base_n, p_ad, p_a, p_b, json.dumps(ae13["counts"]), ae13["n"], p_ad_13, json.dumps(k348_check)))
    w("")
    for scope_name in ("all_phases", "A_to_E_only"):
        w("### 2.%s %s" % ("1" if scope_name == "all_phases" else "2", scope_name.replace("_", " ")))
        w("")
        w("| tier | n | a | b | c | d | a-share | b-share | d-share | P(a or d) | p vs v1_0 base | p vs v1_3 A-E | p(a) | p(b) | (a) entries | (a) med. move w | (a) med. anchor w | (a) same-node | (a) med. overlap | (a) answering depth |")
        w("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
        for t in ("T1", "T2", "T3", "T4", "T5"):
            mx = per_tier[scope_name][t]
            cn = mx["counts"]
            w("| %s | %d | %d | %d | %d | %d | %.3f | %.3f | %.3f | %.3f | %.4f | %.4f | %.4f | %.4f | %d | %s | %s | %s | %s | %s |"
              % (t, mx["n"], cn["a"], cn["b"], cn["c"], cn["d"], mx["a_share"], mx["b_share"], mx["d_share"],
                 mx["a_or_d"] / mx["n"], mx["p_a_or_d_vs_v1_0_base"], mx["p_a_or_d_vs_v1_3_AE"], mx["p_a_vs_base"], mx["p_b_vs_base"],
                 mx["a_entries"], mx.get("a_median_move_words", "-"), mx.get("a_median_anchor_words", "-"),
                 mx.get("a_same_node_share", "-"), mx.get("a_median_max_overlap", "-"), json.dumps(mx.get("a_answering_depth", {}))))
        pm = out["tier_heterogeneity_permutation"][scope_name]
        w("")
        w("Tier heterogeneity of a-share, permutation null (%s, N=%d, seed %d): observed %.4f, **p = %.4f**."
          % (pm["statistic"], pm["N"], pm["seed"], pm["observed"], pm["p"]))
        w("")
    w("### 2.3 By phase (the K348 comparison, re-run on v1_3)")
    w("")
    w("| phase | n | a | b | c | d | P(a or d) | p vs v1_0 base |")
    w("|---|---|---|---|---|---|---|---|")
    for ph, mx in by_phase.items():
        cn = mx["counts"]
        w("| %s | %d | %d | %d | %d | %d | %.3f | %.4f |" % (ph, mx["n"], cn["a"], cn["b"], cn["c"], cn["d"], mx["a_or_d"] / mx["n"], mx["p_a_or_d_vs_v1_0_base"]))
    w("")
    w("## 3. The 69 (a) entries")
    w("")
    w("Per entry: the move and anchor verbatim; the answering locus; the claim a strength-label card would make; the author's grounds verbatim; "
      "and readings. `overlap` is the share of the move's content words present in the answering locus -- a lexical proxy for engagement, not a judgement. "
      "`top sentences` are the two answering-locus sentences sharing the most content words with the move, so the ruler sees what the locus actually says at the point of contact.")
    w("")
    for r in rows:
        w("---")
        w("")
        w("### #%d  `%s#%s`  --  %s, %s, phase %s (%s, %s)" % (r["n"], r["target_id"], r["target_locus"], r["tier"], r["category"], r["phase"], r["seat"], r["date"]))
        w("")
        w("**MOVE (verbatim):** %s" % r["adversarial_move"])
        w("")
        w("**ANCHOR (verbatim):** \"%s\"  -- %d words; found in locus: %s; locus is %d words." % (r["target_anchor"], r["anchor_words"], "yes" if r["anchor_found_in_locus"] else "**NO**", r["locus_words"]))
        w("")
        w("**ANSWERED BY:** %s" % ", ".join("`%s`%s" % (a["ref"], "" if a["same_node"] else " (cross-node)") for a in r["answers"]))
        w("")
        w("**CARD CLAIM (strength label):** %s" % r["card_claim_strength_label"])
        w("")
        w("**GROUNDS (verbatim):** %s" % r["grounds"])
        w("")
        for a in r["answers"]:
            w("- `%s` (%s, %d words) overlap %.2f; shared terms: %s" % (a["ref"], a["locus"], a["locus_words"], a["move_overlap"], ", ".join(a["overlap_terms"]) or "-"))
            for ts in a["top_sentences"]:
                w("  - (%d) \"%s\"" % (ts["overlap_words"], ts["sentence"]))
        w("")
        w("readings: move %d w; strength signals %s; repair signals %s." % (r["move_words"], r["strength_signals"] or "-", r["repair_signals"] or "-"))
        w("")
        w("**R1 asks:** %s  **Ruling:** _(open)_" % r["R1_question"])
        w("")
    mpath = os.path.join(HERE, OUT_STEM + ".md")
    with open(mpath, "wb") as f:
        f.write(("\n".join(L) + "\n").encode("utf-8"))
    print("wrote", os.path.relpath(jpath, ROOT), md5_bytes(open(jpath, "rb").read()), os.path.getsize(jpath), "B")
    print("wrote", os.path.relpath(mpath, ROOT), md5_bytes(open(mpath, "rb").read()), os.path.getsize(mpath), "B")
    print("k348 check:", k348_check)
    print("a-set:", {k: v for k, v in a_readings.items() if k != "lowest_overlap_10"})
    print("tier perm:", out["tier_heterogeneity_permutation"])
    print("move medians:", move_len)


if __name__ == "__main__":
    main()

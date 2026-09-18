#!/usr/bin/env python3
"""K349 Phase G measurement. Repo-relative; imports the validator, never reimplements it.

Emits measure_k349_v0_1.json. Every constant any K349 document quotes is bound here.
Deterministic: no set iteration feeds any ordered output (ccclxvii)."""
import json, os, sys, importlib.util, collections

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

def load_validator(path):
    spec = importlib.util.spec_from_file_location("advval", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def read_json(p):
    with open(p, "rb") as f:
        return json.loads(f.read().decode("utf-8"))

def main():
    vpath = os.path.join(HERE, "adv_map_validator_v0_5.py")
    V = load_validator(vpath)
    corpus = read_json(os.path.join(REPO, "efilist_argument_library_v4_0_0.json"))
    asm = read_json(os.path.join(HERE, "adversarial_map_v1_1.json"))
    nodes = corpus["objections"]
    by = {o["id"]: o for o in nodes}

    # --- the three out-of-enum top-level fields, measured not recalled -------------
    field_counts = collections.Counter()
    for o in nodes:
        for k in ("note", "confidence", "objectionSubforms"):
            if k in o:
                field_counts[k] += 1

    note_nodes = sorted(o["id"] for o in nodes if "note" in o)
    note_words = {i: len(by[i]["note"].split()) for i in note_nodes}

    # --- REACHABILITY. combined.html emits the [NOTE] button INSIDE
    #     `if (conf !== 'full')`, and toggleNote has exactly one caller, so a note on a
    #     node graded full (or ungraded, since `obj.confidence || 'full'`) has its div
    #     emitted at display:none with nothing able to reveal it.
    reach, unreach = [], []
    for i in note_nodes:
        conf = by[i].get("confidence") or "full"
        (unreach if conf == "full" else reach).append(
            {"id": i, "confidence": by[i].get("confidence"), "effective": conf,
             "words": note_words[i]})
    w_reach = sum(e["words"] for e in reach)
    w_unreach = sum(e["words"] for e in unreach)

    conf_dist = collections.Counter(o["confidence"] for o in nodes if "confidence" in o)
    # `full` renders identically to absent: the badge block is skipped for both.
    badge_emitting = sorted(o["id"] for o in nodes
                            if (o.get("confidence") or "full") != "full")
    graded_full = sorted(o["id"] for o in nodes if o.get("confidence") == "full")
    ungraded = sorted(o["id"] for o in nodes if "confidence" not in o)

    # --- do note-bearing nodes already carry bedrock? ------------------------------
    cls_by_node = collections.defaultdict(list)
    for e in asm["entries"]:
        cls_by_node[e["target_id"]].append(e["class"])
    def has(nid, k):
        return k in cls_by_node.get(nid, [])
    note_with_d = sorted(i for i in note_nodes if has(i, "d"))
    corpus_with_d = sorted(i for i in by if has(i, "d"))
    p_note = len(note_with_d) / len(note_nodes)
    p_corpus = len(corpus_with_d) / len(by)

    # --- entry-cap headroom on the note nodes (the ruling the prompt flagged) ------
    per_node = collections.Counter(e["target_id"] for e in asm["entries"])
    headroom = []
    for i in note_nodes:
        nvar = len(V.node_variant_slots(by[i]))
        bound = 3 + 3 * nvar
        headroom.append({"id": i, "entries": per_node[i], "variant_loci": nvar,
                         "bound": bound, "headroom": bound - per_node[i]})
    min_headroom = min(h["headroom"] for h in headroom)

    # --- class base rates, for the ccclxviii gate ---------------------------------
    AE = ("A", "B1", "B2", "C", "D", "E")
    ae = [e for e in asm["entries"] if (e.get("provenance") or {}).get("phase") in AE]
    ae_cls = collections.Counter(e["class"] for e in ae)
    ae_ad = sum(ae_cls[k] for k in ("a", "d"))

    out = {
        "artifact": "measure_k349_v0_1.json",
        "generated_by": "adversarial_map_staging/measure_k349.py",
        "session": "K349",
        "date_operator_local": "2026-09-17",
        "inputs": {
            "corpus_md5": V.md5_bytes(open(os.path.join(REPO, "efilist_argument_library_v4_0_0.json"), "rb").read()),
            "objections_digest": V.objections_digest(corpus),
            "assembly_v1_1_md5": V.md5_bytes(open(os.path.join(HERE, "adversarial_map_v1_1.json"), "rb").read()),
            "validator_v0_5_md5": V.md5_bytes(open(vpath, "rb").read()),
        },
        "out_of_enum_fields": dict(field_counts),
        "note_layer": {
            "nodes": len(note_nodes), "words_total": sum(note_words.values()),
            "per_node_words": note_words,
            "reachable": reach, "unreachable": unreach,
            "reachable_n": len(reach), "unreachable_n": len(unreach),
            "words_reachable": w_reach, "words_unreachable": w_unreach,
            "pct_words_unreachable": round(100.0 * w_unreach / sum(note_words.values()), 1),
        },
        "confidence_layer": {
            "nodes_with_key": sum(field_counts["confidence"] for _ in [0]),
            "distribution": dict(conf_dist),
            "badge_emitting_nodes": badge_emitting,
            "badge_emitting_n": len(badge_emitting),
            "graded_full_n": len(graded_full),
            "ungraded_n": len(ungraded),
            "full_indistinguishable_from_ungraded": True,
        },
        "bedrock_enrichment": {
            "note_nodes_with_a_d_entry": note_with_d,
            "note_nodes_with_d_n": len(note_with_d),
            "note_nodes_n": len(note_nodes),
            "corpus_nodes_with_d_n": len(corpus_with_d),
            "corpus_nodes_n": len(by),
            "p_note": round(p_note, 4), "p_corpus": round(p_corpus, 4),
        },
        "entry_cap_headroom": {"per_node": headroom, "min_headroom": min_headroom},
        "class_base_rate_A_to_E": {
            "counts": dict(ae_cls), "n": len(ae),
            "a_or_d": ae_ad, "rate": round(ae_ad / len(ae), 4),
            "d_rate": round(ae_cls["d"] / len(ae), 4),
        },
    }
    dest = os.path.join(HERE, "measure_k349_v0_1.json")
    if len(sys.argv) > 1:
        dest = sys.argv[1]
    with open(dest, "wb") as f:
        f.write((json.dumps(out, indent=2, sort_keys=False, ensure_ascii=True) + "\n").encode("utf-8"))
    print("wrote", dest, V.md5_bytes(open(dest, "rb").read()))

if __name__ == "__main__":
    main()

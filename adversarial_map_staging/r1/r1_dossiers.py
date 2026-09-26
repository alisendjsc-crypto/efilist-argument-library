#!/usr/bin/env python3
"""r1_dossiers.py -- the R1 reading instrument (L3, 2026-09-25).

Writes one markdown dossier per evidence entry, holding everything a judge needs to rule an (a)
under R1_standard_ruling_L2, drawn from the committed files and nothing else:

  - the node frame (trigger, diagnosis, confidence);
  - the entry: anchor, move, grounds, routing;
  - the target locus in full, and every answering locus in full;
  - every map entry on the target node (all slots, all classes) and on each answering node, each
    (a) carrying its R1 ruling if one is recorded;
  - every other (a) that spends the same answering locus, with its ruling (calibration);
  - the canon records that touch those loci: the register's bedrocks with a tributary on any node
    of the route, canon's residual record for each, K350 when consent-incoherent is on the route,
    K224/K338 when bradley-no-subject or non-identity-problem is, the transhumanist ban when
    transhumanist-objection is, and HR-14 when the route enters its cluster;
  - the mechanical collision screen (a reading list, never a verdict).

L2's builder lived in scratch, so its method could not be reproduced from the repo; this is that
instrument, committed. It judges nothing and drafts nothing (K258).

  python3 r1_dossiers.py --out <dir>                 # every entry not yet ruled
  python3 r1_dossiers.py --out <dir> --n 21 22 26    # named entries
  python3 r1_dossiers.py --out <dir> --all           # all 69

Repo-relative. Reads the evidence file, the map and corpus it names (md5-checked against the
evidence), the register canon pins, the one canon file, and R1_rulings.json. Writes only under
--out. Deterministic: every listing is sorted or in file order.
"""
import argparse, glob, hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
EVID = "adversarial_map_staging/r1/R1_evidence_2026-09-19.json"
RULINGS = "adversarial_map_staging/r1/R1_rulings.json"

# HR-14's cluster: the register's tributary nodes, plus violence-as-reductio, whose routes
# K347 found end at HR-14 (canon adversarial_map.phaseF_proper_K347).
HR14_EXTRA = ("violence-as-reductio",)


def md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


def load(rel):
    return json.load(open(os.path.join(REPO, rel), encoding="utf-8"))


def split_ref(ref):
    node, _, locus = ref.partition("#")
    return node, locus


def locus_text(obj, locus):
    """The reader-facing text at a locus, or None if the locus does not exist."""
    if locus in ("short", "medium", "long"):
        return obj["responses"].get(locus)
    if locus.startswith("archetypeVariants."):
        return obj["responses"].get("archetypeVariants", {}).get(locus.split(".", 1)[1])
    if locus in ("note", "diagnosis", "trigger", "confidence"):
        return obj.get(locus)
    return None


def canon_strings(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from canon_strings(v, path + "." + k if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from canon_strings(v, "%s[%d]" % (path, i))
    elif isinstance(o, str):
        yield path, o


def block(text):
    return "\n".join("> " + ln if ln else ">" for ln in str(text).split("\n"))


class World:
    def __init__(self):
        self.ev = load(EVID)
        inp = self.ev["inputs"]
        self.map_rel, self.corpus_rel = inp["map"], inp["corpus"]
        if not os.path.exists(os.path.join(REPO, self.map_rel)):
            self.map_rel = os.path.join("adversarial_map_staging", os.path.basename(inp["map"]))
        for rel, want in ((self.map_rel, inp["map_md5"]), (self.corpus_rel, inp["corpus_md5"])):
            got = md5(os.path.join(REPO, rel))
            if got != want:
                sys.exit("REFUSED: %s is %s, the evidence was measured at %s" % (rel, got, want))
        self.map = load(self.map_rel)
        self.corpus = {o["id"]: o for o in load(self.corpus_rel)["objections"]}
        canons = sorted(glob.glob(os.path.join(REPO, "project_canon_v38_*.json")))
        if len(canons) != 1:
            sys.exit("REFUSED: expected exactly one project_canon_v38_*.json, found %d" % len(canons))
        self.canon_rel = os.path.basename(canons[0])
        self.canon = json.load(open(canons[0], encoding="utf-8"))
        am = self.canon["adversarial_map"]
        pins = sorted(k for k in am if k.startswith("honest_residuals_register_pin_v0_"))
        pin = am[pins[-1]]
        self.reg_rel = os.path.join("adversarial_map_staging", pin["artifact"])
        if md5(os.path.join(REPO, self.reg_rel)) != pin["md5"]:
            sys.exit("REFUSED: %s does not match its canon pin %s" % (self.reg_rel, pin["md5"]))
        self.reg = load(self.reg_rel)
        self.rulings = load(RULINGS)["rows"]
        self.ruling_by_n = {}
        for r in self.rulings:                       # a later row supersedes an earlier one
            self.ruling_by_n[r["n"]] = r
        self.ev_by_move = {(e["target_id"], e["target_locus"], e["adversarial_move"]): e
                           for e in self.ev["entries"]}
        self.hr14_nodes = set(HR14_EXTRA)
        for b in self.reg["bedrocks"]:
            if b["bedrock_id"] == "HR-14":
                for f in b["facets"]:
                    for t in f["tributaries"]:
                        self.hr14_nodes.add(t["node"])
        self.canon_str = list(canon_strings(self.canon))

    # ---------------------------------------------------------------- helpers
    def entries_on(self, node):
        return [x for x in self.map["entries"] if x["target_id"] == node]

    def ev_of(self, x):
        return self.ev_by_move.get((x["target_id"], x["target_locus"], x["adversarial_move"]))

    def fmt_entry(self, x, this_n=None):
        e = self.ev_of(x)
        n = e["n"] if e else None
        pv = x["provenance"]
        head = "**(%s)** at `%s#%s` · Phase %s · %s · %s" % (
            x["class"], x["target_id"], x["target_locus"], pv.get("phase"), pv.get("seat"), pv.get("date"))
        if n is not None:
            head += " · evidence #%d" % n
        if n is not None and n == this_n:
            head += " · **THIS ENTRY**"
        out = ["- " + head,
               "  - anchor: \"%s\"" % x["target_anchor"],
               "  - move: %s" % x["adversarial_move"],
               "  - grounds: %s" % x["grounds"],
               "  - routing: `%s`" % json.dumps(x["routing"], ensure_ascii=False, sort_keys=True)]
        if x["class"] == "a" and n is not None and n != this_n:
            r = self.ruling_by_n.get(n)
            if r:
                out.append("  - **R1 %s (%s)**: %s" % (r["verdict"], r["row"], r["reason"]))
                if r.get("stronger_continuation"):
                    out.append("    - stronger line: %s" % r["stronger_continuation"])
            else:
                out.append("  - R1: not yet ruled")
        return "\n".join(out)

    def route_nodes(self, e):
        nodes = [e["target_id"]]
        for ref in e["answered_by"]:
            nd, _ = split_ref(ref)
            if nd not in nodes:
                nodes.append(nd)
        return nodes

    # ---------------------------------------------------------------- dossier
    def dossier(self, e):
        n, node, locus = e["n"], e["target_id"], e["target_locus"]
        obj = self.corpus[node]
        L = []
        L.append("# R1 dossier #%d: `%s#%s`" % (n, node, locus))
        L.append("")
        L.append("Phase %s · %s · %s · %s · %s" % (e["phase"], e["tier"], e["category"], e["seat"], e["date"]))
        r = self.ruling_by_n.get(n)
        L.append("")
        L.append("R1 status: **%s**" % ("%s (%s)" % (r["verdict"], r["row"]) if r else "not yet ruled"))
        L.append("")
        L.append("Sources: evidence `%s`, map `%s` `%s`, corpus `%s`, canon `%s`, register `%s`."
                 % (md5(os.path.join(REPO, EVID))[:8], os.path.basename(self.map_rel),
                    md5(os.path.join(REPO, self.map_rel))[:8], md5(os.path.join(REPO, self.corpus_rel))[:8],
                    self.canon_rel, os.path.basename(self.reg_rel)))
        L += ["", "## R1 question", "", e["R1_question"], ""]

        L += ["## Node frame", "", "- trigger: %s" % obj["trigger"], "- diagnosis:", "", block(obj["diagnosis"]), ""]
        if obj.get("confidence"):
            L += ["- confidence: `%s`" % obj["confidence"], ""]

        L += ["## The entry", "",
              "- anchor: \"%s\" (found in locus: %s)" % (e["target_anchor"], e["anchor_found_in_locus"]),
              "- move (%d words):" % e["move_words"], "", block(e["adversarial_move"]), "",
              "- grounds:", "", block(e["grounds"]), "",
              "- answered_by: %s" % ", ".join("`%s`" % a for a in e["answered_by"]), ""]

        L += ["## Target locus in full: `%s#%s`" % (node, locus), ""]
        t = locus_text(obj, locus)
        L += [block(t) if t else "> (LOCUS NOT FOUND)", ""]

        for ref in e["answered_by"]:
            nd, lc = split_ref(ref)
            L += ["## Answering locus in full: `%s`" % ref, ""]
            if nd != node:
                L += ["Node frame: trigger: %s" % self.corpus[nd]["trigger"], ""]
            t = locus_text(self.corpus[nd], lc)
            L += [block(t) if t else "> (LOCUS NOT FOUND)", ""]

        L += ["## Map entries on the target node `%s` (every slot, every class)" % node, ""]
        for x in self.entries_on(node):
            L += [self.fmt_entry(x, this_n=n)]
        L.append("")
        for nd in self.route_nodes(e)[1:]:
            L += ["## Map entries on the answering node `%s` (every slot, every class)" % nd, ""]
            xs = self.entries_on(nd)
            L += [self.fmt_entry(x, this_n=n) for x in xs] if xs else ["- (none)"]
            L.append("")

        L += ["## Other (a)s that spend the same answering locus", ""]
        any_other = False
        for ref in e["answered_by"]:
            others = [o for o in self.ev["entries"] if ref in o["answered_by"] and o["n"] != n]
            L.append("- `%s`: %d other (a)s" % (ref, len(others)))
            for o in others:
                rr = self.ruling_by_n.get(o["n"])
                L.append("  - #%d `%s#%s` [%s]: %s" % (
                    o["n"], o["target_id"], o["target_locus"], o["phase"],
                    ("**%s** (%s) %s" % (rr["verdict"], rr["row"], rr["reason"])) if rr else "not yet ruled"))
                any_other = True
        if not any_other:
            L.append("- (none)")
        L.append("")

        L += ["## Canon records on the route", ""]
        nodes = self.route_nodes(e)
        hr_ids = []
        for b in self.reg["bedrocks"]:
            tribs = [(f["facet_id"], t) for f in b["facets"] for t in f["tributaries"] if t["node"] in nodes]
            if not tribs:
                continue
            hr_ids.append(b["bedrock_id"])
            L.append("### %s %s (register `%s`)" % (b["bedrock_id"], b["name"], os.path.basename(self.reg_rel)))
            L.append("")
            L.append("- gloss: %s" % b["gloss"])
            for fid, t in tribs:
                L.append("- tributary `%s#%s` [%s], facet `%s`: anchor \"%s\"; terminus: %s" % (
                    t["node"], t["locus"], t["phase"], fid, t["anchor"], t.get("terminus_routing")))
            L.append("")
        hr = self.canon["terminal_stability_marker"]["honest_residuals"]
        for k in sorted(hr):
            v = hr[k]
            if isinstance(v, dict) and v.get("register_id") in hr_ids:
                L.append("### canon `terminal_stability_marker.honest_residuals.%s` (%s)" % (k, v["register_id"]))
                L.append("")
                for kk in ("claim", "why_it_is_bedrock", "the_bar", "owed"):
                    if kk in v:
                        L.append("- %s: %s" % (kk, json.dumps(v[kk], ensure_ascii=False)
                                                if not isinstance(v[kk], str) else v[kk]))
                L.append("")
        am = self.canon["adversarial_map"]
        answering_nodes = nodes[1:]
        if "consent-incoherent" in answering_nodes:
            L += ["### K350: `adversarial_map.routing_constraint_consent_incoherent_K350`", "",
                  "```json", json.dumps(am["routing_constraint_consent_incoherent_K350"], indent=1,
                                        ensure_ascii=False), "```", ""]
        if "bradley-no-subject" in answering_nodes or e["phase"] == "B1":
            L += ["### K224 / K338: `adversarial_map.carry_forward_bar` and `k338_amendments.phase_B1`", "",
                  "- rule: %s" % am["carry_forward_bar"]["rule"],
                  "- adjudication_k334: %s" % am["carry_forward_bar"]["adjudication_k334"],
                  "- k338 phase_B1: %s" % am["k338_amendments"]["phase_B1"], ""]
        if "non-identity-problem" in answering_nodes:
            L += ["### K338: non-identity-problem was reclassified (a) -> (d) at HR-05", "",
                  "- %s" % am["k338_amendments"]["phase_B1"], ""]
        if "transhumanist-objection" in answering_nodes:
            L += ["### The transhumanist ban", "",
                  "- K350 joins: %s" % am["routing_constraint_consent_incoherent_K350"]["joins"],
                  "- The ban's text lives in the Phase C and D grounds and in the (b) at "
                  "`transhumanist-objection#long` (listed above).", ""]
        if set(nodes) & self.hr14_nodes:
            v = hr["create_vs_destroy_positive_case"]
            L += ["### HR-14 (the route enters its cluster: %s)" % ", ".join(sorted(set(nodes) & self.hr14_nodes)), "",
                  "- claim: %s" % v["claim"], "- why_it_is_bedrock: %s" % v["why_it_is_bedrock"],
                  "- owed: %s" % (v["owed"] if isinstance(v["owed"], str) else json.dumps(v["owed"], ensure_ascii=False)),
                  "- K347: %s" % json.dumps(am["phaseF_proper_K347"]["findings"]
                                            ["new_bedrock_is_an_artifact_of_the_routing_graph"], ensure_ascii=False), ""]
        refs = ["%s#%s" % (node, locus)] + list(e["answered_by"])
        L += ["### Canon paths naming these exact loci", ""]
        hit = False
        for ref in refs:
            ps = [p for p, s in self.canon_str if ref in s]
            for p in ps:
                L.append("- `%s` names `%s`" % (p, ref))
                hit = True
        if not hit:
            L.append("- (none)")
        L.append("")

        L += ["## Mechanical collision screen (a reading list, not a verdict)", ""]
        for ref in e["answered_by"]:
            nd, lc = split_ref(ref)
            flags = [x for x in self.entries_on(nd) if x["target_locus"] == lc and x["class"] in ("b", "d")]
            L.append("- answering locus `%s`: %s" % (ref, ", ".join(
                "(%s) Phase %s" % (x["class"], x["provenance"]["phase"]) for x in flags) or "no (b)/(d)"))
        for nd in answering_nodes:
            flags = [x for x in self.entries_on(nd) if x["class"] in ("b", "d")]
            L.append("- answering node `%s`, all slots: %s" % (nd, ", ".join(
                "(%s)@%s" % (x["class"], x["target_locus"]) for x in flags) or "no (b)/(d)"))
        flags = [x for x in self.entries_on(node) if x["class"] in ("b", "d")]
        L.append("- target node `%s`, all slots: %s" % (node, ", ".join(
            "(%s)@%s" % (x["class"], x["target_locus"]) for x in flags) or "no (b)/(d)"))
        L.append("- HR-14 cluster on the route: %s" % (", ".join(sorted(set(nodes) & self.hr14_nodes)) or "no"))
        L.append("")
        return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", required=True, help="directory for the dossiers (created if absent)")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--n", type=int, nargs="+", help="evidence numbers")
    g.add_argument("--all", action="store_true", help="all 69 entries")
    a = ap.parse_args()
    w = World()
    by_n = {e["n"]: e for e in w.ev["entries"]}
    if a.n:
        bad = [n for n in a.n if n not in by_n]
        if bad:
            sys.exit("REFUSED: no evidence entry %s" % bad)
        ns = a.n
    elif a.all:
        ns = sorted(by_n)
    else:
        ns = sorted(n for n in by_n if n not in w.ruling_by_n)
    os.makedirs(a.out, exist_ok=True)
    for n in ns:
        e = by_n[n]
        name = "R1_dossier_%02d_%s_%s.md" % (n, e["target_id"], e["target_locus"].replace(".", "-"))
        with open(os.path.join(a.out, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(w.dossier(e))
        print("wrote %s" % name)
    print("%d dossier(s) -> %s" % (len(ns), a.out))


if __name__ == "__main__":
    main()

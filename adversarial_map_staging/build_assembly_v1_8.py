#!/usr/bin/env python3
"""Build adversarial_map_v1_8.json -- v1_7 plus L7's redrafts of gate2's 18 AMENDs (L7, 2026-09-26, R0243).

  i.   It reads adversarial_map_v1_7.json (gate2's judgment pins it) and applies the rows of r1/L7_successor_drafts.json
       that supersede a judged row. v1_7 stays byte-identical, as v1_4 did under L4b's redrafts.
  ii.  AUTHORITY IS CHECKED, NOT ASSUMED. Each superseding row names the row it replaces and the judgment row it
       answers; that judgment row must read AMEND on the row replaced, in gate2's record at the md5 pinned here.
  iii. CONFINEMENT. A redraft may change only what its AMEND names: the move (U-063's sixteen, and SM-08), or for SM-45
       the move, the grounds and the routing (a terminus that moves, copied from a registered (d) by locus AND anchor,
       and filed by register v0_8 under the HR-id and facet claimed). Every other field of the row must equal the row it
       replaces; every other entry of v1_7 carries byte for byte.
  iv.  QUOTES: declared quotations verbatim at their source (corpus at 7b6e65e5; v1_6 entries), and no undeclared
       double-quoted span in a changed field. The validator v0_7 runs in-process under --assembly against the v4.1.5
       corpus; the build refuses on any violation or advisory.

Repo-relative. --out <dir> to emit elsewhere. Deterministic.
"""
import copy, hashlib, json, os, re, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("K348_REPO") or os.path.dirname(_HERE)
STAGE = os.path.join(REPO, "adversarial_map_staging")
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else REPO
OUT = os.path.join(OUT_DIR, "adversarial_map_staging", "adversarial_map_v1_8.json")

sys.path.insert(0, STAGE)
sys.path.insert(0, os.path.join(STAGE, "r1"))
import adv_map_validator_v0_7 as V   # noqa: E402
import pinned                        # noqa: E402

S, R = "adversarial_map_staging", "adversarial_map_staging/r1"
PIN = {
    "base": (S + "/adversarial_map_v1_7.json", "db40b45693eff1297b3f3152c6295c15"),
    "v1_6": (S + "/adversarial_map_v1_6.json", "7a69bc9fd197047c3cf7cecdb37a44ed"),
    "drafts": (R + "/L7_successor_drafts.json", "370e7d02457314e10d6211f95d5ae8c0"),
    "judgment": (R + "/L7_successor_drafts_judgments.json", "bd3b4e89f25e7f874f5aa553b998fe0d"),
    "register": (S + "/honest_residuals_register_v0_8.json", "8f6d38886b95033600752a5be052bd99"),
}
VALIDATOR_MD5 = "8a74dcc452338f127ec03e078090c2ed"
CORPUS = "efilist_argument_library_v4_0_0.json"
CORPUS_PIN = "7b6e65e531018fecb37baf2a4fedd6d1"
FIELDS = ("class", "target_anchor", "adversarial_move", "grounds", "routing")
ALLOWED = {"SM-45": {"adversarial_move", "grounds", "routing"}}
DEFAULT_ALLOWED = {"adversarial_move"}
BY = "library seat, Code (L7); drafter under K258, judges nothing"
DATE = "2026-09-26"


def md5b(b):
    return hashlib.md5(b).hexdigest()


def strings(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)
    elif isinstance(o, str):
        yield o


def main():
    fail = []
    vraw = open(os.path.join(STAGE, "adv_map_validator_v0_7.py"), "rb").read()
    assert md5b(vraw) == VALIDATOR_MD5, "VALIDATOR GUARD: v0_7 is %s" % md5b(vraw)
    raw = {}
    for k, (rel, m) in PIN.items():
        try:
            raw[k] = pinned.bytes_at(REPO, rel, m)
        except LookupError as err:
            print("BASE GUARD: %s" % err)
            return 1
    base = json.loads(raw["base"].decode("utf-8"))
    v16 = json.loads(raw["v1_6"].decode("utf-8"))
    drafts = json.loads(raw["drafts"].decode("utf-8"))
    judgment = json.loads(raw["judgment"].decode("utf-8"))
    register = json.loads(raw["register"].decode("utf-8"))
    cpath = pinned.path_at(REPO, CORPUS, CORPUS_PIN)
    corpus = json.loads(open(cpath, "rb").read().decode("utf-8"))
    nodes = {o["id"]: o for o in corpus["objections"]}
    if judgment["judged"].get("map_v1_7", {}).get("md5") != PIN["base"][1] or \
            judgment["judged"].get("drafts", {}).get("md5") is None:
        fail.append("the judgment record does not judge v1_7 at %s" % PIN["base"][1])
    rows = drafts["rows"]
    by_id = {r["id"]: r for r in rows}
    verdict = {}
    for j in judgment["rows"]:
        if j.get("row_id"):
            verdict.setdefault(j["row_id"], []).append(j)
    trib = {}
    for b in register["bedrocks"]:
        for f in b["facets"]:
            for t in f["tributaries"]:
                trib[(t["node"], t["locus"], t["anchor"])] = (b["bedrock_id"], f["facet_id"])

    # where each first-round row landed in v1_7: amend rows at their entry index, file rows appended in row order
    first = [r for r in rows if not r.get("supersedes")]
    n16 = len(v16["entries"])
    landed, k = {}, 0
    for r in first:
        if r["kind"] == "amend":
            landed[r["id"]] = r["entry"]["i"]
        elif r["kind"] == "file":
            landed[r["id"]] = n16 + k
            k += 1

    def resolve(r, routing):
        rs = routing.get("residue") if isinstance(routing, dict) else None
        if not rs or rs.get("bedrock_name") != "@from":
            return routing
        bf = r.get("bedrock_from")
        if not bf:
            fail.append("%s: '@from' with no bedrock_from" % r["id"])
            return routing
        node, _, loc = bf["locus"].partition("#")
        src = [y for y in v16["entries"] if y["target_id"] == node and y["target_locus"] == loc
               and y["target_anchor"] == bf["anchor"] and y["class"] == "d"]
        if len(src) != 1:
            fail.append("%s: bedrock_from names %d (d)s in v1_6" % (r["id"], len(src)))
            return routing
        if trib.get((node, loc, bf["anchor"])) != (bf["hr"], bf["facet"]):
            fail.append("%s: register v0_8 does not file bedrock_from under %s/%s" % (r["id"], bf["hr"], bf["facet"]))
        out = copy.deepcopy(routing)
        out["residue"]["bedrock_name"] = src[0]["routing"]["residue"]["bedrock_name"]
        return out

    def pool(src):
        kind, _, rest = src.partition(":")
        node, _, loc = rest.partition("#")
        if kind == "corpus":
            if node not in nodes or not V.locus_valid(nodes[node], loc):
                raise KeyError("no corpus locus %s" % rest)
            return [V.locus_text(nodes[node], loc)]
        if kind == "v1_6":
            xs = [y for y in v16["entries"] if y["target_id"] == node and y["target_locus"] == loc]
            if not xs:
                raise KeyError("no v1_6 entry at %s" % rest)
            return [s for y in xs for s in strings({f: y[f] for f in FIELDS})]
        raise KeyError("unknown source kind %r" % kind)

    entries = [copy.deepcopy(e) for e in base["entries"]]
    changed, record = {}, []
    redrafts = [r for r in rows if r.get("supersedes")]
    seen = set()
    for r in redrafts:
        x = by_id.get(r["supersedes"])
        if x is None or x.get("supersedes") or r["supersedes"] in seen:
            fail.append("%s: supersedes %r, which is not a single first-round row" % (r["id"], r["supersedes"]))
            continue
        seen.add(r["supersedes"])
        js = [j for j in verdict.get(r["supersedes"], []) if j["id"] == r.get("answers")]
        if len(js) != 1 or js[0]["verdict"] != "AMEND":
            fail.append("%s: answers %r, which is not gate2's AMEND on %s" % (r["id"], r.get("answers"), r["supersedes"]))
            continue
        # everything but the named fields equals the row replaced
        a = r.get("set") or r.get("new_entry")
        b = x.get("set") or x.get("new_entry")
        if (r["kind"], r["disposition"], r.get("entry"), r.get("new_entry") is None) != \
                (x["kind"], x["disposition"], x.get("entry"), x.get("new_entry") is None):
            fail.append("%s: its kind, disposition or entry differ from %s" % (r["id"], x["id"]))
            continue
        diff = sorted(f for f in set(a) | set(b) if a.get(f) != b.get(f))
        allowed = ALLOWED.get(x["id"], DEFAULT_ALLOWED)
        if not set(diff) <= allowed or "adversarial_move" not in diff:
            fail.append("%s: changes %s; its AMEND allows %s" % (r["id"], diff, sorted(allowed)))
            continue
        declared = []
        for q in r.get("quotes", []):
            try:
                ok = any(q["quote"] in t for t in pool(q["src"]))
            except KeyError as err:
                fail.append("%s: quote source %s -- %s" % (r["id"], q["src"], err))
                continue
            if not ok:
                fail.append("%s: NOT VERBATIM at %s: %r" % (r["id"], q["src"], q["quote"][:80]))
            declared.append(q["quote"])
        for f in diff:
            for s in strings(a.get(f, "")):
                for span in re.findall(r'"([^"]+)"', s):
                    if span not in declared:
                        fail.append("%s: undeclared quotation in %s: %r" % (r["id"], f, span[:60]))
        i = landed.get(x["id"])
        if i is None:
            fail.append("%s: %s landed nowhere in v1_7" % (r["id"], x["id"]))
            continue
        e = entries[i]
        if e["adversarial_move"] != b["adversarial_move"]:
            fail.append("%s: v1_7 entry %d does not carry %s's move" % (r["id"], i, x["id"]))
            continue
        frm = {f: copy.deepcopy(e[f]) for f in diff}
        for f in diff:
            e[f] = resolve(r, a["routing"]) if f == "routing" else a[f]
        rd = {"at": "L7", "date": DATE, "by": BY, "row": r["id"], "supersedes": x["id"], "answers": r["answers"],
              "fields_changed": diff, "from": frm,
              "base": {"artifact": "adversarial_map_v1_7.json", "md5": PIN["base"][1]}}
        if "routing" in diff and r.get("bedrock_from"):
            rd["bedrock_from"] = r["bedrock_from"]
        e["provenance"] = dict(e["provenance"], redrafted_L7=rd)
        changed[i] = r["id"]
        record.append({"row": r["id"], "supersedes": x["id"], "answers": r["answers"], "i": i,
                       "target": "%s#%s" % (e["target_id"], e["target_locus"]), "fields_changed": diff})
    first_amends = {j["row_id"] for jj in verdict.values() for j in jj if j["verdict"] == "AMEND"}
    if first_amends != seen:
        fail.append("AMENDs without a redraft: %s; redrafts without an AMEND: %s"
                    % (sorted(first_amends - seen), sorted(seen - first_amends)))
    for i, e in enumerate(base["entries"]):
        if i not in changed and entries[i] != e:
            fail.append("entry %d moved without a redraft" % i)
    if fail:
        print("REFUSING TO WRITE -- %d failure(s):" % len(fail))
        for f_ in fail:
            print("  " + f_)
        return 1

    m7 = base["meta"]
    meta = {}
    for k_, v in m7.items():
        meta[k_] = v
        if k_ == "l7_successor":
            meta["l7_redrafts"] = {
                "what": ("gate2's 18 AMENDs on the successor drafts, redrafted as superseding rows: 16 restate a move against "
                         "the v4.1.5 text as a reader meets it (U-063), SM-08 states the hub's condition as it stands, and "
                         "SM-45 presses the information paragraph's diagnosis and runs to HR-02 (gate2's lean)."),
                "judgment": {"file": PIN["judgment"][0], "md5": PIN["judgment"][1],
                             "verdicts": "22 ACCEPT, 11 CONFIRM, 18 AMEND, 0 REJECT"},
                "drafts": {"file": PIN["drafts"][0], "md5": PIN["drafts"][1], "rows": len(rows),
                           "superseding": len(redrafts)},
                "as_written": ("L7's redrafts; a seat that did not draft them judges them (K258), recorded in canon, "
                               "never here."),
                "rows": record}
    meta["artifact"] = "adversarial_map_v1_8.json"
    meta["assembled"] = "2026-09-26, efilist Code seat, L7 (the successor, redrafted on gate2's AMENDs)"
    meta["successor_to"] = dict(m7["successor_to"], artifact="adversarial_map_v1_7.json", md5=PIN["base"][1],
                                bytes=len(raw["base"]),
                                and_before_it="adversarial_map_v1_6.json 7a69bc9fd197047c3cf7cecdb37a44ed, and before it "
                                              + m7["successor_to"]["and_before_it"],
                                why_v1_8="gate2 judged v1_7 (22 ACCEPT, 11 CONFIRM, 18 AMEND); these are the 18 AMENDs, "
                                         "applied; nothing else moves.")
    for k_ in ("why_v1_7", "v1_6_is_not_replaced"):
        meta["successor_to"].pop(k_, None)
    meta["successor_to"]["v1_7_is_not_replaced"] = ("v1_7 stays byte-identical on disk: gate2's judgment of the successor "
                                                    "drafts pins it.")
    meta["siblings"] = dict(m7["siblings"], predecessor="adversarial_map_v1_7.json",
                            register="honest_residuals_register_v0_9.json")
    meta["fences"] = m7["fences"].replace("honest_residuals_register_v0_8.json", "honest_residuals_register_v0_9.json")
    out = (json.dumps({"meta": meta, "entries": entries}, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmp = OUT + ".tmp"
    open(tmp, "wb").write(out)
    lines = []
    passed, viol, adv = V.validate([tmp], cpath, assembly=True, out=lines.append)
    if not passed or viol or adv:
        print("REFUSING TO WRITE -- validator v0_7 --assembly: %d violation(s), %d advisory(ies)" % (len(viol), len(adv)))
        for v in (viol + adv)[:30]:
            print("  " + v)
        os.remove(tmp)
        return 1
    os.replace(tmp, OUT)
    print("WROTE %s  %d B  md5 %s" % (OUT, len(out), md5b(out)))
    print("  redrafted %d entries (%d move only) | validator v0_7 --assembly: %d checks, all PASS"
          % (len(changed), sum(1 for x in record if x["fields_changed"] == ["adversarial_move"]),
             len([l_ for l_ in lines if l_.startswith(("PASS", "FAIL", "WARN"))])))
    return 0


if __name__ == "__main__":
    sys.exit(main())

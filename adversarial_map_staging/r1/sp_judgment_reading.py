#!/usr/bin/env python3
"""sp_judgment_reading.py -- gate2's reading instrument for its judgment of L6's X-032 safety-pass drafts
(gate2, 2026-09-26, R0207).

Every figure SP_drafts_judgments.json states as measured, recomputed from the judged artifacts at the md5s they are
pinned to, never from the working tree:

  exit_patterns   gate2's own X-032 patterns (imported from pq_judgment_reading.py at its pinned bytes), swept over the
                  corpus the drafts pin and over the patched corpus for every row: the six loci before, none after
  dashes          for each row, the em-dash style of the rest of its slot (spaced " — " or unspaced) against the
                  replacement's; a replacement that brings the other style into a slot is flagged
  honest_eval     every locus that still says a drive or programming "prevents" or "distorts" honest evaluation or
                  moral judgment, before and after the patch
  knock_on        #3's two halves in why-not-suicide#long after the patch; #44's anchor; #47's anchor; #56's value base

  python3 sp_judgment_reading.py            # print the record
  python3 sp_judgment_reading.py --emit     # write the record beside this file
  python3 sp_judgment_reading.py --check    # compare with the committed record; exit 1 on any difference

Repo-relative. Writes nothing unless --emit is given. Deterministic.
"""
import json, os, re, sys, types

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import pinned  # noqa: E402

RECORD = "adversarial_map_staging/r1/sp_judgment_reading_v0_1.json"
DRAFTS = ("adversarial_map_staging/r1/SP_drafts_L6.json", "050d240fe08f5ea69b883fb4b199c959")
PATCH = ("tools/pin_patch_l6.py", "4686278407b961c3aefa00ac1b08c11a")
FIRST_INSTRUMENT = ("adversarial_map_staging/r1/pq_judgment_reading.py", "d11cfbc7182e8fba0f549467b654b1bd")
MAP = ("adversarial_map_staging/adversarial_map_v1_6.json", "7a69bc9fd197047c3cf7cecdb37a44ed")
CORPUS = "efilist_argument_library_v4_0_0.json"
HONEST = r"(?:prevent|distort)\w*\s+(?:honest|systematically distorting|moral judg)|systematically distorting moral judgment|prevents honest evaluation"
KNOCK = [
    ("#3 half 1", "why-not-suicide#long", "explicitly differentiates between preventing future suffering and terminating existing life"),
    ("#3 half 2", "why-not-suicide#long", "it keeps a body going, it does not weigh the life"),
    ("#3 sincerity", "why-not-suicide#long", "not that someone who argues the case does not mean it"),
    ("#44 anchor", "red-button-repugnant#long", "at what point does the perpetual manufacturing of beings"),
    ("#47 anchor", "red-button-repugnant#archetypeVariants.sophisticate",
     "products of the survival firmware the framework already identifies as distorting honest evaluation"),
    ("#56 value base", "heat-death-futility#long", "HOW MUCH suffering occurs along the way"),
]


def module_at(rel, want, name):
    m = types.ModuleType(name)
    m.__file__ = os.path.join(REPO, rel)
    exec(compile(pinned.bytes_at(REPO, rel, want).decode("utf-8"), m.__file__, "exec"), m.__dict__)
    return m


def style(t):
    return {"spaced": len(re.findall(r" — ", t)), "unspaced": len(re.findall(r"\S—\S", t))}


def measure():
    R1 = module_at(FIRST_INSTRUMENT[0], FIRST_INSTRUMENT[1], "pq_judgment_reading_pinned")
    P = module_at(PATCH[0], PATCH[1], "pin_patch_l6_pinned")
    rec = json.loads(pinned.bytes_at(REPO, DRAFTS[0], DRAFTS[1]).decode("utf-8"))
    corpus_md5 = rec["pinned"]["surfaces"][CORPUS]
    pre_c = json.loads(pinned.bytes_at(REPO, CORPUS, corpus_md5).decode("utf-8"))
    rows = P.select(rec, "all")
    out, _ = P.build(rec, rows, repo=REPO)
    post_c = json.loads(out[CORPUS])
    pre, post = R1.text_map(pre_c), R1.text_map(post_c)

    ex_pre, ex_post = R1.sweep(pre, R1.EXIT), R1.sweep(post, R1.EXIT)
    exit_patterns = {"pattern_count": len(R1.EXIT),
                     "before": {"hits": len(ex_pre), "loci": sorted({h["locus"] for h in ex_pre})},
                     "after_every_row": {"hits": len(ex_post), "loci": sorted({h["locus"] for h in ex_post})}}

    dashes = []
    for r in rows:
        rest = pre[r["locus"]].replace(r["current"], "")
        s_rest, s_new = style(rest), style(r["replacement"])
        mixed = bool((s_new["spaced"] and s_rest["unspaced"] and not s_rest["spaced"]) or
                     (s_new["unspaced"] and s_rest["spaced"] and not s_rest["unspaced"]))
        dashes.append({"row": r["id"], "locus": r["locus"], "slot_rest": s_rest, "replacement": s_new,
                       "brings_the_other_style": mixed})

    def honest(tm):
        return [{"locus": k, "match": m.group(0)} for k, t in tm.items() for m in re.finditer(HONEST, t)]
    h_pre, h_post = honest(pre), honest(post)

    knock = []
    for label, locus, s in KNOCK:
        knock.append({"what": label, "locus": locus, "text": s, "before": pre[locus].count(s), "after": post[locus].count(s)})

    return {
        "artifact": os.path.basename(RECORD),
        "instrument": "adversarial_map_staging/r1/sp_judgment_reading.py",
        "reads": {"drafts": DRAFTS[1], "patch_tool": PATCH[1], "first_instrument": FIRST_INSTRUMENT[1],
                  "corpus": corpus_md5, "set": "all: %d rows (%s)" % (len(rows), ", ".join(r["id"] for r in rows))},
        "exit_patterns": exit_patterns,
        "dashes": {"rows_bringing_the_other_style": [d["row"] for d in dashes if d["brings_the_other_style"]],
                   "per_row": dashes},
        "honest_evaluation_phrasing": {"before": h_pre, "after_every_row": h_post},
        "knock_on": knock,
    }


def main():
    fresh = (json.dumps(measure(), indent=1, ensure_ascii=False) + "\n").encode("utf-8")
    path = os.path.join(REPO, RECORD)
    if "--emit" in sys.argv:
        open(path, "wb").write(fresh)
        print("wrote %s  %s / %d" % (RECORD, pinned.md5(fresh), len(fresh)))
    elif "--check" in sys.argv:
        same = os.path.exists(path) and open(path, "rb").read() == fresh
        print("READING RECORD: %s" % ("matches the committed record" if same else "DIFFERS from the committed record"))
        sys.exit(0 if same else 1)
    else:
        sys.stdout.write(fresh.decode("utf-8"))


if __name__ == "__main__":
    main()

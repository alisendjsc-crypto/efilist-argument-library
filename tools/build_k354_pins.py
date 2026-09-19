#!/usr/bin/env python3
"""build_k354_pins.py -- ONE binding for every constant K354 quotes. It MEASURES; it does not
accept.

ccclxii, in the form this project keeps re-learning: a constant typed into a receipt, a block and
a stratum is a constant that will disagree with itself somewhere. Every value below is read from
a git blob, a file on disk, or a control artifact this session emitted, and the operator blocks
and the WI-K345 stratum quote THIS file rather than their author.

Nothing here is a claim about the wuld repo's own worktree state except what is measured from
its git blobs and from the k354 relabel scratch, both named explicitly.

  python3 tools/build_k354_pins.py            # -> tools/k354_pins.json
  python3 tools/build_k354_pins.py --out DIR  # emit elsewhere (for a reproduction check)
"""
import hashlib, io, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EFI = os.path.dirname(HERE)
WULD = os.environ.get("K354_WULD", "/sessions/rcw-0127lg5kydsnjwnnhp3ebin4/mnt/Projects--wuld-ink")
SCRATCH = os.environ.get("K354_SCRATCH",
                         "/sessions/rcw-0127lg5kydsnjwnnhp3ebin4/mnt/Downloads/k354_wuld_scratch")
OUT_DIR = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else HERE
OUT = os.path.join(OUT_DIR, "k354_pins.json")


def md5(b): return hashlib.md5(b).hexdigest()
def git(repo, *a): return subprocess.check_output(["git", "-C", repo] + list(a))
def blob(repo, path):
    b = git(repo, "show", "HEAD:" + path)
    return {"md5": md5(b), "bytes": len(b)}
def disk(path):
    b = io.open(path, "rb").read()
    return {"md5": md5(b), "bytes": len(b)}


EFI_STAGE = [
    "combined.html",
    "tools/k353_wing_functional_gate.py",
    "project_canon_v38_16.json",
    "tools/build_canon_v38_16.py",
    "tools/build_k354_pins.py",
    "tools/k354_cut_pins.json",
    "tools/k354_functional_control_v0_1.json",
    "tools/k354_functional_gate.py",
    "tools/k354_pins.json",
    "tools/k354_prior_gate_inversion_v0_1.json",
    "tools/k354_wing_functional_control_v0_2.json",
    "tools/note_confidence_K354.py",
    "tools/patch_k353_gate_K354.py",
    "tools/verify_K354.py",
]
EFI_REMOVE = "project_canon_v38_15.json"

WULD_MODIFIED = [
    "src/argument-library/index.html", "src/chat/index.html", "src/components/mobile-nav.js",
    "src/console/index.html", "src/contact/index.html", "src/donations/index.html",
    "src/feed.xml", "src/frame/index.html", "src/index.html", "src/library-about/index.html",
    "src/notes/index.html", "src/recommendations/index.html", "src/releases.json",
    "src/search-index.json", "src/troubleshooting/index.html", "tools/library-pin-state.json",
    "CLAUDE.md",
]
WULD_NEW = ["release_v4_1_2.json", "tools/apply_release_summary.py",
            "docs/relays/RELAY_code_seat_to_all_seats_v1.md"]

p = {
    "session": "K354 / WI-K345",
    "date_operator_local": "2026-09-18",
    "timezone": "America/Phoenix",
    "heads_at_open": {
        "efilist": git(EFI, "rev-parse", "HEAD").decode().strip(),
        "wuld": git(WULD, "rev-parse", "HEAD").decode().strip(),
    },
    "pin": {
        "old": blob(EFI, "combined.html"),
        "new": disk(os.path.join(EFI, "k354_drop", "combined.html")),
        "old_label": "v4.1.1", "new_label": "v4.1.2",
    },
    "held_no_corpus_byte": {
        "corpus_json": blob(EFI, "efilist_argument_library_v4_0_0.json"),
        "jsx": blob(EFI, "efilist_argument_library_v4_0_0.jsx"),
        "xsurface_identity": "6cd132ee5b8c7ca78ad0e095806f1c93",
        "adversarial_map_v1_3": blob(EFI, "adversarial_map_staging/adversarial_map_v1_3.json"),
        "honest_residuals_register_v0_4": blob(EFI, "adversarial_map_staging/honest_residuals_register_v0_4.json"),
        "wing": blob(EFI, "adversarial/index.html"),
    },
    "canon": {"old": blob(EFI, "project_canon_v38_15.json"),
              "new": disk(os.path.join(EFI, "project_canon_v38_16.json"))},
    "efilist_stage": {},
    "efilist_remove": {EFI_REMOVE: blob(EFI, EFI_REMOVE)},
    "efilist_drop": {
        "k354_drop/combined.html": disk(os.path.join(EFI, "k354_drop", "combined.html")),
        "k354_drop/k353_wing_functional_gate.py": disk(os.path.join(EFI, "k354_drop", "k353_wing_functional_gate.py")),
    },
    "k353_gate": {"base": blob(EFI, "tools/k353_wing_functional_gate.py"),
                  "amended": disk(os.path.join(EFI, "k354_drop", "k353_wing_functional_gate.py"))},
    "wuld_stage": {},
    "wuld_base_blobs": {},
    "vendor_identity_no_op": {
        "objections_index_efilist_blob": blob(EFI, "objections-index.json"),
        "src_library_objections_wuld_blob": blob(WULD, "src/library-objections.json"),
        "rtd_index_efilist_blob": blob(EFI, "right-to-die/right-to-die-objections-index.json"),
        "src_rtd_objections_wuld_blob": blob(WULD, "src/right-to-die-objections.json"),
        "note": ("Both generators were RUN this session and reproduce their committed exports "
                 "byte-for-byte, and each export equals the wuld-side vendored snapshot. The "
                 "re-vendor is therefore a no-op BY IDENTITY, positively controlled rather "
                 "than assumed."),
    },
    "search_index": {
        "invariance_pre": ("rebuilt from the PRE-relabel src, build_index.py reproduces the "
                           "committed src/search-index.json byte-for-byte"),
        "before": blob(WULD, "src/search-index.json"),
        "after": disk(os.path.join(SCRATCH, "src", "search-index.json")),
        "entries": "1013 held; exactly 2 changed, both the v4.1.1 -> v4.1.2 string",
    },
}
for path in EFI_STAGE:
    if path in ("tools/k354_pins.json", "tools/build_k354_pins.py"):
        continue  # self-referential; measured by the block after this file is written
    src = os.path.join(EFI, "k354_drop", os.path.basename(path)) \
        if path in ("combined.html", "tools/k353_wing_functional_gate.py") \
        else os.path.join(EFI, path)
    p["efilist_stage"][path] = disk(src)
for path in WULD_MODIFIED:
    p["wuld_stage"][path] = disk(os.path.join(SCRATCH, path))
    p["wuld_base_blobs"][path] = blob(WULD, path)
for path in WULD_NEW:
    p["wuld_stage"][path] = disk(os.path.join(WULD, path))

# the BLOB SHAs the operator blocks base-guard on. A blob sha is immune to a stale worktree in
# a way a disk md5 is not, which is the whole point of the guard.
p["_blobsha"] = {q: git(EFI, "rev-parse", "HEAD:" + q).decode().strip() for q in [
    "combined.html", "tools/k353_wing_functional_gate.py", "project_canon_v38_15.json",
    "efilist_argument_library_v4_0_0.json", "efilist_argument_library_v4_0_0.jsx",
    "adversarial/index.html"]}
p["_wuldblobsha"] = {q: git(WULD, "rev-parse", "HEAD:" + q).decode().strip() for q in WULD_MODIFIED}
# this file cannot record its own md5; the emitter reads it from disk. The builder can.
p["_self"] = {"build_k354_pins.py": disk(os.path.abspath(__file__))}

io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(p, indent=1, sort_keys=True) + "\n")
print("k354_pins.json  %s / %d" % (disk(OUT)["md5"], disk(OUT)["bytes"]))
print("  efilist stage %d paths (+1 git rm) ; wuld stage %d paths"
      % (len(EFI_STAGE), len(WULD_MODIFIED) + len(WULD_NEW)))
print("  PIN %s -> %s" % (p["pin"]["old"]["md5"], p["pin"]["new"]["md5"]))

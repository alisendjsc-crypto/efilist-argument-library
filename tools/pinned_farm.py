#!/usr/bin/env python3
"""pinned_farm.py -- run a script against the corpus a record pins, without editing the script (L5, 2026-09-26).

The declared pin session (R0150) moves the working corpus. Every map, fragment, register and measurement
record pins the pre-pin corpus (meta.source_corpus_md5 04bf6482), and at L5 phase 1 the live instruments
were taught to read those bytes from git history (adversarial_map_staging/r1/pinned.py, path_at).

Three builders cannot be taught: build_assembly_v1_1.py, _v1_2.py and _v1_3.py must stay byte-identical,
because each successor builder asserts its predecessor's md5 and tools/patch_assembly_v1_2.py and
_v1_3.py derive each from the one before by anchored patches (K348, K349, K351). This runs such a script
instead: a scratch root holding a symlink to every top-level entry of the repo except the corpus, which is
written from git at the md5 asked for. The script runs from inside the farm with K347_REPO and K348_REPO
pointed at it, so REPO resolves to the farm whichever way the script computes it. Writes land where the
script writes them, because the directories are symlinks to the real ones: run it, then `git diff` to see
whether it reproduced.

  python3 tools/pinned_farm.py [--corpus-md5 <md5>] <script> [args...]
  python3 tools/pinned_farm.py adversarial_map_staging/build_assembly_v1_3.py

--corpus-md5 defaults to 04bf6482aa0374ee92a81c1d55ec41f8, the pre-pin corpus. Exit status is the script's.
"""
import os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CORPUS = "efilist_argument_library_v4_0_0.json"
PRE_PIN = "04bf6482aa0374ee92a81c1d55ec41f8"
sys.path.insert(0, os.path.join(REPO, "adversarial_map_staging", "r1"))
import pinned  # noqa: E402


def main(argv):
    want = PRE_PIN
    if argv[:1] == ["--corpus-md5"]:
        want, argv = argv[1], argv[2:]
    if not argv:
        sys.exit(__doc__)
    raw = pinned.bytes_at(REPO, CORPUS, want)
    root = tempfile.mkdtemp(prefix="pinned_farm_")
    try:
        for n in os.listdir(REPO):
            if n != CORPUS:
                os.symlink(os.path.join(REPO, n), os.path.join(root, n))
        open(os.path.join(root, CORPUS), "wb").write(raw)
        env = dict(os.environ, K347_REPO=root, K348_REPO=root, PYTHONDONTWRITEBYTECODE="1")
        print("pinned_farm: %s at %s, farm %s" % (CORPUS, want[:8], root), file=sys.stderr)
        return subprocess.run([sys.executable, os.path.join(root, argv[0])] + argv[1:], cwd=root, env=env).returncode
    finally:
        # Unlink, never recurse: every directory in the farm is a symlink to the real one.
        left = []
        for n in os.listdir(root):
            p = os.path.join(root, n)
            if os.path.islink(p) or os.path.isfile(p):
                os.unlink(p)
            else:
                left.append(n)
        if left:
            print("pinned_farm: left %s in place (the script made %s)" % (root, left), file=sys.stderr)
        else:
            os.rmdir(root)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

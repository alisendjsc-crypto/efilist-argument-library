#!/usr/bin/env python3
"""pinned.py -- read a file at the md5 a record pins, from the working tree or its git history (L4c, 2026-09-26).

R1_rulings.json is append-only. A builder, control or gate that pinned it by whole-file md5 refuses on
true state the moment a later row lands, although nothing it read has changed. This resolves the pinned
bytes instead: the working copy if it still matches, else the newest committed blob of that path whose
md5 matches. It never guesses: if neither holds, it raises.

  from pinned import bytes_at
  raw = bytes_at(repo_dir, "adversarial_map_staging/r1/R1_rulings.json", "3f1dfad54021d7920576c7bd4840b62f")

EXTENDED AT L5 (2026-09-26, the declared pin session, R0150 phase 1): path_at() is the same lookup for a
reader that needs a PATH, not bytes -- a builder that hands the corpus to the validator, or a control that
stages it into scratch. The corpus is the case: the pin session moves it, and every map, fragment, register
and measurement record pins the pre-pin corpus (meta.source_corpus_md5 04bf6482). A record checked against
the working corpus would go RED, or silently drift, the moment a repaired sentence lands.

  from pinned import path_at
  CORPUS = path_at(REPO, "efilist_argument_library_v4_0_0.json", "04bf6482aa0374ee92a81c1d55ec41f8")
"""
import atexit, hashlib, os, shutil, subprocess, tempfile

_PATHS = {}


def md5(b):
    return hashlib.md5(b).hexdigest()


def bytes_at(repo, rel, want_md5):
    p = os.path.join(repo, rel)
    if os.path.exists(p):
        b = open(p, "rb").read()
        if md5(b) == want_md5:
            return b
    log = subprocess.run(["git", "-C", repo, "log", "--format=%H", "--", rel],
                         capture_output=True, text=True)
    for sha in log.stdout.split() if log.returncode == 0 else []:
        r = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (sha, rel)], capture_output=True)
        if r.returncode == 0 and md5(r.stdout) == want_md5:
            return r.stdout
    raise LookupError("%s at md5 %s is in neither the working tree nor its git history" % (rel, want_md5))


def path_at(repo, rel, want_md5):
    """A path whose bytes are `rel` at `want_md5`: the working copy if it matches, else the committed blob,
    written once per process into a private temp directory under the SAME basename (a record that names the
    file's basename cannot tell the difference) and removed at exit. Raises as bytes_at does."""
    p = os.path.join(repo, rel)
    if os.path.exists(p) and md5(open(p, "rb").read()) == want_md5:
        return p
    key = (os.path.abspath(repo), rel, want_md5)
    if key not in _PATHS:
        b = bytes_at(repo, rel, want_md5)
        d = tempfile.mkdtemp(prefix="pinned_")
        atexit.register(shutil.rmtree, d, True)
        q = os.path.join(d, os.path.basename(rel))
        open(q, "wb").write(b)
        _PATHS[key] = q
    return _PATHS[key]

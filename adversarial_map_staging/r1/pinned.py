#!/usr/bin/env python3
"""pinned.py -- read a file at the md5 a record pins, from the working tree or its git history (L4c, 2026-09-26).

R1_rulings.json is append-only. A builder, control or gate that pinned it by whole-file md5 refuses on
true state the moment a later row lands, although nothing it read has changed. This resolves the pinned
bytes instead: the working copy if it still matches, else the newest committed blob of that path whose
md5 matches. It never guesses: if neither holds, it raises.

  from pinned import bytes_at
  raw = bytes_at(repo_dir, "adversarial_map_staging/r1/R1_rulings.json", "3f1dfad54021d7920576c7bd4840b62f")
"""
import hashlib, os, subprocess


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

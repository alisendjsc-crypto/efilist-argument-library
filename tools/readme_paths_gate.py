#!/usr/bin/env python3
"""readme_paths_gate.py -- every path README.md names resolves in the tracked tree,
every URL it names answers 200 live. WI-K362 (2026-09-20), the K360 aftercare.

    python tools/readme_paths_gate.py [README.md] [--no-live]

A backtick token or a link target is a path when it has no spaces and looks like a
file or directory. A token with a slash must be tracked exactly (a file) or be a
tracked prefix (a directory); a bare basename resolves if any tracked file carries
it. URLs are fetched by curl.exe (Cloudflare 403s urllib) with a browser UA and
followed; anything but 200 is a finding. Exit 1 on any finding.
"""
import re, subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
readme = ROOT / (sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else 'README.md')
live = '--no-live' not in sys.argv
text = readme.read_bytes().decode('utf-8')

tracked = subprocess.run(['git', '-C', str(ROOT), 'ls-files'], capture_output=True, text=True, check=True).stdout.split('\n')
tracked = [t for t in tracked if t]
tracked_set = set(tracked)
basenames = {t.rsplit('/', 1)[-1] for t in tracked}
dir_prefixes = set()
for t in tracked:
    parts = t.split('/')
    for i in range(1, len(parts)):
        dir_prefixes.add('/'.join(parts[:i]))

PATH_RE = re.compile(r'^\.?[A-Za-z0-9_][A-Za-z0-9_.\-/]*$')
EXT = ('html','md','json','jsx','py','css','js','svg','png','cff','txt','yml','yaml','ps1','csv','tsv')
BARE = {'LICENSE','LICENSE-CODE','README'}
SKIP = re.compile(r'^(v\d+(\.\d+)+|[0-9a-f]{8,32}|\d[\d,]*|plain|scholar|library|examples|coda|full|LEGIBLE|HIGH-CONTRAST|FEEDBACK|md5|CC-BY-4\.0|MIT|NOTICE)$')

candidates = []
for m in re.finditer(r'`([^`\n]+)`', text):
    tok = m.group(1).strip()
    if ' ' in tok or '#' in tok or '://' in tok or SKIP.match(tok) or not PATH_RE.match(tok):
        continue
    if '/' not in tok and not tok.startswith('.') and tok not in BARE and ('.' not in tok or tok.rsplit('.', 1)[-1].lower() not in EXT):
        continue
    candidates.append((tok, text.count('\n', 0, m.start()) + 1))
for m in re.finditer(r'\]\(([^)\s]+)\)', text):
    tgt = m.group(1)
    if '://' in tgt or tgt.startswith('#'):
        continue
    candidates.append((tgt, text.count('\n', 0, m.start()) + 1))

findings = []
seen = set()
for tok, line in candidates:
    key = tok.rstrip('/')
    if (key, line) in seen:
        continue
    seen.add((key, line))
    if '/' in key:
        ok = key in tracked_set or key in dir_prefixes
    else:
        ok = key in tracked_set or key in dir_prefixes or key in basenames
    print(f"{'OK ' if ok else 'RED'} L{line:<4} {tok}")
    if not ok:
        findings.append(f"L{line} path does not resolve: {tok}")

if live:
    urls = sorted({u.rstrip('.,;)}') for u in re.findall(r'https?://[^\s)>`\]]+', text)})
    for u in urls:
        r = subprocess.run(['curl.exe', '-sL', '-A', 'Mozilla/5.0', '-o', 'NUL', '-w', '%{http_code} %{size_download}', u],
                           capture_output=True, text=True)
        code, size = (r.stdout.split() + ['?', '?'])[:2]
        ok = code == '200'
        print(f"{'OK ' if ok else 'RED'} {code:>4} {size:>9} B  {u}")
        if not ok:
            findings.append(f"URL {code}: {u}")

print(f"\n{readme.name}: {len(seen)} path mentions, {len(findings)} findings")
for f in findings:
    print('  ' + f)
sys.exit(1 if findings else 0)

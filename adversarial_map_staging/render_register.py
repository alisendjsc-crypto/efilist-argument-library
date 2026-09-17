#!/usr/bin/env python3
"""Render honest_residuals_register_v0_1.json as its readable companion."""
import json, sys
d=json.loads(open('honest_residuals_register_v0_1.json','rb').read().decode('utf-8')); m=d['meta']
phases=[f['phase'] for f in m['source_fragments']]
L=[];w=L.append
w("# Honest-Residuals Register v0.1"); w("")
w("**Status: WORKING.** Derived from %d honest-residue (d) entries across phases %s."
  % (m['residue_entries'], ", ".join(phases)))
w("Source corpus `%s` / 82 nodes. Rebuild: `python3 build_register.py [--with-draft-d] [--with-e]`." % m['source_corpus_md5'][:8])
w("")
w("**Library-internal.** No corpus, ledger, index or `/combined` byte moves from this artifact.")
w("Not for publication until the map is terminal."); w(""); w("---"); w("")
w("## Why the register is an input, not only an output"); w("")
w("The design doc schedules this for terminal assembly: *(d)-novel items appended to the")
w("honest-residuals register*. That is one phase too late, for a mechanical reason.")
w("")
w("Every (d) entry carries a `novel` boolean. With no register, a phase author decides that")
w("boolean **from memory of the preceding phases** — Phase D recalling what B2 registered three")
w("phases back. That is not a discipline, it is a recall test, and it has been failed once: the")
w("succession brief records N1 (moral realism / is-ought) as *\"first registered at nihilism-label")
w("(d, novel) in Phase D\"*, when the shipped B2 fragment carries its birth certificate at")
w("`phenomenological-existentialism` with `novel: true`, and B2's own `eliminativism` entry")
w("already routes to it as *\"already-surfaced (N1)\"*. B2 precedes D.")
w("")
w("The builder now refuses to write when a bedrock carries more than one birth certificate.")
w("Fed a Phase D fragment that flags N1 novel, it aborts with `HR-04 claims this-program")
w("registration but has 2 novel=true entries (need exactly 1)`.")
w("")
w("Phase E was authored against this register. Both of its (d) entries were decided by lookup")
w("rather than recall, reused registered bedrock strings, and introduced no new birth")
w("certificate — which is what the register is for.")
w("")
w("## What the free text was hiding"); w("")
w("**%d distinct `bedrock_name` strings collapse to %d actual bedrocks.** Nothing was wrong with"
  % (m['distinct_shipped_bedrock_names'], m['bedrocks']))
w("any individual entry; the fragmentation is what happens when a shared namespace is authored")
w("one phase at a time with no shared list to write against.")
w("")
w("| | |"); w("|---|---|")
w("| Residue entries | %d |" % m['residue_entries'])
w("| Distinct shipped `bedrock_name` strings | %d |" % m['distinct_shipped_bedrock_names'])
w("| Actual bedrocks | %d |" % m['bedrocks'])
w("| Registered before this program | %d |" % m['pre_map_registrations'])
w("| Registered **by** this program | %d |" % m['this_program_registrations'])
w("")
if d['audit']:
    w("## Audit"); w("")
    for a in d['audit']:
        w("**`%s` — %s.** %s" % (a['severity'], a['bedrock_id'], a['detail'])); w("")
adj=d['meta'].get('adjacency')
if adj:
    w("## Adjacency (F1 remedy)"); w("")
    w("Over-individuation \u2014 one bedrock wearing two ids \u2014 is the failure the birth-certificate")
    w("check cannot see. Two mechanical signals now narrow which pairs must be adjudicated: a")
    w("`terminus_routing` naming another bedrock, and a corpus node feeding two bedrocks.")
    w("")
    w("| | |"); w("|---|---|")
    w("| Possible pairs | 66 |")
    w("| Candidates derived by signal | %d |" % adj['candidates_derived'])
    w("| Relations declared | %d |" % adj['declared_relations'])
    w("| **Declared but undetected by any signal** | **%d** |" % len(adj['declared_but_undetected']))
    w("")
    w("The last row is the honest part. `HR-04+HR-07` is a real dependency neither signal fires on:")
    w("their terminus routings never name each other and they share no tributary node. It surfaced")
    w("by hand during the D3 triage. **The signals are a floor on what must be adjudicated,")
    w("never a ceiling**, and an empty relations list is now an assertion of independence rather than")
    w("a default: the audit refuses to write while any detected pair goes undeclared.")
    w("")
w("## The register"); w("")
w("| id | bedrock | trib | facets | registered in |"); w("|---|---|---|---|---|")
for b in d['bedrocks']:
    short='**this program**' if b['registered_in']=='this-program' else b['registered_in'].split(':')[0]
    al=(" *(%s)*"%b['alias']) if b['alias'] else ""
    w("| `%s` | %s%s | %d | %d | %s |" % (b['bedrock_id'],b['name'],al,b['tributary_count'],b['facet_count'],short))
w("")
for b in d['bedrocks']:
    al=(" — *%s*"%b['alias']) if b['alias'] else ""
    w("### `%s` %s%s" % (b['bedrock_id'],b['name'],al)); w(""); w(b['gloss']); w("")
    bc=b['birth_certificate']
    w(("**Birth certificate:** phase %s, `%s#%s`." % (bc['phase'],bc['node'],bc['locus'])) if bc
      else ("**Registered before this program:** `%s`." % b['registered_in']))
    w("")
    if b.get('relations'):
        w("**Relations:**"); w("")
        for r in b['relations']:
            w("- `%s` \u2192 `%s` \u2014 %s" % (r['kind'], r['to'], r['note']))
        w("")
    w("**Tributaries (%d across %d facet%s):**" % (b['tributary_count'],b['facet_count'],"" if b['facet_count']==1 else "s")); w("")
    for f in b['facets']:
        w("- **%s** — %s" % (f['facet_id'], ", ".join("`%s` (%s)"%(t['node'],t['phase']) for t in f['tributaries'])))
    w("")
out="\n".join(L)+"\n"
open('honest_residuals_register_v0_1.md','w',encoding='utf-8',newline='\n').write(out)
print("rendered", len(out.encode()), "B")

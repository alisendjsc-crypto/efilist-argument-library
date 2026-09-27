#!/usr/bin/env python3
"""build_ld2.py -- LD2's prototypes, their measured costs, and the design sheet. Writes ONLY under <out>.

  python3 build_ld2.py proto <out>   copy site/ to <out>/site and inject the proposals into the COPIES (one
                                     script per page, marked PROTOTYPE); the tracked pages are never written
  python3 build_ld2.py costs <out>   <out>/costs.json: each proposal's bytes on each page it touches, raw and
                                     gzip, measured by adding it to the real page and compressing both
  python3 build_ld2.py sheet <out>   <out>/sheet_ld2.html: the sheet, with live marks, the prototypes'
                                     screenshots (shoot_ld2.mjs makes <out>/shots) and the costs

Design lane (seat l), 2026-09-26, relay R0144. Every mark is drawn from icons/gen_icons.py's grids through
ld2_marks.py; nothing is pasted. A prototype is NOT the build: a build emits its marks from the generator into
regions a gate reads byte for byte (LD1's law 12). These exist so that Josiah rules on what he sees.
"""
import base64, gzip, html, json, os, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ld2_marks as M

SITE = os.path.join(M.REPO, 'site')

BASE_CSS = '''.mk-tile{display:inline-block;line-height:0;background:#0a0a0a;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.sg,.mk-plate-svg{display:block;shape-rendering:crispEdges}
.sg-c{fill:#e8e4dd}.sg-lit{fill:#ef3a58}
'''
PLATE_CSS = '''.mk-plate{margin:1.4rem 0 .4rem}
.mk-plate .pl{display:inline-block;line-height:0;max-width:100%}
.mk-plate-svg{max-width:100%;height:auto}
.pl-ground{fill:#0a0a0a}.pl-grid{fill:none;stroke:#1f1f1f;stroke-width:1}.pl-lead{fill:#77726a}
.pl-lbl{font:12px var(--mono,ui-monospace,monospace);fill:var(--dim,#b3aea6)}
.mk-plate figcaption{font-size:.72rem;color:var(--dim);margin:.5rem 0 0;max-width:40rem;line-height:1.5}
'''
SPINE_CSS = '''.mk-spine{display:none}
@media (min-width:68rem){
 .mk-spine{display:flex;flex-direction:column;align-items:center;gap:8px;position:fixed;z-index:5;top:50%;
   transform:translateY(-50%);left:calc((100vw - 60rem)/2 - 2.4rem);padding:10px 6px;background:#0a0a0a}
 .mk-spine .sp-edge{position:absolute;left:50%;top:10px;bottom:10px;width:2px;margin-left:-1px;background:#3a3833}
 .mk-spine .sp-n{position:relative;display:block;width:6px;height:6px;background:#77726a}
 .mk-spine .sp-n:hover{background:#e8e4dd}
 .mk-spine .sp-n.lit{background:#ef3a58}
 [data-mode="legible"] .mk-spine,[data-mode="both"] .mk-spine{background:none}
 [data-mode="legible"] .mk-spine .sp-edge,[data-mode="both"] .mk-spine .sp-edge{background:var(--line)}
 [data-mode="legible"] .mk-spine .sp-n,[data-mode="both"] .mk-spine .sp-n{background:var(--faint)}
 [data-mode="legible"] .mk-spine .sp-n.lit,[data-mode="both"] .mk-spine .sp-n.lit{background:var(--accent)}
}
.mk-spine[hidden]{display:none!important}
'''
WING_B_CSS = 'header.site h1 .lib-mark{vertical-align:middle;margin:0 .75rem 0 0;position:relative;top:-.1em}\n'
WING_D_CSS = '.obj-meta .mk-tile{vertical-align:-4px;margin-right:.55rem}\n.chip .mk-tile{margin-right:.4rem;vertical-align:-3px}\n'

# The parts of the wing script. Each is a function body that runs inside one closure sharing W, Q and TM.
JS_B = '''  var h1=document.querySelector("header.site h1");
  if(h1){ h1.insertAdjacentHTML("afterbegin",'<span class="mk-tile lib-mark">'+LIB[W]+'</span>');
    requestAnimationFrame(function(){ h1.classList.add("play"); setTimeout(function(){ h1.classList.remove("play"); }, SPAN[W]*1000+400); }); }
  var ab=document.getElementById("panel-about");
  if(ab&&PLATE[W]) ab.insertAdjacentHTML("beforeend",'<figure class="mk-plate"><span class="pl">'+PLATE[W]+'</span><figcaption>'+CAP[W]+'</figcaption></figure>');
'''
JS_C = '''  var sp=null, nodes=[], cards=[], PL=document.getElementById("panel-library");
  function where(){
    if(sp) sp.hidden=!!(PL&&PL.hidden);
    if(!nodes.length||(sp&&sp.hidden)) return;
    var y=innerHeight*.35, k=0, end=scrollY+innerHeight>=document.documentElement.scrollHeight-2;
    for(var i=0;i<cards.length;i++){ var t=cards[i].getBoundingClientRect().top; if(t<=y||(end&&t<innerHeight)) k=i; }
    for(var j=0;j<nodes.length;j++) nodes[j].classList.toggle("lit", j===k);
  }
  function spine(){
    if(Q.get("spine")==="0") return;
    cards=[].slice.call(document.querySelectorAll("#list .obj"));
    if(!sp){ sp=document.createElement("nav"); sp.className="mk-spine"; sp.setAttribute("aria-hidden","true"); document.body.appendChild(sp); }
    sp.innerHTML='<span class="sp-edge"></span>'+cards.map(function(c){ return '<a class="sp-n" tabindex="-1" href="#'+c.id+'"></a>'; }).join("");
    nodes=[].slice.call(sp.querySelectorAll(".sp-n")); where();
  }
  var LL=document.getElementById("list"); if(LL) new MutationObserver(spine).observe(LL,{childList:true});
  addEventListener("scroll",function(){ requestAnimationFrame(where); },{passive:true});
  addEventListener("resize",where);
  if(PL) new MutationObserver(where).observe(PL,{attributes:true,attributeFilter:["hidden"]});
'''
JS_D = '''  function tierOf(el){ var m=/tier\\s+(\\d)/i.exec(el.textContent); return m?+m[1]:0; }
  function deco(){
    var ms=document.querySelectorAll("#list .obj-meta:not([data-mk])");
    for(var i=0;i<ms.length;i++){ var t=tierOf(ms[i]); if(TM[t]) ms[i].insertAdjacentHTML("afterbegin",'<span class="mk-tile t'+t+'">'+TM[t]+'</span>'); ms[i].setAttribute("data-mk","1"); }
    var cs=document.querySelectorAll('#tier-chips .chip[data-tier]:not([data-mk])');
    for(var j=0;j<cs.length;j++){ var u=+cs[j].getAttribute("data-tier"); if(TM[u]) cs[j].insertAdjacentHTML("afterbegin",'<span class="mk-tile">'+TM[u].replace(/ sg-m/g,"")+'</span>'); cs[j].setAttribute("data-mk","1"); }
  }
  ["list","tier-chips"].forEach(function(id){ var e=document.getElementById(id); if(e) new MutationObserver(deco).observe(e,{childList:true}); });
'''


def js(v):
    return json.dumps(v, ensure_ascii=True)


def wing_script(wings, parts='BCD'):
    """The wing prototype, restricted to `wings`' data and to `parts`."""
    d = {'LIB': {}, 'SPAN': {}, 'PLATE': {}, 'CAP': {}, 'TM': {}}
    css, body = '', ''
    if 'B' in parts:
        d['LIB'] = {w: M.lib_glyph(w, 32) for w in wings}
        d['SPAN'] = {w: M.lib_span(w) for w in wings}
        d['PLATE'] = {w: M.plate(w, gut=170) for w in wings}
        d['CAP'] = {w: '%s&rsquo;s mark, enlarged: %s. Each square is one pixel of the mark in this page&rsquo;s tab.'
                    % (html.escape(M.TITLE[w]), html.escape(M.says(w))) for w in wings}
        css += BASE_CSS + PLATE_CSS + M.motion_css() + WING_B_CSS
        body += JS_B
    if 'C' in parts:
        css += SPINE_CSS
        body += JS_C
    if 'D' in parts:
        d['TM'] = {t: M.tier_glyph(t, 16) for t in M.TIERS}
        css += ('' if 'B' in parts else BASE_CSS) + M.tier_arrival_css() + WING_D_CSS
        body += JS_D
    decl = ', '.join('%s=%s' % (k, js(v)) for k, v in d.items() if v)
    return ('/* LD2 PROTOTYPE (%s) -- not a build. Design lane (seat l), 2026-09-26; build_ld2.py. */\n(function(){\n'
            '  var W=document.currentScript.getAttribute("data-wing"), Q=new URLSearchParams(location.search)%s;\n'
            '  var st=document.createElement("style"); st.textContent=%s; document.head.appendChild(st);\n%s})();\n'
            % (parts, (', ' + decl) if decl else '', js(css), body))


def flag_script(parts='BD'):
    d, css, body = {}, BASE_CSS, ''
    if 'B' in parts:
        d['LADDER'], d['SPAN'] = M.lib_glyph('combined', 32), M.lib_span('combined')
        css += M.motion_css() + '.header h1.mk-h1{display:flex;align-items:center;gap:14px}\n'
        body += '''  var h1=document.querySelector(".header h1");
  if(h1){ h1.insertAdjacentHTML("afterbegin",'<span class="mk-tile lib-mark">'+LADDER+'</span>'); h1.classList.add("mk-h1");
    requestAnimationFrame(function(){ h1.classList.add("play"); setTimeout(function(){ h1.classList.remove("play"); }, SPAN*1000+400); }); }
'''
    if 'D' in parts:
        d['TM'] = {t: M.tier_glyph(t, 16) for t in M.TIERS}
        css += (''.join('.mk-tc .t%d .sg-lit{fill:%s}\n' % (t, c) for t, c in M.TIER_COLOUR.items())
                + M.tier_arrival_css(play='.objection-header.focused')
                + '.tier-badge .mk-tile{margin:-1px 6px -1px -3px;vertical-align:-4px}\n'
                + '.filter-btn .mk-tile{margin-right:7px;vertical-align:-4px}\n')
        body += '''  if(Q.get("c")!=="crimson") document.documentElement.classList.add("mk-tc");
  function deco(){
    var bs=document.querySelectorAll(".tier-badge[data-tier]:not([data-mk])");
    for(var i=0;i<bs.length;i++){ var t=+bs[i].getAttribute("data-tier"); if(TM[t]) bs[i].insertAdjacentHTML("afterbegin",'<span class="mk-tile t'+t+'">'+TM[t]+'</span>'); bs[i].setAttribute("data-mk","1"); }
    var fs=document.querySelectorAll("#tierFilters .filter-btn[data-tier]:not([data-mk])");
    for(var j=0;j<fs.length;j++){ var u=+fs[j].getAttribute("data-tier"); if(TM[u]) fs[j].insertAdjacentHTML("afterbegin",'<span class="mk-tile t'+u+'">'+TM[u].replace(/ sg-m/g,"")+'</span>'); fs[j].setAttribute("data-mk","1"); }
  }
  deco();
  ["results","tierFilters"].forEach(function(id){ var e=document.getElementById(id); if(e) new MutationObserver(deco).observe(e,{childList:true}); });
'''
    decl = ', '.join('%s=%s' % (k, js(v)) for k, v in d.items())
    return ('/* LD2 PROTOTYPE (flagship %s) -- not a build; the flagship is a PIN surface, so this runs on a scratch\n'
            '   copy only. ?c=tier (the lean) lights each mark in its tier colour; ?c=crimson in the house crimson. */\n'
            '(function(){\n  var Q=new URLSearchParams(location.search), %s;\n'
            '  var st=document.createElement("style"); st.textContent=%s; document.head.appendChild(st);\n%s})();\n'
            % (parts, decl, js(css), body))


def door_script():
    marks = {n: M.lib_glyph(n, 32) for n in M.ICONS}
    span = max(M.lib_span(n) for n in marks)
    return '''/* LD2 PROTOTYPE (front door A) -- not a build. Each library mark says its sentence once: the title's on
   arrival, each card's the first time the card is seen; hovering a card says it again. The key's rows and the
   rail never move on their own. The marks are swapped for the same drawings carrying motion classes. */
(function(){
  var MK=%s, SPAN=%s;
  var st=document.createElement("style"); st.textContent=%s; document.head.appendChild(st);
  var h1=document.querySelector("header.site h1 .lib-mark"); if(h1) h1.innerHTML=MK.libraries;
  var cards=[].slice.call(document.querySelectorAll(".lib-card"));
  cards.forEach(function(c){ var h=c.getAttribute("href")||""; var n=h==="/combined"?"combined":h.split("/")[1]; var m=c.querySelector(".lib-mark"); if(m&&MK[n]) m.innerHTML=MK[n]; });
  function say(el){ el.classList.add("play"); setTimeout(function(){ el.classList.remove("play"); }, SPAN*1000+300); }
  var hd=document.querySelector("header.site h1"); if(hd) requestAnimationFrame(function(){ say(hd); });
  if("IntersectionObserver" in window){ var io=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ io.unobserve(e.target); say(e.target); } }); },{threshold:.6});
    cards.forEach(function(c){ if(c.querySelector(".lib-mark")) io.observe(c); }); }
  cards.forEach(function(c){ c.addEventListener("mouseenter",function(){ if(!c.classList.contains("play")) say(c); }); });
})();
''' % (js(marks), js(span), js(M.motion_css()))


def inject(path, tag):
    s = open(path, encoding='utf-8').read()
    assert s.count('</body>') == 1, path
    open(path, 'w', encoding='utf-8', newline='\n').write(s.replace('</body>', tag + '\n</body>'))


def proto(out):
    dst = os.path.join(out, 'site')
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(SITE, dst)
    os.makedirs(os.path.join(dst, 'ld2-proto'))
    files = [('wing.js', wing_script(M.WINGS)), ('flag.js', flag_script()), ('door.js', door_script())]
    for name, body in files:
        open(os.path.join(dst, 'ld2-proto', name), 'w', encoding='ascii', newline='\n').write(body)
    for w in M.WINGS:
        inject(os.path.join(dst, w, 'combined.html'), '<script src="/ld2-proto/wing.js" data-wing="%s"></script>' % w)
    inject(os.path.join(dst, 'combined.html'), '<script src="/ld2-proto/flag.js"></script>')
    inject(os.path.join(dst, 'libraries', 'index.html'), '<script src="/ld2-proto/door.js"></script>')
    for name, body in files:
        print('%-8s %6d B raw  %5d B gzip' % (name, len(body), gz(body.encode())))


def gz(b):
    return len(gzip.compress(b, 9, mtime=0))


def cost(page, script):
    """What `script` adds to `page`, inlined where the build would put it, raw and over the wire (gzip -9)."""
    before = open(os.path.join(SITE, page), 'rb').read()
    after = before.replace(b'</body>', b'<script>' + script.encode() + b'</script>\n</body>', 1)
    return {'raw': len(after) - len(before), 'gzip': gz(after) - gz(before),
            'page_raw': len(before), 'page_gzip': gz(before)}


def costs(out=None):
    c = {'A': {'libraries/index.html': cost('libraries/index.html', door_script())}}
    for p in 'BCD':
        c[p] = {w + '/combined.html': cost(w + '/combined.html', wing_script([w], p)) for w in M.WINGS}
    c['wing total'] = {w + '/combined.html': cost(w + '/combined.html', wing_script([w], 'BCD')) for w in M.WINGS}
    c['flagship package (B + D)'] = {'combined.html': cost('combined.html', flag_script('BD'))}
    if out:
        open(os.path.join(out, 'costs.json'), 'w').write(json.dumps(c, indent=1, sort_keys=True) + '\n')
    return c


# ------------------------------------------------------------------------------------------------------
# THE SHEET
CROPS = {   # shot -> (x, y, w, h) in the screenshot's own pixels
    'wing_desktop_dark': (180, 0, 1020, 800), 'wing_desktop_light': (150, 0, 1080, 800),
    'wing_spine_scrolled': (180, 60, 1020, 720), 'wing_about_plate': (240, 150, 960, 580),
    'head_abortion': None, 'head_transgenderism': None, 'head_anthropocentrism': None, 'head_veganism': None,
    'flag_head': None, 'flag_tier': (30, 180, 1230, 680), 'flag_crimson': (30, 180, 1230, 680),
    'wing_phone_dark': (0, 0, 780, 1450), 'wing_phone_light': (0, 0, 780, 1450),
}


def img(out, name):
    src = os.path.join(out, 'shots', name + '.png')
    dst = os.path.join(out, 'crops', name + '.png')
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    crop = ['-crop', '%dx%d+%d+%d' % (CROPS[name][2], CROPS[name][3], CROPS[name][0], CROPS[name][1]), '+repage'] \
        if CROPS[name] else []
    subprocess.run(['magick', src] + crop + ['-strip', dst], check=True)
    return 'data:image/png;base64,' + base64.b64encode(open(dst, 'rb').read()).decode()


def kb(n):
    return '%.1f KB' % (n / 1024)


SHEET_CSS = '''
:root{--bg:#0b0b0c;--panel:#111113;--fg:#e2ded6;--dim:#a39e95;--faint:#6f6a62;--line:#2a2825;--accent:#ef3a58;--cream:#f5efe6;
  --mono:'IBM Plex Mono',ui-monospace,Menlo,Consolas,monospace}
*{box-sizing:border-box}html{font-size:18px}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--mono);line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:74rem;margin:0 auto;padding:2.2rem 1.4rem 5rem}
h1{font-size:1.9rem;margin:.2rem 0 .3rem;letter-spacing:.01em;line-height:1.25}
h2{font-size:1.45rem;margin:3.2rem 0 .8rem;padding-top:1.4rem;border-top:1px solid var(--line);line-height:1.3}
h3{font-size:1.05rem;margin:1.8rem 0 .5rem;color:var(--fg)}
p,li{max-width:52rem}
.eyebrow{font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;color:var(--dim)}
.lead{font-size:1.05rem}
.box{border:1px solid var(--line);border-left:3px solid var(--accent);background:var(--panel);padding:1rem 1.2rem;margin:1.2rem 0;max-width:60rem}
.box.warn{border-left-color:#d6a93a}
.box p{margin:.35rem 0}
.facts{display:grid;grid-template-columns:9.5rem minmax(0,1fr);gap:.35rem 1.1rem;margin:.8rem 0 1.2rem;max-width:62rem}
.facts dt{color:var(--dim);font-size:.8rem;letter-spacing:.1em;text-transform:uppercase;padding-top:.2rem}
.facts dd{margin:0}
.pin{display:inline-block;font-size:.75rem;letter-spacing:.14em;text-transform:uppercase;padding:.05rem .5rem;border:1px solid;margin-left:.6rem;vertical-align:.2rem}
.pin.no{color:#7fbf8a;border-color:#3f6b47}.pin.yes{color:#ef8a3a;border-color:#8a4a1a}.pin.v0{color:var(--dim);border-color:var(--line)}
.lean{color:var(--accent);font-weight:600}
.grid{display:grid;gap:1.4rem}
.g7{grid-template-columns:repeat(auto-fill,minmax(15rem,1fr))}
.g4{grid-template-columns:repeat(auto-fill,minmax(15rem,1fr))}
.g2{grid-template-columns:repeat(2,minmax(0,1fr))}
@media (max-width:760px){.g2{grid-template-columns:1fr}}
.cell{background:var(--panel);border:1px solid var(--line);padding:1rem}
.cell .nm{font-weight:700;margin:.8rem 0 .1rem}
.cell .says{color:var(--dim);font-size:.85rem;margin:0 0 .35rem}
.cell .mv{font-size:.85rem;margin:0}
.cell .mv b{color:var(--dim);font-weight:500}
.tile{display:inline-block;line-height:0;background:#0a0a0a}
.tile svg{display:block;shape-rendering:crispEdges}
.sg-c{fill:#e8e4dd}.sg-lit{fill:#ef3a58}
.stage{display:flex;gap:1.2rem;align-items:flex-end}
.actual{display:flex;gap:.6rem;align-items:center;color:var(--faint);font-size:.75rem}
button.replay{font:inherit;font-size:.85rem;background:none;color:var(--fg);border:1px solid var(--accent);padding:.35rem .9rem;cursor:pointer;margin:.4rem 0 1rem}
button.replay:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
figure{margin:1rem 0}
figure img{display:block;max-width:100%;height:auto;border:1px solid var(--line)}
figcaption{font-size:.8rem;color:var(--dim);margin:.45rem 0 0;max-width:60rem}
.light{background:var(--cream);color:#1a1816;border-color:#d7ccb9}
.light .says,.light .mv b{color:#5f5a50}
table{border-collapse:collapse;margin:.8rem 0 1.4rem;font-size:.85rem}
th,td{border-bottom:1px solid var(--line);padding:.4rem .9rem .4rem 0;text-align:left;vertical-align:top}
th{color:var(--dim);font-weight:500;font-size:.75rem;letter-spacing:.1em;text-transform:uppercase}
td.n{text-align:right;font-variant-numeric:tabular-nums}
ol.rul>li{margin:0 0 .9rem}
.plain{border-top:1px solid var(--line);margin-top:3rem;padding-top:1.2rem}
.pl-ground{fill:#0a0a0a}.pl-grid{fill:none;stroke:#1f1f1f;stroke-width:1}.pl-lead{fill:#77726a}
.pl-lbl{font:12px var(--mono);fill:#b3aea6}
'''


def sheet(out):
    C = costs(out)
    s = M.silhouettes()
    base = max(v for v, _, _ in M.closest_pairs({k: v for k, v in s.items() if k[0] != 'disposition'}, 'tier', 'tier', 1)
               + M.closest_pairs({k: v for k, v in s.items() if k[0] != 'disposition'}, 'library', 'tier', 1))
    def near(fam):   # (IoU, the disposition's key, the other mark's key), whichever order the pair came in
        v, p, q = M.closest_pairs(s, 'disposition', fam, 1)[0]
        return (v, p[1], q[1]) if p[0] == 'disposition' else (v, q[1], p[1])
    dt, dl = near('tier'), near('library')
    I = {n: img(out, n) for n in CROPS}
    H = []
    w = H.append
    w('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
      '<title>LD2 design sheet</title>'
      '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
      '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;700&display=swap" rel="stylesheet">'
      '<style>' + SHEET_CSS + M.motion_css(gate='', play='.demo.play') + '</style></head><body><div class="wrap">')
    w('<div class="eyebrow">Design lane &middot; seat l &middot; LD2 &middot; 2026-09-26 &middot; for Josiah&rsquo;s eye; nothing here is built</div>')
    w('<h1>Marks that mean something &mdash; five proposals</h1>')
    w('<div class="box"><p class="lead"><b>Recommendation.</b> Build <b>A</b> (the library marks speak once), <b>B</b> '
      '(each wing carries its mark, and its About tab draws it large) and <b>D on the wings</b> (tier marks beside the tier '
      'words) now: no pin. Stage <b>D on the flagship</b> as a pin package, lit in the flagship&rsquo;s own tier colours. '
      'Build <b>C</b> (the reading spine) on Right to Die only first. Keep <b>E</b> (four outcome glyphs) as drawings, '
      'offered to the library&rsquo;s content sessions.</p>'
      '<p>The rule every item passed: a mark or a motion earns its place only if it says something true about structure '
      'that you can check against the words beside it. Every motion says its mark&rsquo;s own sentence, once. Nothing loops. '
      'Nothing moves unless the display is at full effects, on a dark ground, with motion allowed.</p></div>')
    w('<div class="box warn"><p><b>A correction I owe you first.</b> The architecture notes from the last session say tier '
      'marks belong to the flagship alone because &ldquo;no wing carries a tier.&rdquo; That was measured wrong. All five '
      'wing corpora give every objection a tier (Right to Die: 2 at tier 2, 8 at tier 3, 7 at tier 4), and every wing page '
      'already prints &ldquo;tier 3&rdquo; on each card and has a Tier filter. So the tier marks can go on the wings with no '
      'pin, and that is where D starts.</p></div>')

    # A
    w('<h2>A &middot; The library marks speak once <span class="pin no">no pin</span></h2>')
    w('<dl class="facts"><dt>What it says</dt><dd>Each library&rsquo;s mark builds itself the way its own sentence says it is built. The motion is the sentence, performed once.</dd>'
      '<dt>Where</dt><dd>The front door: the title&rsquo;s mark on arrival, each card&rsquo;s mark the first time the card is seen, and again when you hover a card. A wing&rsquo;s own mark beside its title, once, when the page opens (B). Never the rail, never the key.</dd>'
      '<dt>Motion</dt><dd>Opacity and transform only, 0.45&ndash;0.9 s, no loop. Only at full effects, on a dark ground, with motion allowed; otherwise the marks simply sit there.</dd>'
      '<dt>Cost</dt><dd>front door +%s raw, <b>+%s</b> over the wire</dd></dl>'
      % (kb(C['A']['libraries/index.html']['raw']), kb(C['A']['libraries/index.html']['gzip'])))
    w('<button class="replay" type="button" onclick="replay(\'a\')">&#9654; play all seven again</button>')
    w('<div class="grid g7 demo" id="a">')
    for n in M.ICONS:
        w('<div class="cell"><div class="stage"><span class="tile">%s</span><span class="actual"><span class="tile">%s</span>actual size</span></div>'
          '<p class="nm">%s</p><p class="says">%s</p><p class="mv"><b>moves:</b> %s</p></div>'
          % (M.lib_glyph(n, 96), M.lib_glyph(n, 16, moving=False), html.escape(M.TITLE[n]), html.escape(M.says(n)),
             html.escape(M.LIB_MOTION[n][0])))
    w('</div>')
    w('<h3>Two places I departed from the kickoff&rsquo;s wording</h3><ul>'
      '<li><b>Abortion:</b> the kickoff had the lit branch appear last. That stages a choice, ending on one branch, and the '
      'mark says <i>both branches present</i>. So both branches appear together.</li>'
      '<li><b>Right to Die:</b> the step appears in place and never moves toward or through the doorway. Nothing in any motion '
      'depicts an act.</li></ul>')
    w('<p>On the light ground the same marks keep their black tile and stay still, as the front door&rsquo;s tier marks already do.</p>')
    w('<div class="grid g7">' + ''.join('<div class="cell light"><span class="tile">%s</span><p class="nm">%s</p></div>'
      % (M.lib_glyph(n, 48, moving=False), html.escape(M.TITLE[n])) for n in M.ICONS) + '</div>')

    # B
    w('<h2>B &middot; Each wing carries its mark <span class="pin no">no pin</span></h2>')
    per = C['B']
    w('<dl class="facts"><dt>What it says</dt><dd>This page is this library: the icon in its tab, its card on the front door and its title are one object.</dd>'
      '<dt>Where</dt><dd>Beside each wing&rsquo;s title (32 px), and on its About tab drawn large on its pixel grid, each part named in the grammar&rsquo;s words and in its sentence&rsquo;s: <i>edge &middot; the lintel</i>, <i>the opening</i>, <i>lit &middot; the step</i>. The flagship&rsquo;s own title goes in the pin package.</dd>'
      '<dt>Motion</dt><dd>The title&rsquo;s mark says its sentence once when the page opens (A&rsquo;s motion). The plate never moves.</dd>'
      '<dt>Cost</dt><dd>per wing +%s&ndash;%s over the wire (the plate is most of it)</dd></dl>'
      % (kb(min(v['gzip'] for v in per.values())), kb(max(v['gzip'] for v in per.values()))))
    w('<figure><img alt="Right to Die with its mark beside the title, tier marks on the filters and on the first card, and the reading spine in the left margin" src="%s">'
      '<figcaption>Right to Die (prototype), dark. The doorway beside the title; the rest of this image is C and D.</figcaption></figure>' % I['wing_desktop_dark'])
    w(''.join('<figure style="margin:.6rem 0"><img alt="%s title with its mark" src="%s"></figure>' % (M.TITLE[x], I['head_' + x])
      for x in ['abortion', 'transgenderism', 'anthropocentrism', 'veganism'])
      + '<p style="font-size:.8rem;color:var(--dim)">The other four wings&rsquo; titles (prototype), at actual size.</p>')
    w('<figure><img alt="The About tab of Right to Die with the doorway mark drawn large and its parts named" src="%s">'
      '<figcaption>Right to Die&rsquo;s About tab (prototype): the mark on its grid, its parts named. This is where &ldquo;more intricate&rdquo; lives &mdash; at display size, never by crowding the 16-pixel mark.</figcaption></figure>' % I['wing_about_plate'])
    w('<h3>All five plates</h3><div class="grid g2">' + ''.join(
      '<figure><span class="tile" style="background:none">%s</span><figcaption>%s: %s</figcaption></figure>'
      % (M.plate(x, gut=170).replace('class="mk-plate-svg"', 'class="mk-plate-svg" style="max-width:100%;height:auto"'),
         html.escape(M.TITLE[x]), html.escape(M.says(x))) for x in M.PLATES) + '</div>')

    # C
    w('<h2>C &middot; The reading spine <span class="pin no">no pin on the wings</span></h2>')
    w('<dl class="facts"><dt>What it says</dt><dd>&ldquo;One lit element: where to look&rdquo; becomes &ldquo;where you are.&rdquo; One node per objection on the page, in order; the lit node is the one you are reading.</dd>'
      '<dt>Where</dt><dd>The left margin of a wing, only where there is a margin (68 rem and wider). Filtering the list redraws it. Clicking a node jumps to that objection. Hidden on the About tab.</dd>'
      '<dt>Motion</dt><dd>None. It changes as you scroll: feedback, not a loop, and instant, so there is nothing for reduced motion to stop.</dd>'
      '<dt>Phones</dt><dd><span class="lean">Hide it.</span> There is no margin, the layer&rsquo;s chin already owns the bottom edge, and a strip at the top would cost a line of reading space on every scroll. The count (&ldquo;17 / 17 objections&rdquo;) already says where the list is.</dd>'
      '<dt>Light ground</dt><dd>It takes the page&rsquo;s own ink. The marks keep their black tile because they must be the same object as the tab icon; the spine is furniture of this page only.</dd>'
      '<dt>Cost</dt><dd>per wing +%s over the wire</dd></dl>' % kb(max(v['gzip'] for v in C['C'].values())))
    w('<figure><img alt="Right to Die scrolled to its sixth objection, with the sixth node of the spine lit" src="%s">'
      '<figcaption>Scrolled to the sixth objection: the sixth node is lit.</figcaption></figure>' % I['wing_spine_scrolled'])
    w('<figure><img alt="Right to Die in the legible reading mode, cream ground" src="%s">'
      '<figcaption>The legible reading mode: marks keep their tile, the spine takes the page&rsquo;s ink.</figcaption></figure>' % I['wing_desktop_light'])

    # D
    w('<h2>D &middot; Tier marks beside the tier words <span class="pin no">no pin on the wings</span><span class="pin yes">pin on the flagship</span></h2>')
    w('<dl class="facts"><dt>What it says</dt><dd>How the objection is built, before you read a word of it: a reflex, handed down, a structure, bedrock, or about the other objections.</dd>'
      '<dt>Where</dt><dd>Every card&rsquo;s tier line and every tier filter, always beside the tier&rsquo;s words, never instead of them.</dd>'
      '<dt>Motion</dt><dd>A link straight to one objection plays that objection&rsquo;s tier mark once, as it arrives (the one-shots you approved in the game).</dd>'
      '<dt>Colour</dt><dd>Wings: crimson, the house voice, as on the front door. Flagship: <span class="lean">its own tier colours</span>, because its tier badges are already coloured and a crimson mark beside a blue &ldquo;TIER 4&rdquo; puts two accents in one badge.</dd>'
      '<dt>Cost</dt><dd>per wing +%s over the wire; flagship package (its title&rsquo;s mark and the tier marks) +%s</dd></dl>'
      % (kb(max(v['gzip'] for v in C['D'].values())), kb(C['flagship package (B + D)']['combined.html']['gzip'])))
    w('<div class="grid g2"><figure><img alt="Phone, dark" src="%s"><figcaption>Phone, dark: title mark, marked filters, the first card&rsquo;s tier line.</figcaption></figure>'
      '<figure><img alt="Phone, light" src="%s"><figcaption>Phone, legible.</figcaption></figure></div>' % (I['wing_phone_dark'], I['wing_phone_light']))
    w('<h3>The flagship package (a pin move you open): tier colour, then crimson</h3>')
    w('<figure><img alt="Flagship with tier-coloured marks" src="%s"><figcaption><span class="lean">Tier colour (lean).</span> Shape, colour and word agree.</figcaption></figure>'
      '<figure><img alt="Flagship with crimson marks" src="%s"><figcaption>Crimson. T3, T4 and T5 then carry two accents in one badge.</figcaption></figure>'
      % (I['flag_tier'], I['flag_crimson']))
    w('<figure><img alt="The flagship title with its ladder mark" src="%s"><figcaption>B&rsquo;s flagship half, in the same package: the ladder beside ARGUMENT LIBRARY.</figcaption></figure>' % I['flag_head'])

    # E
    w('<h2>E &middot; Outcome glyphs, four drawings <span class="pin v0">v0, not built</span></h2>')
    w('<p>The Adversarial Map sorts every continuation (the next move an opponent makes after reading our rebuttal) four '
      'ways. One layout for all four: the continuation is the node on top, the corpus is the row of three below, and '
      '<b>the lit element is where the continuation stops.</b></p>')
    w('<div class="grid g4">')
    for k, (disp, sent, r) in M.DISP.items():
        w('<div class="cell"><div class="stage"><span class="tile">%s</span><span class="actual"><span class="tile">%s</span>actual size</span></div>'
          '<p class="nm">(%s) %s</p><p class="says">%s</p></div>'
          % (M.glyph(r, 96), M.glyph(r, 16), k, html.escape(disp), html.escape(sent)))
    w('</div>')
    w('<ul><li>All four pass the silhouette law. The closest any comes to a tier mark is (%s) against T%s, overlap %.2f; '
      'to a library mark, (%s) against %s, %.2f. The closest pair already on the site overlaps %.2f.</li>'
      '<li>R0108 named three outcomes: routed, defanged, met. The map has no &ldquo;defanged&rdquo;, and R0108 draws '
      '&ldquo;met&rdquo; as a node in brackets, which is T5&rsquo;s silhouette, so the collision law refuses it. '
      '&ldquo;Routed&rdquo; is (a).</li>'
      '<li>Their home is the /adversarial/ page, which the library&rsquo;s content sessions render. Today it shows (d) only. '
      'So this is a proposal to them, and nothing is built.</li></ul>'
      % (dt[1], dt[2], dt[0], dl[1], M.TITLE[dl[2]], dl[0], base))

    # costs
    w('<h2>Costs, measured</h2><p>Each part added to the real page and both compressed (gzip &minus;9). The kickoff&rsquo;s budget is about 10 KB over the wire per page.</p>')
    def rng(vals):
        lo, hi = kb(min(vals)), kb(max(vals))
        return '+' + lo if lo == hi else '+%s&ndash;%s' % (lo.replace(' KB', ''), hi)
    rows = [('A &middot; library marks speak', 'the front door', C['A']),
            ('B &middot; wing title mark + About plate', 'each wing', C['B']),
            ('C &middot; reading spine', 'each wing', C['C']),
            ('D &middot; tier marks', 'each wing', C['D']),
            ('B + C + D together', 'each wing', C['wing total']),
            ('flagship package (B + D)', 'the flagship', C['flagship package (B + D)'])]
    w('<table><tr><th>proposal</th><th>page</th><th>raw</th><th>over the wire</th><th>that page today, over the wire</th></tr>')
    for label, where, d in rows:
        v = list(d.values())
        w('<tr><td>%s</td><td>%s</td><td class="n">%s</td><td class="n"><b>%s</b></td><td class="n">%s</td></tr>'
          % (label, where, rng([x['raw'] for x in v]), rng([x['gzip'] for x in v]),
             kb(min(x['page_gzip'] for x in v)) if len(v) == 1 else '%s&ndash;%s' % (kb(min(x['page_gzip'] for x in v)), kb(max(x['page_gzip'] for x in v)))))
    w('</table>')

    # rulings
    w('<h2>What I need from you</h2><ol class="rul">'
      '<li><b>Which to build.</b> <span class="lean">Lean: A, B and D on the wings now; D on the flagship staged as a pin package; C on Right to Die first; E as drawings.</span></li>'
      '<li><b>Flagship tier marks: tier colour or crimson.</b> <span class="lean">Lean: tier colour</span>, the flagship&rsquo;s own system.</li>'
      '<li><b>Where the outcome glyphs live.</b> <span class="lean">Lean: /adversarial/, offered to the content sessions</span>, who own that page.</li>'
      '<li><b>Your &ldquo;POV perspective and peripheral blurring&rdquo; line.</b> <span class="lean">Lean: its own session in the wuld-ink lane.</span> '
      'The layer already has both pieces: a camera pan and a peripheral blur, the blur re-measured working after an earlier '
      'build had cut it as inert. So the job is to tune what is shipped. Its source files are not in any repo, but the layer '
      'can be split back into them exactly: the packer that joined them is in wuld-ink&rsquo;s archive, and each part is '
      'marked in the packed file.</li></ol>')
    w('<div class="plain"><h3>In plain words</h3><p>Every library already has a small square icon. This would make each one '
      'build itself once, the way its own shape is described, the first time you see it; put it beside each wing&rsquo;s '
      'title; draw it large on the About tab with its parts labelled; and put the small tier icons next to the words '
      '&ldquo;tier 3&rdquo; wherever they appear. A thin column of dots in the margin of a long wing would light the dot '
      'for the objection you are reading. The flagship gets the same tier icons later, in a pin move you open. Nothing is '
      'live, nothing is committed to the site, and nothing moves on a light page or for readers who turn motion off.</p></div>')
    w('</div><script>function replay(id){var g=document.getElementById(id);g.classList.remove("play");void g.offsetWidth;'
      'g.classList.add("play");}addEventListener("load",function(){replay("a");});</script></body></html>')
    path = os.path.join(out, 'sheet_ld2.html')
    open(path, 'w', encoding='utf-8', newline='\n').write(''.join(H))
    print('sheet', path, os.path.getsize(path), 'B')



# ------------------------------------------------------------------------------------------------------
# THE PREVIEW (step 4 of R0144): the built pages and the flagship package, as preview_ld2.mjs shot them into
# <out>/preview, for Josiah's look before anything goes live.
def preview(out):
    P = os.path.join(out, 'preview')
    def im(name, alt, cap=None, width=None):
        src = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(P, name + '.png'), 'rb').read()).decode()
        st = ' style="max-width:%dpx"' % width if width else ''
        return '<figure><img alt="%s" src="%s"%s>%s</figure>' % (alt, src, st, '<figcaption>%s</figcaption>' % cap if cap else '')
    H = ['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
         '<title>LD2 preview</title><style>' + SHEET_CSS + '</style></head><body><div class="wrap">']
    w = H.append
    w('<div class="eyebrow">Design lane &middot; LD2 &middot; 2026-09-26 &middot; built on a branch, not live</div>')
    w('<h1>What you asked for, built &mdash; before it goes live</h1>')
    w('<div class="box"><p class="lead"><b>What changes for a reader.</b> On the front door, each library&rsquo;s mark '
      'builds itself once the first time you see its card, the way its line in the key says it is built, and again '
      'when you hover the card. Each wing now shows its mark beside its title, the small tier marks sit beside the '
      'words &ldquo;tier 3&rdquo; on every card and filter, and the About tab draws the wing&rsquo;s mark large with its '
      'parts named. Right to Die has a thin column of dots in its left margin; the lit dot is the objection you are '
      'reading. Nothing moves on a light page, for readers who turn motion off, or when effects are turned down.</p>'
      '<p><b>What I need:</b> your word to put this live (merge and push). The flagship&rsquo;s part is packed '
      'separately and waits for a pin move you open.</p></div>')
    w('<h2>The front door</h2>' + im('door_dark', 'Front door, dark', 'Dark ground. The GIF sent with this page shows these marks building themselves.'))
    w('<div class="grid g2">' + im('door_light', 'Front door, legible', 'Legible (light): marks keep their tile and stay still.')
      + im('door_phone', 'Front door, phone', 'Phone.') + '</div>')
    w('<h2>A wing: Right to Die</h2>' + im('rtd_dark', 'Right to Die, dark', 'The doorway beside the title; tier marks on the filters and on each card&rsquo;s tier line; the reading spine in the left margin.'))
    w(im('rtd_spine', 'Right to Die, scrolled', 'Scrolled to the tenth objection: the tenth dot is lit.'))
    w(im('rtd_light', 'Right to Die, legible', 'Legible: the spine takes the page&rsquo;s ink.'))
    w('<div class="grid g2">' + im('rtd_phone_dark', 'Phone, dark', 'Phone: no spine (no margin).') + im('rtd_phone_light', 'Phone, legible') + '</div>')
    w('<h2>Every wing&rsquo;s title and About plate</h2>')
    for x in M.WINGS:
        w(im('title_' + x, M.TITLE[x] + ' title') + im('plate_' + x, M.TITLE[x] + ' plate'))
    w('<h2>The flagship package (waits for your pin move)</h2>'
      + im('flag_head', 'Flagship title with its ladder') + im('flag_badges', 'Flagship tier badges in tier colour',
      'Each tier badge and filter carries its mark, lit in that tier&rsquo;s own colour.'))
    w('<div class="plain"><h3>Measured</h3><p>Chromium and Firefox. Wings: 240 page loads across six widths and four '
      'reading modes, no sideways scrolling on either tab, text contrast at least 5.37:1 (the bar is 4.5). Front door: '
      '80 loads, at least 5.06:1. Every motion check passed (title, cards, links landing on a card, the spine). '
      'Over the wire the front door grows 1.1 KB, Right to Die 3.4 KB, the other wings about 2.4 KB each. The flagship '
      'on the live site is untouched.</p></div>')
    w('</div></body></html>')
    path = os.path.join(out, 'preview_ld2.html')
    open(path, 'w', encoding='utf-8', newline='\n').write(''.join(H))
    print('preview', path, os.path.getsize(path), 'B')


if __name__ == '__main__':
    cmd, out = sys.argv[1], os.path.abspath(sys.argv[2])
    assert not out.startswith(M.REPO + os.sep) and out != M.REPO, 'write outside the repo'
    os.makedirs(out, exist_ok=True)
    {'proto': proto, 'costs': lambda o: print(json.dumps(costs(o), indent=1)), 'sheet': sheet, 'preview': preview}[cmd](out)

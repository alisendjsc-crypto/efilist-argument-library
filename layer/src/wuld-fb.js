/* wuld-fb.js -- per-card feedback. One control per objection, carrying the card's own id.
 *
 * WHY PER-CARD AND NOT A CORNER BUTTON. A corner button produces "something's broken somewhere";
 * a per-card one arrives with the objection id already attached, which is the difference between a
 * report you can act on and one you have to chase. Site-wide comments already have a route --
 * wuld.ink/contact -- so a fourth chin button would add a channel without adding information, and
 * at 320px the chin row is already as wide as it can be.
 *
 * A FORM, SINCE 2026-09-12, WITH THE MAIL DRAFT KEPT AS THE SECOND DOOR. The first version was a
 * mailto: only -- no backend, no storage, no consent banner. In use it opened the reader's mail
 * client, which on a desktop is a chooser dialog and on a phone is a second app, and it required an
 * address before anything could be said. The form posts to the same hosted relay wuld.ink/contact
 * already uses (Formspree, form xpqnzqlr): a message, an optional address so a reply can find its
 * way back, and the card's own context added by the page. The relay accepts JSON from this origin
 * (probed: CORS preflight and a honeypot-filled post both answered 200 from library.wuld.ink), so
 * the panel never leaves the page. The mail draft stays as a link inside the panel -- the alias is
 * still a way in, and it is the fallback the panel offers when the relay refuses.
 *
 * THE PANEL LIVES ON <body>, NOT IN THE CARD. The flagship's toggleObjection() re-renders the whole
 * #results list on every click and every filter, so anything inside a row is destroyed the moment
 * the reader opens a second row. A fixed-position panel anchored to the control's rect survives
 * that; if its card is re-rendered it finds the new control by the card's id and follows it.
 *
 * INJECTED, NOT DELEGATED, AND OBSERVED. The wings build their card list from JSON after load --
 * measured: 0 of 5 wings have a single `class="obj"` in their static HTML -- and re-render it when
 * a filter changes. A one-shot pass at boot would find nothing at all. */
(function () {
  var TO = 'contact@wuld.ink';
  var RELAY = 'https://formspree.io/f/xpqnzqlr';
  /* TWO CARD SHAPES. The wings render <article class="obj"> with an .obj-meta strip and .kw chips. The
     flagship (library.wuld.ink/combined, pin move 2026-09-12) renders a <div class="objection-header">
     row into #results -- the row IS the expander, its heading is the .trigger-text line, the tier and
     register live in the row's own badge strip, and the colloquial names sit in the sibling
     .detail-panel as .keyword chips. Same draft, read from whichever shape the card has. */
  var SEL = 'article.obj[id^="obj-"]:not([data-wz-fb]), div.objection-header[id^="obj-"]:not([data-wz-fb])';
  function isHeader(card) { return card.classList.contains('objection-header'); }

  function heading(card) {
    var h = card.querySelector(isHeader(card) ? '.trigger-text' : 'h2, h3, h4');
    return h ? h.textContent.replace(/\s+/g, ' ').trim() : '';
  }
  /* THE CARD DESCRIBES ITSELF. A report that says only "this one is wrong" costs whoever reads it
     a hunt through five libraries to work out which card it was. So the report arrives carrying the
     card's own context -- the library, the headline, the colloquial names on its chips, and its
     classification strip -- pulled from the card at the moment of the click, which means it cannot
     drift out of date the way a hand-written note would.
     The strip is read child by child rather than with textContent, because the control is itself a
     DOM child of that strip and would otherwise append the word "feedback" to its own report. */
  function strip(card) {
    var m = card.querySelector(isHeader(card) ? ':scope > div > div' : '.obj-meta');
    if (!m) return '';
    var out = '';
    for (var i = 0; i < m.childNodes.length; i++) {
      var n = m.childNodes[i];
      if (n.nodeType === 1 && String(n.className || '').indexOf('wz-fb') > -1) continue;
      out += n.textContent || '';
    }
    return out.replace(/\s+/g, ' ').trim();
  }
  function chips(card) {
    var k, kids;
    if (isHeader(card)) {
      var d = card.nextElementSibling;
      k = d && d.classList.contains('detail-panel') ? d : null;
      kids = k ? k.querySelectorAll('.keyword') : [];
    } else {
      k = card.querySelector('.kw');
      kids = k ? k.children : [];
    }
    if (!k) return [];
    var out = [];
    for (var i = 0; i < kids.length && out.length < 8; i++) {
      var t = kids[i].textContent.replace(/\s+/g, ' ').trim();
      if (t && t.length <= 40) out.push(t);
    }
    return out;
  }
  function clip(s, n) { return s.length > n ? s.slice(0, n - 1).replace(/\s+\S*$/, '') + '\u2026' : s; }

  function context(card) {
    return {
      id: card.id,
      link: location.href.split('#')[0] + '#' + card.id,
      library: (document.title.split('\u2014')[0] || '').trim(),
      objection: clip(heading(card), 240),
      classification: strip(card),
      also: chips(card)
    };
  }

  /* The writing space goes FIRST. Mail clients drop the cursor at the top of the body, so anything
     above the prompt is something the reader has to scroll past before they can type. Everything
     the machine contributed sits below the rule, out of the way but travelling with the message.
     MAILTO LENGTH IS A REAL LIMIT -- Windows passes the whole URL through a shell, and clients
     start truncating well before 2000 characters. So the body is built longest-first and the
     optional parts are dropped, in order, until the encoded URL fits under the budget. */
  var MAX_URL = 1800;
  function href(card) {
    var c = context(card);
    var lead = "(what's wrong, or what's missing?)\n\n\n"
             + "-- added automatically, so you needn't describe which card --\n";
    function build(withKw, headLen) {
      var b = lead;
      if (c.library)   b += 'library:        ' + c.library + '\n';
      if (c.objection) b += 'objection:      "' + clip(c.objection, headLen) + '"\n';
      if (withKw && c.also.length) b += 'also called:    ' + c.also.join(' \u00b7 ') + '\n';
      if (c.classification) b += 'classification: ' + c.classification + '\n';
      return b + 'id:             ' + c.id + '\nlink:           ' + c.link + '\n';
    }
    var subj = 'library feedback \u2014 ' + c.id;
    var tries = [[true, 240], [true, 140], [false, 140], [false, 80]];
    var out;
    for (var i = 0; i < tries.length; i++) {
      out = 'mailto:' + TO + '?subject=' + encodeURIComponent(subj)
          + '&body=' + encodeURIComponent(build(tries[i][0], tries[i][1]));
      if (out.length <= MAX_URL) break;
    }
    return out;
  }

  /* ---- THE PANEL ------------------------------------------------------------------------------- */
  var panel = null, form, ta, email, hp, status, sendBtn, mailLink, titleEl;
  var openId = null, opener = null, sending = false, raf = null, doneTimer = null;
  /* A stray click outside the panel closes it -- popover behaviour -- but not at the cost of what
     was typed: an unsent draft is kept for its card and restored when that card's control is opened
     again. One draft, the last one; a different card starts empty. */
  var draft = null;

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function build() {
    panel = el('div', 'wz-fb-panel');
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-label', 'Feedback on this objection');
    panel.hidden = true;
    var head = el('div', 'wz-fb-head');
    titleEl = el('span', 'wz-fb-title', 'Feedback');
    var x = el('button', 'wz-fb-close', '\u00d7');
    x.type = 'button'; x.setAttribute('aria-label', 'Close');
    x.addEventListener('click', function () { close(true); });
    head.appendChild(titleEl); head.appendChild(x);
    form = el('form', 'wz-fb-form');
    form.setAttribute('novalidate', '');
    ta = el('textarea', 'wz-fb-text');
    ta.name = 'message'; ta.rows = 4; ta.required = true;
    ta.placeholder = "What's wrong, or what's missing?";
    ta.setAttribute('aria-label', "What's wrong, or what's missing?");
    email = el('input', 'wz-fb-email');
    email.type = 'email'; email.name = 'email'; email.autocomplete = 'email';
    email.placeholder = 'your email \u2014 optional, only so a reply can find you';
    email.setAttribute('aria-label', 'Your email, optional, only so a reply can find you');
    /* Honeypot: bots fill every field; the relay discards a post that has this one. */
    var trap = el('div', 'wz-fb-trap'); trap.setAttribute('aria-hidden', 'true');
    hp = el('input'); hp.type = 'text'; hp.name = '_gotcha'; hp.tabIndex = -1; hp.autocomplete = 'off';
    trap.appendChild(hp);
    var row = el('div', 'wz-fb-row');
    sendBtn = el('button', 'wz-fb-send', 'Send'); sendBtn.type = 'submit';
    mailLink = el('a', 'wz-fb-mail', 'or write an email');
    mailLink.rel = 'nofollow';
    mailLink.title = 'Open a mail draft to ' + TO + ' that already names this card';
    status = el('span', 'wz-fb-status'); status.setAttribute('aria-live', 'polite');
    row.appendChild(sendBtn); row.appendChild(mailLink); row.appendChild(status);
    var note = el('p', 'wz-fb-note', 'Sent through the same relay as wuld.ink/contact; nothing is stored on this site.');
    form.appendChild(ta); form.appendChild(email); form.appendChild(trap); form.appendChild(row); form.appendChild(note);
    form.addEventListener('submit', onSubmit);
    panel.appendChild(head); panel.appendChild(form);
    /* Clicks inside the panel are the panel's: the sound layer's delegated listener may still hear
       them (it listens in the capture phase), the page's own handlers must not. */
    panel.addEventListener('click', function (e) { e.stopPropagation(); });
    panel.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); close(true); }
    });
    document.body.appendChild(panel);
    addEventListener('scroll', schedule, true);
    addEventListener('resize', schedule);
    /* The camera pan moves the whole stage under the pointer by up to --wz-pan; the panel is outside
       the stage, so it follows the control on pointer moves too (one rect read per frame at most). */
    addEventListener('pointermove', schedule, true);
    addEventListener('transitionend', function (e) { if (e.propertyName === 'transform') schedule(); }, true);
    document.addEventListener('pointerdown', function (e) {
      if (!openId || panel.hidden) return;
      if (panel.contains(e.target)) return;
      var c = e.target.closest && e.target.closest('.wz-fb');
      if (c && c === opener) return;                 // the control itself toggles, in onClick
      close(false);
    }, true);
  }

  function control(id) {
    var card = document.getElementById(id);
    return card ? card.querySelector('.wz-fb') : null;
  }
  function schedule() { if (openId && !raf) raf = requestAnimationFrame(function () { raf = null; place(); }); }
  function place() {
    if (!openId || panel.hidden) return;
    var c = control(openId);
    if (c) opener = c;                               // the card may have been re-rendered; follow it
    if (!opener) return;
    var r = opener.getBoundingClientRect();
    if (!r.width && !r.height) return;               // control off-DOM mid-render: keep the last place
    var w = Math.min(380, innerWidth - 24);
    panel.style.width = w + 'px';
    var h = panel.offsetHeight || 200;
    var below = r.bottom + 8;
    var top = (below + h < innerHeight - 12) ? below : Math.max(12, r.top - 8 - h);
    panel.style.top = Math.min(top, Math.max(12, innerHeight - h - 12)) + 'px';
    panel.style.left = Math.max(12, Math.min(r.right - w, innerWidth - w - 12)) + 'px';
  }

  function setState(s, msg) {
    panel.setAttribute('data-state', s);
    status.textContent = msg || '';
    sendBtn.disabled = (s === 'sending' || s === 'sent');
  }
  function openFor(card, ctrl) {
    if (!panel) build();
    if (doneTimer) { clearTimeout(doneTimer); doneTimer = null; }
    var c = context(card);
    openId = c.id; opener = ctrl;
    titleEl.textContent = 'Feedback \u2014 ' + c.id;
    mailLink.href = ctrl.href;
    var keep = draft && draft.id === c.id;
    ta.value = keep ? draft.msg : ''; email.value = keep ? draft.email : ''; hp.value = '';
    setState('idle', '');
    panel.hidden = false;
    ctrl.setAttribute('aria-expanded', 'true');
    place();
    try { ta.focus({ preventScroll: true }); } catch (e) { ta.focus(); }
  }
  function close(restoreFocus) {
    if (!panel || panel.hidden) return;
    if (panel.getAttribute('data-state') !== 'sent' && (ta.value.trim() || email.value.trim())) draft = { id: openId, msg: ta.value, email: email.value };
    else if (draft && draft.id === openId) draft = null;
    panel.hidden = true;
    var c = control(openId);
    if (c) c.setAttribute('aria-expanded', 'false');
    if (restoreFocus && c) { try { c.focus({ preventScroll: true }); } catch (e) {} }
    openId = null; opener = null; sending = false;
  }
  window.wzFbClose = function () { close(false); };

  function onSubmit(e) {
    e.preventDefault(); e.stopPropagation();
    if (sending || !openId) return;
    var msg = ta.value.trim();
    if (!msg) { setState('idle', 'Write something first.'); ta.focus(); return; }
    var card = document.getElementById(openId);
    var c = card ? context(card) : { id: openId, link: location.href, library: '', objection: '', classification: '', also: [] };
    var body = {
      _subject: 'library feedback \u2014 ' + c.id,
      message: msg,
      library: c.library, objection: c.objection, also_called: c.also.join(' \u00b7 '),
      classification: c.classification, id: c.id, link: c.link
    };
    var em = email.value.trim();
    if (em) body.email = em;
    if (hp.value) { setState('sent', 'Sent \u2014 thank you.'); doneTimer = setTimeout(function () { close(true); }, 1800); return; }
    sending = true;
    setState('sending', 'Sending\u2026');
    var failed = function (why) {
      sending = false;
      setState('error', why || 'Could not send \u2014 try again, or use the email link.');
    };
    try {
      fetch(RELAY, { method: 'POST', mode: 'cors', headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
        .then(function (r) {
          return r.json().then(function (j) { return { ok: r.ok && !(j && j.ok === false), j: j }; },
                               function () { return { ok: r.ok, j: null }; });
        })
        .then(function (res) {
          if (!res.ok) {
            var why = res.j && res.j.errors && res.j.errors.length && res.j.errors[0].message;
            failed(why ? 'The relay refused it: ' + why + ' \u2014 use the email link.' : null); return;
          }
          sending = false;
          setState('sent', 'Sent \u2014 thank you.');
          doneTimer = setTimeout(function () { close(true); }, 1800);
        })
        .catch(function () { failed(null); });
    } catch (err) { failed(null); }
  }

  function onClick(e) {
    e.preventDefault();            // the href stays a mail draft for the no-script reader and the copy menu
    e.stopPropagation();           // the flagship's row is itself the expander
    var a = e.currentTarget, card = a.closest('article.obj, .objection-header');
    if (!card) return;
    if (openId === card.id && panel && !panel.hidden) { close(true); return; }
    openFor(card, a);
  }

  function pass() {
    var cards = document.querySelectorAll(SEL), n = 0;
    for (var i = 0; i < cards.length; i++) {
      var c = cards[i], hdr = isHeader(c), m = hdr ? c : c.querySelector('.obj-meta');
      c.setAttribute('data-wz-fb', '1');            // set even when there is no meta strip, so a
      if (!m) continue;                             // card without one is not re-examined forever
      var a = document.createElement('a');
      a.className = 'wz-fb';
      a.href = href(c);
      a.rel = 'nofollow';
      a.textContent = 'feedback';   // uppercased by CSS, like every other micro-label on the card
      a.title = 'Report a correction or comment about this objection';
      a.setAttribute('aria-label', 'Report a correction or comment about this objection: ' + (heading(c) || c.id));
      a.setAttribute('aria-haspopup', 'dialog');
      a.setAttribute('aria-expanded', openId === c.id ? 'true' : 'false');
      a.addEventListener('click', onClick);
      /* Appended, not prepended. While the control was floated it had to precede the meta text to
         sit beside it; anchored, its position is set by CSS and DOM order is free to match reading
         order instead -- so a keyboard lands on the meta text first and the utility after it. */
      m.appendChild(a);
      n++;
    }
    if (openId) schedule();                          // a re-render moved the anchor; follow it
    return n;
  }

  window.wzFbInit = function () {
    var n = pass();
    if (window.MutationObserver) {
      var queued = false;
      new MutationObserver(function () {
        if (queued) return;                          // a filter re-render is hundreds of mutations;
        queued = true;                               // coalesce them into one pass on the next frame
        requestAnimationFrame(function () { queued = false; pass(); });
      }).observe(document.body, { childList: true, subtree: true });
    }
    return n;
  };
})();

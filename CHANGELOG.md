# Changelog

All notable changes to the efilist argument library.

Versioning follows a PATCH/MINOR/MAJOR convention keyed on the **invariants subtree** (canon `invariants` block):

- **PATCH** — invariants subtree byte-identical to the prior release; content-advance + score-layer + prose re-cuts only. The structural taxonomy is unchanged.
- **MINOR** — invariants subtree mutated (counts shift, edges added, premises re-cut); corpus topology changes.
- **MAJOR** — schema-class break (RWE schema bump, score model re-architecture, surface-router redesign).

**Invariants anchor.** The v3.7 line ran on anchor `f6b94bf0cb3e6832dbdde0017b876e54` (subtree byte-identical across v3.7-stable → v3.7.3, which is why those were PATCH-class). **v3.8.0 mutated the subtree** — the new anchor is `8727787c5c0d4f8a08280b806db6fcc8` (method: `md5(json.dumps(invariants, sort_keys=True, ensure_ascii=False))`), held byte-identical across v3.8.0 → v3.8.3.

Per-release artifact integrity is canon-anchored in `archive_attestation.release_artifact_md5_set_per_release_manifest_*` and the `archive_attestation.v3_8_*` blocks. Headline counts are read from canon `invariants` (canon v37.3) and cross-verified against the corpus.

---

## Repository structure — 2026-09-20 (no release; the pin stands)

The served tree moved into **`site/`** (wuld-ink WI-K360). The flagship, the wings' pages and what they fetch at runtime, the umbrella front door, the presentation layer, `_headers` and `_redirects` — 52 files by `git mv`, every blob sha identical — and Cloudflare Pages now builds from `site/`, so the canon, the tooling, the staging folders and the records at the repository root are no longer served at `library.wuld.ink`. **No served byte changed:** `/combined` read `006aa9833f7a8b103ad27a289ab22fa9` / 2,987,411 B before and after. The flagship's path in this repository is `site/combined.html` from here on; a pin move edits it there.

---

## [v4.1.2] — 2026-09-18

**PATCH** by the invariants convention; **no corpus byte on any surface** — the cross-surface gate (`tools/xsurface_v4_1_0.py`) reads `6cd132ee5b8c7ca78ad0e095806f1c93` before and after, and the corpus `version` stays `4.1.0`. Flagship-only repairs to the note and confidence layer (K354): the `[NOTE]` control lifted out of `if (conf !== 'full')` so its condition equals its container's — nine containers, nine controls — making 195 words readable that no reader could open, on a card the Adversarial Map's reader surface had just started pointing readers at; `full` renders as full and the silent `|| 'full'` upgrade of 64 never-graded objections is deleted, so absence now means ungraded; the unlabelled 70 % provisional-opacity band removed, rule and class; eleven 5-digit hex literals over six declarations repaired. The canon records it at `session_log_recent` (`K354_note_and_confidence`) and `keyset_delta_ledger.v38_16_K354`.

**This entry and v4.1.1's were written on 2026-09-20, two days after the moves.** Neither pin move touched this file, the README's pin table or the front door's badge; the canon carried the record alone. Same class as v4.0.5's gap above, recorded rather than hidden.

| | md5 | bytes |
|---|---|---|
| superseded — v4.1.0 | `72187f6cf0fccdf8e9f4ec6ca5ce009c` | 2,982,770 |
| superseded — v4.1.1 | `f095c0ce0e5a1d796d57fa5a5dd62f7d` | 2,985,989 |
| **current — v4.1.2** | **`006aa9833f7a8b103ad27a289ab22fa9`** | **2,987,411** |

---

## [v4.1.1] — 2026-09-18

**PATCH** by the invariants convention; **no corpus byte** — corpus `04bf6482aa0374ee92a81c1d55ec41f8` and JSX `b196548b6eb39065842d62292acca89f` unmoved git-to-git, the cross-surface gate identical at `6cd132ee5b8c7ca78ad0e095806f1c93` before and after. The level-independent affordance (K352): a per-card `[DISMANTLE]` control rendered at every response level, the anchor grammar extended to `#obj-<id>@<depth>` (append-only; `@` is outside the id vocabulary), and COPY LINK emitting that suffix so the grammar ships with a producer. Twelve line-indexed edits, reconstructed against the git base byte for byte; 28 functional checks in real Chromium with the pinned base run as a null. The canon records it at `session_log_recent` (`K352_the_affordance`).

| | md5 | bytes |
|---|---|---|
| superseded — v4.1.0 | `72187f6cf0fccdf8e9f4ec6ca5ce009c` | 2,982,770 |
| **current — v4.1.1** | **`f095c0ce0e5a1d796d57fa5a5dd62f7d`** | **2,985,989** |

---

## [v4.1.0] — 2026-09-17

**PATCH by the invariants convention at the top of this file; MINOR by the canon version-class ruling that set the number.** The two conventions are keyed on different things and this is the first release where they disagree, because it is the first release to advance corpus **content** without moving a single count. The invariants subtree is byte-identical, so the rule at the top of this file reads PATCH. Canon's `post_terminal_policy` keys the number on enrichment-versus-intake, and enrichment of existing nodes is MINOR, which is why the queue's `version_class_ruling` set `v4.1.0` rather than `v4.0.6`. Recorded here rather than resolved: both rules are doing their own job correctly.

**The first corpus change since the v4.0.0 content cut of 2026-07-11.** Three pure-subtraction repairs from the nineteen-item v4.1.0 enrichment queue, each removing a claim that is false or unsupported, none adding an argument. They went first because their correctness is judgeable without re-litigating any philosophy: the question is whether the sentence is true, not whether the move is good.

| | node | locus | what went | words |
|---|---|---|---|---|
| **R1** | `happiness-is-choice` | `long` | a heritability coefficient read as the fraction of **one person's** happiness fixed at conception — the coefficient partitions variance *between* people. The slice-of-the-pie carve-up built on it goes with it. | 555 → 589 (+34) |
| **R2** | `just-edgy` | `long` | *"has never been substantively refuted"* — an argument from silence offered as a credential, inside a rebuttal against arguments from authority. Reception is now **described** (more often categorized than answered) rather than **adjudicated**. | 220 → 220 |
| **R3** | `just-depressed` | `long` + `archetypeVariants.defender` | an unsourced one-in-a-hundred ratio organising the node's opening and its close, inside the corpus's most epistemically self-aware rebuttal. Stated qualitatively instead; nothing depended on 1:99 rather than 1:20. | 979 → 978, 347 → 344 |

`subtractive` classifies the **claim**, not the word count. R1 is +34 words because saying why a statistic fails to license an inference takes more room than making the inference took. The bare-deletion variant shipped beside it in the spec as `R1-alt` and was **not** taken.

### R3 had four spans, not three

The spec named three, all in `responses.long`, and its own scope note says a repair that fixes the opening and leaves the close still counting to ninety-nine produces a node that contradicts itself. The same unsourced ratio also stood at `responses.archetypeVariants.defender` — live shipped text, once per surface. It was found by sweeping the **defect** across every locus of every node rather than the five named strings, ratified the same session, and repaired with the other three.

That sweep turned up something larger, which is **not** fixed here and is recorded in canon: `archetypeVariants` is not in the map validator's `LOCI` enum at all, so `target_locus` cannot name it and `anchor-rule` cannot reach it. **16 of 82 nodes carry archetype variants — 10,072 words of live shipped corpus text the Adversarial Map is structurally unable to adjudicate.**

### Three surfaces, no build step

`combined.html` is a hand-assembled superset carrying `REBUTTAL_STRENGTH`, which the JSX does not, and nothing regenerates any surface from any other. The same six spans live in all three, byte-identically, so one replacement pair served all three — 18 span-replacements across 12 line-loci, each line-indexed with a per-line anchor assertion, each surface verified against its **git blob** for a changed set of exactly the named lines.

**A corpus-vs-flagship gate did not exist and now does** (`tools/xsurface_v4_1_0.py`): string-aware bracket-balance extraction of the `const OBJECTIONS` literal from the flagship and the JSX, compared against the corpus file by canonical-serialization md5. All three agree at `a597fb18cac0b12434d63c4cfd23cfff` before and `6cd132ee5b8c7ca78ad0e095806f1c93` after, and the same four leaves moved on every surface.

### The Adversarial Map is frozen, not advanced

Each repaired node carried one Phase E entry classed `(b)` whose verbatim anchor is cut from the sentence being repaired, and `status-enum` pins `status` to `mapped` as a hard check — so after the cut no status value can say an anchor is historical. `coverage: 82/82` is a claim about a **(map, corpus) pair**, bound by `meta-corpus-pin`; advancing the pin under entries authored against the old text would change a receipt's referent while keeping its claim. So `adversarial_map_v1_0.json` stays byte-identical at `c4989e98…` and stays pinned to corpus `6ee1f6f3…`, against which it still validates under `--assembly` at **21 checks, 0 violations, 0 advisories**. Measured both ways: against the post-cut corpus it is FAIL with 5 violations, while `coverage` passes in **both**, which is the proof it only breaks if the entries are *removed*. A successor map is owed: 79 nodes inherit, three re-adjudicate.

| | md5 | bytes |
|---|---|---|
| superseded — v4.0.0 | `e654eabd32fa95e5969d49e6eb15aa87` | 2,963,752 |
| superseded — v4.0.1 | `9d13359e305c6caa3ae64759f3dcc0e6` | 2,963,789 |
| superseded — v4.0.2 | `62d1e8d86056465ebcb5daced38e0a83` | 2,974,039 |
| superseded — v4.0.3 | `62c733ac8263e6413816cfb6d28e3b8a` | 2,982,420 |
| superseded — v4.0.4 | `c60dcb56498debc84d2fb2860cd55167` | 2,982,518 |
| superseded — v4.0.5 | `cee25a00b68ba036138d064c383d9a8b` | 2,982,658 |
| **current — v4.1.0** | **`72187f6cf0fccdf8e9f4ec6ca5ce009c`** | **2,982,770** |

**v4.0.5 has no entry of its own in this file.** It shipped on 2026-09-13 — the load-bearing hierarchy table regenerated from `DEP_GRAPH_DATA.links` and a third era of inert baked node counters stripped — and the release surfaces were never revisited. Its prose is in `release_v4_0_5.json` in the wuld.ink repo. Its hash is added to the ladder above rather than reconstructed as a retrospective entry, which would be inventing a record for a session that is over.

### Changed

- **`combined.html`** (+112 B) — four lines, six span-replacements. **The pin.**
- **`efilist_argument_library_v4_0_0.json`** (+112 B, `04bf6482aa0374ee92a81c1d55ec41f8`) — the same four lines' worth of text, plus the `version` field `4.0.0` → `4.1.0`. **The field names the content cut, not the release**: commit `e922e6c` restored it to `4.0.0` after the v4.0.1-v4.0.4 relabels walked it to `4.0.4` while the content stayed byte-identical, which made one content version wear five hashes and broke validation for every artifact pinning `6ee1f6f3`. v4.1.0 is the first genuine content cut since K219, so it is the first bump that rule licenses. **Filename stays frozen**, per convention. `generated` is untouched: it dates an authoring run, and no run happened.
- **`efilist_argument_library_v4_0_0.jsx`** (+112 B, `b196548b6eb39065842d62292acca89f`) — the same six spans.
- **`project_canon_v38_4.json`** — MINOR; keyset held at 41; `invariants`, `schemas` and `hazard_map` asserted byte-identical by the builder, which is what would have made it MAJOR. v38_3 archived. `canon_version_marker` corrected from a drifted `v38.1`.
- **`adversarial_map_staging/`** — the regen queue records the three as landed; the map artifact itself is **untouched**.
- **`README.md`, `libraries/index.html`** — pin table, front-door badge, status prose, canon filename. Three of these were correcting v4.0.5, not stamping v4.1.0.
- **`tools/`** — `sweep_v4_1_0.py`, `verify_v4_1_0.py`, `xsurface_v4_1_0.py`, `build_canon_v38_4.py`, `restamp_v4_1_0.py`.

### Controls

- **13 of 13 behaved.** A positive control on each tool, then base-md5, base-CR, line-anchor, changed-set, HELD-lost, GONE-survives, word-count, collateral-anchor and json-leaf-set against the sweep, and surface-disagreement against the cross-surface gate. The first collateral-anchor control aborted at the *line* gate and so proved section 1 rather than section 7; it was kept and a second built beside it that applies cleanly and is caught only by the anchor sweep. A control that cannot fail for its own reason proves nothing.
- **Anchor destruction is the receipt.** 90 of the map's 93 anchors hold against the post-cut corpus and exactly the three intended break. An anchor still matching after a subtractive regen would be proof the defect was still in the text.
- **Word counts stated in advance** and asserted on both sides: hashes cannot see a change in meaning that is internally consistent.
- **`objections-index.json` unchanged** — `d034af153aafa08c6f57884a9e7426a1` / 41,800 B. The index projects `id`/`trigger`/`diagnosis`/`keywords` and this cut moved only `responses`, so the wuld.ink objection re-vendor is a no-op **by identity** — proven by regenerating from the post-cut corpus, with the generator first reproducing the committed artifact as a positive control.
- **The objections digest moved** `0218f73b7bfac7c9bcf7d352a5eab5cc` → `2c5a083a31448dec0f1ce41e08ba5b04`. It is computed over `objections` and is independent of the `version` field — the validator's own label-churn self-test sets `version` to `4.0.4` to prove that — so the digest moved because the responses moved.
- **Line counts frozen.** All three surfaces keep their line count; every changed set is exactly the named loci, checked against `git show HEAD:<file>` and not against a copy on disk.

---

## [v4.0.4] — 2026-09-12

**PATCH** by the invariants convention at the top of this file — the invariants subtree is byte-identical and no content changed. One `href`: the flagship's breadcrumb bar named *Refusal Libraries* and did not link it, so the umbrella front door was unreachable from the most-read surface in the suite. **No content change.** The corpus, the grading ledger, both graph literals, the argument-flow matrix, the real-world-examples data and every response are byte-unchanged; the objections index is unchanged (`d034af15…`). The unified diff of the pinned file is **one hunk, two lines**.

**Why a new version.** The same rule as v4.0.1 through v4.0.3: one version maps to one hash. The splice moved the pinned file, so the pin moved; a copy that hashes to `62c733ac…` is v4.0.3, diagnosable, not corrupt.

| | md5 | bytes |
|---|---|---|
| superseded — v4.0.0 | `e654eabd32fa95e5969d49e6eb15aa87` | 2,963,752 |
| superseded — v4.0.1 | `9d13359e305c6caa3ae64759f3dcc0e6` | 2,963,789 |
| superseded — v4.0.2 | `62d1e8d86056465ebcb5daced38e0a83` | 2,974,039 |
| superseded — v4.0.3 | `62c733ac8263e6413816cfb6d28e3b8a` | 2,982,420 |
| **current — v4.0.4** | **`c60dcb56498debc84d2fb2860cd55167`** | **2,982,518** |

### The rule, not the patch

The first breadcrumb segment is a **parent** on every surface except the front door, where it is the current page. So it renders as a **link everywhere**, and as a bare `aria-current="page"` label **only when the served path is `/libraries/`** — with the trailing slash on the `href`, which is the served form and saves a 308 hop. Ratified by the library seat at K233. This release brings the one surface that violated the rule up to a convention the other six already kept, and fixes the trailing slash on the five that kept it imperfectly. The front door already modelled the exception correctly and its bar is untouched.

The two bar implementations are **not** unified here. The flagship ships the inline-styled `nav.rl-wing` (K123); the wings ship the class-based `nav.eyebrow.wing-switcher`. Unifying them is a large change to the pinned file for no reader-visible gain, and it is not what was ratified.

### Changed

- **`combined.html`** (+98 B) — the breadcrumb's first segment becomes a link. Measured on the v4.0.3 bytes: `nav.rl-wing` carried exactly one `href` (`/right-to-die/combined`) and the string `/libraries` appeared **zero** times in the whole 2.98 MB file, so a reader on the flagship reached the front door only by leaving through *Harm & Autonomy* to the right-to-die wing and coming back in from that wing's bar. It is now `<a href="/libraries/">`, held at `#88847c` — the wings' `--faint`, 5.28:1 on the bar's `#0a0a0a`, AA — and carrying the bar's own existing link treatment (`text-decoration:none`, `border-bottom:1px solid rgba(136,132,124,.4)`, `padding-bottom:1px`), so the accent stays reserved for the cross-wing link and no other pixel on the bar moves.
- **The five wings** (`right-to-die`, `abortion`, `transgenderism`, `anthropocentrism`, `veganism`) — `href="/libraries"` → `href="/libraries/"`, exactly once in each `combined.html`, +1 B each. No pin; these auto-deploy.
- **`libraries/index.html`** — the front-door badge `pinned v4.0.3 → v4.0.4`; **every card gains its register** as a fourth `.lib-meta` span — *rebut-only* on the four wings, *argues a thesis* on the flagship and on veganism; and the intro now says once that **"Refusal Libraries" is a venue name, not a category claim**, and that veganism is a flagship-adjacent module arguing harm rather than a wing defending a choice. Why mark it: veganism's register makes positive appraisal native and unremarkable, where the wings' Firewall-A forbids exactly that, so a reader moving from a wing to veganism with nothing on either page marking the change reads it as the firewall failing. No rename — the venue keeps its name and the per-card registers do the categorical work.
- **`README.md`** — pin table takes the v4.0.4 identifier, the new md5 and byte count; the status line gains the nav clause and becomes "None of the four".
- **`efilist_argument_library_v4_0_0.json`** — `version` field only, same-length string, **byte count unchanged**. **Filename stays frozen**, per convention.

### Controls

- **PATCH proof, run on these bytes.** `OBJECTIONS`, `REAL_WORLD_EXAMPLES`, `MAP1_TRANSITIONS`, `DEP_GRAPH_DATA`, `MAP_GRAPH_DATA` and the `id="rwe-data"` script block extracted from the v4.0.3 and the v4.0.4 bytes by bracket-balance and compared: **byte-for-byte identical, all six**, at 612,928 / 509,888 / 1,007,943 / 52,472 / 43,811 / 494,987 bytes (measured with the enclosing delimiters included).
- **`objections-index.json` unchanged** — `d034af153aafa08c6f57884a9e7426a1` / 41,800 B on both sides. It carries no version string, so the wuld.ink objection re-vendor is a no-op by identity — verified, not assumed.
- **The `v4.0.3` mentions in `combined.html` are not swept.** Three occurrences, all comments recording which pin move introduced a block (the phone media block, the premise-family fills, the graph-canvas fit). They are dated records. Three before, three after.
- **The layer is not touched.** No `wuld-layer.css` / `wuld-layer.js` bytes move, and there is no layer deploy in this release.

### Held — deliberately not swept

- **The front door's `.lib-meta` row runs at 2.13:1 on the default ground** (`--faint` `#4a4742` on `#0b0b0c`) — badge, count and version, all three below AA and measured here for the first time. The new register span is given its own value so it clears AA in all four grounds (`#88847c`, 5.28:1 on the default; `var(--dim)` under legible / high-contrast / both, 5.99 / 13.89 / 12.63). Bringing the other three up is a front-door contrast pass of its own and was not ratified with this move.
- **The flagship's bar names one sibling** (*Harm & Autonomy*, linking `/right-to-die/combined`) where the wings' bar names all six, and it uses a category label where the wings use the wing's own name. The asymmetry looks like a deliberate two-pole framing; it was not ratified either way and is not touched here.
- **The K232 flagship panel items.** The LOAD-BEARING table's arithmetic contradicts its own panel prose — Consent Impossibility's 26% resolves against ~255, not 222 (67/255 = 26.3%, 67/222 = 30.2%) — and correcting the two rows named (Convergent Architecture 13→17, Benatar 33→36) takes 222 to 229 and leaves roughly 26 edges unaccounted. Not shipped until the table sums to 255 or the panel text declares a narrower denominator, with the panels' figures bound to the release-time integrity check rather than hand-patched again.
- **The abortion advisory instance stays, and stays singular.** Firewall-B exceptions authored inside the suite = 1; the H4 lone-exception capstone requires exactly one marked exception to exist. Remove it and the capstone loses its subject; add a second and the lone-exception argument dies.
- **`combined.html` L1722** — *"the original 81 objections…"* stays, for the reason given under v4.0.1.

### Open

- **Invariant defect: `DEP_GRAPH_DATA` per-node stored link sums total 245 against an actual 255** — carried from v4.0.1, unchanged.

## [v4.0.3] — 2026-09-12

**PATCH** by the invariants convention at the top of this file — the invariants subtree is byte-identical and no content changed. (v4.0.1 called the same condition MINOR; this entry, like v4.0.2's, follows the definitions.) The flagship is laid out for phones, and the graph views' SVG labels — the carry named under v4.0.2 — are brought to WCAG AA on the ground each is painted on. **No content change.** The corpus, the grading ledger, both graph literals, the argument-flow matrix, the real-world-examples data and every response are byte-unchanged (`OBJECTIONS`, `REAL_WORLD_EXAMPLES`, `MAP1_TRANSITIONS`, `DEP_GRAPH_DATA`, `MAP_GRAPH_DATA` and the `rwe-data` block compared literal for literal); the objections index is unchanged (`d034af15…`).

**Why a new version.** The same rule as v4.0.1 and v4.0.2: one version maps to one hash. The phone block and the fills moved the pinned file, so the pin moved; a copy that hashes to `62d1e8d8…` is v4.0.2, diagnosable, not corrupt.

| | md5 | bytes |
|---|---|---|
| superseded — v4.0.0 | `e654eabd32fa95e5969d49e6eb15aa87` | 2,963,752 |
| superseded — v4.0.1 | `9d13359e305c6caa3ae64759f3dcc0e6` | 2,963,789 |
| superseded — v4.0.2 | `62d1e8d86056465ebcb5daced38e0a83` | 2,974,039 |
| **current — v4.0.3** | **`62c733ac8263e6413816cfb6d28e3b8a`** | **2,982,420** |

### Changed

- **`combined.html`** (+8,381 B) — **the phone layout**: one `@media (max-width: 600px)` block at the end of the page's own stylesheet, nothing outside it. Measured on the v4.0.2 bytes in mobile contexts at 390×844, 360×780 and 430×932: the library view overflowed the viewport by 149 / 179 / 110 px (the view switcher's fourth tab and the RSI METHODOLOGY button off-screen, unreachable by any tap), the mechanism web and dependency graph by 145 / 175 / 104, the argument flow by 369 / 399 / 328 (a `320px | 1fr | 360px` grid), the examples and the coda by 43 / 73 / 3 (the shared nav's mode toggle). On the new bytes every one of 54 states (six views, three widths, both grounds) reads `scrollWidth − clientWidth = 0` with no element rect past the viewport; the wings and the front door stay at 0. The shared nav wraps to two rows when its five buttons do not fit and scrolls with the page instead of sticking (two sticky rows are 11% of a phone screen); the four view tabs become a 2×2 grid — all four visible at 360, where a scrolling strip would hide the fourth; the depth row wraps with its label on its own line; the graph toolbars wrap; the argument flow's three columns stack; the examples' filter bar becomes label | control rows. Every control-row button is at least 36 px tall (nav, view tabs, tier filters, depth, RSI, graph toolbars, zoom buttons, flow controls, examples tabs, selects and reset); the in-card chips (SHOW IN MAP / DEP, COPY, `[ plain ]`, `[NOTE]`, the examples badge and pills) 28 px. On the v4.0.2 bytes 96 of the library view's 107 interactive elements were under 36 px; what remains under 36 is the layer's 82 FEEDBACK controls (26 px, the layer's bytes), the wing-switcher's link (17 px, the K123 inline-styled bar shared with the wings) and the examples' `<summary>` rows (26 px, full-width). **The graph canvases** at phone width: the force layouts are tuned for the desktop canvas and drew three screens wide; on a phone each simulation is now settled synchronously and the zoom transform set to the drawing's bounding box (pinch and drag continue from there; ZOOM FIT does the same), the dependency graph is laid out on its desktop canvas (1400×900) before the fit so its nine premise boxes keep their room, the argument flow's `viewBox` becomes the drawing's bounding box so the labels around the ring stay on the canvas, and the legends start closed (open at 390 they covered half the canvas). None of this runs at 601 px and up: the desktop control (below) says so.
  **The SVG label fills** (TODO 17): every graph-view label measured against the ground it is painted on — the canvas for a label beside its dot, the family rect or the tier circle for a label on one — in all four modes and the K314 states plus the flow map's three other modes: 250 undimmed readings per ground, of which **123 (dark) and 172 (cream) were below 4.5:1**; on the new bytes **0 and 0**, minima 4.93 (dark) and 4.70 (cream, white on the empirical green). Values: the objection labels of both graphs `#555`/`#666` → `#88847c` (the wings' `--faint`, 5.32 on `#0a0a0a`) and `#777`/`#888` → `#615b50` on cream (5.52); the band labels `#333` → `#88847c`, `#999` → `#615b50`, the legible-mode pair likewise; the premise labels and their counts solid (`#e8e8e8` dark, `#fff` cream) with black on the mustard family in both grounds and on characterization in cream (`data-family` stamped on each premise group — the only DOM change); the flow map's T-badges and source label `#1a1a1a` on cream (white inside the red source node stays); the stars `#b8860b` → `#7a5c00` on cream (5.13); the "No successors" text a class with a value per ground instead of one inline `#555`. The K74 de-emphasis states (a selected node's non-neighbours at opacity .12 / .06 — 127 readings per ground) are an opacity, not a colour, and are left as the spec has them.
- **`screenshots/dependency-graph.png`** — re-captured from the new bytes at 1440×900; the only README capture the fills change (the mechanism web's objection labels are hidden until hover).
- **`libraries/index.html`** — the front-door badge `pinned v4.0.2 → v4.0.3`.
- **`README.md`** — pin table takes the v4.0.3 identifier, the new md5 and byte count; the status line names the phone layout and the AA claim widens from "every HTML text colour" to every text colour, the dimmed states excepted.
- **`efilist_argument_library_v4_0_0.json`** — `version` field only. **Filename stays frozen**, per convention.

### Controls

- **Desktop unchanged.** The nine README captures re-taken at 1440×900 from the v4.0.2 and the v4.0.3 bytes under one seeded `Math.random` with each force simulation run to rest: seven byte-identical PNGs; for the two graph captures, whose rasterization carries ±1 channel noise run to run even on the same bytes, the settled SVG DOM (every position and transform) is byte-identical for the mechanism web and identical but for the 13 `data-family` attributes for the dependency graph. The phone half alone leaves all nine desktop states unchanged; the fills change only what they name.
- **The layer is not touched** (`wuld-layer.css` `c06d2310…`, `wuld-layer.js` `89532502…`, no deploy). Checked at 360 and 390: the feedback panel opens 336 / 366 px wide inside the viewport, the tour card is 336 / 340 px, the chin's four 44 px controls sit at y 740 / 802 and cover no toggle; at the foot of every page nothing sits under the chin.
- The K316 battery (`navcheck`, `fbform`, `layerfix`, `wingtoggle`, `k317`) is GREEN on the new bytes.

### Held — deliberately not swept

- **`combined.html` L1722** — *"the original 81 objections…"* stays, for the reason given under v4.0.1.
- **The wing-switcher bar** (`.rl-wing`, inline-styled, K123) wraps to three lines at 390 and its link is 17 px tall; it is one markup in six copies and a change to it belongs with the wings.
- **The layer's FEEDBACK control** is 26 px tall on a phone; the layer is a separate deploy.
- **The graphs' phone canvases are overviews**: fitted, a 7 px label renders at 2–3 px until pinched; the source list and the detail panel carry the text.

### Open

- **Invariant defect: `DEP_GRAPH_DATA` per-node stored link sums total 245 against an actual 255** — carried from v4.0.1, unchanged.

## [v4.0.2] — 2026-09-11

**PATCH** by the invariants convention at the top of this file — the invariants subtree is byte-identical and no content changed. (v4.0.1 called the same condition MINOR; this entry follows the definitions.) The flagship joined the shared presentation layer that the wings and the front door already carried, and its own colours were brought to WCAG AA in both grounds. **No content change.** The corpus, the grading ledger, both graph literals and every response are byte-unchanged; the objections index re-vendors as a no-op (`d034af15…` both sides).

**Why a new version.** The same rule as v4.0.1: one version maps to one hash. The integration moved the pinned file, so the pin moved; a copy that hashes to `9d13359e…` is v4.0.1, diagnosable, not corrupt.

| | md5 | bytes |
|---|---|---|
| superseded — v4.0.0 | `e654eabd32fa95e5969d49e6eb15aa87` | 2,963,752 |
| superseded — v4.0.1 | `9d13359e305c6caa3ae64759f3dcc0e6` | 2,963,789 |
| **current — v4.0.2** | **`62d1e8d86056465ebcb5daced38e0a83`** | **2,974,039** |

### Changed

- **`combined.html`** (+10,250 B) — links `/wuld-layer.css` and `/wuld-layer.js` exactly as the wings do and wraps its content in the layer's `.wz-stage`; the four `body >` rules that switch the three top-level sections rewritten with the descendant combinator so they match with or without the wrapper (measured: without this the sections rendered stacked for ~100 ms, CLS 0.61); a **START HERE** précis at the head of each methodology panel (+4,024 B, every clause sourced to the panel it heads); the colour remap at source — 76 rule edits and template hooks replacing `#444`–`#777` greys with warm values that clear 4.5:1 on the dark ground, the masthead `#8b0000` becoming the library's crimson `#ef3a58` on dark and staying `#8b0000` on cream, tier and grade colours restated per ground via a small palette contract (**0 of 5,680 HTML text elements per mode below 4.5:1**, four modes × eleven states); the four reading-mode buttons collapsed to two `aria-pressed` toggles (LEGIBLE, HIGH-CONTRAST; the mode strings, storage key and event are unchanged); a null guard on the examples view's `#counts` (a reference that never came across from `rwe.html`, one console error per render); the wing-switcher inset by the bezel's top lip.
- **Layer** (`wuld-layer.css` / `wuld-layer.js`, linked, NO-PIN) — the feedback control reads the flagship's row shape as well as the wings' cards; the sound layer sounds the rows; the library tour has a seven-step flagship variant; the `?` chin control accepts the mouse (it had not: the chin is `pointer-events:none` and the button never re-enabled it); tour flags are per surface; cues softened (hover −9 dB at a 250 ms limit, click/expand/collapse −6 dB) with a `--wz-sfx-gain` master; the feedback control opens an in-page form through the same relay as `wuld.ink/contact` (email optional, the mail draft kept as a link); a 6 px horizontal scroll under the camera pan clipped; under the magnifier the pointer is the camera — its place across the viewport maps onto what the scaled page hides past that edge, so a magnified line is readable end to end by the pointer alone and the page's edge never crosses the viewport's — and the flagship's sticky bar (LIBRARY | EXAMPLES | CODA) and the examples sidebar stop being sticky while zoomed, because a sticky element under a scaled ancestor is laid out unscaled and painted scaled and drifted (zoom − 1) × scroll down the viewport.
- **`_headers`** (new) — `/wuld-layer.css` and `/wuld-layer.js` served `private, max-age=0, must-revalidate`, so a layer change reaches every page on the next load. The zone's Browser Cache TTL floors any lower `public` max-age to 4 h, which is how a reader ran the new page against a four-hour-old layer on release evening.
- **`.gitattributes`** — `*.css` and `*.js` added as `text eol=lf`.
- **Wings and the front door** — the four reading-mode buttons collapsed to the same two toggles as the flagship (`right-to-die`, `abortion`, `transgenderism`, `anthropocentrism`, `veganism`, `libraries/`); the front-door badge `pinned v4.0.1 → v4.0.2`.
- **`README.md`** — pin table takes the v4.0.2 identifier, the new md5 and byte count; the screenshots re-captured from the deployed bytes at 1440×900; a section on the presentation layer; the offline note says what does not travel with the file.
- **`efilist_argument_library_v4_0_0.json`** — `version` field only. **Filename stays frozen**, per convention.

### Held — deliberately not swept

- **`combined.html` L1722** — *"the original 81 objections…"* stays, for the reason given under v4.0.1.
- **The graph views' SVG label fills** — 225 of 323 below 4.5:1 against the K74 legibility spec, measured and left; a change to them is a pin move of its own.
- **The flagship's phone layout** — the view-switcher and depth buttons overflow 147/217 px at 390/320, as before the integration (+2 px for the lip); pre-existing, not touched.

### Open

- **Invariant defect: `DEP_GRAPH_DATA` per-node stored link sums total 245 against an actual 255** — carried from v4.0.1, unchanged.

## [v4.0.1] — 2026-09-08

**MINOR** by the invariants convention. **No content change.** The corpus, the grading ledger and both graph literals are byte-unchanged in substance: this release re-stamps display strings that had gone stale against the v4.0.0 cut, and corrects one methodology-provenance count. Seven display loci in `combined.html`, one stale grade line in `README.md`, one front-door badge.

**Why a new version rather than a re-pinned v4.0.0.** A reader who pulled v4.0.0 and hashes it against a pin table that now reads differently could not tell *superseded* from *corrupt* — and the film tells them a mismatch means corrupt. One version maps to one hash, so the hash a reader computes has exactly one release it can belong to.

| | md5 | bytes |
|---|---|---|
| superseded — v4.0.0 | `e654eabd32fa95e5969d49e6eb15aa87` | 2,963,752 |
| **current — v4.0.1** | **`9d13359e305c6caa3ae64759f3dcc0e6`** | **2,963,789** |

An old copy that hashes to the superseded value is diagnosable, not suspect.

### Changed

- **`combined.html`** — seven display loci, executed as a line-indexed pass with a per-line anchor assertion: masthead `81 → 82` objections and `140 → 142` connections (L1727); `catalogs 81 ways → 82` (L2469); `close reading of all 81 → 82 entries` in all three methodology panels (L1650, L1783, L1873); the DEP_GRAPH_DATA drift note `245 vs 254 → 245 vs 255` (L10536).
- **Robustness line (L1652)** — was `the sole drag on 32 of 81 nodes`, a figure that goes stale whenever a single node is regenerated, which is how it went stale. Now `the sole weakest axis on 31 of 82 nodes and tying for weakest on 34 more`. Both figures recomputed independently from `rebuttal_grading_ledger.json`.
- **`README.md`** — pin table takes the v4.0.1 identifier, the new md5 and the new byte count; grade distribution corrected from the pre-v4.0 `n=81: A 36 / B 34 / C 11` to **`n=82: A 28 / B 53 / C 1 / 0 ungraded`**, recomputed from the ledger.
- **`libraries/index.html`** — front-door badge `pinned v4.0.0 → v4.0.1`.
- **`efilist_argument_library_v4_0_0.json`** — `version` field only. **Filename stays frozen**, per convention.

### Held — deliberately not swept

- **`combined.html` L1722** — *"The 35 mechanism clusters were derived bottom-up from the original 81 objections…"* `original` makes it historically exact; it is the sentence explaining why the mechanism count holds at 35 across v4.0, and it is an on-screen beat in the showcase film. Sweeping it to 82 would replace a true claim with a false one. **Flagged do-not-touch: a future count sweep must not "fix" it.**
- **`<span>35</span> MECHANISMS`** — unchanged; the eighty-second objection reused existing mechanisms rather than minting a thirty-sixth.
- **The `.jsx` provenance line** — its only `4.0.0` records that *"the v4.0.0 cut folded at K219 (2026-07-11)"*, which is true history, not a live version stamp. Re-stamping it would falsify a dated record — the same error class as L1722. Not stamped.
- **`rebuttal_grading_ledger.json`** — carries no version field to stamp.

### Open

- **Invariant defect: `DEP_GRAPH_DATA` per-node stored link sums total 245 against an actual 255.** Fields left in place; strip in a post-release maintenance pass. **Do not strip during video production** — it mutates the data literal and re-opens render risk on a filmed artifact.

## [v4.0.0] — 2026-07-11

**MINOR** by the invariants convention (invariants subtree mutated — the first corpus-topology change since the v3.8.0 cut), released as the **v4.0.0 content cut**. Invariants anchor `c18693f413066e1916eb6281a376d2db` → `f5347636b5becaf25e4759b620090118` (the v3.8.0-era anchor predates the v3.9.12 graph-invariant resync; both prior states preserved in canon history).

### Added

- **`self-effacing-under-universalization`** — objection #82, Tier 5 / Meta-Objection, the Kantian universalizability charge ("even if true, 'do not procreate' cannot be universal law"). Full three-depth response triple, library-authored and cold-graded (long **89.8 A**, medium 88.1 A, short 86.0 B; unrounded means banded per the ratified convention). Mechanism web: **Category Error** (primary) + **Formal Logic Attack** — adjudicated EXISTING, mechanism #36 mint rejected; `mechanism_count` holds at 35. Dependency graph: one weak `benatars-asymmetry` link (the residue routes to the asymmetry cluster). Reciprocal disambiguation folded onto `self-defeating` (keywords + diagnosis pointer; the memetic and deontic forms now fence each other off explicitly).
- **Plain-language card** for the new objection (ROUTED register) and a per-node `register` field on all seven Tier-5 layman entries, per the ratified T5 register-dispositions sidecar — promoted this release from `v4_staging/` to the repo root as a durable canon call.
- **`layman_index_validator_v0_4.py`** — register-keyed T5 gate (defanged inherits the T4 hard defeat-vocabulary gate; routed exempt; unclassified register-tier nodes fail). `--warn-tiers` retires.

### Changed

- **`contractualism-scanlon`** responses regenerated wholesale against the strongest modern ex-ante / hypothetical-consent form (Frick engine, Kumar type-standpoint, the proxy-consent analogy battery). Identity fields byte-locked; sources gain Frick, Kumar, and the Reibetanz/Otsuka ex-post critiques. Ledger row superseded under regeneration discipline: headline **B → A** (long 90.6 A / medium 88.9 A / short 86.8 B). The plain-language card is re-mirrored to the regenerated short (the K202 reveal no longer serves a stale mirror).
- Counts across all four surfaces: corpus **81 → 82** objections (tier split 13/17/14/31/**7**, 246 responses), mechanism web **116 → 117** nodes / **140 → 142** links, dependency graph **94 → 95** nodes / **254 → 255** links (167 strong / 88 weak), grading ledger 82 rows, objections-index + flagship layman index 82 entries (layman `schema_version` → `layman_index_v0_3`, `source_index_pin` rotated).
- `combined.html` **v3.9.16 → v4.0.0** (`6dfeb5d4`/2,955,840 → `e654eabd32fa95e5969d49e6eb15aa87`/2,963,752). Canon **v37.40 → v38.0** (MAJOR: invariant block revised). Corpus/JSX filenames minted at `_v4_0_0`, v3_8_0 pair archived.

---

## [v3.8.3] — 2026-05-30

**PATCH** over v3.8.0. `joy-outweighs-harms` long-form strengthen + the batched index/combined surface-parity reconciliation. Invariants subtree byte-identical (anchor `8727787c…`); corpus taxonomic content unchanged at 81 objections.

### Changed

- **`joy-outweighs-harms.responses.long`** re-authored 3,184 → 8,159 chars. The old soundness floor was an etiology-masquerading-as-axiology equivocation (suffering-as-deterrent wielded against a commensurability claim); the new architecture concedes the hedonic scale and a net-positive aggregate, then wins on the **separateness of persons / the unit-switch** — "outweighs" is true of the ensemble and false as a justification to the one who bears the bad. Ledger axes → `{v0.87, s0.83, c0.83, r0.82, a0.80}`. `long.rsi_pct` **76.6 → 83.0**; `long.grade` **C → B**; `headline_grade_long` C → B.
- **Derive-at-render lift (VAR/masochist posture).** This node stores only the long tuple; medium/short are derived at render. The long lift therefore re-derives the displayed shorter tiers: **medium 75.0 D → 81.3 C, short 72.8 D → 79.2 C** — every tier rises, both shorter tiers cross D→C, and the short/medium **prose is byte-identical** (no authoring).
- **`combined.html`** `REBUTTAL_STRENGTH['joy-outweighs-harms']` base axes → `{v0.87, s0.83, c0.83, r0.82, a0.80}` (renders long 83.0 B / medium 81.3 C / short 79.2 C via `depthModifiedRSI`).
- **`rebuttal_grading_ledger`** refreshed for the joy axes overwrite + `depths_note`.

### Changed — batched index surface-parity (the deferred MINOR, executed here)

The index score layer had lagged the ledger since the v3.8.1/.2 foldins (a deliberate accumulate-then-batch deferral). All three were reconciled in one pass:

- **`violence-as-reductio`** index `REBUTTAL_STRENGTH` `{v0.86,s0.82,c0.84,r0.84,a0.83}` (83.8) → `{v0.87,s0.85,c0.87,r0.86,a0.86}` (**86.2 B**) — matches ledger/combined.
- **`negative-util-aggregation`** index `{v0.85,s0.80,c0.85,r0.75,a0.75}` (79.9) → `{v0.86,s0.83,c0.86,r0.82,a0.83}` (**84.0 B**).
- **`joy-outweighs-harms`** index → `{v0.87,s0.83,c0.83,r0.82,a0.80}` (**83.0 B**).
- After this pass, **index == combined == ledger** for all three nodes. No fourth node touched.

### Attestation

- Canon **v37.2 → v37.3 MINOR** (additive `archive_attestation.v3_8_3`; invariants subtree byte-identical, anchor `8727787c…` held pre==post; 81/35/5 unchanged).
- Gates **G1–G6 PASS** (long md5 `7d2ac7b2…` in corpus/jsx/index/combined; short/medium byte-stable; combined renders 83.0/81.3/79.2; index `REBUTTAL_STRENGTH` == ledger for the 3; corpus/jsx/combined parse clean @81; canon v37.3 MINOR). Validator **v1.7 self-test green** (exit 0, `_overall_pass: true`); **corpus `verdict: PASS`** (zero blocking violations).
- Project version classifier: **PATCH-class v3.8.3** (invariants byte-identical to v3.8.0).

### Per-file integrity contract (current working set)

| Artifact | File (local frozen base) | md5 | Size |
|---|---|---|---|
| single-file | `combined.html` ← `combined_v3_8_0.html` | `dbbbc6d1b993b20064ad0a6d9f27b051` | 2,346,607 |
| corpus JSON | `efilist_argument_library_v3_8_0.json` | `36febc9a80e9ffb8af5f5425a3cdad90` | 1,261,374 |
| JSX | `efilist_argument_library_v3_8_0.jsx` | `133945446fbafa12039ae3599c056448` | 1,202,078 |
| index HTML | `index_v3_8_0.html` | `84ad36b948923974ec6eff21a056325d` | 1,800,126 |
| coda | `coda_v3_7.html` | `654f56cf29d9a808fc870dda4c98b3cc` | 11,040 |
| validator | `v3prime_validator_v1_7.py` | `2cfb638d9a95aec20cd890a22e3b9263` | 22,322 |
| RWE schema | `real_world_examples_schema_v1_7.json` | `13ca1171725b8652dffc04b864692d40` | 80,202 |
| grading ledger | `rebuttal_grading_ledger_v3_8_0.json` | `a09946844ec9a2a967b8f965d1cae3d8` | 41,879 |

> Filenames carry a **frozen `_v3_8_0` base** (the MAJOR-cut marker); content advances in place through v3.8.1/.2/.3. The release is identified by git tag, not the filename. See the push handoff for repo-naming options.

---

## [v3.8.2] — 2026-05-30

**PATCH** over v3.8.0. `negative-util-aggregation` long-form strengthen. Invariants subtree byte-identical (anchor `8727787c…`).

### Changed

- **`negative-util-aggregation.responses.long`** re-authored 1,958 → 7,276 chars. Retired the consent-bolt-on (category error) + feasibility-dodge; installed a clean three-conjunct fork + begs-question diagnosis + de-idealization ledger move + layer-1/layer-2 split + an owned maximizing-NU concession. Ledger axes → `{v0.86, s0.83, c0.86, r0.82, a0.83}`; `long.rsi_pct` **79.9 → 84.0**; `long.grade` **C → B**; `headline_grade_long` B. Short 76.2 C / medium 78.3 C held byte-stable.
- **`combined.html`** `REBUTTAL_STRENGTH['negative-util-aggregation']` → `{v0.86,s0.83,c0.86,r0.82,a0.83}` (84.0 B).

### Attestation

- Canon **v37.1 → v37.2 MINOR**; invariants byte-identical (`8727787c…`). Surface-mutation gates 7/7 PASS.

---

## [v3.8.1] — 2026-05-30

**PATCH** over v3.8.0. `violence-as-reductio` long-form strengthen + jsx node-parity closure. Invariants subtree byte-identical (anchor `8727787c…`).

### Changed

- **`violence-as-reductio.responses.long`** strengthened on the NU-centrality seam, 11,795 → 16,595 chars. Regraded **83.8 → 86.2 B** (+2.4). Ledger short/medium deterministic backfill (80.1 C / 82.2 B) + `depths_note`.
- **`combined.html`** `REBUTTAL_STRENGTH['violence-as-reductio']` base axes → `{v0.87,s0.85,c0.87,r0.86,a0.86}`.

### Fixed

- **JSX node-parity closed.** The JSX `OBJECTIONS` array was regenerated from corpus to **81 nodes** with **7 `archetypeVariants`** propagated; the legacy `if_*` archetype keys were retired in favor of `responses.archetypeVariants`. JSX data parity with the corpus is now complete (the React *component* render path remains v3.7-era — see Known limitations).

### Attestation

- Canon **v37.0 → v37.1 MINOR**; invariants byte-identical (`8727787c…`). Gates 7/7 PASS.

---

## [v3.8.0] — 2026-05-30

**MINOR** (3.7 → 3.8). The structural cut the v3.7 line deferred. **The invariants subtree was mutated** — anchor `f6b94bf0…` → `8727787c…`. This is the first topology change since v3.7-stable, executed as one atomic phase-1 MAJOR cut (canon **v36.1 → v37.0**; deep-diff = 15 intended changes, historical records byte-identical).

### Added — taxonomy

- **+3 objections (78 → 81):**
  - `eliminativism` (**T4**) — eliminativism / illusionism about phenomenal valence ("suffering isn't really *bad* / it's just chemicals") deployed to dissolve the harm premise.
  - `solipsism` (**T4**) — only one's own mind is certain, so others' suffering can't ground the harm claim.
  - `suffering-as-meaning` (**T2**) — suffering confers meaning / growth, so it is not a harm to be prevented.
- **+1 mechanism (34 → 35):** `mech_Metaphysical_Deflation` (genuine-engagement type), minted from the `eliminativism` node.

### Changed — topology & schema

- **Dependency graph** 91 → **94 nodes** (81 objections + 13 premises) / 245 → **254 links** (161 → **167 strong** / 84 → **87 weak**).
- **Mechanism web** 112 → **116 nodes** (35 mechanisms + 81 objections) / 133 → **140 links**.
- **Map 1 held at 78 nodes / 2,886 edges** — the 3 new objections are not Map-1-represented; `MAP1_TRANSITIONS` is byte-identical.
- **`if_*` archetype keys retired → `responses.archetypeVariants`** (7 archetypeVariants side-cars spliced across corpus/jsx/combined/index).
- **`refutationalVariants` → `objectionSubforms`** (renamed across all four surfaces).
- **RWE schema v1.6 → v1.7** (`real_world_examples_schema_v1_7.json`); **validator v1.6 → v1.7** (`v3prime_validator_v1_7.py`).
- `totalEntries` 78 → **81**; `totalResponses` 238 → **243**.

### Unchanged

- 5 tiers; 13 premises (9 foundational + 4 diagnostic); 136 attested real-world deployments / 171 attachment edges (the 3 new objections carry no deployments yet — 78/81 objections are attested in the wild).

### Attestation

- Canon **v36.1 → v37.0 MAJOR** (one atomic cut). New invariants anchor `8727787c…`. Base surfaces were `index_v3_7_6.html` / `combined_v3_7_6.html`.

> **Note on v3.7.4 → v3.7.6.** Between the published v3.7.3 and the v3.8.0 cut, the v3.7 line continued with operator-elective content-advance micro-releases (v3.7.4–v3.7.6, benatar short/medium refinements) that were not separately tagged in this public repo; they are folded into the v3.8.0 base. The v3.8.0 cut supersedes them.

---

## [v3.7.3] — 2026-05-23

**PATCH.** `benatar-asymmetry-attack` long-form strengthen + ledger sync re-cut. Invariants subtree byte-identical to v3.7-stable (anchor `f6b94bf0cb3e6832dbdde0017b876e54`); corpus taxonomic content unchanged at 78 objections.

### Changed

- **`benatar-asymmetry-attack.responses.long`** strengthened from 4904ch single-paragraph to 8205ch four-paragraph treatment. Ledger axes re-cut to `{v0.88, s0.81, c0.80, r0.78, a0.84}`. `long.rsi_pct` 78.3 → 82.13; `long.grade` **C → B**; `headline_grade_long` C → B. Short/medium forms held verbatim per v28.2 cold-grade convention.
- **Danger quadrant** (deployment × grade): with the `benatar-asymmetry-attack` regrade, the corpus's two highest-deployment objections (`violence-as-reductio` cleared at v3.7.2, `benatar-asymmetry-attack` cleared here) are both B-band. No nodes remain in the danger quadrant; empty at v3.7.3.
- **`combined.html`** re-synced to v3.7.3 corpus (md5 `29f9d5c0d4befac52dae4ca88ea4211f`, size 2,243,165).
- **`rebuttal_grading_ledger.json`** refreshed for benatar axes overwrite (md5 `9b0b291fe4818587e3d724a7d6daf017`).

### Added

- **`rwe.html`** — fourth view-tab artifact (stats view). Sidecar; not wired into the in-app hash router.
- **`v3_7_cut_invariants.json`**, **`corpus_statistics_spec.md`**, **`sort_feature_spec.md`**.

### Attestation

- Harness `invariant_derivation_harness_v1` GREEN (exit 0). Surface-mutation gates 9/9 PASS. Canon v29.0 → v30.0. Project terminal state → `archived_v3_7_3_stable`. PATCH-class; NOT v3.8.

---

## [v3.7.2] — 2026-05-17

**PATCH.** Content-advance re-cut + publication reconciliation. Structural invariants byte-identical to v3.7 line; 78 objections.

- **`violence-as-reductio.responses.long`** strengthened (11,795 chars). Regraded **C(≈0.805) → B(≈0.838)**. The single most-deployed objection (27 RWE) cleared the danger quadrant.
- **`benatar-asymmetry-attack.responses.long`** strengthened (4904 chars). Blind re-grade C78.3 → C80.7 — band unchanged at v3.7.2 (cleared at v3.7.3).
- **Rendered-counter chrome** corrected from pre-sweep `74 / 222` to canon-attested `78 objections / 245 dependencies` (length-preserving, byte-neutral).
- **Pre-cut ledger sync**: four formerly-ungraded nodes entered `/grades`; ungraded 4 → 0. All 78/78 graded.

---

## [v3.7.1] — 2026-05-14

**MINOR-bookkeeping reconciliation** over v3.7-stable: 77→78 objection-count reconciliation. Single-file `combined.html` shipped (md5 `dd2abd01…`) absorbing library + RWE + coda behind the outer hash router. Public tag `v3.7.1`.

---

## [v3.7-stable] — initial publication

**MINOR.** Authoritative corpus published: 78 objections / 5 tiers / 34 mechanisms / 13 premises (9 foundational + 4 diagnostic) / 91 dependency-graph nodes / 245 dependency links (161 strong / 84 weak) / 112 mechanism-web nodes / 133 mechanism-web links / 2,886 Map 1 transition edges / 136 attested real-world deployments. RWE schema v1.6. Validator v1.6.

---

## Provenance

v3.8.x entries are constructed from canon v37.3's `archive_attestation.v3_8_*` blocks, the `rebuttal_grading_ledger`, and direct corpus/canon-invariant reads (objection/mechanism set-diffs against the v3.7 baseline). v3.7.x entries are carried from the prior changelog (canon v33.0 attestation). Where summaries cite axis tuples, RSI percentages, or md5/byte deltas, those numbers are canon-attested at the release moment they describe.

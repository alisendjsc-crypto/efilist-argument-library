# Flagship ↔ Adversarial interconnection — DESIGN v0.2

**Supersedes v0.1 (K350, never committed) after the library seat's return and Josiah's rulings.**
Status: DESIGN. Nothing built. No byte moves. Not a pin-move session.
Re-derived 2026-09-18 operator-local: efilist `d869809` · wuld `270e797` · pin
`72187f6cf0fccdf8e9f4ec6ca5ce009c` / 2,982,770 · corpus `04bf6482aa0374ee92a81c1d55ec41f8` ·
x-surface `6cd132ee5b8c7ca78ad0e095806f1c93` **GREEN** · assembly v1_2, 138 entries.

---

## WHAT CHANGED FROM v0.1, AND WHY

v0.1 got the constraint right and the consequence wrong.

| v0.1 said | v0.2 says | who moved it |
|---|---|---|
| block **all** of direction one on strongest-vs-repairable | block **(a)** only; **(d) ships** | library seat — and it is worth 20 cards |
| direction two is "nearly free"; the locus gap is a **cost** | it is a **broken link**, and one mechanism fixes it | library seat |
| two options: prose depth (v1) / hash router (v2, pin move) | **one** level-independent affordance, built **first** | library seat; v0.1's split withdrawn |
| 0a: recommend new root | **HR-15 RATIFIED** | Josiah |
| "1 of 39 (d) routings names three bedrocks" | **1, 2 or 10 — definition-sensitive** | re-measured; the ground is weaker than credited |

---

## 1 — `ccclxxiv` IS THE MASTER CONSTRAINT, SO THE ORDER IS MECHANISM FIRST

`combined.html` initialises `let responseLevel = "medium"` (L10278). The map is authored
**7 entries on 5 cards** at `medium` and **77 entries on 72 cards** at `long`. Everything the
reader-facing layer wants to show lives behind a control nothing prompts them to move.

The seat that registered `ccclxxii` calls this its own miss, and names the reason precisely: the
counter-discipline it wrote — *enumerate every condition and evaluate them over the corpus* — is
what pointed at the data and away from the default. **A counter-discipline that redirects attention
is also one that blinds.** Both seats now hold that, and it is in `ccclxxiv`'s counter-discipline:
partition the conditions, count the data ones over the corpus, **read the initializer** for the UI
ones, and report both numbers saying which is which.

**Consequence for this design: no content decision matters until the mechanism exists.**

---

## 2 — THE MECHANISM (build this first)

**A badge that renders at any `responseLevel` and, on activation, forces the level** — switches to
`long` and scrolls to the locus. One mechanism serves both directions: the inbound deep link from
the map's own surface, and the outbound (d) layer on the card.

**Why not flip the default to `long`.** Rejected on register grounds, not on effort. The depth
ladder is a deliberate reading register and the default is every visitor's first impression. The
affordance forces the level for the reader who asked; the default keeps serving the reader who
did not.

**Its disposition, checked rather than assumed.** It renders no map content, so it is **not** a
stance-layer change and does not wait on R4. It **does** move a flagship byte, so it **is a pin
move**: its own deliberate, isolated session, which forces a same-session search-index regen and
objection re-vendor.

**Why the existing covenant is not enough.** `anchor_stability_covenant` (v37.39) is append-only and
self-tested and it covers the **card** — `#obj-<id>`. It says nothing about the **locus**, and
**82%** of all 98 `answered_by` refs (89% within the ship-now subset) point at `#long`. Without the
affordance, "where do we answer this?" lands a reader four times in five on a card opening at
`medium`, where the answer is not.

---

## 3 — THE CLASS SPLIT: (d) SHIPS, (a) WAITS. Ruled, with one refinement.

**The library seat's argument, which I accept.** An **(a)** claims *we answer this*; if the mapped
move was not the strongest, a stronger unmapped move might be unanswered, so the claim overreaches.
A **(d)** claims *this line terminates at bedrock we have named and hold our position across*; a
stronger unmapped move reaches the same or deeper bedrock and does not falsify the card, which never
claimed exhaustiveness.

**And the structural leg is the one that settles it.** (d) is *by construction* the class where the
repairable search failed. The class law adjudicates a → c → b/d, and a repairable-hunting author
lands on **(b)**, the regen-candidate class. Reaching (d) required finding no fixable clause.
**A repairable-hunting author cannot have manufactured a false (d).**

**My refinement, which the seat did not state and which is part of the ruling.** The licence holds
only under a label that claims **terminus**, not **strength**. Under a heading like *"the strongest
objection to this answer"*, a (d) card makes exactly the overreaching claim the (a) card makes, and
R1 bites it just as hard. Under *"where this line terminates"* it does not. **The label is
load-bearing.**

**The ship set: 20 pure-(d) nodes.** 20 entries, 19 at `#long` and 1 at `#diagnosis`, and — measured
— **all 20 authored pre-F**, which is exactly why the asymmetry matters: R1 would otherwise have
killed every one of them. **Zero new reader-facing text**: a (d) needs its bedrock named, and the
register's glosses already read.

| Class | Disposition | Gate |
|---|---|---|
| **(d)** pure, 20 nodes | **SHIP**, terminus label | the affordance |
| **(a)** | WAIT | R1 |
| **(b)** | WAIT | R2 + repairs |
| **(c)** | never | class law — not a continuation of its node's dialectic |

---

## 4 — WHAT JOSIAH AND THE LIBRARY SEAT STILL OWE

| # | Ruling | State |
|---|---|---|
| **R3** | HR-15 | **CLOSED.** Ratified K350. |
| **R1** | strongest-vs-repairable | **OPEN** — releases the (a) surface. Scope corrected: (a) only. |
| **R2** | may a (b) be reader-facing | **OPEN** — my position: OPEN label, or gate only the 5 headline-only-(b) cards and publish the other 21. |
| **R4** | the `/combined` graft | **OPEN** — Josiah **and** the library seat, then an isolated pin-move session. The affordance does **not** wait on it. |

---

## 5 — THE THREE FIGURE RECONCILIATIONS

Two are definitional. The third says something.

- **Default-view reach.** Mine: 7 of 82 cards (`medium` ∪ the always-on `diagnosis` section).
  Theirs: 7 entries on 5 cards (`medium` only). Re-measured: medium 7 entries / 5 cards, diagnosis
  2 / 2, union 9 / 7. Both true of what each measured.
- **Answer targets at `#long`.** Theirs 82% = 80 of all 98 refs. Mine 89% = 66 of the 74 ship-now
  refs. Quote **82%** for the mechanism, **89%** for the ship set.
- **(d) routings naming three bedrocks — neither of us.** Raw distinct tokens ≥3: **10 of 39**.
  Alias-normalised, counting `K224 carry-forward` as an HR-03 reference: **2**. Alias-normalised
  with it correctly excluded — it names the carry-forward **bar**, a routing prohibition, not a
  bedrock: **1**. `terminus_routing` is free text, so **a count over it is a count of a normalizer**,
  and the normalizer moves the answer by an order of magnitude. My "unique in 39 adjudications" was
  true only under a judgment call I made silently. **No consequence for the ruling** — HR-15 rests
  on the structural argument, which is definition-free — but the scatter ground is corroborative at
  best and the record now says so.

---

## 6 — RECOMMENDED SEQUENCE (the seat's, adopted)

1. **Build the fold.** Amend `adv_map_phaseG_v0_1.json` in place on the K338 precedent → assembly
   v1_3 → register v0_4 (HR-15; `HR-06 depends_on HR-15`, `HR-15 sibling_of HR-03`) → render →
   controls. Validator stays v0_6, which is why the amendment route beats minting a phase letter.
2. **The level-independent affordance** — its own isolated pin-move session.
3. **Ship direction two and the 20 pure-(d) cards on it**, under a terminus label.
4. **R1**, which releases (a). Then **R2**, which releases (b).

**Still not recommended:** "55 cards now, 26 after the repairs." The 26 were never the gate.

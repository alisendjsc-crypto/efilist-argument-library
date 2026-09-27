# layer/ — the house layer's sources

`site/wuld-layer.css` and `site/wuld-layer.js` are **packs**, served as-is from `site/` and linked
by every library page. These are the parts they are packed from. `layer/` is outside `site/`, so
nothing here is served.

## Change the layer

1. Edit a part in `layer/src/`. Never edit the packed files.
2. `python3 layer/pack_layer.py` writes both packs.
3. `python3 layer/pack_layer.py --check` is the gate. It must print `GATE GREEN`.
4. Commit the part and both packs together, by name.

A layer change does not move the pin. The flagship links the layer and does not inline it.

## The parts, in pack order

| part | carries |
|---|---|
| `wuld-type.css` | the type scale, the warm cast as colour |
| `wuld-bezel.css` | the frame, the chin and its LEDs, the first-visit hint, per-card feedback (`.wz-fb`), the walkthrough |
| `wuld-vfx.css` | the vfx tier: vignette, focus, bloom, glow, camera pan, peripheral blur, phosphor |
| `wuld-vfx.js` | power-button tiers, the camera pan and the blur opacity it drives, the focus, the magnifier (first part, no banner) |
| `wuld-sfx.js` | sound cues and room tone |
| `wuld-fb.js` | per-card feedback |
| `wuld-tour.js` | the per-view walkthroughs |
| `wuld-furniture.js` | the tail: the frame's markup, injected at the end of `<body>`, then boot (no banner) |

## Where these came from

Restored at WI-K410 (2026-09-26). The K313c packer said to edit the sources in `build/`, but that
folder was never committed to any repo. The packer survived in wuld-ink as
`archive/measurement/k313c_packlayer.py`, so the served packs were split back into parts by its own
banners and re-packed byte for byte equal. `pack_layer.py`'s docstring records its two changes from
K313c.

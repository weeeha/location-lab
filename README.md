# Location Lab

Scout a real place in the browser, then hand it to Seedance 2.0.

Location Lab loads a Gaussian splat of a captured location, lets you fly a camera through it,
mark stills and record camera moves, and exports a reference pack for Seedance's
reference-to-video mode. A clean-angle map shows where the capture is sharp, so you pick
angles that render well before you render them.

## Status

Design phase. The first screen draft is in
[`drafts/2026-10-21-scouting-screen/`](drafts/2026-10-21-scouting-screen/index.html).
It uses a drone frame of Silo No. 5 in Montreal's Old Port as a stand-in for the splat.

## How it fits

```
drone + 360 footage ─► Postshot (splat + COLMAP cameras) ─► Location Lab ─► places pack ─► Seedance
```

The export is a folder: `card.md` with the canonical description, ordered reference stills,
and links to rendered camera-move clips.

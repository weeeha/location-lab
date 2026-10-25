# Location Lab

Notes for any agent working in this repo.

## What this is

A browser tool that turns a real place, captured as a Gaussian splat, into Seedance 2.0
reference material. You load a trained splat, fly a camera through it, mark stills and
record moves, then export a **places pack** that the Video Generation Pipeline already reads.

Part of Nick's film generation suite. Sibling repos, all under `~/ClaudeCode Projects/`:

| Repo | Role here |
|---|---|
| `Video Generation Pileline` ("Pileline" is the real folder name) | Consumes the exported pack. Pack format: `library/README.md` there |
| `Scene Builder V2 (3d editor)` | Visual tokens and the prompt-builder pattern (`lib/prompt.ts`) |
| `Film Maker App/design-system` | Components: shadcn/ui, Geist, Lucide |
| `My Films` | The Montreal film this is first used for (`montreal-film-*.md`) |

## Status

Design phase. No app code yet. The approved screen draft lives in
`drafts/2026-10-21-scouting-screen/` (a drone frame stands in for the splat render).

## Decisions (2026-10-21)

- **Interaction model: scout the location.** Free camera, mark stills, record moves, export
  one reusable pack per location. Chosen over a film-shot-list model and a camera-on-rails model.
- **Clean-angle map.** Training camera positions come from Postshot's COLMAP export. The splat
  is sharp near them and smears away from them; the map shows that live while scouting.
- **Splat only in v1.** Google 3D tiles / map context is v2.
- **Many locations.** The left rail lists locations; the first capture is Silo No. 5, Old Port.
- **Export = a places pack**: `card.md`, `refs/NN-*.png` in Image order, `urls.txt` for clips,
  plus `location.json` (splat path, marks, moves) so a location can be reopened and re-rendered.
  Local dev writes into the pipeline's `library/places/<name>/` through an API route; the
  deployed demo downloads a zip.
- **Clips** upload to Vercel Blob on Nick's personal account, because the pipeline rejects
  local video files. Seedance limits: up to 3 videos, 2 to 15 s each, 15 s combined.
- **Card text** is drafted by local Gemma 4 (vision) from the stills, then edited by hand.
- **Real city vs film city:** the capture locks layout and light; the prompt adds the
  post-collapse look.
- **Frame ratio** switchable per shot: 21:9, 16:9, 9:16.
- **Camera:** drone-style fly (WASD + mouse), orbit on a modifier key.
- **Moves:** keyframes with interpolation, fixed lens per move.
- **Look:** Scene Builder v2 tokens (ink `#0e0e12`, panel `#1a1a22`, gold `#ffc943`) with the
  Film Maker design system components. Dark only.
- **Platforms:** desktop Chrome and Safari. No mobile.
- **Repo:** public from day one. Portfolio listing stays off until Nick says ship.

## Planned stack

Next.js and react-three-fiber (same as Scene Builder v2), [Spark](https://sparkjs.dev/) for
splat rendering (.ply, .spz; needs three.js r180+), clips rendered frame by frame and encoded
in the browser with WebCodecs.

## Not in v1

Map tiles, splat training (Postshot on ArtPC does that), in-app Seedance generation,
characters or dolls.

## Rules

- No capture data in git: footage, splats, COLMAP solves and renders are gitignored. Drafts
  may use a few small frames.
- No GPS coordinates in committed files. DJI `.SRT` sidecars carry them.
- Copy that ships in the UI follows the unslop rules: verb + object labels, no invented numbers.

## Open questions

- Final name: "Location Lab" or "Datacenter".
- Whether Silo No. 5 plays the film's data center.
- Which 360 clips, if any, belong to Silo No. 5.

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

<!-- BEGIN:generation-family -->
## Sibling repos

This repo is one of seventeen related repos for Nick's AI-assisted films, from story and world
through images, 3D and previs, video and sound. They stay separate on purpose (different
stacks, no shared code). The same block sits in the AGENTS.md of every repo below except
Continuity Lab, whose `main` is still empty, and the same table sits in each README between
the `generation-family` markers; change it in all of them or in none.

| Stage | Repo | Local folder (always quote) | What it does | Stack |
|---|---|---|---|---|
| Story and worlds | My Films | `~/CodexProjects/My Films/My-Films` | Source of truth for the film worlds (MTL63, Sky Fleet): bibles, scenes, production plans, generated-image collections and the October 29 archive | Markdown, Python archive tool |
| Story and worlds | Storytelling Kit | `~/ClaudeCode Projects/StoryTelling Kit` | Deck of storytelling cards with artwork editions | Markdown cards, Node scripts, Next.js app in `web/` |
| Story and worlds | Film Writer | `~/ClaudeCode Projects/Film Writer and Planner` | World-first film development: characters, props, locations, scenes and shots, with the screenplay grown from them | Next.js, Drizzle, three.js |
| Craft and reference | film-craft | `~/ClaudeCode Projects/film-craft` | Craft rules, review criteria, measured film norms and dated tool tests, including the video model test | Markdown, Python measurement scripts |
| Craft and reference | Film Analyzer | `~/ClaudeCode Projects/Film Analyzer` | Frame-by-frame close reading of films as a multi-film viewer | Next.js, pnpm monorepo, Zod |
| Craft and reference | Look Tokens | `~/ClaudeCode Projects/Film Tool - Look Tokens` | A film's look as one token table; shot prompts are composed from tokens per tool | Next.js |
| Images | Film Design System | `~/ClaudeCode Projects/Image Generation Pipeline ` (trailing space) | Canon of characters, props and settings with curated reference images; image generation against it | Next.js, SQLite, Gemini |
| Images | Idea to Prop | `~/CodexProjects/idea-to-prop` | Workflow that keeps one prop design connected from concept image through 3D, VFX and fabrication | Python, Codex skill |
| 3D, previs and props | 3D Models | `~/ClaudeCode Projects/3D Models` | Text-to-3D through Meshy, a three.js viewer and gallery, Blender and procedural models | Next.js, react-three-fiber, Meshy API |
| 3D, previs and props | Scene Builder 3D | `~/ClaudeCode Projects/scene-builder-3d` | Shot-first 3D previs: build a set, place characters, frame shots with a camera, play the scene back | Vite, React, three.js, browser-only |
| 3D, previs and props | film-previz | `~/ClaudeCode Projects/film-previz` | Walk a world-model-generated set in the browser and save camera shots (spec stage) | Spec only |
| 3D, previs and props | Location Lab | `~/ClaudeCode Projects/Location Lab` | Scout a captured real place as a Gaussian splat and export a Seedance reference pack (design stage) | HTML drafts |
| 3D, previs and props | film-props | `~/ClaudeCode Projects/film-props` | 3D-printed props and pre-vis sets for the films, printed on the Bambu Lab P1S | CadQuery, STL, 3MF |
| Video | Video Generation Pipeline | `~/ClaudeCode Projects/Video Generation Pileline` ("Pileline" is the real folder name) | Seedance and Runway clients; reference packs in `library/` | Python CLI |
| Video | Local Video Pipeline | `~/ClaudeCode Projects/Local-Video-Pipeline` | Local video generation on the Art PC (RTX 3090): Wan 2.2 and MiniMax H3 in ComfyUI, previz command on the Mac | PowerShell, Python CLI |
| Video | Continuity Lab | `~/ClaudeCode Projects/Video Lab` | Find and repair inconsistencies between generated video shots | Next.js, SQLite, ffmpeg |
| Sound | Audio Generation Pipeline | `~/ClaudeCode Projects/Audio-Generation-Pipeline` | Speech (Qwen3-TTS, Higgs Audio v2), voice cloning, sound effects, on the Mac Studio and the Art PC | Python, shell, PowerShell |

GitHub, all under `weeeha/`. Public: `Video-Generation-Pipeline`, `Audio-Generation-Pipeline`,
`Film-Design-System` (renamed from `Image-Generation-Pipeline-`), `scene-builder-3d`,
`film-previz`, `idea-to-prop`, `Look-Tokens`, `location-lab`. Private: `My-Films`,
`storytelling-kit`, `Film-Planner-`, `film-craft`, `Film-Analyzer-`, `3d-models-playground`
(the 3D Models repo), `film-props`, `Local-Video-Pipeline`, `Video-Lab`.

Not in the family, on hold or unrelated: `FilmMaker` (earlier all-in-one film studio app),
`PropsMaker`, `Codex-Asset-Generation`, `Scene-Builder-v2`, `Runaway` (job research about the
company Runway, not the video tool).

Media folders that are not repos: `~/ClaudeCode Projects/film-craft-media` (film-craft's clips
and image trials, including the October 25 video test in `film-review-2026-10-24/`) and
`~/ClaudeCode Projects/My Films` (older film notes, specs and the 127-title frame study that
film-craft's measurement tools read).

### How they connect

Files mostly move by hand. Known, planned and wanted links:

- **Image → video (planned).** The Film Design System spec names Seedance reference-to-video
  as a later consumer of its canon. The video repo's `library/<category>/<name>/` packs
  (`refs/` + `card.md`) hold the same kind of thing as folders, so an export from the canon
  would land there.
- **3D Models → Scene Builder 3D and video (wanted).** 3D Models generates GLB files through
  Meshy, and Scene Builder 3D stores props as GLB. Nick wants generated models usable as
  previs props and as Seedance references; no step connects them yet. 3D Models also holds
  3D-printing work (toys, sculpture), which is unrelated to film.
- **Scene Builder 3D → video (planned).** Its roadmap milestone M9 exports a shot as a
  provider-neutral zip (grey guide clip, first frame, camera path, prompt) for manual upload,
  with Seedance as the first target. Its idle prototype, `weeeha/Scene-Builder-v2` (folder
  `Scene Builder V2 (3d editor)`), already packaged shots for Seedance.
- **Local video ↔ cloud video.** Local Video Pipeline is the local counterpart of Video
  Generation Pipeline: image-to-video from a first frame and a prompt, rendered on the Art PC
  GPU instead of through Seedance or Runway. Its `previz` command drops drafts in
  `~/Movies/Previz`; nothing moves them into the video repo or the Continuity Lab yet. MiniMax
  H3 drafts are for private previz only, so a distributed shot is made fresh with Wan or a
  cloud service.
- **Video → Continuity Lab.** The Lab imports existing clips into a project folder. Its own
  generation backend (`seedance-fal`, via fal.ai) is planned for its plan 5 and is separate
  from the BytePlus client in the video repo.
- **Audio → video (open).** Seedance 2.5 accepts audio references and the audio repo makes
  voices and effects, but no step connects them. The audio repo also serves OpenClaw's
  Speaker agent, which is unrelated to film work.
- **film-craft → both video repos (done, 25 October 2026).** film-craft's video model test ran
  50 clips: Seedance 2.0 and 2.5 and Runway Gen-4.5 through the Video Generation Pipeline client
  and Runway's web app, Wan 2.2 and MiniMax H3 through Local Video Pipeline's `render.ps1`.
  Verdict: Seedance 2.5 is the model to build on; results in film-craft
  `capabilities/video-model-test/results-day1.md`.
- **Storytelling Kit → film-craft.** The video test's original cards came from the kit's
  `artwork/editions/urban-post-collapse-v1/masters/`.
- **My Films ↔ film-craft.** film-craft's measurement tools read the frame study in
  `~/ClaudeCode Projects/My Films/frames`; its night study measured an MTL63 image batch. The
  My Films October 29 archive holds film-craft-media. Open: MTL63's production plan names no
  video model yet, and no MTL63 shot has been through the video test.
- **Location Lab → video (planned).** Its export is a Seedance reference pack, the same shape
  as the video repo's `library/` packs.
- **Look Tokens ← My Films.** Its demo content is a scene of the Montréal film, transcribed from
  the film's token file.
- **Overlaps with no link yet.** film-previz and Scene Builder 3D both do previs (generated
  walkable sets against sets built from props). Idea to Prop's fabrication end and film-props
  both end in a printed prop. Film Writer and My Films both hold world and story material.

### Working across repos

- Read the sibling's own AGENTS.md (or README) before changing it. Spend rules differ: image,
  3D and cloud video generations cost money and need Nick's go; audio and local video run on
  the Art PC GPU and can pause llama-server while they run.
- Don't copy code between repos. When a shared format appears (a canon export, say),
  document it in both repos it connects and update this block.
- Branch per task in each repo; never push to `main`.
<!-- END:generation-family -->

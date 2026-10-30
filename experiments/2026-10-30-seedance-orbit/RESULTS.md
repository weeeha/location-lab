# Seedance orbit to splat to mesh: results (2026-10-30)

**Status: questionable. Parked, not adopted.** The pipeline runs end to end on the Mac, but
neither the wide nor the close clip gave something usable as a set: the wide orbit is a
backdrop, the close orbit holds only near its path, and the mesh is a lumpy blockout.

## Question

Can a generated Seedance clip of an MTL63 location become a Gaussian splat, and then a 3D
model, good enough for previs?

## What was run

All three clips are image to video from `library/places/mtl63-rooftop/refs/01-wide.png` in
the Video Generation Pipeline, Seedance 2.5, 720p, no audio. Frames at 15 fps, COLMAP on
the CPU, Brush v0.3.0 for 15k steps, Spark for viewing.

| Run | Clip | Lens model | Frames placed | Point depth vs camera travel | Held-out PSNR |
|---|---|---|---|---|---|
| orbit v1 | `rooftop-orbit-v1.mp4`, 10 s, 60° arc from the wide view | PINHOLE: fx 1397, fy 383 | 81 of 151, split in 4 | 222 to 360 vs 12 | 35 to 37.6 dB |
| orbit v2 | same clip | SIMPLE_PINHOLE: 1319 | 151 of 151 | 220+ vs 11 | 36 to 37.6 dB |
| close v1 | `rooftop-close-orbit-v1.mp4`, 12 s, glide to 4 m then ~40° arc | SIMPLE_PINHOLE: 1220 | 181 of 181 | 6 to 11 vs 12 | 23 to 30 dB |

PSNR is the splat against held-out frames (every 10th) from the same clip, so it only tests
the camera path the clip already flew.

## What came out

- **Orbit v1:** the two focal lengths stretched the scene and split the clip. Off-path views
  bend the towers. Fixed in `run.sh` by forcing one focal length.
- **Orbit v2:** clean on its path and up to about 4x the path sideways, but no splat lies
  within 100 units of the camera. The rooftop is painted onto the same far shell as the
  skyline, so it is a backdrop. Nothing to mesh.
- **Close v1:** real depth on the workshop, planters and figure; they keep their shape when
  orbited 30 to 60° past the path. Everything beyond the roof edge smears, the sky streaks,
  and close-up detail is soft because Seedance redraws the workshop as the camera nears.
- **Mesh (close v1):** Poisson over 45,895 opaque splat centers, 160k triangles. Roof peak,
  open front and planter rows are in the right place at the right scale; surfaces are blobs.
  Layout reference at best.

## Why it is questionable

1. A generated clip is not a consistent scene. Seedance changes detail between frames
   (the workshop, a figure that vanishes), and the splat averages that into blur. A real
   capture would not do this.
2. Depth needs parallax: the camera must travel about as far as the subject is away. One
   clip cannot do that for both the near rooftop and the far city.
3. Splat centers are a poor surface. A clean mesh needs a surface-aware trainer (2DGS or
   similar) on a CUDA GPU.
4. Only one location and one first frame were tried. Nothing here generalises yet.

## If picked up again

- Short close orbits of one subject each, camera within one travel length of it.
- Try a surface-aware trainer on ArtPC's 3090 before judging meshes.
- Compare against TRELLIS image to 3D on the same frame, which may be the simpler route to a
  prop-sized model.
- Compare against a real drone capture of Silo No. 5, which is what Location Lab is for.

## Where things are

- Scripts and viewers: this folder (`run.sh`, `view_pose.py`, `mesh_from_splat.py`,
  `viewer.html`, `mesh.html`, both prompts).
- Clips: `Video Generation Pileline/output/rooftop-orbit-v1.mp4` and
  `rooftop-close-orbit-v1.mp4` (ledger rows in `output/ledger.csv`).
- Captures (gitignored, about 1.9 GB, local only): `captures/rooftop-orbit-v1/`,
  `rooftop-orbit-v2/`, `rooftop-close-v1/`, with run logs beside them. Comparison sheets:
  `rooftop-orbit-v2/splat/v1-vs-v2.jpg`, `rooftop-close-v1/close-orbit-results.jpg`,
  `rooftop-close-v1/clip-contact-sheet.jpg`. The mesh is `rooftop-close-v1/mesh.glb`.
- Viewing: serve the repo root (`python3 -m http.server 8765`) and open
  `experiments/2026-10-30-seedance-orbit/viewer.html` or `mesh.html`.

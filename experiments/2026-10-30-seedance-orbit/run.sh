#!/usr/bin/env bash
# Clip -> frames -> COLMAP cameras -> Brush splat, all on the Mac.
# Usage: run.sh <clip.mp4> <capture-name> [fps]
# Writes to captures/<capture-name>/ (gitignored): images/, colmap/, splat/.
set -euo pipefail

clip="$1"
name="$2"
fps="${3:-15}"
root="$(cd "$(dirname "$0")/../.." && pwd)"
out="$root/captures/$name"
brush="${BRUSH:-$HOME/.local/opt/brush-v0.3.0/brush-app-aarch64-apple-darwin/brush_app}"

mkdir -p "$out/images" "$out/colmap/sparse" "$out/splat"

echo "== frames ($fps fps)"
ffmpeg -loglevel error -y -i "$clip" -vf "fps=$fps" -q:v 2 "$out/images/%04d.jpg"
ls "$out/images" | wc -l

echo "== colmap features"
# One camera for the whole clip: a generated video has one fixed, distortion-free lens.
# SIMPLE_PINHOLE (one focal length): with PINHOLE the low-parallax v1 clip solved fx=1397, fy=383.
colmap feature_extractor \
  --database_path "$out/colmap/database.db" \
  --image_path "$out/images" \
  --ImageReader.single_camera 1 \
  --ImageReader.camera_model SIMPLE_PINHOLE \
  --FeatureExtraction.use_gpu 0

echo "== colmap matching (sequential, frames are in order)"
colmap sequential_matcher \
  --database_path "$out/colmap/database.db" \
  --SequentialMatching.overlap 15 \
  --FeatureMatching.use_gpu 0

echo "== colmap mapper"
colmap mapper \
  --database_path "$out/colmap/database.db" \
  --image_path "$out/images" \
  --output_path "$out/colmap/sparse"

# The mapper can split a clip into several models; train on the one with the most frames.
best=""; best_n=0
for m in "$out"/colmap/sparse/*/; do
  n=$(colmap model_analyzer --path "$m" 2>&1 | sed -n 's/.*Registered images: //p')
  echo "model $(basename "$m"): $n frames"
  if [ "${n:-0}" -gt "$best_n" ]; then best="$m"; best_n="$n"; fi
done
colmap model_analyzer --path "$best" 2>&1 | tee "$out/colmap/analysis.txt"

# Brush searches the dataset folder for any sparse/0, so give it a folder holding only the chosen model.
ds="$out/brush-dataset"
rm -rf "$ds"; mkdir -p "$ds/sparse"
ln -s "$out/images" "$ds/images"
cp -R "${best%/}" "$ds/sparse/0"

echo "== brush"
"$brush" "$ds" --total-steps "${STEPS:-15000}" --export-path "$out/splat" --export-every "${STEPS:-15000}" \
  --export-name splat.ply --eval-split-every 10 --eval-every 5000 --eval-save-to-disk
ls -la "$out/splat"

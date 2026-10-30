"""Write a start pose for the viewer from a COLMAP text model.

Usage: python view_pose.py <model_txt_dir> <out.json>
Camera = the middle registered frame; target = median of the sparse points.
Coordinates are flipped (x, -y, -z) to match the viewer's 180-degree X rotation.
"""
import json
import sys

import numpy as np


def quat_to_rot(qw, qx, qy, qz):
    return np.array([
        [1 - 2 * (qy * qy + qz * qz), 2 * (qx * qy - qz * qw), 2 * (qx * qz + qy * qw)],
        [2 * (qx * qy + qz * qw), 1 - 2 * (qx * qx + qz * qz), 2 * (qy * qz - qx * qw)],
        [2 * (qx * qz - qy * qw), 2 * (qy * qz + qx * qw), 1 - 2 * (qx * qx + qy * qy)],
    ])


model, out = sys.argv[1], sys.argv[2]
cams = []
with open(f"{model}/images.txt") as f:
    lines = [l for l in f if not l.startswith("#")]
for header in lines[::2]:
    p = header.split()
    q, t, name = list(map(float, p[1:5])), np.array(list(map(float, p[5:8]))), p[9]
    R = quat_to_rot(*q)
    cams.append((name, -R.T @ t, R.T @ np.array([0, 0, 1.0])))
cams.sort()
name, center, forward = cams[len(cams) // 2]

pts = np.array([list(map(float, l.split()[1:4])) for l in open(f"{model}/points3D.txt") if not l.startswith("#")])
# Orbit around the near scene (10th-percentile depth); the median sits on the far skyline.
depths = np.linalg.norm(pts - center, axis=1)
dist = float(np.percentile(depths, 10))
travel = float(np.ptp(np.array([c for _, c, _ in cams]), axis=0).max())

cam_line = [l for l in open(f"{model}/cameras.txt") if not l.startswith("#")][0].split()
w, h, fx, fy = int(cam_line[2]), int(cam_line[3]), float(cam_line[4]), float(cam_line[5 if cam_line[1] == "PINHOLE" else 4])

flip = np.array([1, -1, -1])
pose = {
    "frame": name,
    "camera": (center * flip).tolist(),
    "target": ((center + forward * dist) * flip).tolist(),
    "frames": len(cams),
    "points": len(pts),
    "camera_travel": travel,
    "intrinsics": {"w": w, "h": h, "fx": fx, "fy": fy},
    "depth_p10_p50_p90": np.percentile(depths, [10, 50, 90]).round(2).tolist(),
}
json.dump(pose, open(out, "w"), indent=2)
print(json.dumps(pose))

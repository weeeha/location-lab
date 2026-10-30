"""Rough mesh from a Brush splat: opaque splat centers near the cameras -> Poisson surface.

Usage: python mesh_from_splat.py <splat.ply> <model_txt_dir> <out.glb> [radius_x_travel]
Keeps splats within radius_x_travel (default 3) times the camera travel of the camera path,
so the far skyline (a flat backdrop in these clips) stays out of the mesh.
"""
import sys

import numpy as np
import open3d as o3d
from plyfile import PlyData

splat_path, model, out = sys.argv[1], sys.argv[2], sys.argv[3]
radius_k = float(sys.argv[4]) if len(sys.argv) > 4 else 3.0

v = PlyData.read(splat_path)["vertex"]
xyz = np.stack([v["x"], v["y"], v["z"]], axis=1)
opacity = 1 / (1 + np.exp(-np.asarray(v["opacity"])))
# Spherical-harmonic DC term to RGB.
rgb = np.clip(0.5 + 0.28209479 * np.stack([v["f_dc_0"], v["f_dc_1"], v["f_dc_2"]], axis=1), 0, 1)


def quat_to_rot(qw, qx, qy, qz):
    return np.array([
        [1 - 2 * (qy * qy + qz * qz), 2 * (qx * qy - qz * qw), 2 * (qx * qz + qy * qw)],
        [2 * (qx * qy + qz * qw), 1 - 2 * (qx * qx + qz * qz), 2 * (qy * qz - qx * qw)],
        [2 * (qx * qz - qy * qw), 2 * (qy * qz + qx * qw), 1 - 2 * (qx * qx + qy * qy)],
    ])


def cam_centers(model_dir):
    lines = [l for l in open(f"{model_dir}/images.txt") if not l.startswith("#")]
    out = []
    for header in lines[::2]:
        p = header.split()
        R = quat_to_rot(*map(float, p[1:5]))
        out.append(-R.T @ np.array(list(map(float, p[5:8]))))
    return np.array(out)


cams = cam_centers(model)
travel = np.ptp(cams, axis=0).max()
dist = np.min(np.linalg.norm(xyz[:, None, :] - cams[None, ::5, :], axis=2), axis=1)
keep = (opacity > 0.3) & (dist < radius_k * travel)
print(f"splats {len(xyz)}, kept {keep.sum()} (opacity>0.3, within {radius_k}x travel={travel:.2f})")
print("nearest splat distance, percentiles 1/10/50:", np.percentile(dist, [1, 10, 50]).round(2))
if keep.sum() < 1000:
    sys.exit("too few splats near the cameras to mesh: this capture is a backdrop, not a set")

pcd = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(xyz[keep]))
# glTF vertex colors are linear; the splat colors are sRGB.
pcd.colors = o3d.utility.Vector3dVector(rgb[keep] ** 2.2)
pcd, _ = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
pcd.estimate_normals(o3d.geometry.KDTreeSearchParamKNN(30))
# Point normals toward the nearest camera so Poisson knows which side is outside.
pts = np.asarray(pcd.points)
near_cam = cams[np.argmin(np.linalg.norm(pts[:, None, :] - cams[None, :, :], axis=2), axis=1)]
n = np.asarray(pcd.normals)
flip = np.sum(n * (near_cam - pts), axis=1) < 0
n[flip] *= -1
pcd.normals = o3d.utility.Vector3dVector(n)

# n_threads=1: the multithreaded Poisson aborts with "Failed to close loop" on these clouds.
mesh, density = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9, n_threads=1)
density = np.asarray(density)
mesh.remove_vertices_by_mask(density < np.quantile(density, 0.1))
mesh.compute_vertex_normals()
# COLMAP is y-down, z-forward; flip to y-up for viewers.
mesh.rotate(np.diag([1.0, -1.0, -1.0]), center=(0, 0, 0))
print(f"mesh: {len(mesh.vertices)} vertices, {len(mesh.triangles)} triangles")
o3d.io.write_triangle_mesh(out, mesh)

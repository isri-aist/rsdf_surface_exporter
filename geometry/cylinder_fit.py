import numpy as np


def fit_cylinder(points):
    pts = np.array(points)

    centroid = pts.mean(axis=0)

    cov = np.cov(pts - centroid, rowvar=False)
    eigvals, eigvecs = np.linalg.eigh(cov)

    axis = eigvecs[:, np.argmax(eigvals)]
    axis = axis / np.linalg.norm(axis)

    # project points onto axis
    projections = np.dot(pts - centroid, axis)

    min_proj = projections.min()
    max_proj = projections.max()

    width = max_proj - min_proj

    # compute radius
    radial_dist = []

    for p in pts:
        v = p - centroid
        proj = np.dot(v, axis) * axis
        radial = v - proj
        radial_dist.append(np.linalg.norm(radial))

    radius = np.mean(radial_dist)

    # center of cylinder
    center = centroid + axis * ((min_proj + max_proj) / 2)

    return center, axis, radius, width

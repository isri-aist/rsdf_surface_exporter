import numpy as np
from mathutils import Matrix, Vector


def compute_plane(verts):
    """
    Given 3+ vertices, compute:
    - origin (p0)
    - plane axes: x_axis, y_axis
    - normal vector
    - rpy angles (roll, pitch, yaw)
    """

    pts = np.array([[v.x, v.y, v.z] for v in verts], dtype=float)

    # Compute plane normal
    centroid_np = pts.mean(axis=0)
    centroid = Vector((centroid_np[0], centroid_np[1], centroid_np[2]))

    centered = pts - centroid_np
    cov = np.cov(centered, rowvar=False)
    eigvals, eigvecs = np.linalg.eigh(cov)

    normal_np = eigvecs[:, np.argmin(eigvals)]
    normal = Vector((normal_np[0], normal_np[1], normal_np[2])).normalized()

    # Define local axes
    x_axis_np = eigvecs[:, np.argmax(eigvals)]
    x_axis = Vector((x_axis_np[0], x_axis_np[1], x_axis_np[2])).normalized()

    y_axis = normal.cross(x_axis).normalized()
    x_axis = y_axis.cross(normal).normalized()

    # Build rotation matrix
    # Columns of matrix = local x, y, z axes
    rot_mat = Matrix(
        (x_axis, y_axis, normal)
    ).transposed()  # Blender expects columns as axes

    # Convert to Euler angles (RPY)
    rpy = rot_mat.to_euler("XYZ")

    return centroid, x_axis, y_axis, normal, rpy

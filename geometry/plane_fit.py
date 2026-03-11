from mathutils import Matrix


def compute_plane(verts):
    """
    Given 3+ vertices, compute:
    - origin (p0)
    - plane axes: x_axis, y_axis
    - normal vector
    - rpy angles (roll, pitch, yaw)
    """

    p0 = verts[0]
    p1 = verts[1]
    p2 = verts[2]

    # Compute plane normal
    v1 = p1 - p0
    v2 = p2 - p0
    normal = v1.cross(v2).normalized()

    # Define local axes
    x_axis = v1.normalized()
    y_axis = normal.cross(x_axis)

    # Build rotation matrix
    # Columns of matrix = local x, y, z axes
    rot_mat = Matrix(
        (x_axis, y_axis, normal)
    ).transposed()  # Blender expects columns as axes

    # Convert to Euler angles (RPY)
    rpy = rot_mat.to_euler("XYZ")

    return p0, x_axis, y_axis, normal, rpy

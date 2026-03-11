def project_to_plane(verts, origin, x_axis, y_axis):
    points = []

    for v in verts:
        rel = v - origin

        x = rel.dot(x_axis)
        y = rel.dot(y_axis)

        points.append((x, y))

    return points

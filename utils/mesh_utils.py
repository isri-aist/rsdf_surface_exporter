import bmesh


def get_selected_face_vertices(context):
    obj = context.edit_object
    mesh = obj.data

    bm = bmesh.from_edit_mesh(mesh)

    verts = []
    seen = set()

    for face in bm.faces:
        if face.select:
            for v in face.verts:
                if v.index not in seen:
                    seen.add(v.index)
                    verts.append(obj.matrix_world @ v.co)

    return verts

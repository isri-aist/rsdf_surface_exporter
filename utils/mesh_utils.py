import bmesh


def get_selected_face_vertices(context):
    obj = context.edit_object
    mesh = obj.data

    bm = bmesh.from_edit_mesh(mesh)

    verts = []

    for face in bm.faces:
        if face.select:
            for v in face.verts:
                verts.append(obj.matrix_world @ v.co)

            break

    return verts

import os

import bpy


def export_meshes(context, link_nodes, meshes_dir):
    """Export each link's mesh geometry to <meshes_dir>/<link_name>.stl.

    Meshes are written in the object's own local space (identity transform)
    so they line up with the matrix_local-derived joint origins in the URDF.
    Works on throwaway duplicates with their own mesh data copy so the
    user's actual scene objects and mesh data are never modified.
    """
    prev_selected = context.selected_objects[:]
    prev_active = context.view_layer.objects.active

    temp_collection = bpy.data.collections.new("RSDF_ROS2_Export_Tmp")
    context.scene.collection.children.link(temp_collection)

    try:
        for node in link_nodes:
            _export_single_mesh(context, node, temp_collection, meshes_dir)
    finally:
        for obj in list(temp_collection.objects):
            mesh_data = obj.data
            bpy.data.objects.remove(obj, do_unlink=True)
            if mesh_data is not None and mesh_data.users == 0:
                bpy.data.meshes.remove(mesh_data)
        bpy.data.collections.remove(temp_collection)

        bpy.ops.object.select_all(action="DESELECT")
        for obj in prev_selected:
            obj.select_set(True)
        context.view_layer.objects.active = prev_active


def _export_single_mesh(context, node, temp_collection, meshes_dir):
    obj = node.obj
    if obj.type != "MESH" or len(obj.data.vertices) == 0:
        return

    dup = obj.copy()
    dup.data = obj.data.copy()
    dup.parent = None
    dup.location = (0.0, 0.0, 0.0)
    dup.rotation_mode = "QUATERNION"
    dup.rotation_quaternion = (1.0, 0.0, 0.0, 0.0)
    dup.rotation_euler = (0.0, 0.0, 0.0)
    temp_collection.objects.link(dup)

    for o in context.selected_objects:
        o.select_set(False)
    dup.select_set(True)
    context.view_layer.objects.active = dup

    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    filepath = os.path.join(meshes_dir, f"{node.name}.stl")
    bpy.ops.wm.stl_export(
        filepath=filepath,
        export_selected_objects=True,
        apply_modifiers=True,
    )

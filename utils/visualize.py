import ast

import bpy


def get_green_material():
    """
    Create or get the standard RSDF green material.
    Works in Solid, Material Preview, and Render modes.
    """
    mat_name = "RSDF_Surface_Green"
    mat = bpy.data.materials.get(mat_name)

    if mat is None:
        mat = bpy.data.materials.new(mat_name)
        mat.use_nodes = True

        # Set Principled BSDF node
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.0, 1.0, 0.0, 0.4)
            bsdf.inputs["Alpha"].default_value = 0.4

        # Transparency
        mat.blend_method = "BLEND"
        mat.shadow_method = "NONE"

    return mat


def create_surface_mesh(surf, name_prefix="RSDF_Surface"):
    """
    Create a mesh in the scene to visualize the RSDF surface.
    Supports planar and cylindrical surfaces.
    Green color is shown in Solid and Material Preview.
    """

    obj = None

    # -----------------------------
    # PLANAR SURFACE
    # -----------------------------
    if surf.surface_type == "PLANE":
        points = ast.literal_eval(surf.points)
        if len(points) < 3:
            return None

        # Convert to 3D verts (Z=0)
        verts = [(x, y, 0) for x, y in points]
        faces = [tuple(range(len(verts)))]

        mesh = bpy.data.meshes.new(f"{name_prefix}_{surf.name}")
        mesh.from_pydata(verts, [], faces)
        mesh.update()

        obj = bpy.data.objects.new(f"{name_prefix}_{surf.name}", mesh)
        bpy.context.collection.objects.link(obj)

    # -----------------------------
    # CYLINDRICAL SURFACE
    # -----------------------------
    elif surf.surface_type == "CYLINDER":
        # 1. Create cylinder along Z
        bpy.ops.mesh.primitive_cylinder_add(
            radius=surf.radius, depth=surf.width, vertices=64
        )
        obj = bpy.context.active_object
        obj.name = f"{name_prefix}_{surf.name}"

        # Swap Z → X axis
        obj.rotation_euler.rotate_axis("Y", -1.57079633)  # -90° around Y

        # 3. Apply RSDF rotation (RPY)
        obj.rotation_euler.rotate_axis("X", surf.rpy_r)
        obj.rotation_euler.rotate_axis("Y", surf.rpy_p)
        obj.rotation_euler.rotate_axis("Z", surf.rpy_y)

        # 4. Move cylinder to origin
        obj.location = (surf.origin_x, surf.origin_y, surf.origin_z)

    else:
        return None

    # -----------------------------
    # Apply transform
    # -----------------------------
    obj.location = (surf.origin_x, surf.origin_y, surf.origin_z)
    obj.rotation_euler = (surf.rpy_r, surf.rpy_p, surf.rpy_y)

    # -----------------------------
    # Apply green material
    # -----------------------------
    mat = get_green_material()
    obj.data.materials.clear()
    obj.data.materials.append(mat)

    # -----------------------------
    # Solid mode / viewport display
    # -----------------------------
    obj.color = (0.0, 1.0, 0.0, 0.4)

    # Ensure transparency and display
    obj.show_in_front = True
    obj.display_type = "TEXTURED"

    # Optional: wireframe overlay
    obj.show_wire = True
    obj.show_all_edges = True

    return obj

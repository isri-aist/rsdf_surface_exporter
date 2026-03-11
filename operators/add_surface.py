import bpy

from ..geometry.cylinder_fit import fit_cylinder
from ..geometry.plane_fit import compute_plane
from ..geometry.projection import project_to_plane
from ..utils.mesh_utils import get_selected_face_vertices
from ..utils.rotation_utils import axis_to_rpy


class RSDF_OT_add_surface(bpy.types.Operator):
    bl_idname = "rsdf.add_surface"
    bl_label = "Add RSDF Surface"

    surface_type: bpy.props.EnumProperty(
        name="Surface Type",
        items=[("PLANE", "Plane", ""), ("CYLINDER", "Cylinder", "")],
        default="PLANE",
    )

    def execute(self, context):
        verts = get_selected_face_vertices(context)

        if len(verts) < 3:
            self.report({"ERROR"}, "Need at least 3 vertices")
            return {"CANCELLED"}

        surf = context.scene.rsdf_surfaces.add()
        surf.name = f"Surface_{len(context.scene.rsdf_surfaces)}"
        surf.surface_type = self.surface_type

        # ----------------------
        # PLANE
        # ----------------------

        if self.surface_type == "PLANE":
            origin, x_axis, y_axis, normal, rpy = compute_plane(verts)

            points = project_to_plane(verts, origin, x_axis, y_axis)

            surf.origin_x = origin.x
            surf.origin_y = origin.y
            surf.origin_z = origin.z

            surf.rpy_r = rpy.x
            surf.rpy_p = rpy.y
            surf.rpy_y = rpy.z

            surf.points = str(points)

        # ----------------------
        # CYLINDER
        # ----------------------

        elif self.surface_type == "CYLINDER":
            center, axis, radius, width = fit_cylinder(verts)

            rpy = axis_to_rpy(axis)

            surf.origin_x = center[0]
            surf.origin_y = center[1]
            surf.origin_z = center[2]

            surf.rpy_r = rpy[0]
            surf.rpy_p = rpy[1]
            surf.rpy_y = rpy[2]

            surf.radius = radius
            surf.width = width

        context.scene.rsdf_surface_index = len(context.scene.rsdf_surfaces) - 1

        return {"FINISHED"}

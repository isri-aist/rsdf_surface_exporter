import xml.etree.ElementTree as ET

import bpy

from ..utils.visualize import create_surface_mesh


class RSDF_OT_load_rsdf(bpy.types.Operator):
    bl_idname = "rsdf.load_rsdf"
    bl_label = "Load RSDF File"
    bl_description = "Load an RSDF XML file and display surfaces"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
        except Exception as e:
            self.report({"ERROR"}, f"Failed to parse RSDF: {e}")
            return {"CANCELLED"}

        context.scene.rsdf_surfaces.clear()

        loaded = 0

        # -------------------------
        # PLANAR SURFACES
        # -------------------------

        for surf_elem in root.findall("planar_surface"):
            surf = context.scene.rsdf_surfaces.add()
            surf.surface_type = "PLANE"
            surf.name = surf_elem.get("name", "Surface")

            origin = surf_elem.find("origin")
            if origin is not None:
                xyz = [float(x) for x in origin.get("xyz", "0 0 0").split()]
                rpy = [float(r) for r in origin.get("rpy", "0 0 0").split()]

                surf.origin_x, surf.origin_y, surf.origin_z = xyz
                surf.rpy_r, surf.rpy_p, surf.rpy_y = rpy

            points_elem = surf_elem.find("points")
            if points_elem is not None:
                pts = []
                for p in points_elem.findall("point"):
                    x, y = map(float, p.get("xy", "0 0").split())
                    pts.append((x, y))
                surf.points = str(pts)

            material_elem = surf_elem.find("material")
            if material_elem is not None:
                surf.material = material_elem.get("name", "plastic")

            create_surface_mesh(surf)
            loaded += 1

        # -------------------------
        # CYLINDRICAL SURFACES
        # -------------------------

        for surf_elem in root.findall("cylindrical_surface"):
            surf = context.scene.rsdf_surfaces.add()
            surf.surface_type = "CYLINDER"
            surf.name = surf_elem.get("name", "Cylinder")

            surf.radius = float(surf_elem.get("radius", 0.0))
            surf.width = float(surf_elem.get("width", 0.0))

            origin = surf_elem.find("origin")
            if origin is not None:
                xyz = [float(x) for x in origin.get("xyz", "0 0 0").split()]
                rpy = [float(r) for r in origin.get("rpy", "0 0 0").split()]

                surf.origin_x, surf.origin_y, surf.origin_z = xyz
                surf.rpy_r, surf.rpy_p, surf.rpy_y = rpy

            material_elem = surf_elem.find("material")
            if material_elem is not None:
                surf.material = material_elem.get("name", "plastic")

            create_surface_mesh(surf)
            loaded += 1

        if loaded > 0:
            context.scene.rsdf_surface_index = 0

        self.report({"INFO"}, f"Loaded {loaded} surfaces")
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

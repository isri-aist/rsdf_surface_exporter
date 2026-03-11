import bpy


class RSDF_PT_panel(bpy.types.Panel):
    bl_label = "RSDF Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RSDF"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="RSDF Operations:")
        row = layout.row()
        row.operator("rsdf.add_surface", text="Add Plane").surface_type = "PLANE"
        row.operator("rsdf.add_surface", text="Add Cylinder").surface_type = "CYLINDER"
        layout.operator("rsdf.load_rsdf", icon="FILE_FOLDER")
        layout.operator("rsdf.export", icon="EXPORT")

        layout.separator()

        layout.label(text="Surfaces:")

        layout.template_list(
            "UI_UL_list",
            "rsdf_surface_list",
            scene,
            "rsdf_surfaces",
            scene,
            "rsdf_surface_index",
        )

        row = layout.row()
        row.operator("rsdf.remove_surface", icon="TRASH")

        # Optional: show editable name and material for selected surface
        if len(scene.rsdf_surfaces) > 0:
            surf = scene.rsdf_surfaces[scene.rsdf_surface_index]
            layout.prop(surf, "name")
            layout.prop(surf, "material")

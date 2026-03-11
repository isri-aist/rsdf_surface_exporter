import bpy


class RSDF_OT_remove_surface(bpy.types.Operator):
    bl_idname = "rsdf.remove_surface"
    bl_label = "Remove RSDF Surface"
    bl_description = "Remove the selected RSDF surface"

    def execute(self, context):
        scene = context.scene
        index = scene.rsdf_surface_index

        if len(scene.rsdf_surfaces) == 0:
            self.report({"WARNING"}, "No surfaces to remove")
            return {"CANCELLED"}

        # Remove linked visualization object if exists
        surf = scene.rsdf_surfaces[index]
        vis_name = f"RSDF_Surface_{surf.name}"
        if vis_obj := bpy.data.objects.get(vis_name):
            bpy.data.objects.remove(vis_obj, do_unlink=True)

        # Remove surface from collection
        scene.rsdf_surfaces.remove(index)

        # Adjust index
        scene.rsdf_surface_index = min(max(0, index - 1), len(scene.rsdf_surfaces) - 1)

        self.report({"INFO"}, "Surface removed")
        return {"FINISHED"}

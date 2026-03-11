import bpy

from ..rsdf_io.rsdf_writer import export_rsdf


class RSDF_OT_export_rsdf(bpy.types.Operator):
    bl_idname = "rsdf.export"
    bl_label = "Export RSDF"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        surfaces = context.scene.rsdf_surfaces

        export_rsdf(self.filepath, surfaces)

        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)

        return {"RUNNING_MODAL"}

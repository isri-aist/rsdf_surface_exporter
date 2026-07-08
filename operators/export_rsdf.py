import bpy
from bpy_extras.io_utils import ExportHelper

from ..rsdf_io.rsdf_writer import export_rsdf


class RSDF_OT_export_rsdf(bpy.types.Operator, ExportHelper):
    bl_idname = "rsdf.export"
    bl_label = "Export RSDF"

    filename_ext = ".rsdf"
    filter_glob: bpy.props.StringProperty(
        default="*.rsdf", options={"HIDDEN"}, maxlen=255
    )

    def execute(self, context):
        surfaces = context.scene.rsdf_surfaces

        export_rsdf(self.filepath, surfaces)

        return {"FINISHED"}

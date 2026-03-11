import bpy

from .data.surface import RSDFSurfaceProperty
from .operators.add_surface import RSDF_OT_add_surface
from .operators.export_rsdf import RSDF_OT_export_rsdf
from .operators.load_rsdf import RSDF_OT_load_rsdf
from .operators.remove_surface import RSDF_OT_remove_surface
from .ui.rsdf_panel import RSDF_PT_panel

bl_info = {
    "name": "RSDF Surface Tool",
    "author": "Thomas Duvinage",
    "version": (1, 0),
    "blender": (5, 0, 1),
    "location": "View3D > Sidebar",
    "category": "Object",
}

classes = (
    RSDFSurfaceProperty,
    RSDF_PT_panel,
    RSDF_OT_add_surface,
    RSDF_OT_export_rsdf,
    RSDF_OT_load_rsdf,
    RSDF_OT_remove_surface,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.rsdf_surfaces = bpy.props.CollectionProperty(
        type=RSDFSurfaceProperty
    )
    bpy.types.Scene.rsdf_surface_index = bpy.props.IntProperty(default=0)


def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)

    del bpy.types.Scene.rsdf_surfaces
    del bpy.types.Scene.rsdf_surface_index


if __name__ == "__main__":
    register()

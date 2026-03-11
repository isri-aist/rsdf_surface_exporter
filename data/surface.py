import bpy


class RSDFSurfaceProperty(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Surface Name", default="Surface")

    surface_type: bpy.props.EnumProperty(
        name="Surface Type",
        items=[("PLANE", "Plane", ""), ("CYLINDER", "Cylinder", "")],
        default="PLANE",
    )

    material: bpy.props.StringProperty(default="plastic")

    origin_x: bpy.props.FloatProperty()
    origin_y: bpy.props.FloatProperty()
    origin_z: bpy.props.FloatProperty()

    rpy_r: bpy.props.FloatProperty()
    rpy_p: bpy.props.FloatProperty()
    rpy_y: bpy.props.FloatProperty()

    points: bpy.props.StringProperty()

    # CYLINDER PARAMETERS
    radius: bpy.props.FloatProperty()
    width: bpy.props.FloatProperty()

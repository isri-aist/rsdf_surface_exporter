import bpy

from ..ros2_io import package_writer, scene_graph


class RSDF_OT_export_ros2_package(bpy.types.Operator):
    bl_idname = "rsdf.export_ros2_package"
    bl_label = "Export ROS2 Description Package"
    bl_description = (
        "Export the current scene as a standalone ROS2 (ament_cmake) "
        "description package: URDF, meshes, RSDF surfaces and a launch file"
    )

    directory: bpy.props.StringProperty(subtype="DIR_PATH")

    package_name: bpy.props.StringProperty(
        name="Package Name",
        description="ROS2 package name (lowercase, underscores)",
        default="",
    )
    robot_name: bpy.props.StringProperty(
        name="Robot Name",
        description="Name used for the robot in the URDF and for output filenames",
        default="",
    )
    include_rsdf: bpy.props.BoolProperty(
        name="Include RSDF Surfaces",
        description="Also export the scene's RSDF surfaces into an rsdf/ directory",
        default=True,
    )
    maintainer_name: bpy.props.StringProperty(name="Maintainer", default="TODO")
    maintainer_email: bpy.props.StringProperty(
        name="Maintainer Email", default="todo@to.do"
    )

    def invoke(self, context, event):
        if not self.package_name:
            self.package_name = package_writer.sanitize_package_name(
                context.scene.name + "_description"
            )
        if not self.robot_name:
            self.robot_name = scene_graph.sanitize_name(context.scene.name)

        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "package_name")
        layout.prop(self, "robot_name")
        layout.prop(self, "include_rsdf")
        layout.prop(self, "maintainer_name")
        layout.prop(self, "maintainer_email")

    def execute(self, context):
        if not self.directory:
            self.report({"ERROR"}, "No output directory selected")
            return {"CANCELLED"}

        package_name = package_writer.sanitize_package_name(self.package_name)
        robot_name = scene_graph.sanitize_name(self.robot_name)

        link_nodes, warnings = scene_graph.build_link_graph(context.scene)

        if not link_nodes:
            self.report(
                {"ERROR"}, "No exportable mesh/empty objects found in the scene"
            )
            return {"CANCELLED"}

        for warning in warnings:
            self.report({"WARNING"}, warning)

        initial_mode = context.object.mode if context.object else "OBJECT"
        if initial_mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")

        try:
            package_dir = package_writer.write_package(
                context,
                self.directory,
                package_name,
                robot_name,
                link_nodes,
                context.scene.rsdf_surfaces,
                self.include_rsdf,
                self.maintainer_name,
                self.maintainer_email,
            )
        finally:
            if initial_mode != "OBJECT" and context.object:
                bpy.ops.object.mode_set(mode=initial_mode)

        self.report({"INFO"}, f"Exported ROS2 package to {package_dir}")
        return {"FINISHED"}

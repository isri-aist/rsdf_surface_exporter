import ast
import xml.etree.ElementTree as ET


def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level + 1)
        if not e.tail or not e.tail.strip():
            e.tail = i
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i


def export_rsdf(filepath, surfaces):
    robot = ET.Element("robot")
    robot.set("name", "object")

    for s in surfaces:
        # ---------------------------
        # PLANAR SURFACE
        # ---------------------------
        if s.surface_type == "PLANE":
            surf = ET.SubElement(robot, "planar_surface")
            surf.set("name", s.name)
            surf.set("link", "base_link")

            origin = ET.SubElement(surf, "origin")
            origin.set("xyz", f"{s.origin_x} {s.origin_y} {s.origin_z}")
            origin.set("rpy", f"{s.rpy_r} {s.rpy_p} {s.rpy_y}")

            pts = ET.SubElement(surf, "points")

            point_list = ast.literal_eval(s.points)

            for x, y in point_list:
                p = ET.SubElement(pts, "point")
                p.set("xy", f"{x} {y}")

            mat = ET.SubElement(surf, "material")
            mat.set("name", s.material)

        # ---------------------------
        # CYLINDRICAL SURFACE
        # ---------------------------
        elif s.surface_type == "CYLINDER":
            surf = ET.SubElement(robot, "cylindrical_surface")
            surf.set("name", s.name)
            surf.set("link", "base_link")
            surf.set("radius", str(s.radius))
            surf.set("width", str(s.width))

            origin = ET.SubElement(surf, "origin")
            origin.set("xyz", f"{s.origin_x} {s.origin_y} {s.origin_z}")
            origin.set("rpy", f"{s.rpy_r} {s.rpy_p} {s.rpy_y}")

            mat = ET.SubElement(surf, "material")
            mat.set("name", s.material)

    indent(robot)

    tree = ET.ElementTree(robot)
    tree.write(filepath, encoding="utf-8", xml_declaration=True)

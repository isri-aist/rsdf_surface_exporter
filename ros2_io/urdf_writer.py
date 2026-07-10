import xml.etree.ElementTree as ET

from ..utils.xml_utils import indent


def build_urdf_string(robot_name, package_name, link_nodes):
    robot = ET.Element("robot")
    robot.set("name", robot_name)
    ET.SubElement(robot, "link", {"name": "base_link"})

    for node in link_nodes:
        robot.append(_link_element(node, package_name))
        robot.append(_joint_element(node))

    indent(robot)
    xml_body = ET.tostring(robot, encoding="unicode")
    return f'<?xml version="1.0"?>\n{xml_body}'


def _link_element(node, package_name):
    link = ET.Element("link", {"name": node.name})

    has_mesh = node.obj.type == "MESH" and len(node.obj.data.vertices) > 0
    if has_mesh:
        mesh_uri = f"package://{package_name}/meshes/{node.name}.stl"
        r, g, b, a = node.material_rgba

        visual = ET.SubElement(link, "visual")
        vgeom = ET.SubElement(visual, "geometry")
        ET.SubElement(vgeom, "mesh", {"filename": mesh_uri})
        material = ET.SubElement(visual, "material", {"name": node.material_name})
        ET.SubElement(material, "color", {"rgba": f"{r} {g} {b} {a}"})

        collision = ET.SubElement(link, "collision")
        cgeom = ET.SubElement(collision, "geometry")
        ET.SubElement(cgeom, "mesh", {"filename": mesh_uri})

    inertial = ET.SubElement(link, "inertial")
    ET.SubElement(inertial, "origin", {"xyz": "0 0 0", "rpy": "0 0 0"})
    ET.SubElement(inertial, "mass", {"value": "1.0"})
    ET.SubElement(
        inertial,
        "inertia",
        {
            "ixx": "0.001",
            "ixy": "0",
            "ixz": "0",
            "iyy": "0.001",
            "iyz": "0",
            "izz": "0.001",
        },
    )
    return link


def _joint_element(node):
    parent = node.parent_name or "base_link"
    origin_attrs = {
        "xyz": " ".join(str(v) for v in node.xyz),
        "rpy": " ".join(str(v) for v in node.rpy),
    }
    spec = node.joint

    if spec is None:
        joint = ET.Element("joint", {"name": f"{node.name}_joint", "type": "fixed"})
        ET.SubElement(joint, "parent", {"link": parent})
        ET.SubElement(joint, "child", {"link": node.name})
        ET.SubElement(joint, "origin", origin_attrs)
        return joint

    joint_name = spec.name or f"{node.name}_joint"
    joint = ET.Element("joint", {"name": joint_name, "type": spec.joint_type})
    ET.SubElement(joint, "parent", {"link": parent})
    ET.SubElement(joint, "child", {"link": node.name})
    ET.SubElement(joint, "origin", origin_attrs)
    ET.SubElement(joint, "axis", {"xyz": spec.axis})

    if spec.joint_type == "continuous":
        limit_attrs = {"effort": str(spec.effort), "velocity": str(spec.velocity)}
    else:
        limit_attrs = {
            "effort": str(spec.effort),
            "velocity": str(spec.velocity),
            "lower": str(spec.lower),
            "upper": str(spec.upper),
        }
    ET.SubElement(joint, "limit", limit_attrs)

    return joint

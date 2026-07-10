import re
from dataclasses import dataclass
from typing import Optional

from ..utils.visualize import SURFACE_VIS_PREFIX

_INVALID_NAME_CHARS = re.compile(r"[^A-Za-z0-9_]")

_JOINT_TYPES = {"revolute", "continuous", "prismatic"}
_JOINT_REQUIRED_FIELDS = {
    "revolute": ("axis", "lower", "upper"),
    "continuous": ("axis",),
    "prismatic": ("axis", "lower", "upper"),
}


def sanitize_name(name):
    return _INVALID_NAME_CHARS.sub("_", name)


@dataclass
class JointSpec:
    joint_type: str
    axis: str
    lower: float = 0.0
    upper: float = 0.0
    effort: float = 1000.0
    velocity: float = 1.0
    name: Optional[str] = None


@dataclass
class LinkNode:
    name: str
    obj: object
    parent_name: Optional[str]
    xyz: tuple
    rpy: tuple
    material_name: str
    material_rgba: tuple
    joint: Optional[JointSpec]


def read_joint_spec(obj):
    if "joint" not in obj:
        return None

    joint_type = obj["joint"]
    if joint_type not in _JOINT_TYPES:
        raise ValueError(f"Object '{obj.name}' has unknown joint type '{joint_type}'")

    missing = [f for f in _JOINT_REQUIRED_FIELDS[joint_type] if f not in obj]
    if missing:
        raise ValueError(
            f"Object '{obj.name}' is missing custom properties {missing} "
            f"required for joint type '{joint_type}'"
        )

    return JointSpec(
        joint_type=joint_type,
        axis=str(obj.get("axis", "0 0 1")),
        lower=float(obj.get("lower", 0.0)),
        upper=float(obj.get("upper", 0.0)),
        effort=float(obj.get("effort", 1000.0)),
        velocity=float(obj.get("velocity", 1.0)),
        name=obj.get("name"),
    )


def _origin_from_object(obj):
    xyz = tuple(obj.matrix_local.to_translation())
    rpy = tuple(obj.matrix_local.to_euler("XYZ"))
    return xyz, rpy


def _material_from_object(obj):
    material = obj.active_material
    if material is None:
        return "default", (1.0, 1.0, 1.0, 1.0)

    color = tuple(material.diffuse_color)
    if len(color) == 3:
        color = color + (1.0,)
    return material.name, color


def _is_exportable(obj):
    if obj.name.startswith(SURFACE_VIS_PREFIX):
        return False
    return obj.type in ("MESH", "EMPTY")


def build_link_graph(scene):
    """Walk the scene's object hierarchy into a flat list of URDF link nodes.

    Returns (nodes, warnings): warnings contains a message for every object
    whose 'joint' custom property was malformed (the object still gets a
    node, with a fixed joint as a fallback).
    """
    nodes = []
    warnings = []
    used_names = set()

    def unique_name(base):
        name = base
        idx = 1
        while name in used_names:
            name = f"{base}_{idx}"
            idx += 1
        used_names.add(name)
        return name

    def walk(obj, parent_name):
        if not _is_exportable(obj):
            return

        link_name = unique_name(sanitize_name(obj.name))
        xyz, rpy = _origin_from_object(obj)
        material_name, material_rgba = _material_from_object(obj)

        try:
            joint = read_joint_spec(obj)
        except ValueError as exc:
            warnings.append(str(exc))
            joint = None

        nodes.append(
            LinkNode(
                name=link_name,
                obj=obj,
                parent_name=parent_name,
                xyz=xyz,
                rpy=rpy,
                material_name=material_name,
                material_rgba=material_rgba,
                joint=joint,
            )
        )

        for child in obj.children:
            walk(child, link_name)

    for obj in scene.objects:
        if obj.parent is None:
            walk(obj, None)

    return nodes, warnings

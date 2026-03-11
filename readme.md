# RSDF Surface Tool

[![Blender Version](https://img.shields.io/badge/Blender-5.0.1-blue)](#)

A Blender addon to create, visualize, and export **RSDF (Robot Surface Description Format)** surfaces from 3D models. Supports **planar and cylindrical surfaces** with full visualization in Blender.

> Warning ! Cylinder export has not been fully tested yet

---

## Features

- Add **planar surfaces** from selected mesh faces
- Add **cylindrical surfaces** from selected mesh geometry
- **Visualize surfaces** in Blender (planes as polygons, cylinders as meshes)
- **Export RSDF XML** compatible with robotics tools
- **Load RSDF XML** into Blender for editing or visualization
- Green color visualization in **Solid** and **Material Preview** modes
- Transparency support and always-visible overlays

---

## Installation

1. Download or clone the repository.
2. Open Blender → **Edit → Preferences → Add-ons → Install…**
3. Select the `rsdf_surface_exporter-1.0.0.zip` file (or the repo folder if using ZIP).
4. Enable the addon.

---

## Usage

### 1. Add Surfaces

1. Select a mesh in Blender.
2. Go to the **3D View Sidebar (Press N) → RSDF Surface Tool**.
3. Use **Add Surface** to create a planar or cylindrical surface.
4. Planar surfaces are automatically projected from selected faces.
5. Cylindrical surfaces can be generated from mesh geometry.

### 2. Visualize

- Surfaces appear as **green objects**:
  - Planes → green polygons
  - Cylinders → green cylinders
- Always visible (`show_in_front`) and semi-transparent
- Supports **Solid shader** and **Material Preview**

### 3. Export RSDF

1. Click **Export RSDF** in the sidebar.
2. Choose a filename and location.
3. The addon generates an XML file compatible with RSDF format.

### 4. Load RSDF

1. Click **Load RSDF** in the sidebar.
2. Select an RSDF XML file.
3. All surfaces are imported with correct position, orientation, and type.

---

## RSDF Format

- **Planar surface**

```xml
<planar_surface name="Surface_1" link="base_link">
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <points>
    <point xy="0 0"/>
    <point xy="1 0"/>
    <point xy="1 1"/>
  </points>
  <material name="plastic"/>
</planar_surface>
```


```xml
<cylindrical_surface name="Surface_2" link="base_link" radius="0.02" width="0.14">
  <origin xyz="0 0 0" rpy="0 -1.57 0"/>
  <material name="plastic"/>
</cylindrical_surface>
```

## To compile after modification

If you want to apply changes to this repo and test it locally, you need to buid the extension before installing it. Please use the command below :

```bash
blender --command extension build
```

## To be improved

* Parent link is set to base_link by default. A way to set it automatically after loading urdf would be better
* Cylindrical loading is not working properly.

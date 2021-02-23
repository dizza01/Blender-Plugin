bl_info = {
    "name": "VU.CITY Plugin",
    "blender": (2, 90, 0),
    "author": "Dawud <d.izza@vu.city>",
    "version": (1, 0, 0),
    "category": "Object",
    "location": "Operator Search",
    "desctription": "VU.CITY Plugin"
}

import pathlib
import bpy


class SelectMesh(bpy.types.Operator):
    """Selects the objects and merges them into one"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.select_mesh"  # Unique identifier for buttons and menu items to reference.
    bl_label = "Select & Merge Meshes"  # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):  # execute() is called when running the operator.

        try:
            #Select mesh
            obj = bpy.context.window.scene.objects[0]
            bpy.context.view_layer.objects.active = obj

            #Merge mesh
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            mesh = [m for m in bpy.context.scene.objects if m.type == 'MESH']
            for obj in mesh:
                obj.select_set(state=True)
                bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.join()

        except:
            self.report({'ERROR'}, f"Please import your FBX/OBJ file first.")

        return {'FINISHED'}  # Lets Blender know the operator finished successfully.


class CorrectOrientation(bpy.types.Operator):
    """Flips X-rotation by 90°"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.correct_orientation"  # Unique identifier for buttons and menu items to reference.
    bl_label = "Rotate by 90°"  # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):  # execute() is called when running the operator.
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            bpy.context.object.rotation_euler[0] = 1.5708
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

        except:
            self.report({'ERROR'}, f'Please select & merge meshes first.')

        return {'FINISHED'}



class MergeByDistance(bpy.types.Operator):
    """Collapse vertices by distance (Medium recommended)"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.merging_distance"  # Unique identifier for buttons and menu items to reference.
    bl_label = "Distance to merge by"  # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    count_cm: bpy.props.FloatProperty(
        name="distance",
        description="Distance in cm to merge by"
    )

    def execute(self, context):  # execute() is called when running the operator.
        try:
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.remove_doubles(threshold=self.count_cm)
        except:
            self.report({'ERROR'}, f'Please select & merge meshes first.')
        return {'FINISHED'}  # Lets Blender know the operator finished successfully.


class OriginToGeometry(bpy.types.Operator):
    """Set the object's origin to geometry"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.origining_geometry"  # Unique identifier for buttons and menu items to reference.
    bl_label = "Origin to Geometry"  # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):  # execute() is called when running the operator.
        try:
            o = bpy.context.object
            mw = o.matrix_world
            glob_vertex_coordinates = [mw @ v.co for v in o.data.vertices]

            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')

            minZ = min([co.z for co in glob_vertex_coordinates])
            verts = [o.matrix_world @ vert.co for vert in o.data.vertices]
            plain_verts = [vert.to_tuple() for vert in verts]

            for v in o.data.vertices:
                if (mw @ v.co).z == minZ:
                    v.select = True
            bpy.ops.object.mode_set(mode='EDIT')

            current_area_type = bpy.context.area.type
            area = bpy.context.area
            old_type = area.type
            area.type = 'VIEW_3D'
            bpy.ops.view3d.snap_cursor_to_selected()
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            bpy.context.area.type = current_area_type
        except:
            self.report({'ERROR'}, f'Please select & merge meshes first.')
        return {'FINISHED'}  # Lets Blender know the operator finished successfully.


class RepositionModel(bpy.types.Operator):
    """Repostion model (default (0,0,0))(you may need to set your origin to your geometry first)"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.repositioning_model"  # Unique identifier for buttons and menu items to reference.
    bl_label = "Zero Model"  # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    count_x: bpy.props.FloatProperty(
        name = "X",
        description = "Eastings"
    )
    count_y: bpy.props.FloatProperty(
        name="Y",
        description="Northings"
    )
    count_z: bpy.props.FloatProperty(
    name = "Z",
    description = "AOD/Height"
    )

    def execute(self, context):  # execute() is called when running the operator.
        try:
            bpy.context.object.location[0] = self.count_x
            bpy.context.object.location[1] = self.count_y
            bpy.context.object.location[2] = self.count_z
        except:
            self.report({'ERROR'}, f'Please select & merge meshes first.')
        return {'FINISHED'}  # Lets Blender know the operator finished successfully.

class RescaleModel(bpy.types.Operator):
    """Rescale your model x0.1"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.rescaling_model"  # Unique identifier for buttons and menu items to reference.
    bl_label = "Scale x0.1"  # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.


    def execute(self, context):  # execute() is called when running the operator.
        try:
            for i in range(0, 3):
                bpy.context.object.scale[i] =  bpy.context.object.scale[i] * 0.1
        except:
            self.report({'ERROR'}, f'Please select & merge meshes first.')
        return {'FINISHED'}  # Lets Blender know the operator finished successfully.

class RescaleModel_x10(bpy.types.Operator):
    """Rescale your model"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.rescaling_model_x10"  # Unique identifier for buttons and menu items to reference.
    bl_label = "Scale x10"  # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):  # execute() is called when running the operator.
        try:
            for i in range(0, 3):
                bpy.context.object.scale[i] =  bpy.context.object.scale[i] * 10
        except:
            self.report({'ERROR'}, f'Please select & merge meshes first.')
        return {'FINISHED'}  # Lets Blender know the operator finished successfully.


class FixSmudges(bpy.types.Operator):
    """Fix smooth shading issues / dark smudges"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.fixing_smudges"  # Unique identifier for buttons and menu items to reference.
    bl_label = "Fix Shading Smudges"  # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):  # execute() is called when running the operator.
        try:
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.context.object.data.use_auto_smooth = False
            bpy.ops.mesh.uv_texture_remove()
            bpy.ops.mesh.faces_shade_flat()
        except:
            self.report({'ERROR'}, f'Please select & merge meshes first.')
        return {'FINISHED'}  # Lets Blender know the operator finished successfully.


class RemoveMaterials(bpy.types.Operator):
    """Remove all materials"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.removing_materials"  # Unique identifier for buttons and menu items to reference.
    bl_label = "Remove Materials"  # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):  # execute() is called when running the operator.

        for material in bpy.data.materials:
            material.user_clear()
            bpy.data.materials.remove(material)

        return {'FINISHED'}  # Lets Blender know the operator finished successfully.


class RevealFaces(bpy.types.Operator):
    """Enable face orientation to see flipped faces"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.revealing_faces"  # Unique identifier for buttons and menu items to reference.
    bl_label = "Reveal Flipped Faces"  # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):  # execute() is called when running the operator.

        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.overlay.show_face_orientation = not space.overlay.show_face_orientation
                        break

        return {'FINISHED'}  # Lets Blender know the operator finished successfully.

class Triangulate(bpy.types.Operator):
    """Translates n-gons & quads to tris"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.triangulate"  # Unique identifier for buttons and menu items to reference.
    bl_label = "Triangulate N-gons & Quads"  # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):  # execute() is called when running the operator.
        try:
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
        except:
            self.report({'ERROR'}, f'Please select & merge meshes first.')
        return {'FINISHED'}  # Lets Blender know the operator finished successfully.


class FlipNormals(bpy.types.Operator):
    """Fix flipped faces (experimental - please merge meshes and collapse vertices for best results)"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.flipping_normals"  # Unique identifier for buttons and menu items to reference.
    bl_label = "Correct Flipped Faces"  # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):  # execute() is called when running the operator.
        try:
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.normals_make_consistent(inside=False)
        except:
            self.report({'ERROR'}, f'Please select & merge meshes first.')
        return {'FINISHED'}  # Lets Blender know the operator finished successfully.


class VIEW3D_PT_SelectMesh(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VU.CITY"
    bl_label = "Start Here"

    def draw(self, context):
        self.layout.operator("object.select_mesh", icon = "COLORSET_07_VEC")
        self.layout.operator("object.correct_orientation", icon = "COLORSET_07_VEC")




class VIEW3D_PT_MergeByDistance(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VU.CITY"
    bl_label = "Optimise / Reduce Detail"

    def draw(self, context):
        props_high = self.layout.operator("object.merging_distance", text="High (10cm)", icon="COLORSET_07_VEC")
        props_high.count_cm = 0.1
        props_high = self.layout.operator("object.merging_distance", text="Medium (5cm)", icon="COLORSET_07_VEC")
        props_high.count_cm = 0.05
        props_low = self.layout.operator("object.merging_distance", text="Low (1cm)", icon="COLORSET_07_VEC")
        props_low.count_cm = 0.01


class VIEW3D_PT_OriginToGeometry(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VU.CITY"
    bl_label = "Zero & Geolocate Model"

    def draw(self, context):
        self.layout.operator("object.origining_geometry", icon = "COLORSET_07_VEC")
        self.layout.operator("object.repositioning_model", icon="COLORSET_07_VEC")
        layout = self.layout
        ob = context.object
        layout.column().prop(ob, "location", text="Geolocate", icon="COLORSET_07_VEC")



class VIEW3D_PT_FixSmudges(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VU.CITY"
    bl_label = "Appearance"

    def draw(self, context):
        self.layout.operator("object.fixing_smudges", icon = "COLORSET_07_VEC")
        self.layout.operator("object.removing_materials", icon = "COLORSET_07_VEC")


class VIEW3D_PT_RescaleModel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VU.CITY"
    bl_label = "Rescale Model"

    def draw(self, context):
        self.layout.operator("object.rescaling_model", text="Scale x0.1", icon = "COLORSET_07_VEC")
        self.layout.operator("object.rescaling_model_x10", text="Scale x10", icon="COLORSET_07_VEC")


class VIEW3D_PT_RevealFaces(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VU.CITY"
    bl_label = "Adjust Faces"

    def draw(self, context):
        self.layout.operator("object.revealing_faces", icon = "COLORSET_07_VEC")
        self.layout.operator("object.flipping_normals", icon = "COLORSET_07_VEC")
        self.layout.operator("object.triangulate", icon = "COLORSET_07_VEC")



class VIEW3D_PT_RotateBy90(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VU.CITY"
    bl_label = "Rotation"

    def draw(self, context):
        self.layout.operator("object.rotating_90", icon = "COLORSET_07_VEC")







blender_classes = [
SelectMesh,CorrectOrientation, MergeByDistance, OriginToGeometry,
    RepositionModel, RescaleModel, RescaleModel_x10 ,FixSmudges, RemoveMaterials,
RevealFaces, FlipNormals, Triangulate, VIEW3D_PT_SelectMesh, VIEW3D_PT_MergeByDistance, VIEW3D_PT_OriginToGeometry, VIEW3D_PT_FixSmudges, VIEW3D_PT_RescaleModel, VIEW3D_PT_RevealFaces
]

def register():

    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)


def unregister():

    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class)

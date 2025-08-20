import bpy
from typing import Optional

bl_info = {
    "name": "Watershapegenerator",
    "author": "Xi Lin",
    "description": "Generates water shapes using Geometry Nodes",
    "blender": (4, 2, 0),
    "version": (1, 0, 0),
    "location": "View3D > N-Panel > WSG",
    "warning": "",
    "category": "Object",
}

RENAME_MAP = {
    "Resample Length": "重新采样长度",
    "Progress": "进度",
}

TARGET_NODEGROUP_NAME = "Liquid With Interface"


# Get the Geometry Nodes modifier from the object
def get_node_modifier(obj: bpy.types.Object) -> Optional[bpy.types.NodesModifier]:
    if obj is None:
        return None
    if TARGET_NODEGROUP_NAME:
        for modifier in obj.modifiers:
            if modifier.type == 'NODES' and modifier.node_group and modifier.node_group.name == TARGET_NODEGROUP_NAME:
                return modifier
        return None
    for modifier in obj.modifiers:
        if modifier.type == 'NODES' and modifier.node_group:
            return modifier
    return None

# Iterate over the inputs of a Geometry Nodes node tree
def iter_gn_inputs(ng: bpy.types.NodeTree):
    if ng is None:
        return
    for item in ng.interface.items_tree:
        if getattr(item, "in_out", None) == 'INPUT' and item.item_type == 'SOCKET':
            yield item


def _apply_obj_prop_to_modifier(mod: bpy.types.NodesModifier, identifier: str, value):
    """Attempt to apply value to modifier instance; fallback to node-group default.

    Returns (applied_instance: bool, applied_asset: bool)
    """
    applied_instance = False
    applied_asset = False
    try:
        key = f'wsg__{identifier}'
        try:
            mod[key] = value
            applied_instance = True
        except Exception:
            applied_instance = False
    except Exception:
        applied_instance = False

    if not applied_instance:
        try:
            ng = mod.node_group
            if ng is not None:
                for item in ng.interface.items_tree:
                    if getattr(item, 'identifier', None) == identifier:
                        if hasattr(item, 'default_value'):
                            try:
                                item.default_value = value
                                applied_asset = True
                            except Exception:
                                applied_asset = False
                        break
        except Exception:
            applied_asset = False

    return applied_instance, applied_asset


class GN_PT_CustomInspector(bpy.types.Panel):
    bl_label = "Geometry Nodes Inspector"
    bl_idname = "GN_PT_custom_inspector"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "WSG"

    @classmethod
    def poll(cls, context):
        return get_node_modifier(context.object) is not None

    def draw(self, context):
        layout = self.layout
        obj = context.object
        mod = get_node_modifier(obj)
        if not mod:
            layout.label(text="No Geometry Nodes modifier found.")
            return

        ng = mod.node_group
        layout.prop(mod, "name", text="Modifier")
        layout.prop(ng, "name", text="Node Group")

        box = layout.box()
        box.label(text="Inputs", icon='NODE_INPUT')

        if obj is None:
            box.label(text="No object selected.")
            return

        for item in iter_gn_inputs(ng):
            display_name = RENAME_MAP.get(item.name, item.name)
            identifier = item.identifier
            key = f'wsg__{identifier}'

            default = getattr(item, 'default_value', None)
            if default is None:
                default = 0

            # ensure id prop exists
            try:
                if key not in obj.keys():
                    obj[key] = default
            except Exception:
                pass

            row = box.row()
            try:
                # bind to object idprop using bracket syntax
                row.prop(obj, f'["{key}"]', text=display_name)
            except Exception:
                row.label(text=f"{display_name} (unsupported)")
                continue

            # apply to modifier instance
            try:
                val = obj.get(key)
                inst, asset = _apply_obj_prop_to_modifier(mod, identifier, val)
                if not inst and not asset:
                    print(f"WSG warning: failed to apply '{identifier}' to modifier or asset")
            except Exception as e:
                print(f"WSG error applying '{identifier}': {e}")



class GN_OT_RenameInterface(bpy.types.Operator):
    bl_idname = "gn.rename_interface_by_map"
    bl_label = "Apply RENAME_MAP to Interface"
    bl_options = {'UNDO'}

    def execute(self, context):
        mod = get_node_modifier(context.object)
        if not mod or not mod.node_group:
            self.report({'WARNING'}, "No valid Geometry Nodes group.")
            return {'CANCELLED'}
        ng = mod.node_group
        changed = 0
        for item in iter_gn_inputs(ng):
            if item.name in RENAME_MAP:
                item.name = RENAME_MAP[item.name]
                changed += 1
        if changed == 0:
            self.report({'INFO'}, "No interface names matched RENAME_MAP.")
        else:
            ng.interface_update(context)
            self.report({'INFO'}, f"Renamed {changed} interface item(s).")
        return {'FINISHED'}


class GN_PT_CustomInspectorFooter(bpy.types.Panel):
    bl_label = "Manage"
    bl_idname = "GN_PT_custom_inspector_footer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "WSG"
    bl_parent_id = "GN_PT_custom_inspector"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.operator("gn.rename_interface_by_map", icon='OUTLINER_DATA_GP_LAYER')


classes = (
    GN_PT_CustomInspector,
    GN_PT_CustomInspectorFooter,
    GN_OT_RenameInterface,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
                  
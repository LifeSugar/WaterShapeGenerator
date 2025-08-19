import bpy
from typing import Optional

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

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
    "Droplet Min Speed": "水滴最小速度",
    "Droplet Max Speed": "水滴最大速度",
    "Droplet Min Size": "水滴最小尺寸",
    "Droplet Max Size": "水滴最大尺寸",
    "Droplet Distance": "液滴距离",
    "Surface Noise": "表面噪声",
    "Wave Speed": "波浪速度",
    "Wave Frequency": "波浪频率",
    "Wave Area": "波浪区域",
    "Wave Amplitude": "波浪振幅",
}

TARGET_NODEGROUP_NAME = "Liquid With Interface"

def get_node_modifier(obj: bpy.types.Object) -> Optional[bpy.types.NodesModifier]:
    if obj is None:
        return None
    if TARGET_NODEGROUP_NAME:
        for modifier in obj.modifiers:
            if modifier.type == 'NODES' and modifier.node_group and modifier.node_group.name == TARGET_NODEGROUP_NAME:
                return modifier
        return None
    # If no specific node group name is provided, return the first nodes modifier found
    for modifier in obj.modifiers:
        if modifier.type == 'NODES' and modifier.node_group:
            return modifier
    return None

def iter_gn_inputs(ng: bpy.types.NodeTree):
    if ng is None:
        return
    for item in ng.interface.items_tree:
        if getattr(item, "in_out", None) == 'INPUT' and item.item_type == 'SOCKET':
            yield item

class GN_PT_CustomInspector(bpy.types.Panel):
    bl_label = "Geometry Nodes Inspector"
    bl_idname = "GN_PT_custom_inspector"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "WSG"

    @classmethod
    def poll(cls, context):
        obj = context.object
        return get_node_modifier(obj) is not None
    
    def draw(self, context):
        layout = self.layout
        obj = context.object
        mod = get_node_modifier(obj)
        if not mod:
            layout.label(text="No Geometry Nodes modifier found.")
            return

        ng = mod.node_group
        row = layout.row()
        row.prop(mod, "name", text = "Modifier")
        row = layout.row()
        row.prop(ng, "name", text = "Node Group")

        box = layout.box()
        box.label(text="Inputs", icon='NODE_INPUT')

        for item in iter_gn_inputs(ng):
            display_name = RENAME_MAP.get(item.name, item.name)
            identifier = item.identifier

            slider = False
            soft_min = None
            soft_max = None

            if hasattr(item, "min_value") and hasattr(item, "max_value"):
                slider = True
                soft_min = float(item.min_value)
                soft_max = float(item.max_value)

            row = box.row()
            prop_path = f'node_group.inputs["{identifier}"]'
            row.prop(mod, prop_path, text=display_name, slider=slider)

        layout.separator()
        help_box = layout.box()
        help_box.label(text="Tips", icon='INFO')
        col = help_box.column(align=True)
        col.label(text="1. Select an object with a Geometry Nodes modifier.")
        col.label(text="2. Adjust the inputs in the panel above.")


class GN_OT_RenameInterface(bpy.types.Operator):
    """把当前 Node Group 的接口名字直接改成 RENAME_MAP（影响所有面板与资产）"""
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
            # 通常改名会立刻刷新；必要时可 tag 更新：
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
import bpy
from . import method

class WATERGENERATOR_PT_GeoNodeProps(bpy.types.Panel):
    bl_label = "几何节点属性"
    bl_idname = "OBJECT_PT_geonode_props_cn"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = '水体生成'

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return bool(obj and obj.modifiers and any(m.type == 'NODES' for m in obj.modifiers))

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        if not obj:
            layout.label(text="请选择一个物体")
            return
        
        top_box = layout.box()
        top_box.label(text=f"当前物体: {obj.name}", icon='OBJECT_DATA')
        col = top_box.column(align=True)
        col.prop(obj, "name", text="物体名称")
        col.operator("wm.debug_operator", text="生成水流")
        col.operator("wm.debug_operator", text="生成水花")
        col.operator("wm.debug_operator", text="水之呼吸")

        geo_nodes_mods = [m for m in obj.modifiers if m.type == 'NODES']
        # if not geo_nodes_mods:
        #     layout.label(text="没有几何节点修饰器")
        #     return

        for mod in geo_nodes_mods:
            ng = getattr(mod, "node_group", None)
            if not ng:
                continue

            box = layout.box()
            box.label(text=f"水体: {ng.name}", icon='NODETREE')

            prop_count = 0

            # 按接口顺序遍历，仅取输入项
            items = getattr(ng.interface, "items_tree", [])
            for item in items:
                try:
                    if getattr(item, "in_out", "INPUT") != 'INPUT':
                        continue
                    if getattr(item, "item_type", "SOCKET") != 'SOCKET':
                        continue

                    key = getattr(item, "identifier", None)
                    name = getattr(item, "name", "") or (key or "")
                    if not key:
                        continue

                    # 有些接口项在当前修饰器上未暴露为自定义属性，跳过
                    if key not in mod.keys():
                        continue

                    display = method.cn_name(name)
                    typ = (getattr(item, "type", None)
                            or getattr(item, "socket_type", None)
                            or getattr(item, "bl_socket_idname", None)
                            or "")

                    # 按类型分发；这些类型 Blender 会自动画出合适的控件
                    if typ in {"NodeSocketFloat", "NodeSocketInt"}:
                        row = box.row(align=True)  # <- 用 box，而不是 layout
                        row.label(text=display)
                        row.prop(mod, f'["{key}"]', text="")
                        prop_count += 1

                    elif typ in {"NodeSocketVector"}:
                        row = box.row(align=True)
                        row.label(text=display)
                        row.prop(mod, f'["{key}"]', text="")
                        prop_count += 1

                    elif typ in {"NodeSocketObject"}:
                        row = box.row(align=True)
                        row.label(text=f"{display}（对象数据，无法在此编辑）")
                        row.prop(mod, f'["{key}"]', text=display)
                        prop_count += 1

                    else:
                        # 兜底（如果真走到这里，会看到 [FALLBACK]）
                        row = box.row(align=True)
                        row.prop(mod, f'["{key}"]', text=display + " [FALLBACK]")
                        print(f"[GeoPropsCN] fallback for {ng.name}::{key} type={typ!r}")
                        prop_count += 1

                                       

                except Exception as e:
                    # 定位哪个 socket 出问题
                    print(f"[GeoPropsCN] 绘制 {ng.name}::{key} 失败: {e}")

            if prop_count == 0:
                box.label(text="没有找到可编辑的属性")
            else:
                box.label(text=f"共找到 {prop_count} 个属性")

        remesh_mods = [m for m in obj.modifiers if m.type == 'REMESH']
        for mod in remesh_mods:
            if mod.mode != 'VOXEL':
                continue
            box.label(text=f"重拓扑: {mod.name}", icon='MOD_REMESH')
            box.prop(mod, "voxel_size", text="细分尺寸")



def register():
    bpy.utils.register_class(WATERGENERATOR_PT_GeoNodeProps)

def unregister():
    bpy.utils.unregister_class(WATERGENERATOR_PT_GeoNodeProps)
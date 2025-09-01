import bpy
from . import method
# from .cn import N_Translation as cn



class WATERGENERATOR_PT_GeoNodeProps(bpy.types.Panel):
    bl_label = "几何节点属性"
    bl_idname = "OBJECT_PT_geonode_props_cn"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = '水体属性'

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

class WATERGENERATOR_PT_MainPanel(bpy.types.Panel):
    bl_label = "水体生成"
    bl_idname = "OBJECT_PT_watergenerator_main_cn"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = '水体生成'

    @classmethod
    def poll(cls, context):
        return True
    
    def draw(self, context):
        from .resource import custom_icons

        
        
        layout = self.layout

        top_box = layout.box()
        tile_row = top_box.row(align=True)

        if "1" in custom_icons:
            icon = custom_icons["1"].icon_id
            tile_row.label(text = "请选择一个水体", icon_value=icon)
        else:
            tile_row.label(text = "生成水流和水花", icon='MOD_FLUIDSIM')

        props = context.scene.water_shape_generator_props

        preview_row = top_box.row(align=True)
        from .resource import preview_collections
         # 检查预览图集合是否已成功加载
        if "main" in preview_collections:
            pcoll = preview_collections["main"]
            # 从属性中获取当前选中的预览图ID
            selected_preview_name = props.preview_selector
            
            # --- 这里是必须添加的安全检查 ---
            # 在使用 selected_preview_name 作为键之前，先检查它是否存在于 pcoll 中
            if selected_preview_name in pcoll:
                # 只有当键有效时，才绘制预览图
                preview_row.template_icon(icon_value=pcoll[selected_preview_name].icon_id, scale=8.0)
            else:
                # 如果键无效（比如插件刚启动时），显示一个提示
                preview_row.label(text="请选择一个预览图")
                
        else:
            # 这个else是当 "main" 预览集不存在时触发
            preview_row.label(text="没有可用的预览图")
            
        # 使用最简单的两列布局方法
        flow = layout.grid_flow(row_major=True, columns=2, even_columns=True, even_rows=False, align=True)
        flow.prop(props, "preview_selector", expand=True) 

        # 添加显示当前选择图片名称的按钮
        button_row = layout.row(align=True)
        
        # 获取当前选择的图片名称
        selected_image = props.preview_selector
        if selected_image:
            # 格式化显示名称
            display_name = selected_image.replace("_", " ").title()
            # 特殊处理数字开头的名称
            if display_name.startswith("Img "):
                display_name = display_name[4:]  # 移除 "Img " 前缀
            button_text = f"生成水体：{display_name}"
        else:
            button_text = "生成水体：无选择"
        
        # 创建按钮，显示当前选择的图片名称，使用自定义图标
        from . import resource
        if resource.custom_icons and "1" in resource.custom_icons:
            icon_value = resource.custom_icons["1"].icon_id
            op = button_row.operator("watergenerator.generate_water_v2", text=button_text, icon_value=icon_value)
            op.water_name = selected_image if selected_image else ""
        else:
            # 备用方案：使用内置图标
            op = button_row.operator("watergenerator.generate_water_v2", text=button_text, icon='MESH_CUBE')
            op.water_name = selected_image if selected_image else "" 

        # 添加分隔符
        layout.separator()
        
        # 集成几何节点属性内容 - 使用原有的poll方法判断是否显示
        if WATERGENERATOR_PT_GeoNodeProps.poll(context):
            # 调用原有类的绘制方法内容
            self._draw_geonode_props(context, layout)

    def _draw_geonode_props(self, context, layout):
        """绘制几何节点属性的方法，从原有的 WATERGENERATOR_PT_GeoNodeProps.draw 移植过来"""
        obj = context.active_object

        if not obj:
            layout.label(text="请选择一个物体")
            return
        
        # 添加几何节点属性标题
        geo_box = layout.box()
        from .resource import custom_icons

        if "1" in custom_icons:
            icon = custom_icons["1"].icon_id
            geo_box.label(text = "请选择一个水体", icon_value=icon)
        else:
            geo_box.label(text = "生成水流和水花", icon='MOD_FLUIDSIM')

        # icon = custom_icons["1"].icon_id
        # geo_box.label(text="水体属性", icon='NODETREE')
        
        top_box = geo_box.box()
        top_box.label(text=f"当前物体: {obj.name}", icon='OBJECT_DATA')
        # col = top_box.column(align=True)
        # col.prop(obj, "name", text="物体名称")
        # col.operator("wm.debug_operator", text="生成水流")
        # col.operator("wm.debug_operator", text="生成水花")
        # col.operator("wm.debug_operator", text="水之呼吸")

        geo_nodes_mods = [m for m in obj.modifiers if m.type == 'NODES']

        for mod in geo_nodes_mods:
            ng = getattr(mod, "node_group", None)
            if not ng:
                continue

            box = geo_box.box()
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

                    # 按类型分发；
                    if typ in {"NodeSocketFloat", "NodeSocketInt"}:
                        row = box.row(align=True)  
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
                        row.label(text=f"{display}")
                        row.prop(mod, f'["{key}"]', text=display)
                        prop_count += 1

                    elif typ in {"NodeSocketString"}:
                        # row.label(text=f"{display}")
                        prop_count += 1

                    elif typ in {"NodeSocketMaterial"}:
                        row = box.row(align=True)
                        row.label(text=f"{display}")
                        row.prop(mod, f'["{key}"]', text="")
                        prop_count += 1

                    else:
                        row = box.row(align=True)
                        row.prop(mod, f'["{key}"]', text=display)
                        print(f"[GeoPropsCN] fallback for {ng.name}::{key} type={typ!r}")
                        prop_count += 1

                                       

                except Exception as e:
                    # 定位哪个 socket 出问题
                    print(f"[GeoPropsCN] 绘制 {ng.name}::{key} 失败: {e}")

            if prop_count == 0:
                box.label(text="没有找到可编辑的属性")
            # else:
                # box.label(text=f"共找到 {prop_count} 个属性")

        remesh_mods = [m for m in obj.modifiers if m.type == 'REMESH']
        for mod in remesh_mods:
            if mod.mode != 'VOXEL':
                continue
            geo_box.label(text=f"重拓扑: {mod.name}", icon='MOD_REMESH')
            geo_box.prop(mod, "voxel_size", text="细分尺寸") 


def register():
    # bpy.utils.register_class(WATERGENERATOR_PT_GeoNodeProps)
    bpy.utils.register_class(WATERGENERATOR_PT_MainPanel)

def unregister():
    # bpy.utils.unregister_class(WATERGENERATOR_PT_GeoNodeProps)
    bpy.utils.unregister_class(WATERGENERATOR_PT_MainPanel)
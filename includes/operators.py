import bpy
import os
from . import method


class WATERGENERATOR_OP_DEBUG(bpy.types.Operator):
    bl_idname = "wm.debug_operator"
    bl_label = "Debug Operator"

    def execute(self, context):
        self.report({'INFO'}, "Debug operator executed")
        method.load_info_from_asset("")
        method.load_collection_from_asset("Liquid on curve with a surface interface")
        return {'FINISHED'}


class WATERGENERATOR_OP_PrintImageName(bpy.types.Operator):
    bl_idname = "watergenerator.print_image_name"
    bl_label = "打印图片名称"
    bl_description = "在终端打印当前选择的图片名称"

    def execute(self, context):
        props = context.scene.water_shape_generator_props
        selected_image = props.preview_selector
        
        if selected_image:
            # 格式化图片名称显示
            display_name = selected_image.replace("_", " ").title()
            print(f"[WaterShapeGenerator] 当前选择的图片: {display_name} (内部名称: {selected_image})")
            self.report({'INFO'}, f"已打印图片名称: {display_name}")
        else:
            print("[WaterShapeGenerator] 没有选择任何图片")
            self.report({'WARNING'}, "没有选择任何图片")
        
        return {'FINISHED'}


class WATERGENERATOR_OP_SetPreview(bpy.types.Operator):
    bl_idname = "watergenerator.set_preview"
    bl_label = "设置预览图"
    bl_description = "设置当前选择的预览图"
    
    image_key = bpy.props.StringProperty()

    def execute(self, context):
        props = context.scene.water_shape_generator_props
        props.preview_selector = self.image_key
        return {'FINISHED'}


class WATERGENERATOR_OP_GenerateWater(bpy.types.Operator):
    bl_idname = "watergenerator.generate_water_v2"
    bl_label = "生成水体"
    bl_description = "从预设文件导入选择的水体物体到光标位置"
    
    water_name: bpy.props.StringProperty(name="水体名称") # pyright: ignore[reportInvalidTypeForm]

    def execute(self, context):
        # 简化的调试版本
        water_name_str = str(self.water_name) if self.water_name else "无名称"
        
        print(f"[WaterShapeGenerator] 操作器收到的水体名称: '{water_name_str}'")
        print(f"[WaterShapeGenerator] 水体名称类型: {type(self.water_name)}")
        
        if not water_name_str or water_name_str == "无名称":
            self.report({'WARNING'}, "没有指定水体名称")
            return {'CANCELLED'}
        
        # 构建预设文件路径
        current_dir = os.path.dirname(__file__)
        addon_path = os.path.dirname(current_dir)
        preset_file = os.path.join(addon_path, "assets", "water_preset.blend")
        
        # 检查预设文件是否存在
        if not os.path.exists(preset_file):
            self.report({'ERROR'}, f"预设文件不存在: {preset_file}")
            print(f"[WaterShapeGenerator] 预设文件不存在: {preset_file}")
            return {'CANCELLED'}
        
        # 准备可能的物体名称变体
        possible_names = [
            water_name_str,
            water_name_str.replace("_", " "),
            water_name_str.replace(" ", "_"),
            water_name_str.lower(),
            water_name_str.upper(),
            water_name_str.title(),
        ]
        
        # 如果名称以img_开头，也尝试去掉前缀
        if water_name_str.startswith("img_"):
            base_name = water_name_str[4:]
            possible_names.extend([
                base_name,
                base_name.replace("_", " "),
                base_name.title(),
            ])
        
        # 去重
        possible_names = list(dict.fromkeys(possible_names))
        print(f"[WaterShapeGenerator] 尝试匹配的名称: {possible_names}")
        
        try:
            # 尝试从预设文件导入物体
            found_object = None
            
            with bpy.data.libraries.load(preset_file) as (data_from, data_to):
                available_objects = list(data_from.objects)
                print(f"[WaterShapeGenerator] 预设文件中的可用物体: {available_objects}")
                
                # 查找匹配的物体名称
                for name in possible_names:
                    if name in data_from.objects:
                        data_to.objects = [name]
                        found_object = name
                        print(f"[WaterShapeGenerator] 匹配到物体: {name}")
                        break
                
                if not found_object:
                    self.report({'WARNING'}, f"未找到物体 '{water_name_str}'")
                    print(f"[WaterShapeGenerator] 未找到物体: {water_name_str}")
                    return {'CANCELLED'}
            
            # 链接导入的物体到当前场景
            imported_obj = None
            for obj in data_to.objects:
                if obj is not None:
                    bpy.context.collection.objects.link(obj)
                    imported_obj = obj
                    break
            
            if imported_obj:
                # 设置物体位置为3D光标位置
                cursor_location = bpy.context.scene.cursor.location
                imported_obj.location = cursor_location.copy()
                
                # 选中新导入的物体
                bpy.ops.object.select_all(action='DESELECT')
                imported_obj.select_set(True)
                bpy.context.view_layer.objects.active = imported_obj
                
                self.report({'INFO'}, f"成功生成水体: {imported_obj.name}")
                print(f"[WaterShapeGenerator] 成功导入水体 '{imported_obj.name}' 到位置 {cursor_location}")
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, "导入失败：无法链接物体")
                return {'CANCELLED'}
                
        except Exception as e:
            self.report({'ERROR'}, f"导入水体时发生错误: {str(e)}")
            print(f"[WaterShapeGenerator] 导入错误: {e}")
            return {'CANCELLED'}
    

def register():
    bpy.utils.register_class(WATERGENERATOR_OP_DEBUG)
    bpy.utils.register_class(WATERGENERATOR_OP_PrintImageName)
    bpy.utils.register_class(WATERGENERATOR_OP_SetPreview)
    bpy.utils.register_class(WATERGENERATOR_OP_GenerateWater)

def unregister():
    bpy.utils.unregister_class(WATERGENERATOR_OP_GenerateWater)
    bpy.utils.unregister_class(WATERGENERATOR_OP_SetPreview)
    bpy.utils.unregister_class(WATERGENERATOR_OP_PrintImageName)
    bpy.utils.unregister_class(WATERGENERATOR_OP_DEBUG)
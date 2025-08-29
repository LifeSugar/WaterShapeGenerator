import bpy
from . import resource

def get_preview_images(self, context):
    if "main" not in resource.preview_collections:
        return []
    
    pcoll = resource.preview_collections["main"]
    
    # EnumProperty 需要一个包含 (ID, 显示名称, 描述) 的元组列表
    return [(name, name.replace("_", " ").title(), "") for name, item in pcoll.items()]


class WaterShapeGeneratorProperties(bpy.types.PropertyGroup):
    preview_selector : bpy.props.EnumProperty(
        name="选择预览图",
        description="切换不同的预览图片",
        items = get_preview_images,
    ) # pyright: ignore[reportInvalidTypeForm]
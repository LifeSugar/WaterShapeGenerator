import bpy
from . import resource

# 添加缓存来避免文字跳变
_cached_preview_items = []

def get_preview_images(self, context):
    global _cached_preview_items
    
    if "main" not in resource.preview_collections:
        return []
    
    pcoll = resource.preview_collections["main"]
    
    # 如果预览集合没有改变，返回缓存的结果
    if _cached_preview_items and len(_cached_preview_items) == len(pcoll):
        return _cached_preview_items
    
    # EnumProperty 需要一个包含 (ID, 显示名称, 描述) 的元组列表
    # 创建稳定的枚举项，避免文字跳变
    items = []
    for name, item in pcoll.items():
        # 清理显示名称，移除文件扩展名和特殊字符
        clean_name = name.replace("_", " ")
        if "." in clean_name:
            clean_name = clean_name.split(".")[0]  # 移除文件扩展名
        
        # 特殊处理数字开头的名称
        if clean_name.startswith("img_"):
            clean_name = clean_name[4:]  # 移除 "img_" 前缀
        
        # 标题化处理，但避免过于复杂的字符串操作
        display_name = clean_name.title()
        
        # 确保描述是稳定的
        description = f"预览图: {display_name}"
        
        items.append((name, display_name, description))
    
    # 缓存结果
    _cached_preview_items = items
    return items


class WaterShapeGeneratorProperties(bpy.types.PropertyGroup):
    preview_selector : bpy.props.EnumProperty(
        name="选择预览图",
        description="切换不同的预览图片",
        items = get_preview_images,
    ) # pyright: ignore[reportInvalidTypeForm]
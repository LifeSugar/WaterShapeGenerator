import bpy 
import os
from bpy.utils import previews

custom_icons = None

def register_icon():
    global custom_icons
    custom_icons = previews.new()
    current_dir = os.path.dirname(__file__)
    addon_path = os.path.dirname(current_dir)
    icons_dir = os.path.join(addon_path, "assets", "icons")
    for icon in os.listdir(icons_dir):
        if icon.endswith(".png"): 
            name = os.path.splitext(icon)[0]
            custom_icons.load(name, os.path.join(icons_dir, icon), 'IMAGE')
            print(f"[WaterShapeGenerator] Loaded icon: {name}")

def unregister_icon():
    global custom_icons
    previews.remove(custom_icons)
    custom_icons = None


preview_collections = {}

def register_previews():
    # 路径构建是正确的
    previews_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "images")
    if not os.path.exists(previews_dir):
        print(f"[GeoPropsCN] 预览图目录不存在: {previews_dir}")
        return
    
    # 创建新的预览集
    pcoll = previews.new()

    # 将预览集存入全局字典
    preview_collections["main"] = pcoll

    # 遍历目录中的所有文件 (已简化循环)
    for image_file in sorted(os.listdir(previews_dir)):
        if image_file.lower().endswith((".png", ".jpg", ".jpeg")):
            name = os.path.splitext(image_file)[0]
            # 加载图片
            pcoll.load(name, os.path.join(previews_dir, image_file), 'IMAGE')
            print(f"加载预览图: {name}")

def unregister_previews():
    for pcoll in preview_collections.values():
        previews.remove(pcoll)
    preview_collections.clear()

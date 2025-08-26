import bpy
import os

# 英文属性名到中文的映射（基于 socket 的 name）
PROPERTY_NAME_MAP = {
    "Resample Length": "重采样长度",
    "Progress": "进度",
    "Droplet Min Speed": "液滴最小速度",
    "Droplet Max Speed": "液滴最大速度",
    "Droplet Min Size": "液滴最小尺寸",
    "Droplet Max Size": "液滴最大尺寸",
    "Droplet Distance": "液滴距离",
    "Surface Noise": "表面噪声",
    "Wave Speed": "波浪速度",
    "Wave Frequency": "波浪频率",
    "Wave Area": "波浪区域",
    "Wave Amplitude": "波浪幅度",
    "Curve": "曲线",
}

def cn_name(name: str) -> str:
    return PROPERTY_NAME_MAP.get(name, name)

#文件操作
def _add_root():
    return os.path.dirname(os.path.dirname(__file__))

#获取对象
def load_info_from_asset(obj_name: str, blend_name: str = "debug.blend"):
    # addon_root = os.path.dirname(os.path.dirname(__file__))
    # asset_path = os.path.join(addon_root, "assets", "debug.blend")
    asset_path = os.path.join(_add_root(), "assets", blend_name)
    if not os.path.exists(asset_path):
        print(f"Asset file not found: {asset_path}")
        return None

    with bpy.data.libraries.load(asset_path, link=False) as (data_from, data_to):
        # if obj_name in data_from.objects:
        #     data_to.objects = [obj_name]
        # else:
        #     print(f"Object '{obj_name}' not found in the asset file.")
        #     return None
        for obj in data_from.objects:
            print(f"Found object in asset: {obj}")
        for col in data_from.collections:
            print(f"Found collection in asset: {col}")
        for mat in data_from.materials:
            print(f"Found material in asset: {mat}")
        for node_group in data_from.node_groups:
            print(f"Found node group in asset: {node_group}")

#获取集合
def load_collection_from_asset(col_name: str, blend_name: str = "debug.blend"):
    asset_path = os.path.join(_add_root(), "assets", blend_name)
    if not os.path.exists(asset_path):
        print(f"Asset file not found: {asset_path}")
        return None

    with bpy.data.libraries.load(asset_path, link=False) as (data_from, data_to):
        if col_name in data_from.collections:
            data_to.collections = [col_name]
        else:
            print(f"Collection '{col_name}' not found in the asset file.")
            return None

    for col in data_to.collections:
        if col is not None:
            bpy.context.scene.collection.children.link(col)
            print(f"Linked collection: {col.name}")
            for obj in col.objects:
                print(f" - Contains object: {obj.name}")
        else:
            print("No collection loaded.")
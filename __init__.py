# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import bpy
import os
from .includes import panels, operators, resource, properties


bl_info = {
    "name": "水体生成器",
    "blender": (3, 0, 0),
    "category": "Object",
}

classes = [
    properties.WaterShapeGeneratorProperties,
    operators.WATERGENERATOR_OP_DEBUG,
    operators.WATERGENERATOR_OP_PrintImageName,
    operators.WATERGENERATOR_OP_SetPreview,
    operators.WATERGENERATOR_OP_GenerateWater,
    # panels.WATERGENERATOR_PT_GeoNodeProps,  # 不再注册，但保留类用于在主面板中调用
    panels.WATERGENERATOR_PT_MainPanel,
]

def register():
    resource.register_icon()
    resource.register_previews()

    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.water_shape_generator_props = bpy.props.PointerProperty(type=properties.WaterShapeGeneratorProperties)

def unregister():
    del bpy.types.Scene.water_shape_generator_props

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    resource.unregister_icon()
    resource.unregister_previews()

if __name__ == "__main__":
    register()

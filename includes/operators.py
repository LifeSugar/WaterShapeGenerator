import bpy
from . import method



class WATERGENERATOR_OP_DEBUG(bpy.types.Operator):
    bl_idname = "wm.debug_operator"
    bl_label = "Debug Operator"

    def execute(self, context):
        self.report({'INFO'}, "Debug operator executed")
        method.load_info_from_asset("")
        method.load_collection_from_asset("Liquid on curve with a surface interface")
        return {'FINISHED'}
    

def register():
    bpy.utils.register_class(WATERGENERATOR_OP_DEBUG)

def unregister():
    bpy.utils.unregister_class(WATERGENERATOR_OP_DEBUG)
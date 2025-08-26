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
from .includes import panels, operators

bl_info = {
    "name": "水体生成器",
    "blender": (3, 0, 0),
    "category": "Object",
}

def register():
    panels.register()
    operators.register()

def unregister():
    panels.unregister()
    operators.unregister()

if __name__ == "__main__":
    register()

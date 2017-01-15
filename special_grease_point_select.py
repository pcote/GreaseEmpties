# grease_empties.py Copyright (C) 2016, cotejrp1
#
# Place empties along the path of grease pencil strokes
#
# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

bl_info = {
    "name": "Special Grease Point Select",
    "author": "cotejrp1",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "To be determined",
    "description": "Selection of points on a grease pencil stroke.",
    "warning": "work in progress",
    "wiki_url": "none",
    "category": "Uncategorized",
}

import bpy
from bpy.props import IntProperty, EnumProperty


def points(strokes):
    for stroke in strokes:
        for point in stroke.points:
            yield point


class GreaseSpecialSelect(bpy.types.Operator):
    bl_label = "Grease Special Select"
    bl_idname = "object.grease_special_select"
    bl_options = {"REGISTER", "UNDO"}

    every_nth = IntProperty("Every Nth", min=1, max=100, default=1)
    select_methods = [(x,x,x) for x in "random every_nth".split()]
    select_method_choice = EnumProperty(name="Selection Method", items=select_methods)


    @classmethod
    def poll(cls, cxt):
        pencil = cxt.scene.grease_pencil
        return pencil and pencil.layers.active.active_frame.strokes
    
    def execute(self, cxt):
        
        def every_nth_select(idx, pt):
            if idx % self.every_nth == 0:
                return True
            else:
                return False
        
        
        def random_select():
            import random
            import time
            random.seed(time.time())
            return bool(random.randrange(2))
        
        
        pencil = cxt.scene.grease_pencil
        pencil.use_stroke_edit_mode = True
        strokes = pencil.layers.active.active_frame.strokes
        
        for n, point in enumerate(points(strokes)):
            if self.select_method_choice == "every_nth":
                point.select = every_nth_select(n, point)
            else:
                point.select = random_select()
        return {"FINISHED"}


class GreaseSelectPanel(bpy.types.Panel):
    bl_label = "Grease Pencil Select"
    bl_region_type = "TOOLS"
    bl_category = "Grease Pencil"
    bl_space_type = "VIEW_3D"
    
    def draw(self, cxt):
        layout = self.layout
        row = layout.row()
        col = row.column()
        col.operator(GreaseSpecialSelect.bl_idname)


def register():
    bpy.utils.register_class(GreaseSpecialSelect)
    bpy.utils.register_class(GreaseSelectPanel)    


def unregister():
    bpy.utils.unregister_class(GreaseSpecialSelect)
    bpy.utils.unregister_class(GreaseSelectPanel)

if __name__ == '__main__':
    register()

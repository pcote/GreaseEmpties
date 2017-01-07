import bpy
from bpy.props import IntProperty, EnumProperty

def points(strokes):
    for stroke in strokes:
        for point in stroke.points:
            yield point


def get_empty_options():
    draw_type_choices = ['PLAIN_AXES', 'ARROWS', 'SINGLE_ARROW', 'CIRCLE',
                         'CUBE', 'SPHERE', 'CONE', 'IMAGE']
    draw_type_choices = [(x, x, x) for x in draw_type_choices]
    return draw_type_choices


class GreaseEmpties(bpy.types.Operator):
    bl_label = "Grease Empties"
    bl_idname = "object.grease_empties"
    bl_options = {"REGISTER", "UNDO"}

    every_nth = IntProperty("Every Nth", min=1, max=100, default=1)
    draw_type_choice = EnumProperty(name="Empty Draw Type", items=get_empty_options())

    def execute(self, cxt):
        pencil = cxt.scene.grease_pencil
        strokes = pencil.layers.active.active_frame.strokes

        for n, point in enumerate(points(strokes)):
            if n % self.every_nth == 0:
                x, y, z = point.co
                new_empty = bpy.data.objects.new("empty", object_data=None)
                cxt.scene.objects.link(new_empty)
                new_empty.location = x, y, z
                new_empty.empty_draw_type = self.draw_type_choice
        return {"FINISHED"}


def register():
    bpy.utils.register_class(GreaseEmpties)


def unregister():
    bpy.utils.unregister_class(GreaseEmpties)


if __name__ == '__main__':
    register()
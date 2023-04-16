import pyvista as pv

from package.figures.figure import Figure, FigureTypes
from package.figures.primitives.cone import Cone
from package.figures.primitives.cylinder import Cylinder
from package.figures.primitives.curve import Curve
from package.figures.primitives.line import Line
from package.figures.primitives.plane import Plane
from package.figures.primitives.revolution_surface import RevolutionSurface

import uuid
import copy


class ObjectManager:
    def __init__(self):
        self.objects = dict()

    def create_cone(self, curve, point, t_bounce, v_bounce, **kwargs) -> str:
        uid = uuid.uuid4()
        cone = Cone(curve, point, t_bounce, v_bounce, uid, **kwargs)
        self.objects[uid] = cone

        return uid

    def update_cone(self, uid, **kwargs):
        if uid not in self.objects:
            raise Exception("Figure not found")

        obj = self.objects[uid]

        if obj.get_type() == FigureTypes.CONE:
            raise Exception("Object is not a cone")

        obj.update_settings(**kwargs)

    def create_cylinder(self, curve, direction, t_bounce, v_bounce, **kwargs) -> str:
        uid = uuid.uuid4()

        cylinder = Cylinder(curve, direction, t_bounce, v_bounce, uid, **kwargs)
        self.objects[uid] = cylinder

        return uid

    def update_cylinder(self, uid, **kwargs):
        if uid not in self.objects:
            raise Exception("Figure not found")

        obj = self.objects[uid]

        if obj.get_type() == FigureTypes.CYLINDER:
            raise Exception("Object is not a cylinder")

        obj.update_settings(**kwargs)

    def create_revolution_surface(self, curve, direction, point, t_bounce, **kwargs) -> str:
        uid = uuid.uuid4()

        surf = RevolutionSurface(curve, direction, point, t_bounce, uid, **kwargs)
        self.objects[uid] = surf

        return uid

    def update_revolution_surface(self, uid, **kwargs):
        if uid not in self.objects:
            raise Exception("Figure not found")

        obj = self.objects[uid]

        if obj.get_type() == FigureTypes.REVOLUTION:
            raise Exception("Object is not a revolution surface")

        obj.update_settings(**kwargs)

    def create_curve(self, curve, t_bounce, **kwargs) -> str:
        uid = uuid.uuid4()

        curve = Curve(curve, t_bounce, uid, **kwargs)
        self.objects[uid] = curve

        return uid

    def update_curve(self, uid, **kwargs):
        if uid not in self.objects:
            raise Exception("Figure not found")

        obj = self.objects[uid]

        if obj.get_type() == FigureTypes.CYLINDER:
            raise Exception("Object is not a cylinder")

        obj.update_settings(**kwargs)

    def create_line(self, point1, point2, t_bounce, **kwargs) -> str:
        uid = uuid.uuid4()

        line = Line(point1, point2, t_bounce, uid, **kwargs)
        self.objects[uid] = line

        return uid

    def update_line(self, uid, **kwargs):
        if uid not in self.objects:
            raise Exception("Figure not found")

        obj = self.objects[uid]

        if obj.get_type() == FigureTypes.LINE:
            raise Exception("Object is not a line")

        obj.update_settings(**kwargs)

    def create_plane(self, normal, point, size, **kwargs) -> str:
        uid = uuid.uuid4()

        plane = Plane(normal, point, size, uid, **kwargs)
        self.objects[uid] = plane

        return uid

    def update_plane(self, uid, **kwargs):
        if uid not in self.objects:
            raise Exception("Figure not found")

        obj = self.objects[uid]

        if obj.get_type() == FigureTypes.PLANE:
            raise Exception("Object is not a plane")

        obj.update_settings(**kwargs)

    def get_figure(self, uid: str) -> Figure:
        if uid not in self.objects:
            raise Exception("Figure not found")
        return copy.deepcopy(self.objects[uid])

    def get_figure_mesh(self, uid: str) -> pv.PolyData:
        if uid not in self.objects:
            raise Exception("Figure not found")
        return self.objects[uid].get_mesh()

    def get_figure_actor(self, uid: str) -> pv.Actor:
        if uid not in self.objects:
            raise Exception("Figure not found")
        return self.objects[uid].get_actor()

    def get_figure_settings(self, uid: str) -> dict:
        if uid not in self.objects:
            raise Exception("Figure not found")
        return self.objects[uid].get_settings()

    def update_figure_actor(self, uid: str, actor: str):
        if uid not in self.objects:
            raise Exception("Figure not found")
        return self.objects[uid].update_actor(actor)

    def delete_figure(self, uid: str) -> Figure:
        if uid not in self.objects:
            raise Exception("Figure not found")
        obj = self.objects[uid]
        del self.objects[uid]
        return obj.copy()

    def update_object_settings(self, uid: str, **kwargs) -> Figure:
        obj = self.objects[uid]
        obj.update_settings(**kwargs)
        return obj


# Example
if __name__ == "__main__":
    import numpy as np
    manager = ObjectManager()
    curve = (lambda t: np.sin(t), lambda t: np.cos(t) * 0, lambda t: t)
    t_bounce = (0, 2 * np.pi)
    v_bounce = (0, 2)
    point = (5, 5, 5)
    direction = (2,5,3)
    
    uid = manager.create_revolution_surface(curve, direction, point, t_bounce)

    p = pv.Plotter()
    p.add_mesh(manager.get_figure_mesh(uid))
    p.show()

    curve1 = (lambda t: np.sin(t), lambda t: np.cos(t), lambda t: t * 0 + 5)
    vector = (0, 0, 1)
    uid = manager.create_curve(curve1, t_bounce)
    p = pv.Plotter()
    p.add_mesh(manager.get_figure_mesh(uid))
    p.show()

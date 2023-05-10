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

    def create_cone(self, curve, point, t_bounds, v_bounds, **kwargs) -> str:
        uid = uuid.uuid4()
        cone = Cone(curve, point, t_bounds, v_bounds, uid, **kwargs)
        self.objects[uid] = cone

        return uid

    def update_cone(self, uid, **kwargs):
        if uid not in self.objects:
            raise Exception("Figure not found")

        obj = self.objects[uid]

        if obj.get_type() != FigureTypes.CONE:
            raise Exception("Object is not a cone")

        obj.update_parameters(**kwargs)

    def create_cylinder(self, curve, direction, t_bounds, v_bounds, **kwargs) -> str:
        uid = uuid.uuid4()

        cylinder = Cylinder(curve, direction, t_bounds, v_bounds, uid, **kwargs)
        self.objects[uid] = cylinder

        return uid

    def update_cylinder(self, uid, **kwargs):
        if uid not in self.objects:
            raise Exception("Figure not found")

        obj = self.objects[uid]

        if obj.get_type() != FigureTypes.CYLINDER:
            raise Exception("Object is not a cylinder")

        obj.update_parameters(**kwargs)

    def create_revolution_surface(self, curve, direction, point, t_bounds, **kwargs) -> str:
        uid = uuid.uuid4()

        surf = RevolutionSurface(curve, direction, point, t_bounds, uid, **kwargs)
        self.objects[uid] = surf

        return uid

    def update_revolution_surface(self, uid, **kwargs):
        if uid not in self.objects:
            raise Exception("Figure not found")

        obj = self.objects[uid]

        if obj.get_type() != FigureTypes.REVOLUTION:
            raise Exception("Object is not a revolution surface")

        obj.update_parameters(**kwargs)

    def create_curve(self, curve, t_bounds, **kwargs) -> str:
        uid = uuid.uuid4()

        curve = Curve(curve, t_bounds, uid, **kwargs)
        self.objects[uid] = curve

        return uid

    def update_curve(self, uid, **kwargs):
        if uid not in self.objects:
            raise Exception("Figure not found")

        obj = self.objects[uid]

        if obj.get_type() != FigureTypes.CURVE:
            raise Exception("Object is not a curve")

        obj.update_parameters(**kwargs)
    

    def compute_intersections(self):
        planes = [pv.PolyData(self.objects[uid].get_mesh().extract_surface()).triangulate() for uid in self.objects if self.objects[uid].get_type() == FigureTypes.PLANE]
        intersections = []
        
        for uid in self.objects:
            if self.objects[uid].get_type() == FigureTypes.PLANE:
                continue
            mesh = pv.PolyData(self.objects[uid].get_mesh().extract_surface()).triangulate()
            for plane in planes:
                intersection,_,_ = mesh.intersection(plane)
                if intersection.n_verts == 0:
                    intersections.append(intersection)
        return intersections
            

    def create_line(self, point1, point2, t_bounds, **kwargs) -> str:
        uid = uuid.uuid4()

        line = Line(point1, point2, t_bounds, uid, **kwargs)
        self.objects[uid] = line

        return uid

    def update_line(self, uid, **kwargs):
        if uid not in self.objects:
            raise Exception("Figure not found")

        obj = self.objects[uid]

        if obj.get_type() != FigureTypes.LINE:
            raise Exception("Object is not a line")

        obj.update_parameters(**kwargs)

    def create_plane(self, normal, point, size, **kwargs) -> str:
        uid = uuid.uuid4()

        plane = Plane(normal, point, size, uid, **kwargs)
        self.objects[uid] = plane

        return uid

    def update_plane(self, uid, **kwargs):
        if uid not in self.objects:
            raise Exception("Figure not found")

        obj = self.objects[uid]

        if obj.get_type() != FigureTypes.PLANE:
            raise Exception("Object is not a plane")

        obj.update_parameters(**kwargs)

    def get_labels(self, figure_type, counter):
        labels = dict()
        t = figure_type["t_bounds"]
        if figure_type["FigureTypes"] == FigureTypes.CONE:
            labels["C" + str(counter)] = figure_type["point"]
            labels["Y" + str(counter)] = (figure_type["curve"][0](t[0] * 0.9),
                                          figure_type["curve"][1](t[0] * 0.9),
                                          figure_type["curve"][2](t[0] * 0.9))

            labels["P" + str(counter)] = (figure_type["curve"][0](t[0] * 0.5),
                                          figure_type["curve"][1](t[0] * 0.5),
                                          figure_type["curve"][2](t[0] * 0.5))
            s = tuple((ai + bi)/2 for ai, bi in zip(labels["P" + str(counter)], figure_type["direction"]))
            labels["L" + str(counter)] = s
            return labels

        elif figure_type["FigureTypes"] == FigureTypes.CYLINDER:
            labels["P" + str(counter)] = (figure_type["curve"][0](t[0] * 0.5),
                                          figure_type["curve"][1](t[0] * 0.5),
                                          figure_type["curve"][2](t[0] * 0.5))
            s = tuple((ai + bi)/2 for ai, bi in zip(labels["P" + str(counter)], figure_type["direction"]))
            labels["S" + str(counter)] = s

            labels["Y" + str(counter)] = (figure_type["curve"][0](t[0] * 0.9),
                                          figure_type["curve"][1](t[0] * 0.9),
                                          figure_type["curve"][2](t[0] * 0.9))
            return labels

        elif figure_type["FigureTypes"] == FigureTypes.CURVE:
            labels["P" + str(counter)] = (figure_type["curve"][0](t[0] * 0.5),
                                          figure_type["curve"][1](t[0] * 0.5),
                                          figure_type["curve"][2](t[0] * 0.5))
            return labels

        elif figure_type["FigureTypes"] == FigureTypes.LINE:
            labels["P" + str(counter)] = (figure_type["curve"][0](t[0] * 0.5),
                                          figure_type["curve"][1](t[0] * 0.5),
                                          figure_type["curve"][2](t[0] * 0.5))
            return labels

        elif figure_type["FigureTypes"] == FigureTypes.PLANE:
            labels["M" + str(counter)] = figure_type["point"]
            labels["n" + str(counter)] = tuple((ai + bi)/ 2 for ai, bi in zip(figure_type["point"], figure_type["normal"]))
            return labels

        elif figure_type["FigureTypes"] == FigureTypes.REVOLUTION:
            labels["P" + str(counter)] = figure_type["point"]

            s = tuple((ai + bi)/2 for ai, bi in zip(labels["P" + str(counter)], figure_type["direction"]))
            labels["S" + str(counter)] = s
            labels["Y" + str(counter)] = (figure_type["curve"][0](t[0] * 0.9),
                                          figure_type["curve"][1](t[0] * 0.9),
                                          figure_type["curve"][2](t[0] * 0.9))
            return labels
    def get_label_lines(self, figure_type):
        meshes = []
        t = figure_type["t_bounds"]
        P = (figure_type["curve"][0](t[0] * 0.5),
             figure_type["curve"][1](t[0] * 0.5),
             figure_type["curve"][2](t[0] * 0.5))
        if figure_type["FigureTypes"] == FigureTypes.CONE:
            curve = self.create_curve(figure_type["curve"], t)
            meshes.append(self.get_figure_mesh(curve))
            line = self.create_line(figure_type["point"], P, t)
            meshes.append(self.get_figure_mesh(line))
            return meshes

        elif figure_type["FigureTypes"] == FigureTypes.CYLINDER:

            s = tuple(ai + bi for ai, bi in zip(P, figure_type["direction"]))
            line = self.create_line(P, s, t)
            meshes.append(self.get_figure_mesh(line))

            curve = self.create_curve(figure_type["curve"], t)
            meshes.append(self.get_figure_mesh(curve))
            return meshes

        elif figure_type["FigureTypes"] == FigureTypes.PLANE:
            s = tuple(ai + bi for ai, bi in zip(figure_type["point"], figure_type["normal"]))

            line = self.create_line(figure_type["point"], s, t)
            meshes.append(self.get_figure_mesh(line))
            return meshes

        elif figure_type["FigureTypes"] == FigureTypes.REVOLUTION:

            s = tuple(ai + bi for ai, bi in zip(figure_type["point"], figure_type["direction"]))
            line = self.create_line(figure_type["point"], s, t)
            meshes.append(self.get_figure_mesh(line))

            curve = self.create_curve(figure_type["curve"], t)
            meshes.append(self.get_figure_mesh(curve))
            return meshes

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
        #return obj.copy()

    def update_object_settings(self, uid: str, **kwargs) -> Figure:
        obj = self.objects[uid]
        obj.update_settings(**kwargs)
        return obj


# Example
if __name__ == "__main__":
    import numpy as np

    manager = ObjectManager()
    curve = (lambda t: np.sin(t), lambda t: np.cos(t) * 0, lambda t: t)
    t_bounds = (0, 2 * np.pi)
    v_bounds = (0, 2)
    point = (5, 5, 5)
    direction = (2, 5, 3)

    uid = manager.create_revolution_surface(curve, direction, point, t_bounds)

    p = pv.Plotter()
    p.add_mesh(manager.get_figure_mesh(uid))
    p.show()

    curve1 = (lambda t: np.sin(t), lambda t: np.cos(t), lambda t: t * 0 + 5)
    vector = (0, 0, 1)
    uid = manager.create_curve(curve1, t_bounds)
    p = pv.Plotter()
    p.add_mesh(manager.get_figure_mesh(uid))
    p.show()

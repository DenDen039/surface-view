import pyvista as pv

from package.figures.figure import Figure, FigureTypes
from package.figures.primitives.cone import Cone
from package.figures.primitives.cylinder import Cylinder
from package.figures.primitives.curve import Curve
from package.figures.primitives.line import Line
from package.figures.primitives.plane import Plane
from package.figures.primitives.parametric_surface import ParametricSurface
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
        if len(planes) == 0:
            return []
        intersections = []
        
        for uid in self.objects:
            if self.objects[uid].get_type() in (FigureTypes.PLANE, FigureTypes.CURVE, FigureTypes.LINE):
                continue
            mesh = pv.PolyData(self.objects[uid].get_mesh().extract_surface()).triangulate().decimate(0.7)
            for plane in planes:
                intersection, _, _ = mesh.intersection(plane, split_first=False, split_second=False)

                if intersection.n_points != 0:
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
    
    def create_paramteric_surface(self, surface, t_bounds, v_bounds, **kwargs) -> str:
        uid = uuid.uuid4()

        surface = ParametricSurface(surface, t_bounds, v_bounds, uid, **kwargs)
        self.objects[uid] = surface

        return uid

    def update_plane(self, uid, **kwargs):
        if uid not in self.objects:
            raise Exception("Figure not found")

        obj = self.objects[uid]

        if obj.get_type() != FigureTypes.PARAMETRIC_SURFACE:
            raise Exception("Object is not a parametric surface")

        obj.update_parameters(**kwargs)


    def get_labels(self, figure_type, counter):
        labels = dict()
        t = figure_type["t_bounds"]
        if figure_type["FigureTypes"] == FigureTypes.CONE:

            c = figure_type["point"]
            c_r = tuple(round(coord, 2) for coord in c)
            labels["C" + str(c_r)] = c
            y = (figure_type["curve"][0](t[0] * 0.9),
                  figure_type["curve"][1](t[0] * 0.9),
                  figure_type["curve"][2](t[0] * 0.9))
            y_r = tuple(round(coord, 2) for coord in y)
            labels["Y" + str(y_r)] = y
            P = (figure_type["curve"][0](t[0] * 0.5),
                 figure_type["curve"][1](t[0] * 0.5),
                 figure_type["curve"][2](t[0] * 0.5))
            P_r = tuple(round(coord, 2) for coord in P)
            labels["P" + str(P_r)] = P
            s = tuple((ai + bi)/2 for ai, bi in zip(labels["P" + str(P_r)], figure_type["point"]))
            s_r = tuple(round(coord, 2) for coord in s)
            labels["L" + str(s_r)] = s

            return labels

        elif figure_type["FigureTypes"] == FigureTypes.CYLINDER:
            P = (figure_type["curve"][0](t[0] * 0.5),
                 figure_type["curve"][1](t[0] * 0.5),
                 figure_type["curve"][2](t[0] * 0.5))
            P_r = tuple(round(coord, 2) for coord in P)
            labels["P" + str(P_r)] = P
            s = tuple((ai + bi) for ai, bi in zip(labels["P" + str(P_r)], figure_type["direction"]))
            s_r = tuple(round(coord, 2) for coord in s)
            labels["S" + str(s_r)] = s

            y = (figure_type["curve"][0](t[0] * 0.9),
                 figure_type["curve"][1](t[0] * 0.9),
                 figure_type["curve"][2](t[0] * 0.9))
            y_r = tuple(round(coord, 2) for coord in y)
            labels["Y" + str(y_r)] = y
            return labels

        elif figure_type["FigureTypes"] == FigureTypes.CURVE:
            P = (figure_type["curve"][0](t[0] * 0.5),
                 figure_type["curve"][1](t[0] * 0.5),
                 figure_type["curve"][2](t[0] * 0.5))
            P_r = tuple(round(coord, 2) for coord in P)
            labels["P" + str(P_r)] = P
            return labels

        elif figure_type["FigureTypes"] == FigureTypes.LINE:

            P = tuple((ai + bi) / 2 for ai, bi in zip(figure_type["point1"], figure_type["point2"]))
            P_r = tuple(round(coord, 2) for coord in P)
            labels["P" + str(P_r)] = P

            return labels


        elif figure_type["FigureTypes"] == FigureTypes.PLANE:
            m = figure_type["point"]
            m_r = tuple(round(coord, 2) for coord in m)
            labels["M" + str(m_r)] = m
            n = tuple((ai + bi) for ai, bi in zip(figure_type["point"], figure_type["normal"]))
            n_r = tuple(round(coord, 2) for coord in n)
            labels["n" + str(n_r)] = n
            return labels

        elif figure_type["FigureTypes"] == FigureTypes.REVOLUTION:

            P = figure_type["point"]
            P_r = tuple(round(coord, 2) for coord in P)
            labels["P" + str(P_r)] = P

           # s = tuple((ai + bi)/2 for ai, bi in zip(labels["P" + str(counter)], figure_type["direction"]))
            #labels["S" + str(counter)] = s
            s = tuple((ai + bi) for ai, bi in zip(labels["P" + str(P_r)], figure_type["direction"]))
            s_r = tuple(round(coord, 2) for coord in s)
            labels["S" + str(s_r)] = s
            y = (figure_type["curve"][0](t[0] * 0.9),
                 figure_type["curve"][1](t[0] * 0.9),
                 figure_type["curve"][2](t[0] * 0.9))
            y_r = tuple(round(coord, 2) for coord in y)
            labels["Y" + str(y_r)] = y
            return labels

    def get_label_lines(self, figure_type):
        meshes = []

        if figure_type["FigureTypes"] in [FigureTypes.LINE, FigureTypes.CURVE, FigureTypes.POINT]:
            return meshes

        t = figure_type["t_bounds"]

        if figure_type["FigureTypes"] == FigureTypes.PLANE:
            s = tuple(ai + bi for ai, bi in zip(figure_type["point"], figure_type["normal"]))

            line = self.create_line(figure_type["point"], s, [0, 1.05])
            meshes.append(self.get_figure_mesh(line))
            return meshes


        P = (figure_type["curve"][0](t[0] * 0.5),
             figure_type["curve"][1](t[0] * 0.5),
             figure_type["curve"][2](t[0] * 0.5))

        if figure_type["FigureTypes"] == FigureTypes.CONE:
            curve = Curve(figure_type["curve"], t, uuid.uuid4())
            #curve = self.create_curve(figure_type["curve"], t)
            meshes.append(curve.get_mesh())

            line = Line(P, figure_type["point"], figure_type["v_bounds"] , uuid.uuid4()) # [t_i * 0.1 for t_i in t]
            meshes.append(line.get_mesh())
            return meshes

        elif figure_type["FigureTypes"] == FigureTypes.CYLINDER:

            s = tuple(ai + bi for ai, bi in zip(P, figure_type["direction"]))

            line = Line(P, s, figure_type["v_bounds"], uuid.uuid4())

            #line = self.create_line(P, s, t)
            #meshes.append(self.get_figure_mesh(line))
            meshes.append(line.get_mesh())

            #curve = self.create_curve(figure_type["curve"], t)
            curve = Curve(figure_type["curve"], t, uuid.uuid4())
            meshes.append(curve.get_mesh())
            #meshes.append(self.get_figure_mesh(curve))
            return meshes

        elif figure_type["FigureTypes"] == FigureTypes.REVOLUTION:

            s = tuple(ai + bi for ai, bi in zip(figure_type["point"], figure_type["direction"]))
            line = self.create_line(figure_type["point"], s, (t[0] * 0.7, t[1] *0.1))
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

    def wipe(self):
        self.objects = dict()

# Example
if __name__ == "__main__":
    import numpy as np
    manager = ObjectManager()
    theta_bounds = (-100,100)
    phi_bounds = (0,2*np.pi)
    a = 3
    b = 3
    c = 5
    surface = (lambda theta,phi: a*np.cosh(theta)*np.cos(phi),
               lambda theta,phi: b*np.cosh(theta)*np.sin(phi),
               lambda theta,phi: c * np.sinh(theta))
    

    uid = manager.create_paramteric_surface(surface, theta_bounds, phi_bounds)

    p = pv.Plotter()
    p.add_mesh(manager.get_figure_mesh(uid))
    p.show()

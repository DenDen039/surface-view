from package.object_manager.manager import ObjectManager
from package.figures.figure import FigureTypes
from unittest.mock import MagicMock
from numpy import *
import json


class ObjectStorage:
    def __init__(self, PW, SWO):

        self.objManager = ObjectManager()
        self.storage = dict()
        self.SWO = SWO
        self.PW = PW
        self.counter = 0
        self.label_counter = 0
        self.feature_flag = False

    def save(self, path):
        jsonString = json.dumps(self.storage)
        jsonFile = open(path, "w")
        jsonFile.write(jsonString) 
        jsonFile.close()

    def load(self, path):
        with open(path, "r") as f:
            objects = json.load(f)

        self.feature_flag = False
        for obj in objects.values():
            self.create(obj)
        self.feature_flag = True

    def enable_intersections(self, intersections):
        self.feature_flag = intersections
        if self.feature_flag:
            intersections = self.objManager.compute_intersections()
            self.PW.drawIntersections(intersections)
        else:
            self.PW.drawIntersections([])

    def delete(self, uid):
        del self.storage[uid]
        self.objManager.delete_figure(uid)
        self.PW.remove_mesh(uid)
        if self.feature_flag:
            intersections = self.objManager.compute_intersections()
            self.PW.drawIntersections(intersections)
        self.SWO.delete(uid)

    def update(self, uid, new_data: dict):
        self.storage[uid] = new_data
        if new_data["FigureTypes"] == FigureTypes.CONE:
            self.objManager.update_cone(uid, **new_data)
        elif new_data["FigureTypes"] == FigureTypes.CYLINDER:
            self.objManager.update_cylinder(uid, **new_data)
        elif new_data["FigureTypes"] == FigureTypes.CURVE:
            self.objManager.update_curve(uid, **new_data)
        elif new_data["FigureTypes"] == FigureTypes.LINE:
            self.objManager.update_line(uid, **new_data)
        elif new_data["FigureTypes"] == FigureTypes.PLANE:
            self.objManager.update_plane(uid, **new_data)
        elif new_data["FigureTypes"] == FigureTypes.REVOLUTION:
            self.objManager.update_revolution_surface(uid, **new_data)
        else:
            raise Exception(f"Invalid Figure type {new_data['FigureTypes']}")

        self.objManager.update_object_settings(uid, **new_data)

        self.PW.remove_mesh(uid)
        self.PW.add_mesh(uid, self.objManager.get_figure_mesh(uid), **self.objManager.get_figure_settings(uid))
        if self.feature_flag:
            intersections = self.objManager.compute_intersections()
            self.PW.drawIntersections(intersections)
        self.SWO.update(uid, new_data["name"], new_data["FigureTypes"], new_data["color"])

    def create(self, to_create: dict):
        if to_create["name"] == '':
            to_create["name"] = 'untitled_' + str(self.counter)
            self.counter += 1
        if self.feature_flag:
            intersections = self.objManager.compute_intersections()
            self.PW.drawIntersections(intersections)
        if to_create["FigureTypes"] == FigureTypes.CONE:
            uid = self.objManager.create_cone(**to_create)
        elif to_create["FigureTypes"] == FigureTypes.CYLINDER:
            uid = self.objManager.create_cylinder(**to_create)
        elif to_create["FigureTypes"] == FigureTypes.CURVE:
            uid = self.objManager.create_curve(**to_create)
        elif to_create["FigureTypes"] == FigureTypes.LINE:
            uid = self.objManager.create_line(**to_create)
        elif to_create["FigureTypes"] == FigureTypes.PLANE:
            uid = self.objManager.create_plane(**to_create)
        elif to_create["FigureTypes"] == FigureTypes.REVOLUTION:
            uid = self.objManager.create_revolution_surface(**to_create)
        else:
            raise Exception(f"Invalid Figure type {to_create['FigureTypes']}")

        self.storage[uid] = to_create
        self.SWO.add(uid, to_create["name"], to_create["FigureTypes"], to_create["color"])
        self.PW.add_mesh(uid, self.objManager.get_figure_mesh(uid), to_create["FigureTypes"],
                         [self.objManager.get_label_lines(to_create), self.objManager.get_labels(to_create, self.label_counter)],
                         **self.objManager.get_figure_settings(uid))
        self.label_counter += 1

        return uid


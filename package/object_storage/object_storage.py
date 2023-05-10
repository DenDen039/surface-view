from package.object_manager.manager import ObjectManager
from package.figures.figure import FigureTypes
from unittest.mock import MagicMock
from numpy import *
import json
from uuid import UUID

from package.parser import Parser
from unittest.mock import MagicMock
from numpy import *

class ObjectStorage:
    def __init__(self, PW, SOW):

        self.objManager = ObjectManager()
        self.storage = dict()
        self.SOW = SOW
        self.PW = PW
        self.counter = 0
        self.__enable_intersections = True
        self.label_counter = 0
        self.parser = Parser()

    @property
    def enable_intersections(self):
        return self.__enable_intersections

    @enable_intersections.setter
    def enable_intersections(self, value: bool):
        if value:
            intersections = self.objManager.compute_intersections()
            self.PW.add_intersections(intersections)
            self.__enable_intersections = value
        else:
            intersections = []
            self.PW.add_intersections(intersections)
            self.__enable_intersections = value

    def load(self, file_path):
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            converted_data = {UUID(key): value for key, value in data.items()}
        temp = self.__enable_intersections
        self.__enable_intersections = False
        for obj in converted_data.values():
            self.create(obj)
        self.__enable_intersections = temp

    def save(self, file_path):
        converted_data = {str(key): value for key, value in self.storage.items()}
        with open(file_path, 'w') as json_file:
            json.dump(converted_data, json_file)

    def delete(self, uid):
        del self.storage[uid]
        self.PW.remove_label(uid)
        self.label_counter -= 1
        self.objManager.delete_figure(uid)
        self.PW.remove_mesh(uid)
        if self.enable_intersections:
            intersections = self.objManager.compute_intersections()
            self.PW.add_intersections(intersections)
        self.SOW.delete(uid)


    def update(self, uid, new_data: dict):
        self.storage[uid] = new_data
        if new_data["FigureTypes"] == FigureTypes.CONE:
            new_data["curve_string"] = new_data["curve"]

            new_data["curve"] = [self.parser.parse_expression_string_to_lambda(new_data["curve"][0]),
                                 self.parser.parse_expression_string_to_lambda(new_data["curve"][1]),
                                 self.parser.parse_expression_string_to_lambda(new_data["curve"][2])]
            self.objManager.update_cone(uid, **new_data)

        elif new_data["FigureTypes"] == FigureTypes.CYLINDER:

            new_data["curve_string"] = new_data["curve"]

            new_data["curve"] = [self.parser.parse_expression_string_to_lambda(new_data["curve"][0]),
                                 self.parser.parse_expression_string_to_lambda(new_data["curve"][1]),
                                 self.parser.parse_expression_string_to_lambda(new_data["curve"][2])]

            self.objManager.update_cylinder(uid, **new_data)
        elif new_data["FigureTypes"] == FigureTypes.CURVE:

            new_data["curve_string"] = new_data["curve"]

            new_data["curve"] = [self.parser.parse_expression_string_to_lambda(new_data["curve"][0]),
                                 self.parser.parse_expression_string_to_lambda(new_data["curve"][1]),
                                 self.parser.parse_expression_string_to_lambda(new_data["curve"][2])]

            self.objManager.update_curve(uid, **new_data)
        elif new_data["FigureTypes"] == FigureTypes.LINE:
            self.objManager.update_line(uid, **new_data)
        elif new_data["FigureTypes"] == FigureTypes.PLANE:
            self.objManager.update_plane(uid, **new_data)
        elif new_data["FigureTypes"] == FigureTypes.REVOLUTION:

            new_data["curve_string"] = new_data["curve"]

            new_data["curve"] = [self.parser.parse_expression_string_to_lambda(new_data["curve"][0]),
                                 self.parser.parse_expression_string_to_lambda(new_data["curve"][1]),
                                 self.parser.parse_expression_string_to_lambda(new_data["curve"][2])]

            self.objManager.update_revolution_surface(uid, **new_data)
        else:
            raise Exception(f"Invalid Figure type {new_data['FigureTypes']}")

        self.objManager.update_object_settings(uid, **new_data)

        self.PW.remove_mesh(uid)
        self.PW.remove_label(uid)

        #self.PW.add_mesh(uid, self.objManager.get_figure_mesh(uid), **self.objManager.get_figure_settings(uid))

        self.PW.add_mesh(uid, self.objManager.get_figure_mesh(uid),
                         new_data["FigureTypes"],
                         [self.objManager.get_label_lines(new_data),
                          self.objManager.get_labels(new_data, self.label_counter)],
                         **self.objManager.get_figure_settings(uid))


        self.PW.add_label(uid)

        if self.enable_intersections:
            intersections = self.objManager.compute_intersections()
            self.PW.add_intersections(intersections, color="red", line_width=5)

        self.SOW.update(uid, new_data["name"], new_data["FigureTypes"], new_data["color"])

    def create(self, to_create: dict):
        if to_create["name"] == '':
            to_create["name"] = 'untitled_' + str(self.counter)
            self.counter += 1

        if to_create["FigureTypes"] == FigureTypes.CONE:
            to_create["curve_string"] = to_create["curve"]

            to_create["curve"] = [self.parser.parse_expression_string_to_lambda(to_create["curve"][0]),
                                  self.parser.parse_expression_string_to_lambda(to_create["curve"][1]),
                                  self.parser.parse_expression_string_to_lambda(to_create["curve"][2])]
            uid = self.objManager.create_cone(**to_create)
        elif to_create["FigureTypes"] == FigureTypes.CYLINDER:
            to_create["curve_string"] = to_create["curve"]

            to_create["curve"] = [self.parser.parse_expression_string_to_lambda(to_create["curve"][0]),
                                  self.parser.parse_expression_string_to_lambda(to_create["curve"][1]),
                                  self.parser.parse_expression_string_to_lambda(to_create["curve"][2])]
            uid = self.objManager.create_cylinder(**to_create)
        elif to_create["FigureTypes"] == FigureTypes.CURVE:
            to_create["curve_string"] = to_create["curve"]

            to_create["curve"] = [self.parser.parse_expression_string_to_lambda(to_create["curve"][0]),
                                  self.parser.parse_expression_string_to_lambda(to_create["curve"][1]),
                                  self.parser.parse_expression_string_to_lambda(to_create["curve"][2])]
            uid = self.objManager.create_curve(**to_create)
        elif to_create["FigureTypes"] == FigureTypes.LINE:
            uid = self.objManager.create_line(**to_create)
        elif to_create["FigureTypes"] == FigureTypes.PLANE:
            uid = self.objManager.create_plane(**to_create)
        elif to_create["FigureTypes"] == FigureTypes.REVOLUTION:
            to_create["curve_string"] = to_create["curve"]

            to_create["curve"] = [self.parser.parse_expression_string_to_lambda(to_create["curve"][0]),
                                  self.parser.parse_expression_string_to_lambda(to_create["curve"][1]),
                                  self.parser.parse_expression_string_to_lambda(to_create["curve"][2])]
            uid = self.objManager.create_revolution_surface(**to_create)
        else:
            raise Exception(f"Invalid Figure type {to_create['FigureTypes']}")


        self.storage[uid] = to_create
        self.SOW.add(uid, to_create["name"], to_create["FigureTypes"], to_create["color"])
        self.PW.add_mesh(uid, self.objManager.get_figure_mesh(uid),
                         to_create["FigureTypes"],
                         [self.objManager.get_label_lines(to_create),
                          self.objManager.get_labels(to_create, self.label_counter)],
                         **self.objManager.get_figure_settings(uid))
       # self.enable_intersections = True
        if self.__enable_intersections:
            intersections = self.objManager.compute_intersections()
            self.PW.add_intersections(intersections, color="red", line_width=5)

        #self.PW.add_label(uid)
        self.label_counter += 1

        return uid


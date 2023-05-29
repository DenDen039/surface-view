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
    def __init__(self, PW, SOW, intersections_color, line_width):

        self.objManager = ObjectManager()
        self.storage = dict()
        self.SOW = SOW
        self.PW = PW
        self.counter = 0
        self.__enable_intersections = True
        self.label_counter = 0
        self.parser = Parser()

        self.saves_counter = self.untitled_counter()
        self.__intersections_color = intersections_color
        self.__line_width = line_width

    @property
    def enable_intersections(self):
        return self.__enable_intersections

    @enable_intersections.setter
    def enable_intersections(self, value: bool):
        self.__enable_intersections = value
        self.__draw_intersections()

    @property
    def intersections_color(self):
        return self.__intersections_color

    @intersections_color.setter
    def intersections_color(self, value):
        self.__intersections_color = value
        self.PW.remove_intersections()
        self.__draw_intersections()

    @property
    def line_width(self):
        print("line_width getter invoked")
        return self.__line_width

    @line_width.setter
    def line_width(self, value: float):
        self.__line_width = value
        self.__draw_intersections()

    def __draw_intersections(self):
        if not self.__enable_intersections:
            self.PW.remove_intersections()
            return

        intersections = self.objManager.compute_intersections()
        if self.__intersections_color is not None:
            colors = [self.intersections_color for i in range(len(intersections))]
        else:
            r = lambda: random.randint(150, 255)
            colors = ['#%02X%02X%02X' % (r(), r(), r()) for i in range(len(intersections))]

        self.PW.add_intersections(intersections, colors, self.line_width)

    def load(self, file_path):

       with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            converted_data = {UUID(key): value for key, value in data.items()}

            self.PW.clear_actors()
            self.PW.remove_intersections()
            self.objManager.wipe()
            for item in self.storage.keys():
                self.PW.remove_label(item)

            for obj in self.storage.keys():
                self.SOW.delete(obj)

            temp = self.enable_intersections
            self.enable_intersections = False
            for obj in converted_data.values():
                self.create(obj)
            self.enable_intersections = temp

    def save(self, file_path):
        save_items = self.storage.items()
        for item in save_items:
            if 'curve' in item[1]:
                item[1]['curve'], item[1]['curve_string'] = item[1]['curve_string'], None

        converted_data = {str(key): value for key, value in save_items}

        print(converted_data)
        if file_path is not None:
            with open(file_path, 'w') as json_file:
                json.dump(converted_data, json_file)
        else:
            file_name = f"untitled_{self.saves_counter}.json"
            file_path = f"scenes/{file_name}"

            print(file_path)
            with open(file_path, 'w') as json_file:
                json.dump(converted_data, json_file)
                self.saves_counter += 1

    def untitled_counter(self) -> int:
        import os

        if os.path.isdir("scenes") == False:
            dir_path = "scenes"
            os.mkdir(dir_path)

        files = os.listdir("scenes/")

        numbers = list(filter(lambda str: str.startswith("untitled_"), files))
        numbers = [int(numbers[i].split('untitled_')[-1].split('.json')[0]) for i in range(len(numbers))]
        if numbers:
            print(numbers)
            return max(numbers) + 1
        else:
            return 0


    def delete(self, uid):
        del self.storage[uid]
        self.PW.remove_label(uid)
        self.label_counter -= 1
        self.objManager.delete_figure(uid)
        self.PW.remove_mesh(uid)
        if self.__enable_intersections:
            self.__draw_intersections()
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

        if self.__enable_intersections:
            self.__draw_intersections()

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
            self.__draw_intersections()

        #self.PW.add_label(uid)
        self.label_counter += 1

        return uid


import PyQt5
import PyQt5.QtCore
from PyQt5.QtWidgets import *
import pyvista as pv
from pyvistaqt import QtInteractor
from package.ui.Widgets.CustomWidgets import Creator
import package.ui.Widgets.generated.userinterface_ as userinterface_
from package.figures.figure import *


from package.object_storage.object_storage import ObjectStorage


import ast
from numpy import *



# TODO: add parser (maybe as class)
#       add additional fields to user input (name of object, color, opacity, t_bounds)
#       rename bounds -> bounds
#       add update_widget
#       add prototype of storage_object_widget
#           1. List of objects in left
#           2. Add update, delete methods
#           3. Integrate with storage_object
#       refactor gui
#       add @fenik_fam `s PW
#       better function parser
#       parser for CommonObjectWidget

import ast
import numpy as np
import re




def parse_expression(expression):
    # Check that the expression only contains the variable "t"
    if "t" not in expression.replace(" ", ""):
        raise ValueError("Expression must contain the variable 't'")
    # Check that the expression only contains valid numpy functions and operators
    allowed_functions = set(np.__dict__.keys())
    allowed_operators = set("+-*/()")
    expression_functions = set(re.findall(r"\b\w+\b", expression)) - set(["t"])
    if not expression_functions.issubset(allowed_functions):
        raise ValueError("Expression contains invalid function(s)")
    for token in expression.split():
        if token not in allowed_operators and token not in expression_functions and not re.match(r"^\d+\.?\d*$", token):
            raise ValueError(f"Invalid character(s) in expression token: {token}")
    # Define the lambda function using the expression
    f = lambda t: eval(expression, {"__builtins__": None, "np": np, "t": t})
    return f

def parse_expression(expresion):

    expr = lambda t: eval(expresion)
    return expr
#                                                    #
# REPLACE THIS FUNCTION WITH THE ONE FROM @fenik_fam #
#                       vvv                          #

class PyvistaPyQtWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create the QtInteractor object
        self.interactor = QtInteractor(self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.interactor)
        self.setLayout(self.layout)

        # Initialize the Pyvista plotter
        self.plotter = self.interactor

        self.plotter.enable_depth_peeling(10)



    def add_mesh(self, uid, mesh, **kwargs):
        self.plotter.add_mesh(mesh, **kwargs)
        self.plotter.reset_camera()
        self.plotter.update()

    def test_scene(self):
        sphere = pv.Sphere()
        self.add_mesh("1", sphere, opacity=0.50, color="red")
        self.add_mesh("1", pv.Sphere(2, (1, 1, 1)), opacity=0.5, color="red")

        self.add_mesh("1", pv.Sphere(2, (3, 1, 1)), opacity=0.50, color="red")
        self.add_mesh("1", pv.Sphere(0.5, (3, -0.7, 1)), opacity=0.5, color="red")

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        # Load ui file
        #uic.loadUi("ui/userinterface.ui",self)

        _ui = userinterface_.Ui_MainWindow()
        _ui.setupUi(self)
        _ui.retranslateUi(self)

        self.creator = Creator()

        # Define our widgets
        self.toolbox = self.findChild(QGroupBox, 'tools_box')
        self.toolbox_layout = QVBoxLayout()
        self.commonWidget = QWidget()
        self.inside = QWidget()
        self.toolbox_layout.addWidget(self.commonWidget)
        self.toolbox_layout.addWidget(self.inside)
        self.toolbox.setLayout(self.toolbox_layout)

        self.widget = self.findChild(QWidget, 'widget')

        self.scrollArea = self.findChild(QScrollArea, 'scrollArea')
        self.scrollAreaContents = self.findChild(QWidget, 'scrollAreaWidgetContents')
        self.scrollAreaLayout = QVBoxLayout()
        self.scrollAreaLayout.setAlignment(PyQt5.QtCore.Qt.AlignTop)
        # for i in range(40):
        #    self.scrollAreaLayout.addWidget(Creator.ObjectWidget(self))
        self.scrollAreaContents.setLayout(self.scrollAreaLayout)

        self.console = self.findChild(QTextBrowser, 'textBrowser')

        self.save = self.findChild(QAction, 'save')
        self.save_as = self.findChild(QAction, 'save_as')
        self.save_image = self.findChild(QAction, 'save_image')
        self.open = self.findChild(QAction, 'open')
        self.new_scene = self.findChild(QAction, 'new_scene')
        self.show_tools = self.findChild(QAction, 'tools')
        self.show_console = self.findChild(QAction, 'console')
        self.setting = self.findChild(QAction, 'setting')

       # self.creator = Creator()



        # Define layout for future replacement
        self.main_layout = self.findChild(QHBoxLayout, 'horizontalLayout')

        # Initializing pyvista scene
        self.pyvista_widget = PyvistaPyQtWidget(self)


        self.main_layout.removeWidget(self.widget)
        self.widget.deleteLater()
        self.main_layout.removeWidget(self.toolbox)

        self.main_layout.addWidget(self.pyvista_widget, 2)
        #self.pyvista_widget.test_scene()

        self.main_layout.addWidget(self.toolbox)

        # Click the action
        self.show_tools.triggered.connect(self.hide_unhide_tools)
        self.show_console.triggered.connect(self.hide_unhide_console)

        #self.new_scene.triggered.connect(self.add_object)

        self.add_object()

        # Show the app
        self.show()

        # Keep track of hidden or not
        self.hidden_tools = False
        self.hidden_console = False


        self.object_storage = ObjectStorage(self.pyvista_widget)
        #self.parser = Parser()

        self.objects_list = {}



    def add_object(self): # DEBUG VERSION, SUBJECT TO CHANGE

        #contextMenu = QMenu(self)

        #menu_choice_conical = contextMenu.addAction("Add conical surface")
        #menu_choice_conical.triggered.connect(lambda: self.openCreateWidget(0))



        self.choiceWidget = QWidget()
        choiceWidgetLayout = QVBoxLayout()

        choice_conical = QPushButton("Add conical surface")
        choice_conical.clicked.connect(lambda: self.openCreateWidget(FigureTypes.CONE))
        choiceWidgetLayout.addWidget(choice_conical)

        choice_curve = QPushButton("Add curve")
        choice_curve.clicked.connect(lambda: self.openCreateWidget(FigureTypes.CURVE))
        choiceWidgetLayout.addWidget(choice_curve)

        choice_cylindrical = QPushButton("Add cylindrical surface")
        choice_cylindrical.clicked.connect(lambda: self.openCreateWidget(FigureTypes.CYLINDER))
        choiceWidgetLayout.addWidget(choice_cylindrical)

        choice_line = QPushButton("Add line")
        choice_line.clicked.connect(lambda: self.openCreateWidget(FigureTypes.LINE))
        choiceWidgetLayout.addWidget(choice_line)

        choice_plane = QPushButton("Add plane")
        choice_plane.clicked.connect(lambda: self.openCreateWidget(FigureTypes.PLANE))
        choiceWidgetLayout.addWidget(choice_plane)

        choice_point = QPushButton("Add point")
        choice_point.clicked.connect(lambda: self.openCreateWidget(FigureTypes.POINT))
        choiceWidgetLayout.addWidget(choice_point)
        choice_point.setEnabled(False)

        choice_rotation = QPushButton("Add rotation surface")
        choice_rotation.clicked.connect(lambda: self.openCreateWidget(FigureTypes.REVOLUTION))
        choiceWidgetLayout.addWidget(choice_rotation)

        choice_vector = QPushButton("Add vector")
        choice_vector.clicked.connect(lambda: self.openCreateWidget(7))
        choiceWidgetLayout.addWidget(choice_vector)
        choice_vector.setEnabled(False)

        self.choiceWidget.setLayout(choiceWidgetLayout)


        self.toolbox_layout.removeWidget(self.commonWidget)
        self.toolbox_layout.removeWidget(self.inside)

        self.inside.deleteLater()
        self.commonWidget.deleteLater()

        self.inside = self.choiceWidget
        self.toolbox_layout.addWidget(self.inside)
        self.toolbox_layout.update()

    def openCreateWidget(self, _type: FigureTypes):

        self.commonWidget = self.creator.CommonSettingsWidget()
        self.commonWidget.Form.inputName.setText("Object")
        self.commonWidget.Form.inputColor.setText("white")
        self.commonWidget.Form.inputTBounds.setText("-10, 10")
        self.commonWidget.Form.inputVBounds.setText("0, 1")


        applyButton = None
        match _type:
            case FigureTypes.CONE:
                self.createWidget = self.creator.CreateConicalWidget()
            case FigureTypes.CURVE:
                self.createWidget = self.creator.CreateCurveWidget()
            case FigureTypes.CYLINDER:
                self.createWidget = self.creator.CreateCylindricalWidget()
            case FigureTypes.LINE:
                self.createWidget = self.creator.CreateLineWidget()
            case FigureTypes.PLANE:
                self.createWidget = self.creator.CreatePlaneWidget()
            case FigureTypes.POINT:
                self.createWidget = self.creator.CreatePointWidget()
            case FigureTypes.REVOLUTION:
                self.createWidget = self.creator.CreateRotationFigureWidget()
           # case FigureTypes.VE:
           #    self.createWidget = self.creator.CreateVectorWidget()
            case _:
                self.createWidget = QWidget()

        self.toolbox_layout.removeWidget(self.inside)
        self.inside.deleteLater()

        self.inside = self.createWidget
        self.toolbox_layout.addWidget(self.commonWidget)
        self.toolbox_layout.addWidget(self.inside)
        self.toolbox_layout.update()

        print(f"type: {_type}")
        self.createWidget.Form.applyButton.clicked.connect(lambda: createObject(_type, False, 0))
        self.createWidget.Form.cancelButton.clicked.connect(self.add_object)

        def input_point():

            point_input_x = self.findChild(QLineEdit, "point_input_x").text()
            point_input_y = self.findChild(QLineEdit, "point_input_y").text()
            point_input_z = self.findChild(QLineEdit, "point_input_z").text()
            try:
                point_input_x = float(point_input_x)
                point_input_y = float(point_input_y)
                point_input_z = float(point_input_z)
            except:
                self.console.append("Incorrect value in point input")
                return False

            return point_input_x, point_input_y, point_input_z

        def input_vector():
            vector_input_x = self.findChild(QLineEdit, "vector_input_x").text()
            vector_input_y = self.findChild(QLineEdit, "vector_input_y").text()
            vector_input_z = self.findChild(QLineEdit, "vector_input_z").text()
            try:
                vector_input_x = float(vector_input_x)
                vector_input_y = float(vector_input_y)
                vector_input_z = float(vector_input_z)
            except:
                self.console.append("Incorrect value in vector input")
                return False
    
            return vector_input_x, vector_input_y, vector_input_z
        
        def input_curve():

            curve_input_x = self.findChild(QLineEdit, "curve_input_x").text()
            curve_input_y = self.findChild(QLineEdit, "curve_input_y").text()
            curve_input_z = self.findChild(QLineEdit, "curve_input_z").text()

            _curve_input_x_text = curve_input_x
            _curve_input_y_text = curve_input_y
            _curve_input_z_text = curve_input_z

            try:
                curve_input_x = parse_expression(curve_input_x)
                curve_input_y = parse_expression(curve_input_y)
                curve_input_z = parse_expression(curve_input_z)
            except:
                self.console.append("Incorrect value in curve input")
                return False

            return curve_input_x, curve_input_y, curve_input_z

        def input_line():

            point_input_x_1 = self.findChild(QLineEdit, "input_x_1").text()
            point_input_y_1 = self.findChild(QLineEdit, "input_y_1").text()
            point_input_z_1 = self.findChild(QLineEdit, "input_z_1").text()
            try:
                point_input_x_1 = float(point_input_x_1)
                point_input_y_1 = float(point_input_y_1)
                point_input_z_1 = float(point_input_z_1)
            except:
                self.console.append("Incorrect value in line`s point 1 input")
                return False

            point_input_x_2 = self.findChild(QLineEdit, "input_x_2").text()
            point_input_y_2 = self.findChild(QLineEdit, "input_y_2").text()
            point_input_z_2 = self.findChild(QLineEdit, "input_z_2").text()
            try:
                point_input_x_2 = float(point_input_x_2)
                point_input_y_2 = float(point_input_y_2)
                point_input_z_2 = float(point_input_z_2)
            except:
                self.console.append("Incorrect value in line`s point 2 input")
                return False

            return point_input_x_1, point_input_y_1, point_input_z_1, point_input_x_2, point_input_y_2, point_input_z_2

        def objectslist_append(uid):

            storage = self.object_storage.storage
            print(storage[uid])
            object_name = storage[uid]["name"]
            object_type = storage[uid]["FigureTypes"]

            objectWidget = self.creator.ObjectWidget()
            objectWidget.Form.label_name.setText(object_name)
            objectWidget.Form.label_type.setText(object_type)
            objectWidget.Form.label_color.setText(str(uid))

            objectWidget.Form.button_edit.clicked.connect(lambda: edit_object(uid))

            self.objects_list[uid] = objectWidget
            self.scrollAreaLayout.addWidget(self.objects_list[uid])


        def edit_object(uid):

            storage = self.object_storage.storage
            _type = storage[uid]["FigureTypes"]
            self.openCreateWidget(_type)
            button_delete = QPushButton("Delete")
            self.createWidget.Form.verticalLayout.addWidget(button_delete)

            self.commonWidget.Form.inputName.setText(storage[uid]["name"])
            self.commonWidget.Form.inputColor.setText("white")
            self.commonWidget.Form.inputTBounds.setText(str(storage[uid]["t_bounds"][0]) + ", " + str(storage[uid]["t_bounds"][1]))
            self.commonWidget.Form.inputVBounds.setText(str(storage[uid]["v_bounds"][0]) + ", " + str(storage[uid]["v_bounds"][1]))

            match  _type:
                case FigureTypes.CONE:
                    self.createWidget.Form.point_input_x.setText(str(storage[uid]["point"][0]))
                    self.createWidget.Form.point_input_y.setText(str(storage[uid]["point"][1]))
                    self.createWidget.Form.point_input_z.setText(str(storage[uid]["point"][2]))

                    self.createWidget.Form.curve_input_x.setText(str(storage[uid]["curve"][0]))
                    self.createWidget.Form.curve_input_y.setText(str(storage[uid]["curve"][1]))
                    self.createWidget.Form.curve_input_z.setText(str(storage[uid]["curve"][2]))


                case FigureTypes.CURVE:
                    self.createWidget = self.creator.CreateCurveWidget()
                case FigureTypes.CYLINDER:
                    self.createWidget = self.creator.CreateCylindricalWidget()
                case FigureTypes.LINE:
                    self.createWidget = self.creator.CreateLineWidget()
                case FigureTypes.PLANE:
                    self.createWidget = self.creator.CreatePlaneWidget()
                case FigureTypes.POINT:
                    self.createWidget = self.creator.CreatePointWidget()
                case FigureTypes.REVOLUTION:
                    self.createWidget = self.creator.CreateRotationFigureWidget()

            self.createWidget.Form.applyButton.clicked.connect(lambda: createObject(_type, True, uid))
            self.createWidget.Form.verticalLayout.button_delete.clicked.connect(lambda: deleteObject(uid)) # TODO: FIX THIS

        def createObject(_type, update_mode, uid):

            name = self.commonWidget.Form.inputName.text()
            color = self.commonWidget.Form.inputColor.text()
            t_bounds = [float(x) for x in self.commonWidget.Form.inputTBounds.text().split(",")]
            v_bounds = [float(x) for x in self.commonWidget.Form.inputTBounds.text().split(",")]

            input = {}

            match _type:
                case FigureTypes.CONE:  # Conical surface

                    if not input_point():
                        return
                    point_input_x, point_input_y, point_input_z = input_point()

                    if not input_curve():
                        return
                    curve_input_x, curve_input_y, curve_input_z = input_curve()


                    print("test")

                    self.console.append(
                        f"For this conical surface point x = {point_input_x}, y = {point_input_y}, z = {point_input_z}")
                    print(
                        f"For this conical surface curve x = {str(curve_input_x)}, y = {str(curve_input_y)}, z = {str(curve_input_z)}")


                    input = {

                        "curve": (curve_input_x, curve_input_y, curve_input_z),
                        "point": (point_input_x, point_input_y, point_input_z),
                        "t_bounds": t_bounds,
                        "v_bounds": v_bounds,
                        "name": name,
                        "FigureTypes": FigureTypes.CONE,
                    }

                case FigureTypes.CURVE:  # Curve

                    if not input_curve():
                        return
                    curve_input_x, curve_input_y, curve_input_z = input_curve()

                    self.console.append(
                        f"For this curve x = {curve_input_x}, y = {curve_input_y}, z = {curve_input_z}")

                    input = {

                        "curve": (curve_input_x, curve_input_y, curve_input_z),
                        "t_bounds": t_bounds,
                        "v_bounds": v_bounds,
                        "name": name,
                        "FigureTypes": FigureTypes.CURVE,
                    }

                case FigureTypes.CYLINDER:  # Cylindrical surface

                    if not input_vector():
                        return
                    vector_x, vector_y, vector_z = input_vector()

                    if not input_curve():
                        return
                    curve_input_x, curve_input_y, curve_input_z = input_curve()

                    self.console.append(
                        f"For this Cylindrical surface vector x = {vector_x}, y = {vector_y}, z = {vector_z}")

                    self.console.append(
                        f"For this Cylindrical surface curve x = {str(curve_input_x)}, y = {str(curve_input_y)}, z = {str(curve_input_z)}")

                    input = {

                        "curve": (curve_input_x, curve_input_y, curve_input_z),
                        "direction": (vector_x, vector_y, vector_z),
                        "t_bounds": t_bounds,
                        "v_bounds": v_bounds,
                        "name": name,
                        "FigureTypes": FigureTypes.CYLINDER,
                    }

                case FigureTypes.LINE:  # Create line

                    if not input_line():
                        return
                    line_x1, line_y1, line_z1, line_x2, line_y2, line_z2 = input_line()

                    self.console.append(
                        f"For this line x1 = {line_x1}, y1 = {line_y1}, z1 = {line_z1}"
                        f"              x2 = {line_x2}, y2 = {line_y2}, z2 = {line_z2}")

                    input = {

                        "point1": (line_x1, line_y1, line_z1),
                        "point2": (line_x2, line_y2, line_z2),
                        "t_bounds": t_bounds,
                        "v_bounds": v_bounds,
                        "name": name,
                        "FigureTypes": FigureTypes.LINE,
                    }

                case FigureTypes.PLANE: # Create plane

                    if not input_point():
                        return
                    point_input_x, point_input_y, point_input_z = input_point()

                    if not input_vector():
                        return
                    vector_input_x, vector_input_y, vector_input_z = input_vector()

                    self.console.append(
                        f"For this Plane point x = {point_input_x}, y = {point_input_y}, z = {point_input_z}")
                    self.console.append(
                        f"For this Plane normal vector x = {vector_input_x}, y = {vector_input_y}, z = {vector_input_z}")

                    input = {

                        "normal": (vector_input_x, vector_input_y, vector_input_z),
                        "point": (point_input_x, point_input_y, point_input_z),
                        "size": 1,
                        "t_bounds": t_bounds,
                        "v_bounds": v_bounds,
                        "name": name,
                        "FigureTypes": FigureTypes.PLANE,
                    }


                case FigureTypes.POINT:  # Create point
                    if not input_point():
                        return
                    point_input_x, point_input_y, point_input_z = input_point()

                    self.console.append(
                        f"For this point x = {point_input_x}, y = {point_input_y}, z = {point_input_z}")

                case FigureTypes.REVOLUTION:  # Create Rotation Surface

                    if not input_line():
                        return
                    line_x1, line_y1, line_z1, line_x2, line_y2, line_z2 = input_line()

                    if not input_curve():
                        return
                    curve_input_x, curve_input_y, curve_input_z = input_curve()

                    self.console.append(
                        f"For this Rotation surface line x1 = {line_x1}, y1 = {line_y1}, z1 = {line_z1}"
                        f"              x2 = {line_x2}, y2 = {line_y2}, z2 = {line_z2}")

                    self.console.append(
                        f"For this Cylindrical surface curve x = {str(curve_input_x)}, y = {str(curve_input_y)}, z = {str(curve_input_z)}")

                    input = {

                        "curve": (curve_input_x, curve_input_y, curve_input_z),
                        "direction": np.array((line_x1, line_y1, line_z1)),
                        "point": np.array((line_x2, line_y2, line_z2)),
                        "t_bounds": t_bounds,
                        "v_bounds": v_bounds,
                        "name": name,
                        "FigureTypes": FigureTypes.REVOLUTION,
                    }

                case 7: # Create vector

                    if not input_vector():
                        return
                    vector_input_x, vector_input_y, vector_input_z = input_vector()
                    self.console.append(
                        f"For this  vector x = {vector_input_x}, y = {vector_input_y}, z = {vector_input_z}")
                case _:
                    ...
            if update_mode == 0:
                self.console.append(f"Created {input['FigureTypes']} object with name {input['name']}")
                uid = self.object_storage.create(input)

                objectslist_append(uid)
            else:
                self.console.append(f"Update {input['FigureTypes']} object with name {input['name']}")
                self.object_storage.update(uid, input)

        def deleteObject(uid):
            self.object_storage.delete(uid)
            del self.objects_list[uid]

    def updateWidget(self):

        self.add_object()


    def hide_unhide_tools(self):
        if self.hidden_tools:
            self.toolbox.show()
            self.hidden_tools = False
        else:
            self.toolbox.hide()
            self.hidden_tools = True

    def hide_unhide_console(self):
        if self.hidden_console:
            self.console.show()
            self.hidden_console = False
        else:
            self.console.hide()
            self.hidden_console = True


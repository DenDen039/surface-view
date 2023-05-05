import PyQt5
import PyQt5.QtCore
from PyQt5.QtWidgets import *

from package.ui.Widgets.CustomWidgets import Creator
import package.ui.Widgets.generated.userinterface_ as userinterface_
from package.figures.figure import *

from package.qt_widgets.plotter_widget import PlotterWidget

from package.object_storage.object_storage import ObjectStorage
from package.parser import Parser

from numpy import *



# TODO: finish parses class
#       add update_widget
#       refactor gui
#       better f(t) parser
#

import numpy as np
import re


def parse_expression(expresion):

    expr = lambda t: eval(expresion)
    return expr

class ColoredWidget(QWidget):
    def __init__(self, color):
        super(ColoredWidget,self).__init__()
        self.setAutoFillBackground(True)

        self.palette = self.palette()
        self.palette.setColor(PyQt5.QtGui.QPalette.Window, PyQt5.QtGui.QColor(color))
        self.setPalette(self.palette)

    def change_color(self, color):
        self.palette.setColor(PyQt5.QtGui.QPalette.Window, PyQt5.QtGui.QColor(color))
        self.setPalette(self.palette)

class StorageObjectWidget(QScrollArea):
    def __init__(self, UI):
        super(StorageObjectWidget, self).__init__()

        self.creator = Creator()
        self.UI = UI


        self.setVerticalScrollBarPolicy(PyQt5.QtCore.Qt.ScrollBarAlwaysOn)
        self.setSizeAdjustPolicy(PyQt5.QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.setWidgetResizable(True)
        self.setAlignment(PyQt5.QtCore.Qt.AlignLeading | PyQt5.QtCore.Qt.AlignLeft | PyQt5.QtCore.Qt.AlignTop)

        self.scroll_area_content = QWidget(self)

        self.setWidget(self.scroll_area_content)

        self.scroll_area_layout = QVBoxLayout()
        self.scroll_area_layout.setAlignment(PyQt5.QtCore.Qt.AlignTop)

        self.scroll_area_content.setLayout(self.scroll_area_layout)

       # self.show()

        self.widgets = {}
        self.color_widget = {}

        print("Storage object Widget initialized")

    def add(self, uid, name, type, color):

        self.color_widget[uid] = ColoredWidget(color)
        objectWidget = self.creator.ObjectWidget()
        objectWidget.Form.horizontalLayout.replaceWidget(objectWidget.Form.color_view, self.color_widget[uid])
        objectWidget.Form.color_view.deleteLater()
       # objectWidget.Form.horizontalLayout.addWidget(_color,2)
        objectWidget.Form.label_name.setText(name)
        objectWidget.Form.label_type.setText(type)
       # objectWidget.Form.label_color.setText(str(uid))
        objectWidget.Form.button_edit.clicked.connect(lambda: self.UI.edit_object(uid))

        self.widgets[uid] = objectWidget
        self.scroll_area_layout.addWidget(self.widgets[uid])
        print("added new widget")

    def delete(self, uid):
        self.widgets[uid].deleteLater()

    def update(self, uid, name, type, color):

        self.widgets[uid].Form.label_name.setText(name)
        self.widgets[uid].Form.label_type.setText(type)
        #self.widgets[uid].Form.label_color.setText(str(uid))
        self.color_widget[uid].change_color(color)
        print("updating widget")

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
        #self.scrollAreaLayout = QVBoxLayout()
        #self.scrollAreaLayout.setAlignment(PyQt5.QtCore.Qt.AlignTop)
        # for i in range(40):
        #    self.scrollAreaLayout.addWidget(Creator.ObjectWidget(self))
#       self.scrollAreaContents.setLayout(self.scrollAreaLayout)

        self.console = self.findChild(QTextBrowser, 'textBrowser')

        self.save = self.findChild(QAction, 'save')
        self.save_as = self.findChild(QAction, 'save_as')
        self.save_image = self.findChild(QAction, 'save_image')
        self.open = self.findChild(QAction, 'open')
        self.new_scene = self.findChild(QAction, 'new_scene')
        self.show_tools = self.findChild(QAction, 'tools')
        self.show_console = self.findChild(QAction, 'console')
        self.setting = self.findChild(QAction, 'setting')

        self.horizontal_layout = self.findChild(QHBoxLayout, "horizontalLayout_2")

       # self.creator = Creator()



        # Define layout for future replacement
        self.main_layout = self.findChild(QHBoxLayout, 'horizontalLayout')

        # Initializing pyvista scene
        self.pyvista_widget = PlotterWidget(self)


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
        self.hide_unhide_console()
        self.show_console.setChecked(0)

        self.SWO = StorageObjectWidget(self)
        self.object_storage = ObjectStorage(self.pyvista_widget, self.SWO)

        self.horizontal_layout.replaceWidget(self.scrollArea, self.SWO)
        # self.horizontal_layout.addWidget(self.SWO)
        self.scrollArea.deleteLater()
        self.scrollAreaContents.deleteLater()
        self.parser = Parser()

        self.objects_list = {}



    def clear_right(self):
        for i in reversed(range(self.toolbox_layout.count())):
             self.toolbox_layout.itemAt(i).widget().setParent(None)

    def add_object(self):

        #contextMenu = QMenu(self)

        #menu_choice_conical = contextMenu.addAction("Add conical surface")
        #menu_choice_conical.triggered.connect(lambda: self.openCreateWidget(0))

        self.clear_right()

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

        choice_rotation = QPushButton("Add rotation surface")
        choice_rotation.clicked.connect(lambda: self.openCreateWidget(FigureTypes.REVOLUTION))
        choiceWidgetLayout.addWidget(choice_rotation)

        self.choiceWidget.setLayout(choiceWidgetLayout)

        self.toolbox_layout.removeWidget(self.commonWidget)
        self.toolbox_layout.removeWidget(self.inside)

        self.inside.deleteLater()
        self.commonWidget.deleteLater()

        self.inside = self.choiceWidget
        self.toolbox_layout.addWidget(self.inside)
        self.toolbox_layout.update()

    def openCreateWidget(self, _type: FigureTypes):

        self.clear_right()

        self.commonWidget = self.creator.CommonSettingsWidget()
        self.commonWidget.Form.inputName.setText("Object")
        self.commonWidget.Form.button_color.setText("")
        self.commonWidget.Form.button_color.setStyleSheet("background-color : white")
        self.commonWidget.Form.inputOpacity.setText("0.5")
        self.commonWidget.Form.inputTBounds.setText("-10, 10")
        self.commonWidget.Form.inputTBounds.setEnabled(False)
        self.commonWidget.Form.inputVBounds.setText("0, 1")
        self.commonWidget.Form.inputVBounds.setEnabled(False)
        self.commonWidget.Form.button_color.clicked.connect(self.change_color)


        applyButton = None
        match _type:
            case FigureTypes.CONE:
                self.createWidget = self.creator.CreateConicalWidget()
                self.commonWidget.Form.inputTBounds.setEnabled(True)
                self.commonWidget.Form.inputVBounds.setEnabled(True)
            case FigureTypes.CURVE:
                self.createWidget = self.creator.CreateCurveWidget()
                self.commonWidget.Form.inputTBounds.setEnabled(True)
            case FigureTypes.CYLINDER:
                self.createWidget = self.creator.CreateCylindricalWidget()
                self.commonWidget.Form.inputTBounds.setEnabled(True)
                self.commonWidget.Form.inputVBounds.setEnabled(True)
            case FigureTypes.LINE:
                self.createWidget = self.creator.CreateLineWidget()
                self.commonWidget.Form.inputTBounds.setEnabled(True)
            case FigureTypes.PLANE:
                self.createWidget = self.creator.CreatePlaneWidget()
            case FigureTypes.POINT:
                self.createWidget = self.creator.CreatePointWidget()
            case FigureTypes.REVOLUTION:
                self.commonWidget.Form.inputTBounds.setEnabled(True)
                self.createWidget = self.creator.CreateRotationFigureWidget()
           # case FigureTypes.VE:
           #    self.createWidget = self.creator.CreateVectorWidget()
            case _:
                self.createWidget = QWidget()

        self.toolbox_layout.removeWidget(self.inside)
        self.inside.deleteLater()
        #self.toolbox_layout.removeWidget(self.commonWidget)

        self.inside = self.createWidget
        self.toolbox_layout.addWidget(self.commonWidget)
        self.toolbox_layout.addWidget(self.inside)
        self.toolbox_layout.update()

        print(f"type: {_type}")
        self.createWidget.Form.applyButton.disconnect()
        self.createWidget.Form.applyButton.clicked.connect(lambda: self.createObject(_type, False, 0))
        self.createWidget.Form.cancelButton.clicked.connect(self.add_object)

    def input_point(self):

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

    def input_vector(self):
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

    def input_curve(self):

        #curve_input_x = self.inside.verticalLayout.curve_input_x.text()
        curve_input_x = self.findChild(QLineEdit, "curve_input_x").text()
        curve_input_y = self.findChild(QLineEdit, "curve_input_y").text()
        curve_input_z = self.findChild(QLineEdit, "curve_input_z").text()

        _curve_input_x_text = curve_input_x
        _curve_input_y_text = curve_input_y
        _curve_input_z_text = curve_input_z

        if self.parser.check_expression_string(curve_input_x) and self.parser.check_expression_string(curve_input_y) and self.parser.check_expression_string(curve_input_z):
            return curve_input_x, curve_input_y, curve_input_z

        self.console.append("Incorrect value in curve input")
        return False

    def input_line(self):

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

    def edit_object(self, uid):
        print(uid)
        storage = self.object_storage.storage
        print(storage)
        _type = storage[uid]["FigureTypes"]
        self.openCreateWidget(_type)

        button_delete = QPushButton("Delete")
        self.createWidget.Form.verticalLayout.addWidget(button_delete)

        self.commonWidget.Form.inputName.setText(storage[uid]["name"])
        self.commonWidget.Form.button_color.setStyleSheet(f"background-color : {storage[uid]['color']}")
        self.commonWidget.color = storage[uid]['color']
        self.commonWidget.Form.inputOpacity.setText(str(storage[uid]["opacity"]))
        self.commonWidget.Form.inputTBounds.setText(str(storage[uid]["t_bounds"][0]) + ", " + str(storage[uid]["t_bounds"][1]))
        self.commonWidget.Form.inputTBounds.setEnabled(False)
        self.commonWidget.Form.inputVBounds.setText(str(storage[uid]["v_bounds"][0]) + ", " + str(storage[uid]["v_bounds"][1]))
        self.commonWidget.Form.inputVBounds.setEnabled(False)

        match  _type:
            case FigureTypes.CONE:

                self.commonWidget.Form.inputTBounds.setEnabled(True)
                self.commonWidget.Form.inputVBounds.setEnabled(True)

                self.createWidget.Form.point_input_x.setText(str(storage[uid]["point"][0]))
                self.createWidget.Form.point_input_y.setText(str(storage[uid]["point"][1]))
                self.createWidget.Form.point_input_z.setText(str(storage[uid]["point"][2]))

                self.createWidget.Form.curve_input_x.setText(str(storage[uid]["curve_string"][0]))
                self.createWidget.Form.curve_input_y.setText(str(storage[uid]["curve_string"][1]))
                self.createWidget.Form.curve_input_z.setText(str(storage[uid]["curve_string"][2]))

            case FigureTypes.CURVE:

                self.commonWidget.Form.inputTBounds.setEnabled(True)

                self.createWidget.Form.curve_input_x.setText(str(storage[uid]["curve_string"][0]))
                self.createWidget.Form.curve_input_y.setText(str(storage[uid]["curve_string"][1]))
                self.createWidget.Form.curve_input_z.setText(str(storage[uid]["curve_string"][2]))

            case FigureTypes.CYLINDER:

                self.commonWidget.Form.inputTBounds.setEnabled(True)
                self.commonWidget.Form.inputVBounds.setEnabled(True)

                self.createWidget.Form.curve_input_x.setText(str(storage[uid]["curve_string"][0]))
                self.createWidget.Form.curve_input_y.setText(str(storage[uid]["curve_string"][1]))
                self.createWidget.Form.curve_input_z.setText(str(storage[uid]["curve_string"][2]))

                self.createWidget.Form.vector_input_x.setText(str(storage[uid]["direction"][0]))
                self.createWidget.Form.vector_input_y.setText(str(storage[uid]["direction"][1]))
                self.createWidget.Form.vector_input_z.setText(str(storage[uid]["direction"][2]))

            case FigureTypes.LINE:

                self.commonWidget.Form.inputTBounds.setEnabled(True)

                self.createWidget.Form.input_x_1.setText(str(storage[uid]["point1"][0]))
                self.createWidget.Form.input_y_1.setText(str(storage[uid]["point1"][1]))
                self.createWidget.Form.input_z_1.setText(str(storage[uid]["point1"][2]))

                self.createWidget.Form.input_x_2.setText(str(storage[uid]["point2"][0]))
                self.createWidget.Form.input_y_2.setText(str(storage[uid]["point2"][1]))
                self.createWidget.Form.input_z_2.setText(str(storage[uid]["point2"][2]))

            case FigureTypes.PLANE:
                self.createWidget.Form.point_input_x.setText(str(storage[uid]["point"][0]))
                self.createWidget.Form.point_input_y.setText(str(storage[uid]["point"][1]))
                self.createWidget.Form.point_input_z.setText(str(storage[uid]["point"][2]))

                self.createWidget.Form.vector_input_x.setText(str(storage[uid]["normal"][0]))
                self.createWidget.Form.vector_input_y.setText(str(storage[uid]["normal"][1]))
                self.createWidget.Form.vector_input_z.setText(str(storage[uid]["normal"][2]))

            case FigureTypes.POINT:
                self.createWidget.Form.point_input_x.setText(str(storage[uid]["point"][0]))
                self.createWidget.Form.point_input_y.setText(str(storage[uid]["point"][1]))
                self.createWidget.Form.point_input_z.setText(str(storage[uid]["point"][2]))

            case FigureTypes.REVOLUTION:

                self.commonWidget.Form.inputTBounds.setEnabled(True)

                self.createWidget.Form.curve_input_x.setText(str(storage[uid]["curve_string"][0]))
                self.createWidget.Form.curve_input_y.setText(str(storage[uid]["curve_string"][1]))
                self.createWidget.Form.curve_input_z.setText(str(storage[uid]["curve_string"][2]))

                self.createWidget.Form.input_x_1.setText(str(storage[uid]["direction"][0]))
                self.createWidget.Form.input_y_1.setText(str(storage[uid]["direction"][1]))
                self.createWidget.Form.input_z_1.setText(str(storage[uid]["direction"][2]))

                self.createWidget.Form.input_x_2.setText(str(storage[uid]["point"][0]))
                self.createWidget.Form.input_y_2.setText(str(storage[uid]["point"][1]))
                self.createWidget.Form.input_z_2.setText(str(storage[uid]["point"][2]))

        self.createWidget.Form.applyButton.disconnect()
        self.createWidget.Form.applyButton.clicked.connect(lambda: self.createObject(_type, True, uid))
        button_delete.clicked.connect(lambda: self.deleteObject(uid))

    def createObject(self, _type, update_mode, uid):

        name = self.commonWidget.Form.inputName.text()
        color = self.commonWidget.color
        opacity = self.commonWidget.Form.inputOpacity.text()

        if not self.parser.parse_two_floats(self.commonWidget.Form.inputTBounds.text()):
            self.console.append("Incorrect input in t_bounds")
            return
        t_bounds = self.parser.parse_two_floats(self.commonWidget.Form.inputTBounds.text())

        if not self.parser.parse_two_floats(self.commonWidget.Form.inputVBounds.text()):
            self.console.append("Incorrect input in v_bounds")
            return
        v_bounds = self.parser.parse_two_floats(self.commonWidget.Form.inputVBounds.text())


        input = {}

        match _type:
            case FigureTypes.CONE:  # Conical surface

                if not self.input_point():
                    return
                point_input_x, point_input_y, point_input_z = self.input_point()

                if not self.input_curve():
                    return
                curve_input_x, curve_input_y, curve_input_z = self.input_curve()


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

                if not self.input_curve():
                    return
                curve_input_x, curve_input_y, curve_input_z = self.input_curve()

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

                if not self.input_vector():
                    return
                vector_x, vector_y, vector_z = self.input_vector()

                if not self.input_curve():
                    return
                curve_input_x, curve_input_y, curve_input_z = self.input_curve()

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

                if not self.input_line():
                    return
                line_x1, line_y1, line_z1, line_x2, line_y2, line_z2 = self.input_line()

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

                if not self.input_point():
                    return
                point_input_x, point_input_y, point_input_z = self.input_point()

                if not self.input_vector():
                    return
                vector_input_x, vector_input_y, vector_input_z = self.input_vector()

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
                if not self.input_point():
                    return
                point_input_x, point_input_y, point_input_z = self.input_point()

                self.console.append(
                    f"For this point x = {point_input_x}, y = {point_input_y}, z = {point_input_z}")

            case FigureTypes.REVOLUTION:  # Create Rotation Surface

                if not self.input_line():
                    return
                line_x1, line_y1, line_z1, line_x2, line_y2, line_z2 = self.input_line()

                if not self.input_curve():
                    return
                curve_input_x, curve_input_y, curve_input_z = self.input_curve()

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

                if not self.input_vector():
                    return
                vector_input_x, vector_input_y, vector_input_z = self.input_vector()
                self.console.append(
                    f"For this  vector x = {vector_input_x}, y = {vector_input_y}, z = {vector_input_z}")
            case _:
                ...

        input["color"] = color
        input["opacity"] = float(opacity)

        if update_mode == 0:
            self.console.append(f"Created {input['FigureTypes']} object with name {input['name']}")
            uid = self.object_storage.create(input)
            print(self.object_storage.storage[uid])
            print("creating new object")
            print(uid)
            #self.objectslist_append(uid)
        else:
            self.console.append(f"Update {input['FigureTypes']} object with name {input['name']}")
            print("updating object")
            self.object_storage.update(uid, input)

    def deleteObject(self, uid):

        self.object_storage.delete(uid)
        self.console.append(f"Deleted object {uid}")


        self.add_object()

    def change_color(self):
        color = self.commonWidget.palette.getColor()

        if color.isValid():
            self.commonWidget.color = color.name()
            self.commonWidget.Form.button_color.setStyleSheet(f"background-color : {color.name()}")

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


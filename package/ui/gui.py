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
#       rename bounce -> bounds
#       add update_widget
#       add prototype of storage_object_widget
#           1. List of objects in left
#           2. Add update, delete methods
#           3. Integrate with storage_object
#       refactor gui
#       add @fenik_fam `s PW
#       better function parser
#       parser for CommonObjectWidget





def parse_expression(expr_str):

    if not ('t' in expr_str):
        expr_str = expr_str + "+t*0"

    func = lambda t: eval(expr_str)

    # Return the lambda function
    return func

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
        self.console = self.findChild(QTextBrowser, 'textBrowser')

        self.save = self.findChild(QAction, 'save')
        self.save_as = self.findChild(QAction, 'save_as')
        self.save_image = self.findChild(QAction, 'save_image')
        self.open = self.findChild(QAction, 'open')
        self.new_scene = self.findChild(QAction, 'new_scene')
        self.show_tools = self.findChild(QAction, 'tools')
        self.show_console = self.findChild(QAction, 'console')
        self.setting = self.findChild(QAction, 'setting')

        self.creator = Creator()



        # Define layout for future replacement
        self.main_layout = self.findChild(QHBoxLayout, 'horizontalLayout')

        # Initializing pyvista scene
        self.pyvista_widget = PyvistaPyQtWidget(self)


        self.main_layout.removeWidget(self.widget)
        self.main_layout.removeWidget(self.toolbox)

        self.main_layout.addWidget(self.pyvista_widget, 1)
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


    def add_object(self): # DEBUG VERSION, SUBJECT TO CHANGE

        #contextMenu = QMenu(self)

        #menu_choice_conical = contextMenu.addAction("Add conical surface")
        #menu_choice_conical.triggered.connect(lambda: self.openCreateWidget(0))



        self.choiceWidget = QWidget()
        choiceWidgetLayout = QVBoxLayout()

        choice_conical = QPushButton("Add conical surface")
        choice_conical.clicked.connect(lambda: self.openCreateWidget(0))
        choiceWidgetLayout.addWidget(choice_conical)

        choice_curve = QPushButton("Add curve")
        choice_curve.clicked.connect(lambda: self.openCreateWidget(1))
        choiceWidgetLayout.addWidget(choice_curve)

        choice_cylindrical = QPushButton("Add cylindrical surface")
        choice_cylindrical.clicked.connect(lambda: self.openCreateWidget(2))
        choiceWidgetLayout.addWidget(choice_cylindrical)

        choice_line = QPushButton("Add line")
        choice_line.clicked.connect(lambda: self.openCreateWidget(3))
        choiceWidgetLayout.addWidget(choice_line)

        choice_plane = QPushButton("Add plane")
        choice_plane.clicked.connect(lambda: self.openCreateWidget(4))
        choiceWidgetLayout.addWidget(choice_plane)

        choice_point = QPushButton("Add point")
        choice_point.clicked.connect(lambda: self.openCreateWidget(5))
        choiceWidgetLayout.addWidget(choice_point)
        choice_point.setEnabled(False)

        choice_rotation = QPushButton("Add rotation surface")
        choice_rotation.clicked.connect(lambda: self.openCreateWidget(6))
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


    def openCreateWidget(self, _id: int):

        self.commonWidget = self.creator.CommonSettingsWidget()
        self.commonWidget.Form.inputName.setText("Object")
        self.commonWidget.Form.inputColor.setText("white")
        self.commonWidget.Form.inputTBounds.setText("-10, 10")
        self.commonWidget.Form.inputVBounds.setText("0, 1")


        applyButton = None
        match _id:
            case 0:
                self.createWidget = self.creator.CreateConicalWidget()
            case 1:
                self.createWidget = self.creator.CreateCurveWidget()
            case 2:
                self.createWidget = self.creator.CreateCylindricalWidget()
            case 3:
                self.createWidget = self.creator.CreateLineWidget()
            case 4:
                self.createWidget = self.creator.CreatePlaneWidget()
            case 5:
                self.createWidget = self.creator.CreatePointWidget()
            case 6:
                self.createWidget = self.creator.CreateRotationFigureWidget()
            case 7:
                self.createWidget = self.creator.CreateVectorWidget()
            case _:
                self.createWidget = QWidget()

        self.toolbox_layout.removeWidget(self.inside)
        self.inside.deleteLater()



        self.inside = self.createWidget
        self.toolbox_layout.addWidget(self.commonWidget)
        self.toolbox_layout.addWidget(self.inside)
        self.toolbox_layout.update()

        print(_id)
        self.createWidget.Form.applyButton.clicked.connect(lambda: createObject(_id))
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

        def createObject(id):

            name = self.commonWidget.Form.inputName.text()
            color = self.commonWidget.Form.inputColor.text()
            t_bounds = [float(x) for x in self.commonWidget.Form.inputTBounds.text().split(",")]
            v_bounds = [float(x) for x in self.commonWidget.Form.inputTBounds.text().split(",")]

            input = {}

            match id:
                case 0:  # Conical surface

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
                        "t_bounce": t_bounds,
                        "v_bounce": v_bounds,
                        "name": name,
                        "FigureTypes": FigureTypes.CONE,
                    }




                case 1:  # Curve surface

                    if not input_curve():
                        return
                    curve_input_x, curve_input_y, curve_input_z = input_curve()

                    self.console.append(
                        f"For this conical surface curve x = {curve_input_x}, y = {curve_input_y}, z = {curve_input_z}")

                    input = {

                        "curve": (curve_input_x, curve_input_y, curve_input_z),
                        "t_bounce": t_bounds,
                        "v_bounce": v_bounds,
                        "name": name,
                        "FigureTypes": FigureTypes.CURVE,
                    }

                case 2:  # Cylindrical surface

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
                        "t_bounce": t_bounds,
                        "v_bounce": v_bounds,
                        "name": name,
                        "FigureTypes": FigureTypes.CYLINDER,
                    }

                case 3:  # Create line

                    if not input_line():
                        return
                    line_x1, line_y1, line_z1, line_x2, line_y2, line_z2 = input_line()

                    self.console.append(
                        f"For this line x1 = {line_x1}, y1 = {line_y1}, z1 = {line_z1}"
                        f"              x2 = {line_x2}, y2 = {line_y2}, z2 = {line_z2}")

                    input = {

                        "point1": (line_x1, line_y1, line_z1),
                        "point2": (line_x2, line_y2, line_z2),
                        "t_bounce": t_bounds,
                        "v_bounce": v_bounds,
                        "name": name,
                        "FigureTypes": FigureTypes.LINE,
                    }

                case 4: # Create plane

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
                        "t_bounce": t_bounds,
                        "v_bounce": v_bounds,
                        "name": name,
                        "FigureTypes": FigureTypes.PLANE,
                    }


                case 5:  # Create point
                    if not input_point():
                        return
                    point_input_x, point_input_y, point_input_z = input_point()

                    self.console.append(
                        f"For this point x = {point_input_x}, y = {point_input_y}, z = {point_input_z}")

                case 6:  # Create Rotation Surface

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
                        "direction": (line_x1, line_y1, line_z1),
                        "point": (line_x2, line_y2, line_z2),
                        "t_bounce": t_bounds,
                        "v_bounce": v_bounds,
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

            self.object_storage.create(input)


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


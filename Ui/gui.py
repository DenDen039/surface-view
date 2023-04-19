from PyQt5.QtWidgets import *
import pyvista as pv
from pyvistaqt import QtInteractor
import sys
from Ui.CustomWidgets.CustomWidgets import *

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



    def add_mesh(self, mesh, **kwargs):
        self.plotter.add_mesh(mesh, **kwargs)
        self.plotter.reset_camera()
        self.plotter.update()

    def test_scene(self):
        sphere = pv.Sphere()
        self.add_mesh(sphere, opacity=0.50, color="red")
        self.add_mesh(pv.Sphere(2, (1, 1, 1)), opacity=0.5, color="red")

        self.add_mesh(pv.Sphere(2, (3, 1, 1)), opacity=0.50, color="red")
        self.add_mesh(pv.Sphere(0.5, (3, -0.7, 1)), opacity=0.5, color="red")


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        # Load ui file
        uic.loadUi("ui/userinterface.ui",self)

        # Define our widgets
        self.toolbox = self.findChild(QGroupBox, 'tools_box')
        self.toolbox_layout = QVBoxLayout()
        self.inside = QWidget()
        self.toolbox_layout.addWidget(self.inside)
        self.toolbox.setLayout(self.toolbox_layout)

        self.widget = self.findChild(QWidget, 'widget')
        self.scrollArea = self.findChild(QScrollArea, 'scrollArea')
        self.textBrowser = self.findChild(QTextBrowser, 'textBrowser')

        self.save = self.findChild(QAction, 'save')
        self.save_as = self.findChild(QAction, 'save_as')
        self.save_image = self.findChild(QAction, 'save_image')
        self.open = self.findChild(QAction, 'open')
        self.new_scene = self.findChild(QAction, 'new_scene')
        self.tools = self.findChild(QAction, 'tools')
        self.console = self.findChild(QAction, 'console')
        self.setting = self.findChild(QAction, 'setting')

        # Define layout for future replacement
        self.main_layout = self.findChild(QHBoxLayout, 'horizontalLayout')

        # Initializing pyvista scene
        self.pyvista_widget = PyvistaPyQtWidget(self)


        self.main_layout.removeWidget(self.widget)
        self.main_layout.removeWidget(self.toolbox)

        self.main_layout.addWidget(self.pyvista_widget, 1)
        self.pyvista_widget.test_scene()

        self.main_layout.addWidget(self.toolbox)

        # Click the action
        self.tools.triggered.connect(self.hide_unhide_tools)
        self.console.triggered.connect(self.hide_unhide_console)

        self.new_scene.triggered.connect(self.add_object)

        # Show the app
        self.show()

        # Keep track of hidden or not
        self.hidden_tools = False
        self.hidden_console = False


    def add_object(self): # DEBUG VERSION, SUBJECT TO CHANGE
        self.win2 = QWidget()
        win2layout = QVBoxLayout()

        choice_conical = QPushButton("Add conical surface")
        choice_conical.clicked.connect(lambda: self.openCreateWidget(0))
        win2layout.addWidget(choice_conical)

        choice_curve = QPushButton("Add curve")
        choice_curve.clicked.connect(lambda: self.openCreateWidget(1))
        win2layout.addWidget(choice_curve)

        choice_cylindrical = QPushButton("Add cylindrical surface")
        choice_cylindrical.clicked.connect(lambda: self.openCreateWidget(2))
        win2layout.addWidget(choice_cylindrical)

        choice_line = QPushButton("Add line")
        choice_line.clicked.connect(lambda: self.openCreateWidget(3))
        win2layout.addWidget(choice_line)

        choice_plane = QPushButton("Add plane")
        choice_plane.clicked.connect(lambda: self.openCreateWidget(4))
        win2layout.addWidget(choice_plane)

        choice_point = QPushButton("Add point")
        choice_point.clicked.connect(lambda: self.openCreateWidget(5))
        win2layout.addWidget(choice_point)

        choice_rotation = QPushButton("Add rotation surface")
        choice_rotation.clicked.connect(lambda: self.openCreateWidget(6))
        win2layout.addWidget(choice_rotation)

        choice_vector = QPushButton("Add vector")
        choice_vector.clicked.connect(lambda: self.openCreateWidget(7))
        win2layout.addWidget(choice_vector)

        self.win2.setLayout(win2layout)

        print("Showing win2")
        self.win2.show()

    def openCreateWidget(self, id: int):

        match id:
            case 0:
                self.createWidget = CreateConicalWidget()
            case 1:
                self.createWidget = CreateCurveWidget()
            case 2:
                self.createWidget = CreateCylindricalWidget()
            case 3:
                self.createWidget = CreateLineWidget()
            case 4:
                self.createWidget = CreatePlaneWidget()
            case 5:
                self.createWidget = CreatePointWidget()
            case 6:
                self.createWidget = CreateRotationFigureWidget()
            case 7:
                self.createWidget = CreateVectorWidget()
            case _:
                self.createWidget = QWidget()

        self.toolbox_layout.removeWidget(self.inside)
        self.inside.deleteLater()

        self.inside = self.createWidget
        self.toolbox_layout.addWidget(self.inside)
        self.toolbox_layout.update()

        self.applyButton = self.findChild(QPushButton, "applyButton")



    def hide_unhide_tools(self):
        if self.hidden_tools:
            self.toolbox.show()
            self.hidden_tools = False
        else:
            self.toolbox.hide()
            self.hidden_tools = True

    def hide_unhide_console(self):
        if self.hidden_console:
            self.textBrowser.show()
            self.hidden_console = False
        else:
            self.textBrowser.hide()
            self.hidden_console = True



app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()

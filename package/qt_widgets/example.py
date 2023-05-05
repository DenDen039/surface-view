import sys, numpy as np
#sys.path.append("C:\\surface-view\\package")
from package.figures.figure import Figure, FigureTypes
from package.figures.primitives.cone import Cone
from package.figures.primitives.cylinder import Cylinder
from package.figures.primitives.curve import Curve
from package.figures.primitives.line import Line
from package.figures.primitives.plane import Plane
from package.figures.primitives.revolution_surface import RevolutionSurface
from package.object_manager.manager import ObjectManager
from package.qt_widgets.plotter_widget import PlotterWidget 

import uuid
import copy

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout() 

        vbox_left = QVBoxLayout()
        vbox_right = QVBoxLayout()


        btn1 = QPushButton('add meshes')
        btn2 = QPushButton('remove one')
        btn3 = QPushButton('clear')
        btn4 = QPushButton('screenshot')

        btn9 = QPushButton('add label')

        orientation_button_layout = QHBoxLayout()
        btn5 = QPushButton('XY')
        btn6 = QPushButton('YZ')

        zoom_button_layout = QHBoxLayout()
        btn7 = QPushButton('zoom in')
        btn8 = QPushButton('zoom out')

        blur_button_layout = QHBoxLayout()
        btn10 = QPushButton('blur')
        btn11 = QPushButton('remove blur')

        hide_show_button_layout = QHBoxLayout()
        btn12 = QPushButton('hide mesh')
        btn13 = QPushButton('show mesh')

        intersections_button_layout = QHBoxLayout()
        btn14 = QPushButton('add intersections')
        btn15 = QPushButton('remove intersections')

        manager = ObjectManager()

        curve = (lambda t: np.sin(t), lambda t: np.cos(t) * 0, lambda t: t)
        t_bounce = (0, 2 * np.pi)
        v_bounce = (0, 2)
        point = (5, 5, 5)

        curve2 = (lambda t: t, lambda t: np.cos(t), lambda t: np.sin(t) * 0)
        t_bounce2 = (0, 2 * np.pi)
        v_bounce2 = (0, 2)
        direction2 = (1, 1, 1)

        normal = (0, 1, 0)
        point = (3, 5, 5)
        size = 1
        uid3 = manager.create_plane(normal, point, size)

        curve3 = (lambda t: np.sin(t) * 0, lambda t: np.cos(t), lambda t: t)
        direction3 = (0, 0, 1)
        t_bounce3 = (np.pi * 0.5,  1.5 * np.pi)

        uid1 = manager.create_cone(curve, point, t_bounce, v_bounce, resolution=50)
        uid2 = manager.create_cylinder(curve2, direction2, t_bounce2, v_bounce2, resolution=50)
        uid3 = manager.create_plane(normal, point, size, resolution=50)
        uid4 = manager.create_revolution_surface(curve3, direction3, [0, 0, 0], t_bounce3, resolution=50)

        uid5 = manager.create_curve(curve, t_bounce)

        myWidget = PlotterWidget()

        def add():
            meshes = [manager.get_figure_mesh(uid5)]

            points = dict()
            points["Y1"] = (1, 1, 1)
            points["X1"] = (3, 5, 5)

            labels = [meshes, points]

            myWidget.add_mesh(uid1, manager.get_figure_mesh(uid1), "Cone", labels, color='blue')
            myWidget.add_label(uid1)
            #myWidget.show_edges_mesh(uid1)
            #myWidget.highlight_mesh(uid1, color='red', line_width=4)

            #myWidget.add_mesh(uid2, manager.get_figure_mesh(uid2), "Cylinder", color='cyan')
            #myWidget.show_edges_mesh(uid2)
            #myWidget.highlight_mesh(uid2, color='blue', line_width=4)
            
            #myWidget.add_mesh(uid3, manager.get_figure_mesh(uid3), "Plane", color='purple')
            #myWidget.show_edges_mesh(uid3)
            #myWidget.highlight_mesh(uid3)

            #myWidget.add_mesh(uid4, manager.get_figure_mesh(uid4), "Revolution", color='green')
            #myWidget.show_edges_mesh(uid4)
            #myWidget.highlight_mesh(uid4, color='black', line_width=4)

        def add_label():
            myWidget.add_label(uid1)

        def hide_mesh():
            myWidget.hide_mesh(uid3)

        def show_mesh():
            myWidget.show_mesh(uid3)
            
        def remove():
            myWidget.remove_label(uid1)

        def clear():
            myWidget.clear_actors()

        def viewXY():
            myWidget.view_xy()

        def viewYZ():
            myWidget.view_yz()

        def screenshot():
            myWidget.take_screenshot()

        def show_intersections():
            intersec = [manager.get_figure_mesh(uid2), manager.get_figure_mesh(uid3)]
            myWidget.add_intersections(intersec)

        def remove_intersection():
            myWidget.remove_intersections()

        def blur():
            myWidget.blur()

        def remove_blur():
            myWidget.remove_blur()


        btn1.clicked.connect(add)
        btn2.clicked.connect(remove)
        btn3.clicked.connect(clear)
        btn4.clicked.connect(screenshot)

        btn5.clicked.connect(viewXY)
        btn6.clicked.connect(viewYZ)

        btn9.clicked.connect(add_label)

        btn10.clicked.connect(blur)
        btn11.clicked.connect(remove_blur)

        btn12.clicked.connect(hide_mesh)
        btn13.clicked.connect(show_mesh)

        btn14.clicked.connect(show_intersections)
        btn15.clicked.connect(remove_intersection)

        vbox_left.addWidget(btn1)
        vbox_left.addWidget(btn2)
        vbox_left.addWidget(btn3)
        vbox_left.addWidget(btn4)
        vbox_left.addWidget(btn9)

        orientation_button_layout.addWidget(btn5)
        orientation_button_layout.addWidget(btn6)
        zoom_button_layout.addWidget(btn7)
        zoom_button_layout.addWidget(btn8)
        blur_button_layout.addWidget(btn10)
        blur_button_layout.addWidget(btn11)
        hide_show_button_layout.addWidget(btn12)
        hide_show_button_layout.addWidget(btn13)
        intersections_button_layout.addWidget(btn14)
        intersections_button_layout.addWidget(btn15)


        vbox_left.addLayout(orientation_button_layout)
        vbox_left.addLayout(zoom_button_layout)
        vbox_left.addLayout(blur_button_layout)
        vbox_left.addLayout(hide_show_button_layout)
        vbox_left.addLayout(intersections_button_layout)

        vbox_right.addWidget(myWidget)

        hbox.addLayout(vbox_left)
        hbox.addLayout(vbox_right)

        self.setLayout(hbox)

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Example')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

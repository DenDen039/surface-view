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

        btn5 = QPushButton('XY')
        btn6 = QPushButton('YZ')
        btn7 = QPushButton('zoom in')
        btn8 = QPushButton('zoom out')

        manager = ObjectManager()

        curve = (lambda t: np.sin(t), lambda t: np.cos(t) * 0, lambda t: t)
        t_bounce = (0, 2 * np.pi)
        v_bounce = (0, 2)
        point = (5, 5, 5)

        curve2 = (lambda t: t, lambda t: np.cos(t), lambda t: np.sin(t) * 0)
        t_bounce2 = (0, 2 * np.pi)
        v_bounce2 = (0, 2)
        point2 = (5, 5, 5)

        curve3 = (lambda t: 2 * t, lambda t: np.cos(2 * t), lambda t: np.sin(t))
        t_bounce3 = (0, 2 * np.pi)
        v_bounce3 = (2, 1.5)
        point3 = (1, 40, 0)

        uid1 = manager.create_cone(curve, point, t_bounce, v_bounce)
        uid2 = manager.create_cone(curve2, point2, t_bounce2, v_bounce2)
        uid3 = manager.create_cone(curve3, point3, t_bounce3, v_bounce3)

        myWidget = PlotterWidget(manager.objects)

        def add():
            myWidget.add_mesh(uid3, color='grey', opacity=0.5)
            myWidget.add_mesh(uid2, color='red')
            myWidget.add_mesh(uid1, color='blue')

        def remove():
            myWidget.remove_mesh(uid1)
            myWidget.remove_mesh(uid2)

        def clear():
            myWidget.clear_actors()

        def viewXY():
            myWidget.view_xy()

        def viewYZ():
            myWidget.view_yz()

        def zoom_in():
            myWidget.zoom_in()

        def zoom_out():
            myWidget.zoom_out()

        def screenshot():
            myWidget.take_screenshot()

        def blur():
            myWidget.plotter.add_blurring()

        btn1.clicked.connect(add)
        btn2.clicked.connect(remove)
        btn3.clicked.connect(clear)
        btn4.clicked.connect(screenshot)
        btn5.clicked.connect(viewXY)
        btn6.clicked.connect(viewYZ)
        btn7.clicked.connect(zoom_in)
        btn8.clicked.connect(zoom_out)

        vbox_left.addWidget(btn1)
        vbox_left.addWidget(btn2)
        vbox_left.addWidget(btn3)
        vbox_left.addWidget(btn4)
        vbox_left.addWidget(btn5)
        vbox_left.addWidget(btn6)
        #vbox_left.addWidget(btn7)
        #vbox_left.addWidget(btn8)

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

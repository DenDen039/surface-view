"""
    This file converts custom widgets` .ui files to QWidget classes.
    Nothing should be changed here, unless new files are added

    Import this file as:

    from Widgets.CustomWidgets import *

"""

from PyQt5 import uic, QtWidgets
import ui.Widgets.CreateConicalWidget_ as CreateConicalWidget_
import ui.Widgets.CreateCurveWidget_ as CreateCurveWidget_
import ui.Widgets.CreateRotationFigureWidget_ as CreateRotationFigureWidget_
import ui.Widgets.CreateLineWidget_ as CreateLineWidget_
import ui.Widgets.CreatePlaneWidget_ as CreatePlaneWidget_
import ui.Widgets.CreatePointWidget_ as CreatePointWidget_
import ui.Widgets.CreateCylindricalWidget_ as CreateCylindricalWidget_
import ui.Widgets.CreateVectorWidget_ as CreateVectorWidget_
import ui.Widgets.ObjectWidget_ as ObjectWidget_

class CreateConicalWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CreateConicalWidget, self).__init__()
        Widget = CreateConicalWidget_.Ui_Form()
        Widget.setupUi(self)
        Widget.retranslateUi(self)


class CreateCurveWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CreateCurveWidget, self).__init__()
        Widget = CreateCurveWidget_.Ui_Form()
        Widget.setupUi(self)
        Widget.retranslateUi(self)


class CreateCylindricalWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CreateCylindricalWidget, self).__init__()
        Widget = CreateCylindricalWidget_.Ui_Form()
        Widget.setupUi(self)
        Widget.retranslateUi(self)


class CreateLineWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CreateLineWidget, self).__init__()
        Widget = CreateLineWidget_.Ui_Form()
        Widget.setupUi(self)
        Widget.retranslateUi(self)


class CreatePlaneWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CreatePlaneWidget, self).__init__()
        Widget = CreatePlaneWidget_.Ui_Form()
        Widget.setupUi(self)
        Widget.retranslateUi(self)


class CreatePointWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CreatePointWidget, self).__init__()
        Widget = CreatePointWidget_.Ui_Form()
        Widget.setupUi(self)
        Widget.retranslateUi(self)


class CreateRotationFigureWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CreateRotationFigureWidget, self).__init__()
        Widget = CreateRotationFigureWidget_.Ui_Form()
        Widget.setupUi(self)
        Widget.retranslateUi(self)


class CreateVectorWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CreateVectorWidget, self).__init__()
        Widget = CreateVectorWidget_.Ui_Form()
        Widget.setupUi(self)
        Widget.retranslateUi(self)


class ObjectWidget(QtWidgets.QWidget):
    def __init__(self):
        super(ObjectWidget, self).__init__()
        Widget = ObjectWidget_.Ui_Form()
        Widget.setupUi(self)
        Widget.retranslateUi(self)

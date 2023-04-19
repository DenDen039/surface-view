"""
    This file converts custom widgets` .ui files to QWidget classes.
    Nothing should be changed here, unless new files are added

    Import this file as:

    from CustomWidgets.CustomWidgets import *

"""

from PyQt5 import uic, QtWidgets


class CreateConicalWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CreateConicalWidget, self).__init__()
        uic.loadUi("CustomWidgets\CreateConicalWidget.ui", self)


class CreateCurveWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CreateCurveWidget, self).__init__()
        uic.loadUi("CustomWidgets\CreateCurveWidget.ui", self)


class CreateCylindricalWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CreateCylindricalWidget, self).__init__()
        uic.loadUi("CustomWidgets\CreateCylindricalWidget.ui", self)


class CreateLineWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CreateLineWidget, self).__init__()
        uic.loadUi("CustomWidgets\CreateLineWidget.ui", self)


class CreatePlaneWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CreatePlaneWidget, self).__init__()
        uic.loadUi("CustomWidgets\CreatePlaneWidget.ui", self)


class CreatePointWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CreatePointWidget, self).__init__()
        uic.loadUi("CustomWidgets\CreatePointWidget.ui", self)


class CreateRotationFigureWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CreateRotationFigureWidget, self).__init__()
        uic.loadUi("CustomWidgets\CreateRotationFigureWidget.ui", self)


class CreateVectorWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CreateVectorWidget, self).__init__()
        uic.loadUi("CustomWidgets\CreateVectorWidget.ui", self)


class ObjectWidget(QtWidgets.QWidget):
    def __init__(self):
        super(ObjectWidget, self).__init__()
        uic.loadUi("CustomWidgets\ObjectWidget.ui", self)

"""
    This file converts custom widgets` .ui files to QWidget classes.
    Nothing should be changed here, unless new files are added

    Import this file as:

    from Widgets.CustomWidgets import *

"""

from PyQt5 import QtWidgets
import package.ui.Widgets.generated.CreateConicalWidget_ as CreateConicalWidget_
import package.ui.Widgets.generated.CreateCurveWidget_ as CreateCurveWidget_
import package.ui.Widgets.generated.CreateRotationFigureWidget_ as CreateRotationFigureWidget_
import package.ui.Widgets.generated.CreateLineWidget_ as CreateLineWidget_
import package.ui.Widgets.generated.CreatePlaneWidget_ as CreatePlaneWidget_
import package.ui.Widgets.generated.CreatePointWidget_ as CreatePointWidget_
import package.ui.Widgets.generated.CreateCylindricalWidget_ as CreateCylindricalWidget_
import package.ui.Widgets.generated.CreateVectorWidget_ as CreateVectorWidget_
import package.ui.Widgets.generated.CommonSettingsWidget_ as CommonSettingsWidget_
import package.ui.Widgets.generated.ObjectWidget_ as ObjectWidget_
import package.ui.Widgets.generated.SettingsWidget_ as SettingsWidget_
import package.ui.Widgets.generated.HelpWidget_ as HelpWidget_

class Creator:

    def __init__(self):
        ...

    def CreateConicalWidget(self):

        Widget = QtWidgets.QWidget()
        Form = CreateConicalWidget_.Ui_Form()
        Form.setupUi(Widget)
        Widget.Form = Form

        return Widget

    def CreateCurveWidget(self):
        Widget = QtWidgets.QWidget()
        Form = CreateCurveWidget_.Ui_Form()
        Form.setupUi(Widget)
        Widget.Form = Form

        return Widget

    def CreateCylindricalWidget(self):
        Widget = QtWidgets.QWidget()
        Form = CreateCylindricalWidget_.Ui_Form()
        Form.setupUi(Widget)
        Widget.Form = Form

        return Widget

    def CreateLineWidget(self):
        Widget = QtWidgets.QWidget()
        Form = CreateLineWidget_.Ui_Form()
        Form.setupUi(Widget)
        Widget.Form = Form

        return Widget

    def CreatePlaneWidget(self):

        Widget = QtWidgets.QWidget()
        Form = CreatePlaneWidget_.Ui_Form()
        Form.setupUi(Widget)
        Widget.Form = Form

        return Widget

    def CreatePointWidget(self):

        Widget = QtWidgets.QWidget()
        Form = CreatePointWidget_.Ui_Form()
        Form.setupUi(Widget)
        Widget.Form = Form

        return Widget

    def CreateRotationFigureWidget(self):

        Widget = QtWidgets.QWidget()
        Form = CreateRotationFigureWidget_.Ui_Form()
        Form.setupUi(Widget)
        Widget.Form = Form

        return Widget

    def CreateVectorWidget(self):

        Widget = QtWidgets.QWidget()
        Form = CreateVectorWidget_.Ui_Form()
        Form.setupUi(Widget)
        Widget.Form = Form

    def CommonSettingsWidget(self):
        Widget = QtWidgets.QWidget()
        Form = CommonSettingsWidget_.Ui_Form()
        Form.setupUi(Widget)
        Widget.Form = Form

        Widget.color = "#FFFFFF"
        Widget.palette = QtWidgets.QColorDialog()

        return Widget

    def ObjectWidget(self):
        Widget = QtWidgets.QWidget()
        Form = ObjectWidget_.Ui_Form()
        Form.setupUi(Widget)
        Widget.Form = Form

        return Widget

    def SettingsWidget(self):

        Widget = QtWidgets.QWidget()
        Form = SettingsWidget_.Ui_Form()
        Form.setupUi(Widget)
        Widget.Form = Form

        return Widget

    def HelpWidget(self):

        Widget = QtWidgets.QWidget()
        Form = HelpWidget_.Ui_Form()
        Form.setupUi(Widget)
        Widget.Form = Form

        return Widget

# Actual version @09.06.2023 12:55
import uuid

import PyQt5
import PyQt5.QtCore
from PyQt5.QtWidgets import *

from package.ui.Widgets.CustomWidgets import Creator
import package.ui.Widgets.generated.userinterface_ as userinterface_
from package.figures.figure import *

from package.qt_widgets.plotter_widget import PlotterWidget

from package.object_storage.object_storage import ObjectStorage
from package.parser import Parser

from package.ui.input_warnings_handler import Handler

from numpy import *



# TODO: refactor gui

import numpy as np
import re


class ColoredWidget(QWidget):
    """
      Class representing a color widget in the application. Used to create colored rectangle
      in layout environment.

      This class extends the QWidget class from the PyQt5 library to create a custom widget
      that displays a colored area. It provides functionality to set and retrieve the color
      of the widget.

      Attributes:
          color (str): color of this widget instance
    """

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
    """
          Class is representing storage object widget - widget that contains Creator.ObjectWidget()
          for each figure on the screen

          Attributes:
              UI (QMainWindow): UI where this object is to be instantiated
        """

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

        self.__object_visible = True

       # self.show()

        self.widgets = {}
        self.color_widget = {}

        print("Storage object Widget initialized")

    def add(self, uid, name, type, color) -> None:

        self.color_widget[uid] = ColoredWidget(color)
        objectWidget = self.creator.ObjectWidget()
        objectWidget.Form.horizontalLayout.replaceWidget(objectWidget.Form.color_view, self.color_widget[uid])
        objectWidget.Form.color_view.deleteLater()
       # objectWidget.Form.horizontalLayout.addWidget(_color,2)
        objectWidget.Form.label_name.setText(name)
        objectWidget.Form.label_type.setText(type)
       # objectWidget.Form.label_color.setText(str(uid))
        objectWidget.Form.button_edit.clicked.connect(lambda: self.UI.edit_object(uid))
        objectWidget.Form.visibiityCheckBox.stateChanged.connect(lambda: self.UI.edit_visibility(uid, objectWidget.Form.visibiityCheckBox.isChecked()))

        self.widgets[uid] = objectWidget
        self.scroll_area_layout.addWidget(self.widgets[uid])
        print("added new widget")

    def delete(self, uid) -> None:

        if uid in self.widgets.keys():
            self.widgets[uid].deleteLater()
            del self.widgets[uid]

    def update(self, uid, name, type, color) -> None:

        self.widgets[uid].Form.label_name.setText(name)
        self.widgets[uid].Form.label_type.setText(type)
        #self.widgets[uid].Form.label_color.setText(str(uid))
        self.color_widget[uid].change_color(color)
        print("updating widget")

class UI(QMainWindow):
    """
      Class representing the user interface of the application.

      This class extends the QMainWindow class from the PyQt5 library to create the main window
      and manage the graphical user interface (GUI) elements of the application.

      Attributes:
          None

      All methods are to be used only internally.

      """

    def __init__(self):
        super(UI, self).__init__()
        # Load ui file
        #uic.loadUi("ui/userinterface.ui",self)

        _ui = userinterface_.Ui_MainWindow()
        _ui.setupUi(self)
        _ui.retranslateUi(self)

        self.creator = Creator()
        self.help_window = self.creator.HelpWidget()

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
        self.help = self.findChild(QAction, 'help')

        self.show_tools = self.findChild(QAction, 'tools')
        self.show_console = self.findChild(QAction, 'console')
        self.settings = self.findChild(QAction, 'settings')



        self.horizontal_layout = self.findChild(QHBoxLayout, "horizontalLayout_2")

       # self.creator = Creator()



        # Define layout for future replacement
        self.main_layout = self.findChild(QHBoxLayout, 'horizontalLayout')

        # Initializing pyvista scene
        self.pyvista_widget = PlotterWidget(self)


        self.main_layout.removeWidget(self.widget)
        self.widget.deleteLater()
        self.main_layout.removeWidget(self.toolbox)

        self.main_layout.addWidget(self.pyvista_widget, 4)
        #self.pyvista_widget.test_scene()

        self.main_layout.addWidget(self.toolbox)

        # Click the action
        self.show_tools.triggered.connect(self.hide_unhide_tools)
        self.show_console.triggered.connect(self.hide_unhide_console)
        self.settings.triggered.connect(self.open_settings_widget)
        self.help.triggered.connect(self.open_help_window)
        self.new_scene.triggered.connect(self.wipe_scene)

        # Show the app
        self.show()

        # Keep track of hidden or not
        self.hidden_tools = False
        self.hidden_console = False
        self.hide_unhide_console()
        self.show_console.setChecked(0)

        self.SOW = StorageObjectWidget(self)
        self.object_storage = ObjectStorage(self.pyvista_widget, self.SOW, None, 3.5)

        self.highlights_enabled = True
        self.labels_enabled = True
        self.object_storage.__enable_intersections = True

        self.standart_colors = dict()
        self.standart_colors[FigureTypes.LINE] = '#FFFFFF'
        self.standart_colors[FigureTypes.PLANE] = '#42f593'
        self.standart_colors[FigureTypes.CURVE] = '#cfc951'
        self.standart_colors[FigureTypes.CONE] = '#f57a16'
        self.standart_colors[FigureTypes.CYLINDER] = '#4e3c99'
        self.standart_colors[FigureTypes.REVOLUTION] = '#c842f5'
        self.standart_colors[FigureTypes.PARAMETRIC_SURFACE] = '#ff00ff'

        self.horizontal_layout.replaceWidget(self.scrollArea, self.SOW)
        # self.horizontal_layout.addWidget(self.SOW)
        self.scrollArea.deleteLater()
        self.scrollAreaContents.deleteLater()
        self.parser = Parser()

        self.handler = Handler(self)

        self.color_picker = QColorDialog()

        # По хорошему конечно это всё в отдельный класс вынести, но пока сойдёт
        self.settingsWidget = self.creator.SettingsWidget()
        self.highlight_color = "red"
        self.highlight_width = 2.5
        self.intersections_enabled = True
        self.intersections_width = 3.5
        self.intersections_color = None

        self.screenshot_extension = ".bmp"

        self.settingsWidget.palette = self.settingsWidget.palette()

        self.label_width = 8
        self.label_font_size = 12
        self.label_point_size = 14


        self.save.triggered.connect(self.save_file)
        self.save_as.triggered.connect(self.save_file_as)
        self.open.triggered.connect(self.load_file)

        self.save_image.triggered.connect(self.take_screenshot)
        self.objects_list = {}


        self.add_object()

    def open_help_window(self) -> None:
        self.help_window.show()

    def take_screenshot(self) -> None:
        try:
            self.pyvista_widget.take_screenshot(self.screenshot_extension, '')
        except PermissionError:
            self.handler.error("Permission error. Please run program as an administrator or reinstall it to the other folder")
        except Exception as e:
            self.handler.error(f"Unknown error while saving {e}")

    def open_settings_widget(self) -> None:

        self.settingsWidget.show()

        self.settingsWidget.Form.intersectionsSelectColorButton.disconnect()
        self.settingsWidget.Form.outlineColorButton.disconnect()

        self.settingsWidget.Form.intersectionsEnableCheckBox.setChecked(self.intersections_enabled)
        self.settingsWidget.Form.intersectionsWidthLineEdit.setText(str(self.intersections_width))
        self.settingsWidget.Form.randomIntersectionsColorCheckBox.setChecked(True if self.intersections_color is None else False)
        self.settingsWidget.Form.intersectionsSelectColorButton.setStyleSheet(f"background-color : {self.intersections_color if self.intersections_color is not None else 'grey'}")
        self.settingsWidget.Form.intersectionsSelectColorButton.setEnabled(False if self.intersections_color is None else True)
        self.new_color_int = self.intersections_color
        self.new_color_high = self.highlight_color

        self.settingsWidget.Form.labelsWidthLineEdit.setText(str(self.label_width))
        self.settingsWidget.Form.labelsFontSizeLineEdit.setText(str(self.label_font_size))
        self.settingsWidget.Form.labelsPointSizeLineEdit.setText(str(self.label_point_size))
        self.settingsWidget.Form.checkBox.setChecked(True if self.labels_enabled else False)
        self.settingsWidget.Form.outlineColorButton.setStyleSheet(f"background-color : {self.highlight_color}")

        self.settingsWidget.Form.screenshotFormatComboBox.setCurrentText(self.screenshot_extension)


        def block_unblock(state: bool):
            self.settingsWidget.Form.intersectionsSelectColorButton.setEnabled(state)

        def select_intersection_color():
            new_color = self.color_picker.getColor()
            if new_color.isValid():
                self.new_color_int = new_color.name()
                self.settingsWidget.Form.intersectionsSelectColorButton.setStyleSheet(f"background-color : {self.new_color_int}")

        def select_outline_color():
            new_color = self.color_picker.getColor()
            if new_color.isValid():
                self.new_color_high = new_color.name()
                self.settingsWidget.Form.outlineColorButton.setStyleSheet(
                    f"background-color : {self.new_color_high}")



        def apply():

            try:
                self.intersections_width = float(self.settingsWidget.Form.intersectionsWidthLineEdit.text())
            except Exception as e:
                self.handler.error(f"Incorrect input in intersections width input \n {e}")
                return

            try:
                self.label_width = float(self.settingsWidget.Form.labelsWidthLineEdit.text())
            except Exception as e:
                self.handler.error(f"Incorrect input in labels width input \n {e}")
                return

            try:
                self.label_font_size = float(self.settingsWidget.Form.labelsFontSizeLineEdit.text())
            except Exception as e:
                self.handler.error(f"Incorrect input in labels font size input \n {e}")
                return

            try:
                self.label_point_size = float(self.settingsWidget.Form.labelsPointSizeLineEdit.text())
            except Exception as e:
                self.handler.error(f"Incorrect input in labels point size input \n {e}")
                return

            self.intersections_width = abs(float(self.settingsWidget.Form.intersectionsWidthLineEdit.text()))
            self.object_storage.line_width = self.intersections_width
            self.console.append(f"Changed intersections width to {self.object_storage.line_width}")

            self.label_width = abs(float(self.settingsWidget.Form.labelsWidthLineEdit.text()))
            self.pyvista_widget.label_width = self.label_width
            self.console.append(f"Changed label lines width to {self.pyvista_widget.label_width}")

            self.label_font_size = abs(float(self.settingsWidget.Form.labelsFontSizeLineEdit.text()))
            self.pyvista_widget.font_size = self.label_font_size
            self.console.append(f"Changed font size to {self.object_storage.line_width}")

            self.label_point_size = abs(float(self.settingsWidget.Form.labelsPointSizeLineEdit.text()))
            self.pyvista_widget.point_size = self.label_point_size
            self.console.append(f"Changed label point size to {self.pyvista_widget.point_size}")

            if self.settingsWidget.Form.randomIntersectionsColorCheckBox.isChecked():
                self.object_storage.intersections_color = None
                self.intersections_color = None
            else:
                if self.new_color_int is None:
                    self.new_color_int = "grey"
                self.intersections_color = self.new_color_int
                self.object_storage.intersections_color = self.intersections_color

            if self.settingsWidget.Form.intersectionsEnableCheckBox.isChecked():
                self.set_intersections(True)
                self.intersections_enabled = True
            else:
                self.set_intersections(False)
                self.intersections_enabled = False

            if self.settingsWidget.Form.checkBox.isChecked():
                self.pyvista_widget.labels_enabled = True
                self.labels_enabled = True
            else:
                self.pyvista_widget.labels_enabled = False
                self.labels_enabled = False

            self.highlight_color = self.new_color_high
            self.pyvista_widget.highlight_color = self.highlight_color

            self.screenshot_extension = self.settingsWidget.Form.screenshotFormatComboBox.currentText()

            self.settingsWidget.Form.applyButton.disconnect()
            self.settingsWidget.Form.cancelButton.disconnect()
            self.settingsWidget.Form.resetButton.disconnect()
            self.settingsWidget.hide()

        def cancel():

            self.settingsWidget.Form.applyButton.disconnect()
            self.settingsWidget.Form.cancelButton.disconnect()
            self.settingsWidget.Form.resetButton.disconnect()
            self.settingsWidget.hide()

        def reset():
            self.settingsWidget.Form.intersectionsEnableCheckBox.setChecked(True)
            self.settingsWidget.Form.intersectionsWidthLineEdit.setText("3.5")
            self.settingsWidget.Form.randomIntersectionsColorCheckBox.setChecked(True)
            self.settingsWidget.Form.intersectionsSelectColorButton.setStyleSheet(f"background-color : red")
            self.settingsWidget.Form.intersectionsSelectColorButton.setEnabled(False)

            self.settingsWidget.Form.outlineColorButton.setStyleSheet(f"background-color : red")

        self.settingsWidget.Form.applyButton.clicked.connect(apply)
        self.settingsWidget.Form.cancelButton.clicked.connect(cancel)
        self.settingsWidget.Form.resetButton.clicked.connect(reset)

        self.settingsWidget.Form.randomIntersectionsColorCheckBox.stateChanged.connect(
            lambda: block_unblock(not self.settingsWidget.Form.randomIntersectionsColorCheckBox.isChecked()))

        self.settingsWidget.Form.intersectionsSelectColorButton.clicked.connect(select_intersection_color)
        self.settingsWidget.Form.outlineColorButton.clicked.connect(select_outline_color)

    def wipe_scene(self) -> None:
        if self.handler.warning("Create new scene? Current scene will be cleared"):
            self.pyvista_widget.clear_actors()
            self.pyvista_widget.remove_intersections()
            self.object_storage.objManager.wipe()
            self.openCreateWidget(FigureTypes.CONE)
            self.add_object()
            self.object_storage.wipe_everything()

        return

    def save_file(self) -> None:
        try:
            self.object_storage.save(None)
        except Exception as e:
            self.handler.error("Saving error\n" + str(e))
            print("Saving error")
            print(e)

    def save_file_as(self) -> None:
        try:
            fname = QFileDialog.getSaveFileName(self, "Save Scene", "scenes/untitled", ".json")
            fname = str(fname[0]) + str(fname[1])
            print(fname)
            self.object_storage.save(fname)
        except Exception as e:
            self.handler.error("Saving error\n" + str(e))
            print("Saving error")
            print(e)
        ...

    def load_file(self) -> None:
        try:
            fname = QFileDialog.getOpenFileName(self, "Load Scene", "scenes/", "JSON files (*.json)")

            print(fname)
            self.object_storage.load(fname[0])
        except Exception as e:
            self.handler.error("Loading error \n" + str(e))
            print(e)
        finally:
            # Please don`t touch, it just works
            self.openCreateWidget(FigureTypes.CONE)
            self.add_object()

    def set_intersections(self, mode: bool) -> None:
        if mode:
            self.object_storage.enable_intersections = True
        else:
            self.object_storage.enable_intersections = False
            self.pyvista_widget.remove_intersections()
        print(f"intersections are now {mode}")

    def clear_right(self) -> None:
        for i in reversed(range(self.toolbox_layout.count())):
             self.toolbox_layout.itemAt(i).widget().setParent(None)

    def remove_all_highlights(self) -> None:
        for object in self.object_storage.storage:
            print(f"trying to delete highlight from {str(object)}")
            self.pyvista_widget.remove_highlight(object)
        print(self.pyvista_widget.actors_HL)

    def remove_all_labels(self) -> None:
        for object in self.pyvista_widget.actors_drawed_labels:
            print(f"trying to delete highlight from {str(object)}")
            self.pyvista_widget.remove_label(object)

    # CHOOSE NEW OBJECT WIDGET #
    def add_object(self) -> None:

        #contextMenu = QMenu(self)

        #menu_choice_conical = contextMenu.addAction("Add conical surface")
        #menu_choice_conical.triggered.connect(lambda: self.openCreateWidget(0))

        self.remove_all_highlights()

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

        choice_parametric_surface = QPushButton("Add parametric surface")
        choice_parametric_surface.clicked.connect(lambda: self.openCreateWidget(FigureTypes.PARAMETRIC_SURFACE))
        choiceWidgetLayout.addWidget(choice_parametric_surface)

        choiceWidgetLayout.addStretch()

        self.choiceWidget.setLayout(choiceWidgetLayout)

        self.toolbox_layout.removeWidget(self.commonWidget)
        self.toolbox_layout.removeWidget(self.inside)

        self.inside.deleteLater()
        self.commonWidget.deleteLater()

        self.inside = self.choiceWidget
        self.toolbox_layout.addWidget(self.inside)
        self.toolbox_layout.update()

    # CREATE NEW OBJECT WIDGET #
    def openCreateWidget(self, _type: FigureTypes) -> None:


        self.clear_right()

        self.commonWidget = self.creator.CommonSettingsWidget()
        self.commonWidget.Form.inputName.setText("Object")
        self.commonWidget.Form.button_color.setText("")
        self.commonWidget.Form.button_color.setStyleSheet(f"background-color : {self.standart_colors[_type]}")
        self.commonWidget.color = self.standart_colors[_type]
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
            case FigureTypes.PARAMETRIC_SURFACE:
                self.commonWidget.Form.inputTBounds.setEnabled(True)
                self.commonWidget.Form.inputVBounds.setEnabled(True)
                self.createWidget = self.creator.CreateSurfaceWidget()

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

    def input_point(self) -> tuple[float, float, float]:

        point_input_x = self.findChild(QLineEdit, "point_input_x").text()
        point_input_y = self.findChild(QLineEdit, "point_input_y").text()
        point_input_z = self.findChild(QLineEdit, "point_input_z").text()
        try:
            point_input_x = float(point_input_x)
            point_input_y = float(point_input_y)
            point_input_z = float(point_input_z)
        except:
            self.handler.warning("Incorrect value in point input")
            return False

        return point_input_x, point_input_y, point_input_z

    def input_vector(self) -> tuple[float, float, float]:
        vector_input_x = self.findChild(QLineEdit, "vector_input_x").text()
        vector_input_y = self.findChild(QLineEdit, "vector_input_y").text()
        vector_input_z = self.findChild(QLineEdit, "vector_input_z").text()
        try:
            vector_input_x = float(vector_input_x)
            vector_input_y = float(vector_input_y)
            vector_input_z = float(vector_input_z)
        except:
            self.handler.warning("Incorrect value in vector input")
            return False

        if vector_input_x == 0 and vector_input_y == 0 and vector_input_z == 0:
            self.handler.error("Zero vector input")
            return

        return vector_input_x, vector_input_y, vector_input_z

    def input_curve(self) -> tuple[str, str, str]:

        #curve_input_x = self.inside.verticalLayout.curve_input_x.text()
        curve_input_x = self.findChild(QLineEdit, "curve_input_x").text()
        curve_input_y = self.findChild(QLineEdit, "curve_input_y").text()
        curve_input_z = self.findChild(QLineEdit, "curve_input_z").text()

        _curve_input_x_text = curve_input_x
        _curve_input_y_text = curve_input_y
        _curve_input_z_text = curve_input_z

        try:
            a = self.parser.parse_expression_string_to_lambda(curve_input_x)
            a = self.parser.parse_expression_string_to_lambda(curve_input_x)
            a = self.parser.parse_expression_string_to_lambda(curve_input_x)
        except:
            self.handler.error("Incorrect value in curve input")
            return False


        if self.parser.check_expression_string(curve_input_x) and self.parser.check_expression_string(curve_input_y) and self.parser.check_expression_string(curve_input_z):
            return curve_input_x, curve_input_y, curve_input_z

        self.handler.warning("Incorrect value in curve input")
        return False

    def input_parametric_surface(self) -> tuple[str, str, str]:

        curve_input_x = self.findChild(QLineEdit, "surface_input_x").text()
        curve_input_y = self.findChild(QLineEdit, "surface_input_y").text()
        curve_input_z = self.findChild(QLineEdit, "surface_input_z").text()

        _curve_input_x_text = curve_input_x
        _curve_input_y_text = curve_input_y
        _curve_input_z_text = curve_input_z

        try:
            a = self.parser.parse_expression_string_to_lambda_two_params(curve_input_x)
            a = self.parser.parse_expression_string_to_lambda_two_params(curve_input_x)
            a = self.parser.parse_expression_string_to_lambda_two_params(curve_input_x)
        except:
            self.handler.error("Incorrect value in parametric surface input")
            return False

        if self.parser.check_expression_string_two_params(curve_input_x) and self.parser.check_expression_string_two_params(
                curve_input_y) and self.parser.check_expression_string_two_params(curve_input_z):
            return curve_input_x, curve_input_y, curve_input_z

        self.handler.error("Incorrect value in parametric surface input")
        return False

    def input_line(self) -> tuple[float, float, float, float, float, float]:

        point_input_x_1 = self.findChild(QLineEdit, "input_x_1").text()
        point_input_y_1 = self.findChild(QLineEdit, "input_y_1").text()
        point_input_z_1 = self.findChild(QLineEdit, "input_z_1").text()
        try:
            point_input_x_1 = float(point_input_x_1)
            point_input_y_1 = float(point_input_y_1)
            point_input_z_1 = float(point_input_z_1)
        except:
            self.handler.warning("Incorrect value in line`s point 1 input")
            return False

        point_input_x_2 = self.findChild(QLineEdit, "input_x_2").text()
        point_input_y_2 = self.findChild(QLineEdit, "input_y_2").text()
        point_input_z_2 = self.findChild(QLineEdit, "input_z_2").text()
        try:
            point_input_x_2 = float(point_input_x_2)
            point_input_y_2 = float(point_input_y_2)
            point_input_z_2 = float(point_input_z_2)
        except:
            self.handler.warning("Incorrect value in line`s point 2 input")
            return False

        return point_input_x_1, point_input_y_1, point_input_z_1, point_input_x_2, point_input_y_2, point_input_z_2

    def edit_object(self, uid) -> None:
        self.remove_all_labels()
        self.remove_all_highlights()
        print(f"editing {uid}")
        storage = self.object_storage.storage
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

                self.createWidget.Form.input_x_1.setText(str(storage[uid]["point"][0]))
                self.createWidget.Form.input_y_1.setText(str(storage[uid]["point"][1]))
                self.createWidget.Form.input_z_1.setText(str(storage[uid]["point"][2]))

                self.createWidget.Form.input_x_2.setText(str(storage[uid]["direction"][0]))
                self.createWidget.Form.input_y_2.setText(str(storage[uid]["direction"][1]))
                self.createWidget.Form.input_z_2.setText(str(storage[uid]["direction"][2]))

            case FigureTypes.PARAMETRIC_SURFACE:
                self.commonWidget.Form.inputTBounds.setEnabled(True)
                self.commonWidget.Form.inputVBounds.setEnabled(True)
                self.createWidget.Form.surface_input_x.setText(str(storage[uid]["surface_string"][0]))
                self.createWidget.Form.surface_input_y.setText(str(storage[uid]["surface_string"][1]))
                self.createWidget.Form.surface_input_z.setText(str(storage[uid]["surface_string"][2]))



        self.createWidget.Form.applyButton.disconnect()

        self.createWidget.Form.applyButton.clicked.connect(lambda: self.edit_apply_button_clicked(_type, uid))
        self.createWidget.Form.cancelButton.clicked.connect(self.edit_cancel_button_clicked)

        if not uid in self.pyvista_widget.actors_HL:
            self.pyvista_widget.highlight_mesh(uid)

        if self.labels_enabled and _type!=FigureTypes.PARAMETRIC_SURFACE:
            self.pyvista_widget.add_label(uid)

        button_delete.clicked.connect(lambda: self.deleteObject(uid))

    def edit_apply_button_clicked(self, _type: FigureTypes, uid: uuid.uuid4) -> None:
        self.pyvista_widget.remove_intersections()
        self.createObject(_type, True, uid)
        if uid not in self.pyvista_widget.actors_HL:
            self.pyvista_widget.highlight_mesh(uid)

    def edit_cancel_button_clicked(self) -> None:
        self.remove_all_highlights()
        self.remove_all_labels()
        self.add_object()

    def edit_visibility(self, uid, state: bool) -> None:
        if uid in self.object_storage.storage.keys():
            if state:
                self.pyvista_widget.show_mesh(uid)
            else:
                self.pyvista_widget.hide_mesh(uid)

    def createObject(self, _type, update_mode, uid) -> None:

        name = self.commonWidget.Form.inputName.text()
        color = self.commonWidget.color
        opacity = self.commonWidget.Form.inputOpacity.text()

        if not self.parser.parse_two_floats(self.commonWidget.Form.inputTBounds.text()):
            self.handler.error("Incorrect input in t_bounds")
            return
        t_bounds = self.parser.parse_two_floats(self.commonWidget.Form.inputTBounds.text())

        if t_bounds[0] >= t_bounds[1]:
            self.handler.error("t bounds is zero or less")
            return

        if not self.parser.parse_two_floats(self.commonWidget.Form.inputVBounds.text()):
            self.handler.error("Incorrect input in v_bounds")
            return
        v_bounds = self.parser.parse_two_floats(self.commonWidget.Form.inputVBounds.text())

        if v_bounds[0] >= v_bounds[1]:
            self.handler.error("v bounds is zero or less")
            return

        input = {}

        match _type:
            case FigureTypes.CONE:  # Conical surface

                if not self.input_point():
                    return
                point_input_x, point_input_y, point_input_z = self.input_point()

                if not self.input_curve():
                    return
                curve_input_x, curve_input_y, curve_input_z = self.input_curve()

                #checking if point is on curve
                cx = self.parser.parse_expression_string_to_lambda(curve_input_x)
                cy = self.parser.parse_expression_string_to_lambda(curve_input_y)
                cz = self.parser.parse_expression_string_to_lambda(curve_input_z)

                px, py, pz = point_input_x, point_input_y, point_input_z

                epsilon = 0.5
                bounds = np.arange(t_bounds[0], t_bounds[1], 0.4)
                _temp = False
                for t in bounds:
                    if px - epsilon < cx(t) < px + epsilon:
                        if py - epsilon < cy(t) < py + epsilon:
                            if pz - epsilon < cz(t) < pz + epsilon:
                                _temp = True
                                break
                if _temp:
                    if not self.handler.warning("Point is lying on curve or very close to it"):
                        return

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

                bounds = [abs(self.pyvista_widget.get_bounds()[0]) + abs(self.pyvista_widget.get_bounds()[1]),
                          abs(self.pyvista_widget.get_bounds()[2]) + abs(self.pyvista_widget.get_bounds()[3]),
                          abs(self.pyvista_widget.get_bounds()[4]) + abs(self.pyvista_widget.get_bounds()[5])]

                input = {

                    "normal": (vector_input_x, vector_input_y, vector_input_z),
                    "point": (point_input_x, point_input_y, point_input_z),

                    "size": (max(bounds), max(bounds)),

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
                    f"For this Rotation surface curve x = {str(curve_input_x)}, y = {str(curve_input_y)}, z = {str(curve_input_z)}")

                input = {

                    "curve": (curve_input_x, curve_input_y, curve_input_z),
                    "direction": (line_x2, line_y2, line_z2),
                    "point": (line_x1, line_y1, line_z1),
                    "t_bounds": t_bounds,
                    "v_bounds": v_bounds,
                    "name": name,
                    "FigureTypes": FigureTypes.REVOLUTION,
                }

            case FigureTypes.PARAMETRIC_SURFACE:

                if not self.input_parametric_surface():
                    return
                curve_input_x, curve_input_y, curve_input_z = self.input_parametric_surface()

                self.console.append(
                    f"For this parametric surface x = {curve_input_x}, y = {curve_input_y}, z = {curve_input_z}")

                input = {

                    "surface": (curve_input_x, curve_input_y, curve_input_z),
                    "t_bounds": t_bounds,
                    "v_bounds": v_bounds,
                    "name": name,
                    "FigureTypes": FigureTypes.PARAMETRIC_SURFACE,
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
        try:
            input["opacity"] = float(opacity)
        except:
            self.handler.error("Incorrect input in opacity. Float expected")
            return


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

    def deleteObject(self, uid) -> None:

        self.pyvista_widget.remove_intersections()
        self.object_storage.delete(uid)
        self.console.append(f"Deleted object {uid}")


        self.add_object()

    def change_color(self) -> None:
        color = self.commonWidget.palette.getColor()

        if color.isValid():
            self.commonWidget.color = color.name()
            self.commonWidget.Form.button_color.setStyleSheet(f"background-color : {color.name()}")

    def hide_unhide_tools(self) -> None:
        if self.hidden_tools:
            self.toolbox.show()
            self.hidden_tools = False
        else:
            self.toolbox.hide()
            self.hidden_tools = True

    def hide_unhide_console(self) -> None:
        if self.hidden_console:
            self.console.show()
            self.hidden_console = False
        else:
            self.console.hide()
            self.hidden_console = True


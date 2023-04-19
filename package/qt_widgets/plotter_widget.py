import pyvista as pv
from pyvistaqt import BackgroundPlotter
from PyQt5 import QtWidgets


class PlotterWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # создаем plotter PyVista и сохраняем его как атрибут
        self.plotter = BackgroundPlotter(show=False)
        self.plotter.add_axes()
        self.plotter.show_grid()

        # создаем размещение виджета
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.plotter.interactor)

    def add_mesh(self, manager, uid):
        self.plotter.add_mesh(manager.get_figure_mesh(uid))

    def add_axes(self, **kwargs):
        self.plotter.add_axes(**kwargs)

    def add_text(self, text, position=None, **kwargs):
        self.plotter.add_text(text, position=position, **kwargs)

    def add_scalar_bar(self, **kwargs):
        self.plotter.add_scalar_bar(**kwargs)

    def remove_scalar_bar(self):
        self.plotter.remove_scalar_bar()

    def clear(self):
        self.plotter.clear()

    def update(self):
        self.plotter.update()

    def show_plot(self):
        self.plotter.show()

    def create_mesh(self, uid):
        self.plotter.add_mesh()

    def delete_mesh(self, uid):
        self.plotter.remove_actor(uid)

    def change_plotter_settings(self, **kwargs):
        for key, value in kwargs.items():
            if key == "t_bounce":
                self.__t_bounce = value
            elif key == "v_bounce":
                self.__v_bounce = value
            elif key == "curve":
                self.__curve = value
            elif key == "point":
                self.__point = value
            elif key == "resolution":
                self.__resolution = value
            else:
                raise ValueError(f"Unknown parameter {key}")


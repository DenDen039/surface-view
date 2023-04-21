import pyvista as pv
from pyvistaqt import BackgroundPlotter
from PyQt5 import QtWidgets

class PlotterWidget(QtWidgets.QWidget):
    def __init__(self, objects: dict, parent=None, window_size=[1280, 720]):
        super().__init__(parent=parent)

        self.plotter = BackgroundPlotter(show=False)
        self.plotter.enable_anti_aliasing()
        self.plotter.window_size = window_size

        self.plotter.add_axes()
        self.plotter.show_grid()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.plotter.interactor)

        self.objects = objects
        self.actors = dict()


    def add_mesh(self, uid: str, **kwargs):
        self.actors[uid] = self.plotter.add_mesh(self.objects[uid].get_mesh(), **kwargs)
        if uid not in self.objects:
            raise Exception("Figure not found")

    def remove_mesh(self, uid: str):
        self.plotter.remove_actor(self.actors[uid])
        if uid not in self.objects:
            raise Exception("Figure not exist")

    def clear_actors(self):
        for actor in self.actors:
            self.remove_mesh(actor)
        self.actors = dict()
        self.plotter.fly_to([0, 0, 0])

    def unlock_camera(self):
        self.plotter.enable_fly_to_right_click()
        
    def view_xy(self):
        self.plotter.view_xy()
    
    def view_xz(self):
        self.plotter.view_xz()

    def view_yx(self):
        self.plotter.view_yx()

    def view_yz(self):
        self.plotter.view_yz()
    
    def view_zx(self):
        self.plotter.view_zx()

    def view_zy(self):
        self.plotter.view_zy()

    def take_screenshot(self, file_name):
        if file_name.split('.')[-1] not in ['.png', '.jpeg', '.jpg', '.bmp', '.tif', '.tiff']:
            raise Exception("Unfortunately, this graphic format is not supported")
        self.plotter.screenshot(f"photos\{file_name}")
        
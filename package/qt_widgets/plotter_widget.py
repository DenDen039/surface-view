import numpy as np
import pyvista as pv
from pyvistaqt import BackgroundPlotter
from PyQt5 import QtWidgets

class PlotterWidget(QtWidgets.QWidget):
    def __init__(self,
                 #objects: dict,
                 parent=None, window_size=[1280, 720], zoom=-10):
        super().__init__(parent=parent)

        self.plotter = BackgroundPlotter(show=False)
        self.plotter.enable_anti_aliasing()
        self.zoom = zoom
        self.plotter.window_size = window_size

        self.plotter.add_axes()
        self.plotter.show_grid()
        self.plotter.camera.Zoom(self.zoom)
        self.plotter.enable_terrain_style()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.plotter.interactor)

        #self.objects = objects
        self.actors = dict()

    def add_mesh(self, uid: str, mesh, **kwargs):
        #if uid not in self.objects:
        #    raise Exception("Figure not found")
        self.actors[uid] = self.plotter.add_mesh(mesh, **kwargs)
        self.update_camera()

    def remove_mesh(self, uid: str):
        if uid not in self.actors:
            raise Exception("Figure not exist")
        self.plotter.remove_actor(self.actors[uid])
        self.actors.pop(uid)
        self.update_camera()

    def clear_actors(self):
        for actor in self.actors:
            self.remove_mesh(actor)
        self.actors = dict()

    def unlock_camera(self):
        self.plotter.enable_fly_to_right_click()

    def update_camera(self):
        x_min, x_max, y_min, y_max, z_min, z_max = self.plotter.bounds
        new_position = tuple([(x_min + x_max) / 2, (y_min + y_max) / 2, (z_min + z_max) / 2])
        self.plotter.fly_to(new_position)
        
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

    def zoom_in(self):
        self.zoom += 1
        self.plotter.camera.Zoom(self.zoom)

    def zoom_out(self):
        self.zoom -= 1
        self.plotter.camera.Zoom(self.zoom)

    def take_screenshot(self, file_name='untitled.png'):
        if file_name.split('.')[-1] not in ['png', 'jpeg', 'jpg', 'bmp', 'tif', 'tiff']:
            print(file_name.split('.')[-1])
            raise Exception("Unfortunately, this graphic format is not supported")
        self.plotter.screenshot(f"photos\{file_name}")
        
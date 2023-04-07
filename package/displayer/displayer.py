import pyvista as pv
import numpy as np

from typing import Callable

class Displayer:
    # TODO change surfaces to dict, add uids, add remove surface method
    # TODO add plot parameter for each surface. We can create Surface class which will contain opacity, color, etc.
    def __init__(self,**kwargs) -> None:
        self.plotter = pv.Plotter(**kwargs,notebook=False,)
        

        self.surfaces = []

    def __reset(self):
        for a in self.plotter.renderer.actors.values():
            if isinstance(a, pv.Actor):
                a.prop.show_edges = False

    def __callback(self,actor):
        self.__reset()
        actor.prop.show_edges = True

    def update_displayer(self):
        self.plotter.clear_actors()
        for surface in self.surfaces:
            self.plotter.add_mesh(surface[0],surface[1])

    def clear_displayer(self):
        self.plotter().clear_actors()
        self.surfaces = []

    def add_surface(self,surface_grid:pv.StructuredGrid, **kwargs):
        self.surfaces.append((surface_grid))
        self.plotter.add_mesh(surface_grid,**kwargs)

    def show_plot(self):
        self.plotter.enable_mesh_picking(self.__callback, left_clicking=True, use_actor=True, show=False,show_message=False)
        self.plotter.enable_mesh_picking(show_message=False)
        self.plotter.show()

    def get_plotter(self):
        return self.plotter
# Example
if __name__ == "__main__":
    def create_sphere(cx,cy,cz, r, resolution=100):
        '''
        create sphere with center (cx, cy, cz) and radius r
        '''
        phi = np.linspace(0, 2*np.pi, 2*resolution)
        theta = np.linspace(0, np.pi, resolution)

        theta, phi = np.meshgrid(theta, phi)

        r_xy = r*np.sin(theta)
        x = cx + np.cos(phi) * r_xy
        y = cy + np.sin(phi) * r_xy
        z = cz + r * np.cos(theta)
        return x,y,z
    
    disp = Displayer()

    x1,y1,z1 = create_sphere(0,0,0,4)
    x2,y2,z2 = create_sphere(3,3,3,4)

    disp.add_surface(pv.StructuredGrid(x1, y1, z1),color='r')
    disp.add_surface(pv.StructuredGrid(x2, y2, z2),color='g')

    disp.show_plot()
    
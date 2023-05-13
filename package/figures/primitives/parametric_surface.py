import pyvista as pv
import numpy as np
from package.figures.figure import Figure, FigureTypes


class ParametricSurface(Figure):
    def __init__(
            self,
            surface,
            v_bounds: tuple[float,float],
            t_bounds: tuple[float, float],
            uid: str,
            resolution: int = 250,
            **kwargs
    ):
        super().__init__(uid, FigureTypes.PARAMETRIC_SURFACE, **kwargs)

        self.__t_bounds = t_bounds
        self.__surface = surface
        self.__v_bounds = v_bounds
        self.__resolution = resolution

    def update_parameters(self, **kwargs):
        for key, value in kwargs.items():
            if key == "t_bounds":
                self.__t_bounds = value
            elif key == "v_bounds":
                self.__v_bounds = value
            elif key == "surface":
                self.__surface = value
            elif key == "resolution":
                self.__resolution = value

    def get_mesh(self):
        t_bounds = self.__t_bounds
        v_bounds = self.__v_bounds
        curve = self.__surface

        t = np.arange(t_bounds[0], t_bounds[1]+0.05, 0.05)
        v = np.arange(v_bounds[0], v_bounds[1]+0.05, 0.05)

        v, t = np.meshgrid(v, t)

        x,y,z = curve[0](t,v),curve[1](t,v),curve[2](t,v)

        return pv.StructuredGrid(
            x, y, z
        )  
import pyvista as pv
import numpy as np
from package.figures.figure import Figure, FigureTypes


class Curve(Figure):
    def __init__(
        self,
        curve,
        t_bounds: tuple[float, float],
        uid: str,
        resolution: int = 250,
        **kwargs
    ):
        super().__init__(uid, FigureTypes.CURVE, **kwargs)

        self.__t_bounds = t_bounds
        self.__curve = curve
        self.__resolution = resolution

    def update_parameters(self, **kwargs):
        for key, value in kwargs.items():
            if key == "t_bounds":
                self.__t_bounds = value
            elif key == "curve":
                self.__curve = value

    def get_mesh(self):
        t = np.arange(self.__t_bounds[0], self.__t_bounds[1], 0.05)

        x = self.__curve[0](t)
        y = self.__curve[1](t)
        z = self.__curve[2](t)

        return pv.StructuredGrid(x, y, z)

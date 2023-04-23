import pyvista as pv
import numpy as np
from package.figures.figure import Figure, FigureTypes


class Curve(Figure):
    def __init__(
        self,
        curve,
        t_bounce: tuple[float, float],
        uid: str,
        resolution: int = 500,
        **kwargs
    ):
        super().__init__(uid, FigureTypes.CURVE, **kwargs)

        self.__t_bounce = t_bounce
        self.__curve = curve
        self.__resolution = resolution

    def update_parameters(self, **kwargs):
        for key, value in kwargs.items():
            if key == "t_bounce":
                self.__t_bounce = value
            elif key == "curve":
                self.__curve = value

    def get_mesh(self):
        t = np.linspace(self.__t_bounce[0], self.__t_bounce[1], self.__resolution)

        x = self.__curve[0](t)
        y = self.__curve[1](t)
        z = self.__curve[2](t)

        return pv.StructuredGrid(x, y, z)

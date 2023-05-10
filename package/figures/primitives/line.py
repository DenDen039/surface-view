from package.figures.figure import Figure, FigureTypes
import numpy as np
import pyvista as pv


class Line(Figure):
    def __init__(
        self,
        point1: tuple[float, float, float],
        point2: tuple[float, float, float],
        t_bounds: tuple[float, float],
        uid: str,
        resolution: int = 250,
        **kwargs
    ):
        super().__init__(uid, FigureTypes.LINE, **kwargs)

        self.__t_bounds = t_bounds
        self.__point1 = point1
        self.__point2 = point2
        self.__resolution = resolution

    def update_parameters(self, **kwargs):
        for key, value in kwargs.items():
            if key == "t_bounds":
                self.__t_bounds = value
            elif key == "point1":
                self.__point1 = value
            elif key == "point2":
                self.__point2 = value

    def get_mesh(self):
        t_bounds = self.__t_bounds
        point1 = self.__point1
        point2 = self.__point2
        resolution = self.__resolution

        t = np.arange(t_bounds[0], t_bounds[1], 0.05)

        x = point1[0] + t * (point2[0] - point1[0])
        y = point1[1] + t * (point2[1] - point1[1])
        z = point1[2] + t * (point2[2] - point1[2])

        return pv.StructuredGrid(
            x, y, z
        )  # pv.Polydata(pv.StructuredGrid(x, y, z).extract_points())

from package.figures.figure import Figure, FigureTypes
import numpy as np
import pyvista as pv


class Cylinder(Figure):
    def __init__(
        self,
        curve,
        direction: tuple[float, float, float],
        t_bounds: tuple[float, float],
        v_bounds: tuple[float, float],
        uid: str,
        resolution: int = 100,
        **kwargs,
    ):
        super().__init__(uid, FigureTypes.CYLINDER, **kwargs)

        self.__t_bounds = t_bounds
        self.__v_bounds = v_bounds
        self.__curve = curve
        self.__direction = direction
        self.__resolution = resolution

    def update_parameters(self, **kwargs):
        for key, value in kwargs.items():
            if key == "t_bounds":
                self.__t_bounds = value
            elif key == "v_bounds":
                self.__v_bounds = value
            elif key == "curve":
                self.__curve = value
            elif key == "direction":
                self.__direction = value
            elif key == "resolution":
                self.__resolution = value

    def get_mesh(self) -> pv.StructuredGrid:
        t_bounds = self.__t_bounds
        v_bounds = self.__v_bounds
        curve = self.__curve
        direction = self.__direction
        resolution = self.__resolution
        t = np.linspace(t_bounds[0], t_bounds[1], resolution)
        v = np.linspace(v_bounds[0], v_bounds[1], resolution)

        v, t = np.meshgrid(v, t)

        curve = (
            curve[0](t),
            curve[1](t),
            curve[2](t),
        )

        self.x = curve[0] + v * direction[0]
        self.y = curve[1] + v * direction[1]
        self.z = curve[2] + v * direction[2]

        return pv.StructuredGrid(
            self.x, self.y, self.z
        )  # pv.PolyData(pv.StructuredGrid(self.x, self.y, self.z).extract_surface()).triangulate()

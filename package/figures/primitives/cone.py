from package.figures.figure import Figure, FigureTypes
import numpy as np
import pyvista as pv


class Cone(Figure):
    def __init__(
        self,
        curve,
        point: tuple[float, float, float],
        t_bounce: tuple[float, float],
        v_bounce: tuple[float, float],
        uid: str,
        resolution: int = 500,
        **kwargs,
    ):
        super().__init__(uid, FigureTypes.CONE, **kwargs)

        self.__t_bounce = t_bounce
        self.__v_bounce = v_bounce
        self.__curve = curve
        self.__point = point
        self.__resolution = resolution

    def update_parameters(self, **kwargs):
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

    def get_mesh(self) -> pv.StructuredGrid:
        t_bounce = self.__t_bounce
        v_bounce = self.__v_bounce
        curve = self.__curve
        point = self.__point
        resolution = self.__resolution
        t = np.linspace(t_bounce[0], t_bounce[1], resolution)
        v = np.linspace(v_bounce[0], v_bounce[1], resolution)

        v, t = np.meshgrid(v, t)

        curve = (
            curve[0](t),
            curve[1](t),
            curve[2](t),
        )

        self.x = curve[0] + v * (point[0] - curve[0])
        self.y = curve[1] + v * (point[1] - curve[1])
        self.z = curve[2] + v * (point[2] - curve[2])

        return pv.StructuredGrid(
            self.x, self.y, self.z
        )  # pv.PolyData(pv.StructuredGrid(self.x, self.y, self.z).extract_surface()).triangulate()

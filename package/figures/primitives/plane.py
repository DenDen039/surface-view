from package.figures.figure import Figure, FigureTypes
import numpy as np
import pyvista as pv


class Plane(Figure):
    def __init__(
        self,
        normal: tuple[float, float, float],
        point: tuple[float, float, float],
        size: float,
        uid: str,
        resolution: int = 50,
        **kwargs,
    ):
        super().__init__(uid, FigureTypes.PLANE, **kwargs)

        self.__normal = normal
        self.__point = point
        self.__size = size
        self.__resolution = resolution

    def update_parameters(self, **kwargs):
        for key, value in kwargs.items():
            if key == "normal":
                self.__normal = value
            elif key == "point":
                self.__point = value
            elif key == "size":
                self.__size = value
            elif key == "resolution":
                self.__resolution = value

    def get_mesh(self) -> pv.StructuredGrid:
        normal = self.__normal
        point = self.__point
        size = self.__size
        resolution = self.__resolution

        if not isinstance(normal, np.ndarray):
            normal = np.array(normal)

        if not isinstance(point, np.ndarray):
            point = np.array(point)

        plane_source = pv.Plane(
            center=point,
            direction=normal,
            i_size=size,
            j_size=size,
            i_resolution=resolution,
            j_resolution=resolution,
        )

        spacing = 1.0
        bounds = plane_source.bounds
        dims = ((np.array(bounds[1::2]) - np.array(bounds[::2])) / spacing).astype(
            int
        ) + 1

        x, y, z = np.mgrid[
            bounds[0] : bounds[1] : dims[0] * 1j,
            bounds[2] : bounds[3] : dims[1] * 1j,
            bounds[4] : bounds[5] : dims[2] * 1j,
        ]

        return pv.StructuredGrid(x, y, z)

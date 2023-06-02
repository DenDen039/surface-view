from package.figures.figure import Figure, FigureTypes
import numpy as np
import pyvista as pv


class Plane(Figure):
    def __init__(
        self,
        normal: tuple[float, float, float],
        point: tuple[float, float, float],
        size: tuple[float,float],
        uid: str,
        resolution: int = 2,
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

        plane = pv.Plane(center=np.asarray(self.__point), direction=np.asarray(self.__normal),
                            i_size=self.__size[0], j_size=self.__size[1],
                            i_resolution=self.__resolution,
                            j_resolution=self.__resolution,
                            )
        bounds = plane.bounds
        x = np.linspace(bounds[0], bounds[1], 2)
        y = np.linspace(bounds[2], bounds[3], 2)
        z = np.linspace(bounds[4], bounds[5], 2)

        xv, yv, zv = np.meshgrid(x, y, z, indexing='ij')
        grid = pv.StructuredGrid(xv, yv, zv)
        resampled_polydata = plane.sample(grid)

        return pv.wrap(resampled_polydata)
import pyvista as pv
import numpy as np
from package.figures.figure import Figure, FigureTypes


class RevolutionSurface(Figure):
    def __init__(
            self,
            curve,
            direction,
            point,
            t_bounds: tuple[float, float],
            uid: str,
            resolution: int = 250,
            **kwargs
    ):
        super().__init__(uid, FigureTypes.REVOLUTION, **kwargs)

        self.__t_bounds = t_bounds
        self.__curve = curve
        self.__direction = direction
        self.__resolution = resolution
        self.__point = point

    def __rotate_point_around_line(self, direction, angle):

        rotation_matrix = np.array([[np.cos(angle) + direction[0] ** 2 * (1 - np.cos(angle)),
                                     direction[0] * direction[1] * (1 - np.cos(angle)) - direction[2] * np.sin(angle),
                                     direction[0] * direction[2] * (1 - np.cos(angle)) + direction[1] * np.sin(angle)],
                                    [direction[1] * direction[0] * (1 - np.cos(angle)) + direction[2] * np.sin(angle),
                                     np.cos(angle) + direction[1] ** 2 * (1 - np.cos(angle)),
                                     direction[1] * direction[2] * (1 - np.cos(angle)) - direction[0] * np.sin(angle)],
                                    [direction[2] * direction[0] * (1 - np.cos(angle)) - direction[1] * np.sin(angle),
                                     direction[2] * direction[1] * (1 - np.cos(angle)) + direction[0] * np.sin(angle),
                                     np.cos(angle) + direction[2] ** 2 * (1 - np.cos(angle))]])
        return rotation_matrix

    def update_parameters(self, **kwargs):
        for key, value in kwargs.items():
            if key == "t_bounds":
                self.__t_bounds = value
            elif key == "point":
                self.__point = value
            elif key == "curve":
                self.__curve = value
            elif key == "direction":
                self.__direction = value
            elif key == "resolution":
                self.__resolution = value

    def get_mesh(self):
        t_bounds = self.__t_bounds
        curve = self.__curve
        direction = self.__direction
        line_point = self.__point

        t = np.arange(t_bounds[0], t_bounds[1] + 0.05, 0.05)
        theta = np.linspace(0, 2 * np.pi, 180)

        direction = direction / np.linalg.norm(direction)

        points_on_curve = np.vstack((curve[0](t), curve[1](t), curve[2](t))).T

        matrices = []
        points = []

        for angle in theta:
            matrices.append(self.__rotate_point_around_line(direction, angle))
            points.append(points_on_curve)

        surface_points = (np.array(points) - line_point)@np.array(matrices) + line_point

        x, y, z = (
            surface_points[:, :, 0],
            surface_points[:, :, 1],
            surface_points[:, :, 2],
        )

        return pv.StructuredGrid(x, y, z)

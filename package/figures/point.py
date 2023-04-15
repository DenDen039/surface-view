import numpy as np
import pyvista as pv
from package.figures.figure import Figure, FigureTypes

# TODO delete or finish


class Point:
    def __init__(
        self,
        uid: str,
        type: str = FigureTypes.POINT,
        color: str = "black",
        width: float = 2,
        opacity: float = 0.5,
    ):
        self.__color = color
        self.__opacity = opacity
        self.__uid = uid
        self.__type = type
        self.__width = width

    def update_settings(self, **kwargs):
        for key, value in kwargs.items():
            if key == "color":
                self.__color = value
            elif key == "opacity":
                self.__opacity = value
            elif key == "width":
                self.__width = value
            else:
                raise Exception("invalid key")

    # Getters
    def get_uid(self):
        return self.__uid

    def get_type(self):
        return self.__type

    def get_settings(self):
        settings = {
            "color": self.__color,
            "opacity": self.__opacity,
            "width": self.__width,
        }
        return settings

    def get_point(self):
        raise Exception("method has no implementation")

# Base class for all figures
import pyvista as pv
from enum import Enum


class FigureTypes(str, Enum):
    CONE = "Cone"
    CYLINDER = "Cylinder"
    CURVE = "Curve"
    LINE = "Line"
    PLANE = "Plane"
    FIGURE = "Figure"
    POINT = "Point"
    REVOLUTION = "Revolution"


class Figure:
    def __init__(
        self,
        uid: str,
        type: str = FigureTypes.FIGURE,
        color: str = "#FFFFFF",
        opacity: float = 0.5,
        line_width: float = 5,
        enable_edges: bool = False,
    ):
        self.__color = color
        self.__opacity = opacity
        self.__line_width = line_width
        self.__enable_edges = enable_edges
        self.__uid = uid
        self.__titles = []
        self.__type = type

    def add_title(self, point, title):
        pass

    def update_settings(self, **kwargs):
        for key, value in kwargs.items():
            if key == "color":
                self.__color = value
            elif key == "opacity":
                self.__opacity = value
            elif key == "line_width":
                self.__line_width = value
            elif key == "enable_edges":
                self.__enable_edges = value
            else:
                raise Exception("invalid key")

    # Getters
    def get_uid(self):
        return self.__uid

    def get_type(self):
        return self.__type

    def get_settings(self):
        settings = {
            "color": str(self.__color),
            "opacity": self.__opacity,
            "line_width": self.__line_width,
            #"enable_edges": self.__enable_edges,
        }
        return settings

    def get_mesh(self) -> pv.StructuredGrid:
        raise Exception("method has no implementation")

from pyvistaqt import BackgroundPlotter
from package.figures.figure import FigureTypes
from PyQt5 import QtWidgets


class PlotterWidget(QtWidgets.QWidget):
    '''A widget used for creating and displaying scenes.

       Args:
           parent (QWidget, optional): Parent widget. Default is None.

       Attributes:
           plotter (BackgroundPlotter): Object for plotting figures.
           layout (QVBoxLayout): Layout manager for placing the plotter widget.
           meshes (dict): Dictionary for storing mesh data.
           actors (dict): Dictionary for storing actor objects.
           actors_types (dict): Dictionary for storing actor types.
           actors_settings (dict): Dictionary for storing actor settings.
           actors_HL (dict): Dictionary for storing highlighted actors.
           actors_labels (dict): Dictionary for storing actor labels.
           actors_drawed_labels (dict): Dictionary for storing drawn actor labels.
           intersections_list (list): List of intersections.
           photo_counter (int): Counter for untitled photos.
           __highlight_color (str): Default highlight color.
           __highlight_width (float): Default highlight width.
           __label_colors (list): List of colors for labels.
           __intersection_color (str): Default intersection color.
           __intersection_width (float): Default intersection width.
           __labels_enabled (bool): Flag indicating whether labels are enabled.
           __label_width (int): Label width.
           __point_size (int): Point size.
           __font_size (int): Font size.
       '''
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.plotter = BackgroundPlotter(show=False)

        self.plotter.enable_anti_aliasing()
        self.plotter.enable_depth_peeling()

        self.plotter.add_axes()
        self.plotter.show_grid()
        self.plotter.enable_zoom_style()
        self.plotter.enable_terrain_style(mouse_wheel_zooms=True)
        self.plotter.view_isometric()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.plotter.interactor)

        self.meshes = dict()
        self.actors = dict()
        self.actors_types = dict()
        self.actors_settings = dict()
        self.actors_HL = dict()
        self.actors_labels = dict()
        self.actors_drawed_labels = dict()
        self.intersections_list = list()
        self.photo_counter = self.untitled_counter()

        self.__highlight_color = "red"
        self.__highlight_width = 2.5
        self.__label_colors = ["green", "blue", "yellow", "purple", "cyan", "red"]
        self.__intersection_color = "red"
        self.__intersection_width = 2.5

        self.__labels_enabled = True
        self.__label_width = 8
        self.__point_size = 14
        self.__font_size = 12

    @property
    def highlight_color(self):
        return self.__highlight_color

    @highlight_color.setter
    def highlight_color(self, value: str):
        self.__highlight_color = value

    @property
    def labels_enabled(self):
        return self.__labels_enabled

    @labels_enabled.setter
    def labels_enabled(self, value: bool):
        self.__labels_enabled = value

    @property
    def label_width(self):
        return self.__label_width

    @label_width.setter
    def label_width(self, value: float):
        self.__label_width = value

    @property
    def point_size(self):
        return self.__point_size

    @point_size.setter
    def point_size(self, value: float):
        self.__point_size = value

    @property
    def font_size(self):
        return self.__font_size

    @font_size.setter
    def font_size(self, value: float):
        self.__font_size = value

    def add_mesh(self, uid: str, mesh, figure_type, labels, **kwargs) -> None:
        if uid in self.actors:
            raise Exception("Figure already exists")
        self.meshes[uid] = mesh
        self.actors[uid] = self.plotter.add_mesh(self.meshes[uid], **kwargs)
        self.actors_types[uid] = figure_type
        self.actors_settings[uid] = kwargs
        self.actors_labels[uid] = labels
        self.update_camera()

    def hide_mesh(self, uid: str) -> None:
        if uid not in self.actors:
            raise Exception("Figure not exist")
        self.remove_mesh(uid)
        self.actors[uid] = self.plotter.add_mesh(self.meshes[uid], opacity=0)#, **self.actors_settings[uid])

    def show_mesh(self, uid: str) -> None:
        if uid not in self.actors:
            raise Exception("Figure not exist")
        self.remove_mesh(uid)
        self.actors[uid] = self.plotter.add_mesh(self.meshes[uid], **self.actors_settings[uid])

    def remove_mesh(self, uid: str) -> None:
        if uid not in self.actors:
            raise Exception("Figure not exist")
        if uid in self.actors_HL:
            self.remove_highlight(uid)
        self.plotter.remove_actor(self.actors[uid])
        self.actors.pop(uid)
        self.update_camera()

    def highlight_mesh(self, uid: str, color: str='red', line_width: float=2.5) -> None:

        color = self.highlight_color
        if uid not in self.actors:
                raise Exception("Figure not exist")
        if self.actors_types[uid] in [FigureTypes.PLANE]:
            boundary = self.meshes[uid].extract_feature_edges(boundary_edges=True, non_manifold_edges=False, manifold_edges=False)
            self.actors_HL[uid] = self.plotter.add_mesh(boundary, color=color, line_width=line_width)

        elif self.actors_types[uid] in [FigureTypes.LINE, FigureTypes.CURVE]:
            self.remove_mesh(uid)
            self.actors[uid] = self.plotter.add_mesh(self.meshes[uid], render_lines_as_tubes=True, **self.actors_settings[uid])

        elif self.actors_types[uid] in [FigureTypes.REVOLUTION, FigureTypes.CONE, FigureTypes.CYLINDER, FigureTypes.PARAMETRIC_SURFACE]:
            self.remove_mesh(uid)
            self.actors[uid] = self.plotter.add_mesh(self.meshes[uid],
                                                     silhouette=dict(color=color, line_width=line_width,
                                                                     feature_angle=60), **self.actors_settings[uid])
           # self.actors[uid] = self.plotter.add_mesh(self.meshes[uid], silhouette=dict(color=color, line_width=line_width), **self.actors_settings[uid])
            self.actors_HL[uid] = self.plotter.actors[list(self.plotter.actors.keys())[-2]]
        else:
            raise Exception("Unknown figure type")
        
    def remove_highlight(self, uid: str) -> None:

        if uid in self.actors_HL:
            if self.actors_types[uid] in [FigureTypes.CONE, FigureTypes.CYLINDER, FigureTypes.PLANE, FigureTypes.REVOLUTION, FigureTypes.PARAMETRIC_SURFACE]:
                  self.plotter.remove_actor(self.actors_HL[uid])
                  del self.actors_HL[uid]
        if self.actors_types[uid] in [FigureTypes.LINE, FigureTypes.CURVE]:
                  self.remove_mesh(uid)
                  self.actors[uid] = self.plotter.add_mesh(self.meshes[uid], **self.actors_settings[uid])

    def show_edges_mesh(self, uid: str, color: str='white') -> None:
        if uid not in self.actors:
            raise Exception("Figure not exist")
        self.remove_mesh(uid)
        self.actors[uid] = self.plotter.add_mesh(self.meshes[uid], show_edges=True, edge_color=color, **self.actors_settings[uid])

    def hide_edges_mesh(self, uid: str) -> None:
        if uid not in self.actors_HL:
            raise Exception("Figure not exist")
        self.remove_mesh(uid)
        self.actors[uid] = self.plotter.add_mesh(self.meshes[uid], show_edges=False, **self.actors_settings[uid])

    def add_intersections(self, intersections, colors, line_width) -> None:
        print(f"intersections:{intersections}")

        for i in range(len(intersections)):
            new_intersection = self.plotter.add_mesh(intersections[i], render_lines_as_tubes=True, color=colors[i],
                                                     line_width=line_width)
            self.intersections_list.append(new_intersection)

    def remove_intersections(self) -> None:
        for item in self.intersections_list:
            self.plotter.remove_actor(item)
        self.intersections_list.clear()
        self.update_camera()

    def add_label(self, uid, point_size=14, line_width=8, font_size=12) -> None:
        if not self.labels_enabled:
            return
        point_size = self.__point_size
        line_width = self.label_width
        font_size = int(self.font_size)
        meshes = self.actors_labels[uid][0]
        colors = ["green", "blue", "yellow", "purple", "cyan", "red"]
        drawed_meshes = list()
        for i in range(len(meshes)):
            drawed_meshes.append(self.plotter.add_mesh(meshes[i], color=colors[i], line_width=line_width, render_lines_as_tubes=True))

        points = list(self.actors_labels[uid][1].values())
        labels = list(self.actors_labels[uid][1].keys())
        self.plotter.add_point_labels(points, labels, always_visible=True, italic=True, font_size=font_size, point_color='red', point_size=point_size, show_points=True, render_points_as_spheres=True)

        drawed_points = [self.plotter.actors[list(self.plotter.actors.keys())[-2]], self.plotter.actors[list(self.plotter.actors.keys())[-1]]]
        self.actors_drawed_labels[uid] = drawed_meshes + drawed_points

    def remove_label(self, uid) -> None:
        if uid not in self.actors_drawed_labels.keys():
            return
        for actor in self.actors_drawed_labels[uid]:
            self.plotter.remove_actor(actor)

    def clear_actors(self) -> None:
        for actor in list(self.actors.keys()):
            self.remove_mesh(actor)
        self.actors = dict()
        self.update_camera()

    def unlock_camera(self) -> None:
        self.fly = self.plotter.enable_fly_to_right_click()

    def lock_camera(self) -> None:
        self.update_camera()

    def update_camera(self) -> None:
        self.plotter.view_isometric()

    def get_bounds(self) -> tuple:
        return self.plotter.bounds
        
    def view_xy(self) -> None:
        self.plotter.view_xy()
    
    def view_xz(self) -> None:
        self.plotter.view_xz()

    def view_yx(self) -> None:
        self.plotter.view_yx()

    def view_yz(self) -> None:
        self.plotter.view_yz()
    
    def view_zx(self) -> None:
        self.plotter.view_zx()

    def view_zy(self) -> None:
        self.plotter.view_zy()

    def blur(self) -> None:
        self.plotter.add_blurring()
    
    def remove_blur(self) -> None:
        self.plotter.remove_blurring()

    def take_screenshot(self, extension: str, file_path='') -> None:
        if file_path == '':
            file_name = 'untitled_' + str(self.photo_counter) + extension
            try:
                self.photo_counter += 1

                self.plotter.screenshot(f"photos/{file_name}")
            except PermissionError as e:
                raise e
            except Exception as e:
                raise e

        else:
            if file_path.split('.')[-1] not in ['png', 'jpeg', 'jpg', 'bmp', 'tif', 'tiff']:
                raise Exception("Unfortunately, this graphic format is not supported")
            self.plotter.screenshot(file_path)

    def untitled_counter(self) -> int:
        import os
        
        if os.path.isdir("photos") == False:
            dir_path = "photos"
            os.mkdir(dir_path)

        files = os.listdir("photos/")

        numbers = list(filter(lambda str: str.startswith("untitled_"), files))
        numbers = [int(numbers[i].split('untitled_')[-1].split(".")[0]) for i in range(len(numbers))]
        if numbers:
            print(numbers)
            return max(numbers) + 1
        else:
            return 0

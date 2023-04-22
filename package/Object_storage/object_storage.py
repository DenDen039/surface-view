from package.object_manager.manager import ObjectManager
from package.figures.figure import FigureTypes


class ObjectStorage:
    def __init__(self):
        self.objManager = ObjectManager()
        self.storage = dict()
        self.SWO = SWO()
        self.PW = PW()
        self.counter = 0

    def delete(self, uid):
        del self.storage[uid]
        self.objManager.delete_figure(uid)
        self.PW.delete_mesh(uid)
        self.SWO.update()

    def update(self, uid, new_data: dict):
        self.storage[uid] = new_data
        if new_data["FigureTypes"] == FigureTypes.CONE:
            self.objManager.update_cone_mesh(uid, new_data)
        elif new_data["FigureTypes"] == FigureTypes.CYLINDER:
            self.objManager.update_cylinder_mesh(uid, new_data)
        elif new_data["FigureTypes"] == FigureTypes.CURVE:
            self.objManager.update_curve_mesh(uid, new_data)
        elif new_data["FigureTypes"] == FigureTypes.LINE:
            self.objManager.update_line_mesh(uid, new_data)
        elif new_data["FigureTypes"] == FigureTypes.PLANE:
            self.objManager.update_plane_mesh(uid, new_data)
        elif new_data["FigureTypes"] == FigureTypes.REVOLUTION:
            self.objManager.update_revolution_surface_mesh(uid, new_data)
        else:
            raise Exception(f"Invalid Figure type {new_data['FigureTypes']}")

        self.PW.redraw_mesh(uid, self.objManager.get_figure_mesh(uid), **self.objManager.get_figure_settings(uid))
        self.SWO.update()

    def create(self, to_create: dict):
        if to_create["name"] == '':
            to_create["name"] = 'untitled_' + str(self.counter)
            self.counter += 1

        if to_create["FigureTypes"] == FigureTypes.Cone:
            uid = self.objManager.create_cone(to_create["curve"],
                                              to_create["point"],
                                              to_create["t_bounce"],
                                              to_create["v_bounce"])
            self.storage[uid] = to_create
            self.SWO.Display(uid, to_create["name"])
            self.PW.add_mesh(uid, self.objManager.get_figure_mesh(uid), **self.objManager.get_figure_settings(uid))
        elif to_create["FigureTypes"] == FigureTypes.CYLINDER:
            uid = self.objManager.create_cylinder(to_create["curve"],
                                                  to_create["direction"],
                                                  to_create["t_bounce"],
                                                  to_create["v_bounce"])
            self.storage[uid] = to_create
            self.SWO.Display(uid, to_create["name"])
            self.PW.add_mesh(uid, self.objManager.get_figure_mesh(uid), **self.objManager.get_figure_settings(uid))
        elif to_create["FigureTypes"] == FigureTypes.CURVE:
            uid = self.objManager.create_curve(to_create["curve"],
                                               to_create["t_bounce"])
            self.storage[uid] = to_create
            self.SWO.Display(uid, to_create["name"])
            self.PW.add_mesh(uid, self.objManager.get_figure_mesh(uid), **self.objManager.get_figure_settings(uid))
        elif to_create["FigureTypes"] == FigureTypes.LINE:
            uid = self.objManager.create_line(to_create["point1"],
                                              to_create["point2"],
                                              to_create["t_bounce"])
            self.storage[uid] = to_create
            self.SWO.Display(uid, to_create["name"])
            self.PW.add_mesh(uid, self.objManager.get_figure_mesh(uid), **self.objManager.get_figure_settings(uid))
        elif to_create["FigureTypes"] == FigureTypes.PLANE:
            uid = self.objManager.create_plane(to_create["normal"],
                                               to_create["point"],
                                               to_create["size"])
            self.storage[uid] = to_create
            self.SWO.Display(uid, to_create["name"])
            self.PW.add_mesh(uid, self.objManager.get_figure_mesh(uid), **self.objManager.get_figure_settings(uid))
        elif to_create["FigureTypes"] == FigureTypes.REVOLUTION:
            uid = self.objManager.create_revolution_surface(to_create["curve"],
                                                            to_create["direction"],
                                                            to_create["t_bounce"])
            self.storage[uid] = to_create
            self.SWO.Display(uid, to_create["name"])
            self.PW.add_mesh(uid, self.objManager.get_figure_mesh(uid), **self.objManager.get_figure_settings(uid))
        else:
            raise Exception(f"Invalid Figure type {to_create['FigureTypes']}")

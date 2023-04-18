from package.object_manager.manager import ObjectManager

class ObjectStorage:
    def __init__(self):
        self.objManager = ObjectManager()
        self.storage = dict()
        self.SWO = SWO()
        self.PW = PW()
        self.counter = 0

    def create(self, to_create:dict):
        if to_create[name] == '':
            to_create[name] = 'untitled_' + str(self.counter)
            self.counter += 1

        if to_create[FigureTypes] == "Cone":
            uid = self.objManager.create_cone(to_create[curve],
                                        to_create[point],
                                        to_create[t_bounce],
                                        to_create[v_bounce])
            self.storage[uid] = to_create
            self.SWO.Display(uid,to_create[name])
            self.PW.Draw(uid,self.objManager.get_figure_mesh(uid))
        elif to_create[FigureTypes] == "Cylinder":
            uid = self.objManager.create_cylinder(to_create[curve],
                                        to_create[direction],
                                        to_create[t_bounce],
                                        to_create[v_bounce])
            self.storage[uid] = to_create
            self.SWO.Display(uid, to_create[name])
            self.PW.Draw(uid, self.objManager.get_figure_mesh(uid))
        elif to_create[FigureTypes] == "Curve":
            uid = self.objManager.create_curve(to_create[curve],
                                        to_create[t_bounce])
            self.storage[uid] = to_create
            self.SWO.Display(uid, to_create[name])
            self.PW.Draw(uid, self.objManager.get_figure_mesh(uid))
        elif to_create[FigureTypes] == "Line":
            uid = self.objManager.create_line(to_create[point1],
                                        to_create[point2],
                                        to_create[t_bounce])
            self.storage[uid] = to_create
            self.SWO.Display(uid, to_create[name])
            self.PW.Draw(uid, self.objManager.get_figure_mesh(uid))
        elif to_create[FigureTypes] == "Plane":
            uid = self.objManager.create_plane(to_create[normal],
                                        to_create[point],
                                        to_create[size])
            self.storage[uid] = to_create
            self.SWO.Display(uid, to_create[name])
            self.PW.Draw(uid, self.objManager.get_figure_mesh(uid))
        elif to_create[FigureTypes] == "Revolution":
            uid = self.objManager.create_revolution_surface(to_create[curve],
                                        to_create[direction],
                                        to_create[t_bounce])
            self.storage[uid] = to_create
            self.SWO.Display(uid, to_create[name])
            self.PW.Draw(uid, self.objManager.get_figure_mesh(uid))
        else:
            pass
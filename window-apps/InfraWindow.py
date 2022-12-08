#!/usr/bin/python3

import sys, os, json, gi, cairo
import copy, math

from BaseWindow import BaseWindow
from NaviWindow import NaviWindow
from TerrWindow import TerrWindow
from TerrWindow import TerrPainter
from TerrWindow import TerrGraph

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
            
class InfraPainter:
    def __init__(self, config, library, battlefield):
        self.selected_infrastructure = set()
        self.battlefield =  battlefield
        self.library = library
        self.config = config

    def get_infrastructure_params(self, name, xloc, yloc, *args):
        color = self.library["infrastructure"][name]["color"]
        wbox, hbox = self.library["infrastructure"][name]["size"]
        xoffset, yoffset = self.config["window-offset"]
        zoom = self.config["window-zoom"]
        xloc, yloc = xloc*zoom, yloc*zoom
        xloc, yloc = xloc + xoffset, yloc + yoffset
        wbox, hbox = wbox*zoom, hbox*zoom
        return color, zoom, xloc, yloc, wbox, hbox

    def draw_building_0(self, context, params, index):
        outs = self.get_infrastructure_params("building-0", *params)
        color, zoom, xloc, yloc, wbox, hbox = outs
        if index in self.selected_infrastructure:
            color = self.config["selection-color"]
        xloc =  xloc - wbox / 2
        yloc =  yloc - hbox / 2

        context.set_source_rgba(*color)
        context.rectangle(xloc, yloc, wbox, 5*zoom)
        context.rectangle(xloc, yloc+hbox-5*zoom, wbox, 5*zoom)
        context.rectangle(xloc, yloc, 5*zoom, hbox)
        context.rectangle(xloc+wbox-5*zoom, yloc, 5*zoom, hbox)
        context.rectangle(xloc+15*zoom, yloc+15*zoom, 25*zoom, 25*zoom)
        context.rectangle(xloc+50*zoom, yloc+20*zoom, 20*zoom, 20*zoom)
        context.rectangle(xloc+45*zoom, yloc+50*zoom, 15*zoom, 20*zoom)
        context.rectangle(xloc+15*zoom, yloc+60*zoom, 25*zoom, 25*zoom)
        context.rectangle(xloc+65*zoom, yloc+65*zoom, 20*zoom, 20*zoom)
        context.fill()

    def draw_seeport_0(self, context, params, index):
        outs = self.get_infrastructure_params("seeport-0", *params)
        color, zoom, xloc, yloc, wbox, hbox = outs
        if index in self.selected_infrastructure:
            color = self.config["selection-color"]
        xloc =  xloc - wbox / 2
        yloc =  yloc - hbox / 2

        context.set_source_rgba(*color)
        context.rectangle(xloc, yloc, wbox, 5*zoom)
        context.rectangle(xloc, yloc+hbox-5*zoom, wbox, 5*zoom)
        context.rectangle(xloc, yloc, 5*zoom, hbox)
        context.rectangle(xloc+wbox-5*zoom, yloc, 5*zoom, hbox)
        context.rectangle(xloc+50*zoom, yloc+10*zoom, 50*zoom, 130*zoom)
        context.rectangle(xloc+10*zoom, yloc+10*zoom, 130*zoom, 30*zoom)
        context.rectangle(xloc+10*zoom, yloc + hbox - 40*zoom, 130*zoom, 30*zoom)
        context.fill()

    def draw_seeport_1(self, context, params, index):
        outs = self.get_infrastructure_params("seeport-1", *params)
        color, zoom, xloc, yloc, wbox, hbox = outs
        if index in self.selected_infrastructure:
            color = self.config["selection-color"]
        xloc =  xloc - wbox / 2
        yloc =  yloc - hbox / 2

        context.set_source_rgba(*color)
        context.rectangle(xloc, yloc, wbox, 5*zoom)
        context.rectangle(xloc, yloc+hbox-5*zoom, wbox, 5*zoom)
        context.rectangle(xloc, yloc, 5*zoom, hbox)
        context.rectangle(xloc+wbox-5*zoom, yloc, 5*zoom, hbox)
        context.rectangle(xloc+40*zoom, yloc+10*zoom, 25*zoom, 80*zoom)
        context.rectangle(xloc+10*zoom, yloc+10*zoom, 80*zoom, 20*zoom)
        context.rectangle(xloc+10*zoom, yloc + hbox - 30*zoom, 80*zoom, 20*zoom)
        context.fill()

    def draw_airport_0(self, context, params, index):
        outs = self.get_infrastructure_params("seeport-0", *params)
        color, zoom, xloc, yloc, wbox, hbox = outs
        if index in self.selected_infrastructure:
            color = self.config["selection-color"]
        xloc =  xloc - wbox / 2
        yloc =  yloc - hbox / 2

        context.set_source_rgba(*color)
        context.rectangle(xloc, yloc, wbox, 5*zoom)
        context.rectangle(xloc, yloc+hbox-5*zoom, wbox, 5*zoom)
        context.rectangle(xloc, yloc, 5*zoom, hbox)
        context.rectangle(xloc+wbox-5*zoom, yloc, 5*zoom, hbox)
        context.rectangle(xloc+40*zoom, yloc+10*zoom, 25*zoom, 130*zoom)
        context.rectangle(xloc+10*zoom, yloc+40*zoom, 130*zoom, 25*zoom)
        context.fill()

    def draw_fortress_0(self, context, params, index):
        outs = self.get_infrastructure_params("fortress-0", *params)
        color, zoom, xloc, yloc, wbox, hbox = outs
        if index in self.selected_infrastructure:
            color = self.config["selection-color"]
        xloc =  xloc - wbox / 2
        yloc =  yloc - hbox / 2

        sq = 10*zoom
        context.set_source_rgba(*color)
        context.rectangle(xloc, yloc, sq, sq)
        context.rectangle(xloc + wbox - sq, yloc, sq, sq)
        context.rectangle(xloc, yloc + hbox - sq, sq, sq)
        context.rectangle(xloc + wbox - sq, yloc + hbox - sq, sq, sq)
        context.rectangle(xloc + (wbox - sq) / 3, yloc + hbox - sq, sq, sq)
        context.rectangle(xloc + 2 * (wbox - sq) / 3, yloc + hbox - sq, sq, sq)
        context.rectangle(xloc + (wbox - sq), yloc + (hbox - sq) / 3, sq, sq)
        context.rectangle(xloc + (wbox - sq), yloc + 2 * (hbox - sq) / 3, sq, sq)
        context.rectangle(xloc + (wbox - sq) / 3, yloc, sq, sq)
        context.rectangle(xloc + 2 * (wbox - sq) / 3, yloc, sq, sq)
        context.rectangle(xloc, yloc + (hbox - sq) / 3, sq, sq)
        context.rectangle(xloc, yloc + 2 * (hbox - sq) / 3, sq, sq)
        context.fill()

    def draw(self, context):
        infra_list = self.battlefield["infrastructure"]
        for ix, (shape, *params) in enumerate(infra_list):
            assert shape in self.library["infrastructure"]            
            if shape == "fortress-0": self.draw_fortress_0(context, params, ix)
            elif shape == "building-0": self.draw_building_0(context, params, ix)
            elif shape == "seeport-0": self.draw_seeport_0(context, params, ix)
            elif shape == "seeport-1": self.draw_seeport_1(context, params, ix)
            elif shape == "airport-0": self.draw_airport_0(context, params, ix)
            else: raise ValueError(f"Not supported shape: {shape}")

class InfraGraph(TerrGraph):
    def __init__(self, config, library, battlefield):
        self.battlefield = battlefield
        self.library = library
        self.config = config

    def check_infra(self, xloc, yloc):
        selection = set()
        infra_list = self.battlefield["infrastructure"]
        for ix, (shape, *params) in enumerate(infra_list):
            xo, yo, *other = params
            d2 = (xloc-xo)**2 + (yloc-yo)**2
            if d2 < self.config["selection-radius2"]:
                selection.add(ix)
        return selection

    def boxbox_collision(self, size1, xy1, size2, xy2):
        x1o, x1e = xy1[0] - size1[0]/2, xy1[0] + size1[0]/2        
        x2o, x2e = xy2[0] - size2[0]/2, xy2[0] + size2[0]/2
        y1o, y1e = xy1[1] - size1[1]/2, xy1[1] + size1[1]/2
        y2o, y2e = xy2[1] - size2[1]/2, xy2[1] + size2[1]/2
        xstatus = False
        if x1o < x2o and x1o > x2e: xstatus = True
        if x1e < x2o and x1e > x2e: xstatus = True
        if x1o < x2e and x1o > x2o: xstatus = True
        if x1e < x2e and x1e > x2o: xstatus = True
        ystatus = False
        if y1o < y2o and y1o > y2e: ystatus = True
        if y1e < y2o and y1e > y2e: ystatus = True
        if y1o < y2e and y1o > y2o: ystatus = True
        if y1e < y2e and y1e > y2o: ystatus = True
        return xstatus and ystatus
        
    def validate_infra_location(self, infra, xyloc):
        shape_in  = self.library["infrastructure"][infra]["shape"]
        size_in  = self.library["infrastructure"][infra]["size"]
        for infr, x, y, *params in self.battlefield["infrastructure"]:
            shape  = self.library["infrastructure"][infr]["shape"]
            size  = self.library["infrastructure"][infr]["size"]
            if shape == "box" and shape_in == "box":
                coll = self.boxbox_collision(size_in, xyloc, size, (x, y))
                if coll: return False
            else: raise ValueError("unkown collision method!")
        return True

class MultiPainter(list):
    def draw(self, context):
        for item in self: item.draw(context)

class InfraWindow(TerrWindow):
    default_app_controls = {
        "infra-num-to-add": 0,
        "selection-add": False,
        "current-mode": "navigation",
        "available-modes": {
            "F1": "navigation",
            "F2": "selection",
            "F3": "inserting",
            "F4": "deleting",
            "F5": "editing"
        }
    }

    def __init__(self, config, library, battlefield):
        self.app_controls = copy.deepcopy(self.default_app_controls)        
        self.terr_painter = TerrPainter(config, library, battlefield)
        self.infra_painter = InfraPainter(config, library, battlefield)
        self.graph = InfraGraph(config, library, battlefield)
        self.painter = MultiPainter()
        self.painter.append(self.terr_painter)
        self.painter.append(self.infra_painter)
        self.battlefield =  battlefield
        self.library = library
        self.config = config

        title = config["window-title"]
        width, height = config["window-size"]
        BaseWindow.__init__(self, title, width, height)
        print(f"Window {title} ready to work")

    def on_click(self, widget, event):
        xoffset, yoffset = self.config["window-offset"]
        width, height = self.config["window-size"]
        zoom = self.config["window-zoom"]
        ox = (int(event.x) - xoffset) / zoom
        oy = (int(event.y) - yoffset) / zoom

        if event.button == 1:
            if self.check_mode("selection", "deleting", "editing"):
                selection = self.graph.check_infra(ox, oy)
                if not self.app_controls["selection-add"]:
                    self.infra_painter.selected_infrastructure = selection
                else: self.infra_painter.selected_infrastructure |= selection
                print(f"({round(ox, 2)}, {round(oy, 2)}) --> {selection}")
                self.draw_content()

            elif self.check_mode("inserting"):
                buildlist = list(sorted(self.library["infrastructure"].keys()))
                build = buildlist[self.app_controls["infra-num-to-add"]]
                xyro = round(ox), round(oy)
                if self.graph.validate_infra_location(build, xyro):
                    insrow = (build, *xyro, 1.0)
                    self.battlefield["infrastructure"].append(insrow)
                    print("add infra", insrow)
                    self.draw_content()
                else: print("Location colision!")
            else: print(f"({round(ox, 2)}, {round(oy, 2)}), ")
        elif event.button == 3:
            terr = self.graph.check_terrain(ox, oy)
            print(f"({round(ox, 2)}, {round(oy, 2)}) --> {terr}")
        return True

    def delete_selection(self):
        if not self.infra_painter.selected_infrastructure:
            print("No infra selected...")
            return

        for ix in reversed(sorted(self.infra_painter.selected_infrastructure)):
            di = self.battlefield["infrastructure"].pop(ix)
            print(f"delete infrastructure element: {di}...")
        self.infra_painter.selected_infrastructure = set()
        self.draw_content()
        
    def save_map(self, prefix1, prefix2):
        ex = lambda f: os.path.exists(f)
        fn = lambda px, c: f"{px}-{c}.json"
        bex = lambda px1, px2, c: ex(fn(px1, c)) or ex(fn(px2, c))
        counter = 0
        while bex(prefix1, prefix2, counter):
            counter += 1
        outfield = fn("outfield", counter)
        print(f"save {outfield}")
        with open(outfield, "w") as fd:
            json.dump(self.battlefield, fd)
        outlib = fn("outlib", counter)
        print(f"save {outlib}")
        with open(outlib, "w") as fd:
            json.dump(self.library, fd)

    def on_press(self, widget, event):
        key_name = Gdk.keyval_name(event.keyval)
        if key_name == "Escape":
            print("##> ESC - go back to default controls")
            self.app_controls = copy.deepcopy(self.default_app_controls)
            self.infra_painter.selected_infrastructure = set()
            for key, name in self.app_controls["available-modes"].items():
                print(key, "-->", name)
            self.draw_content()

        elif key_name in self.app_controls["available-modes"]:
            mode = self.app_controls["available-modes"][key_name]
            self.app_controls["current-mode"] = mode
            print("##> mode", mode)

        elif key_name in "sS":
            if self.check_mode("navigation"):
                print("##> save")
                self.save_map("outlib", "outfield")
            else: print("Current mode does not support keys sS")

        elif key_name == "Insert":
            if self.check_mode("inserting"):
                self.app_controls["infra-num-to-add"] += 1
                ilen = len(self.library["infrastructure"])
                self.app_controls["infra-num-to-add"] %= ilen
                bl = list(sorted(self.library["infrastructure"].keys()))
                print("infra:", bl[self.app_controls["infra-num-to-add"]])
            else: print("Current mode does not support inserting")
            
        elif key_name == "Delete":
            if self.check_mode("deleting"):
                print("##> delete")
                self.delete_selection()
            else: print("Current mode does not support deleting")

        elif key_name in "aA":
            if self.check_mode("selection"):
                new_val = not self.app_controls["selection-add"]
                self.app_controls["selection-add"] = new_val
                print("##> selection-add", new_val)
            else: print("Current mode does not support keys aA")

        elif key_name == "Up" and self.check_mode("editing"):
            if not self.infra_painter.selected_infrastructure:
                print("no selected infrastructure...")
            for infra in self.infra_painter.selected_infrastructure:
                b, x, y, *params = self.battlefield["infrastructure"][infra]
                y -= self.config["move-editing"]
                self.battlefield["infrastructure"][infra] = b, x, y, *params
            self.draw_content()
        elif key_name == "Down" and self.check_mode("editing"):
            if not self.infra_painter.selected_infrastructure:
                print("no selected infrastructure...")
            for infra in self.infra_painter.selected_infrastructure:
                b, x, y, *params = self.battlefield["infrastructure"][infra]
                y += self.config["move-editing"]
                self.battlefield["infrastructure"][infra] = b, x, y, *params
            self.draw_content()
        elif key_name == "Left" and self.check_mode("editing"):
            if not self.infra_painter.selected_infrastructure:
                print("no selected infrastructure...")
            for infra in self.infra_painter.selected_infrastructure:
                b, x, y, *params = self.battlefield["infrastructure"][infra]
                x -= self.config["move-editing"]
                self.battlefield["infrastructure"][infra] = b, x, y, *params
            self.draw_content()
        elif key_name == "Right" and self.check_mode("editing"):
            if not self.infra_painter.selected_infrastructure:
                print("no selected infrastructure...")
            for infra in self.infra_painter.selected_infrastructure:
                b, x, y, *params = self.battlefield["infrastructure"][infra]
                x += self.config["move-editing"]
                self.battlefield["infrastructure"][infra] = b, x, y, *params
            self.draw_content()
                
        else: NaviWindow.on_press(self, widget, event)

    def check_mode(self, *args):
        return self.app_controls["current-mode"] in args

def run_example():
    example_config = {
        "window-title": "infra-window",
        "window-zoom": 0.0366,
        "window-size": (1800, 820),
        "window-offset": (500, 100),
        "selection-color": (0.8, 0, 0.8),
        "selection-radius2": 9000,
        "move-sensitive": 50,
        "move-editing": 1
    }
    
    from MapExamples import library0
    from MapExamples import battlefield0

    if len(sys.argv) >= 3:
        library_json = sys.argv[1]
        battlefield_json = sys.argv[2]
        print(f"load: {library_json}")
        with open(library_json, "r") as fd1:
            library0 = json.load(fd1)
        print(f"load: {battlefield_json}")
        with open(battlefield_json, "r") as fd2:
            battlefield0 = json.load(fd2)        
    InfraWindow(example_config, library0, battlefield0)

    try: Gtk.main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
if __name__ == "__main__": run_example()
        

#!/usr/bin/python3

import sys, os, json, gi, cairo, math
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

    def draw(self, context):
        infra_list = self.battlefield["infrastructure"]
        for ix, (shape, *params) in enumerate(infra_list):
            assert shape in self.library["infrastructure"]            
            if shape == "building-0": self.draw_building_0(context, params, ix)
            else: raise ValueError(f"Not supported shape: {shape}")

class InfraGraph(TerrGraph):
    def __init__(self, config, battlefield):
        self.battlefield = battlefield
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

class MultiPainter(list):
    def draw(self, context):
        for item in self: item.draw(context)

class InfraWindow(TerrWindow):
    def __init__(self, config, library, battlefield):
        self.graph = InfraGraph(config, battlefield)

        self.terr_painter = TerrPainter(config, library, battlefield)
        self.infra_painter = InfraPainter(config, library, battlefield)
        self.painter = MultiPainter()
        self.painter.append(self.terr_painter)
        self.painter.append(self.infra_painter)

        self.battlefield =  battlefield
        self.library = library
        self.config = config

        title = config["window-title"]
        width, height = config["window-size"]
        BaseWindow.__init__(self, title, width, height)
        
    def on_click(self, widget, event):
        xoffset, yoffset = self.config["window-offset"]
        width, height = self.config["window-size"]
        zoom = self.config["window-zoom"]
        ox = (int(event.x) - xoffset) / zoom
        oy = (int(event.y) - yoffset) / zoom

        if event.button == 1:
            selection = self.graph.check_infra(ox, oy)
            self.infra_painter.selected_infrastructure = selection
            print(f"({round(ox, 2)}, {round(oy, 2)}) --> {selection}")
            self.draw_content()
        elif event.button == 3:
            terr = self.graph.check_terrain(ox, oy)
            print(f"({round(ox, 2)}, {round(oy, 2)}) --> {terr}")
        return True

    def delete_selection(self):
        if not self.infra_painter.selected_infrastructure:
            print("No infra selected...")
            return
        print("d...")
        
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
        if key_name == "Insert":
            print("##> save")
            self.save_map("outlib", "outfield")
        elif key_name == "Delete":
            print("##> delete")
            self.delete_selection()
        else: NaviWindow.on_press(self, widget, event)
    
def run_example():
    example_config = {
        "window-title": "infra-window",
        "window-zoom": 0.0366,
        "window-size": (1800, 820),
        "window-offset": (500, 100),
        "selection-color": (0.8, 0, 0.8),
        "selection-radius2": 9000,
        "move-sensitive": 50
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
        

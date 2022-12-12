#!/usr/bin/python3

import sys, os, gi, cairo
import copy, math, json

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
        self.background_flag = True
        self.battlefield = battlefield
        self.library = library
        self.config = config

    def get_infrastructure_params(self, index, name, xloc, yloc, *args):
        color = self.library["infrastructure"][name]["color"]
        wbox, hbox = self.library["infrastructure"][name]["size"]
        xoffset, yoffset = self.config["window-offset"]
        zoom = self.config["window-zoom"]
        xloc, yloc = xloc * zoom, yloc * zoom
        xloc, yloc = xloc + xoffset, yloc + yoffset
        wbox, hbox = wbox * zoom, hbox * zoom
        if index in self.selected_infrastructure:
            color = self.config["selection-color"]
        xloc, yloc =  xloc - wbox / 2, yloc - hbox / 2
        return color, zoom, xloc, yloc, wbox, hbox

    def draw_bg(self, context, xloc, yloc, wbox, hbox):
        if not self.background_flag: return
        context.set_source_rgba(1, 1, 1)
        context.rectangle(xloc, yloc, wbox, hbox)
        context.fill()
        
    def draw_route(self, context, params, index, width):
        node1 = self.battlefield["infrastructure"][params[0]]
        node2 = self.battlefield["infrastructure"][params[1]]
        outs1 = self.get_infrastructure_params(index, *node1)
        outs2 = self.get_infrastructure_params(index, *node2)
        _, zoom, xloc1, yloc1, wbox1, hbox1 = outs1
        _, _, xloc2, yloc2, wbox2, hbox2 = outs2

        color = self.library["infrastructure"]["route-0"]["color"]
        context.set_source_rgba(*color)
        context.set_line_width(zoom * width)
        context.move_to(xloc1 + wbox1/2, yloc1 + hbox1/2)
        context.line_to(xloc2 + wbox2/2, yloc2 + hbox2/2) 
        context.stroke()

    def draw_route_0(self, context, params, index):
        self.draw_route(context, params, index, 5.5)
    def draw_route_1(self, context, params, index):
        self.draw_route(context, params, index, 12)
        
    def draw_node(self, context, params, index, radius_factor):
        outs = self.get_infrastructure_params(index, "node-0", *params)
        color, zoom, xloc, yloc, wbox, hbox = outs
        xloc, yloc =  xloc + wbox / 2, yloc + hbox / 2
        r = (wbox + hbox) * radius_factor
        context.set_source_rgba(*color)
        context.arc(xloc, yloc, r, 0, 2 * math.pi)
        context.fill()

    def draw_node_0(self, context, params, index):
        self.draw_node(context, params, index, 0.12)
    def draw_node_1(self, context, params, index):
        self.draw_node(context, params, index, 0.3)
        
    def draw_building_0(self, context, params, index):
        outs = self.get_infrastructure_params(index, "building-0", *params)
        color, zoom, xloc, yloc, wbox, hbox = outs
        self.draw_bg(context, xloc, yloc, wbox, hbox)

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

    def draw_building_1(self, context, params, index):
        outs = self.get_infrastructure_params(index, "building-1", *params)
        color, zoom, xloc, yloc, wbox, hbox = outs
        self.draw_bg(context, xloc, yloc, wbox, hbox)

        context.set_source_rgba(*color)
        context.rectangle(xloc, yloc, wbox, 5*zoom)
        context.rectangle(xloc, yloc+hbox-5*zoom, wbox, 5*zoom)
        context.rectangle(xloc, yloc, 5*zoom, hbox)
        context.rectangle(xloc+wbox-5*zoom, yloc, 5*zoom, hbox)
        context.rectangle(xloc+15*zoom, yloc+15*zoom, 25*zoom, 25*zoom)
        context.rectangle(xloc+15*zoom, yloc+45*zoom, 25*zoom, 25*zoom)
        context.rectangle(xloc+45*zoom, yloc+15*zoom, 25*zoom, 25*zoom)
        context.rectangle(xloc+45*zoom, yloc+45*zoom, 25*zoom, 25*zoom)
        context.rectangle(xloc+85*zoom, yloc+15*zoom, 25*zoom, 25*zoom)
        context.rectangle(xloc+85*zoom, yloc+45*zoom, 25*zoom, 25*zoom)
        context.fill()

    def draw_seeport_0(self, context, params, index):
        outs = self.get_infrastructure_params(index, "seeport-0", *params)
        color, zoom, xloc, yloc, wbox, hbox = outs
        self.draw_bg(context, xloc, yloc, wbox, hbox)

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
        outs = self.get_infrastructure_params(index, "seeport-1", *params)
        color, zoom, xloc, yloc, wbox, hbox = outs
        self.draw_bg(context, xloc, yloc, wbox, hbox)

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
        outs = self.get_infrastructure_params(index, "seeport-0", *params)
        color, zoom, xloc, yloc, wbox, hbox = outs
        self.draw_bg(context, xloc, yloc, wbox, hbox)

        context.set_source_rgba(*color)
        context.rectangle(xloc, yloc, wbox, 5*zoom)
        context.rectangle(xloc, yloc+hbox-5*zoom, wbox, 5*zoom)
        context.rectangle(xloc, yloc, 5*zoom, hbox)
        context.rectangle(xloc+wbox-5*zoom, yloc, 5*zoom, hbox)
        context.rectangle(xloc+40*zoom, yloc+10*zoom, 25*zoom, 130*zoom)
        context.rectangle(xloc+10*zoom, yloc+40*zoom, 130*zoom, 25*zoom)
        context.fill()

    def draw_fortress_0(self, context, params, index):
        outs = self.get_infrastructure_params(index, "fortress-0", *params)
        color, zoom, xloc, yloc, wbox, hbox = outs
        self.draw_bg(context, xloc, yloc, wbox, hbox)

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
        routes_tmp_list, nodes_tmp_list = [], []
        infra_list = self.battlefield["infrastructure"]
        for ix, (shape, *params) in enumerate(infra_list):
            if shape is None: continue
            assert shape in self.library["infrastructure"]
            if self.library["infrastructure"][shape]["shape"] == "line":
                routes_tmp_list.append((ix, (shape, *params)))
            else: nodes_tmp_list.append((ix, (shape, *params)))

        for ix, (shape, *params) in routes_tmp_list:
            if shape == "route-0": self.draw_route_0(context, params, ix)
            elif shape == "route-1": self.draw_route_1(context, params, ix)
            else: raise ValueError(f"Not supported line shape: {shape}")

        for ix, (shape, *params) in nodes_tmp_list:
            if shape == "fortress-0": self.draw_fortress_0(context, params, ix)
            elif shape == "building-0": self.draw_building_0(context, params, ix)
            elif shape == "building-1": self.draw_building_1(context, params, ix)
            elif shape == "seeport-0": self.draw_seeport_0(context, params, ix)
            elif shape == "seeport-1": self.draw_seeport_1(context, params, ix)
            elif shape == "airport-0": self.draw_airport_0(context, params, ix)
            elif shape == "node-0": self.draw_node_0(context, params, ix)
            elif shape == "node-1": self.draw_node_1(context, params, ix)
            else: raise ValueError(f"Not supported node shape: {shape}")
        
class InfraGraph(TerrGraph):
    def __init__(self, config, library, battlefield):
        self.battlefield = battlefield
        self.library = library
        self.config = config

    def clean_null_infra(self):
        infra_list = self.battlefield["infrastructure"]
        new_infra_list = copy.deepcopy(infra_list)
        for ix, (shape, *params) in enumerate(infra_list):
            if shape is not None: continue
            for jx, (sh0, n1, n2, *p) in enumerate(infra_list):
                if not self.is_shape_line(sh0): continue
                if n1 > ix: new_infra_list[jx][1] -= 1
                if n2 > ix: new_infra_list[jx][2] -= 1
        for ix in reversed(range(len(new_infra_list))):
            if new_infra_list[ix][0] is None:
                del new_infra_list[ix]
        self.battlefield["infrastructure"] = new_infra_list
        removed = len(infra_list) - len(new_infra_list)
        print("Removed empty rows:", removed)

    def find_infra(self, xloc, yloc):
        selection = set()
        infra_list = self.battlefield["infrastructure"]
        for ix, (shape, *params) in enumerate(infra_list):
            if shape is None: continue
            xo, yo, *other = params
            d2 = (xloc-xo)**2 + (yloc-yo)**2
            if d2 < self.config["selection-radius2"]:
                selection.add(ix)
        return selection

    def is_shape_line(self, shape):
        if shape is None: return False
        s = self.library["infrastructure"][shape]["shape"]
        return s == "line"
    def is_shape_box(self, shape):
        if shape is None: return False
        s = self.library["infrastructure"][shape]["shape"]
        return s == "box"

    def validate(self):
        fails = set()
        shape_flag, shape_list = True, []
        infra_list = self.battlefield["infrastructure"]
        for ix, (shape, *params) in enumerate(infra_list):
            if shape is None: continue
            if shape not in self.library["infrastructure"]:
                shape_list.append(ix)
                shape_flag = False
        if shape_flag: print("shapes: OK")
        else: print("shapes: ERROR", shape_list)
        fails |= set(shape_list)
        
        collision_flag, collision_list = True, []
        for ix, (shape, *params) in enumerate(infra_list):
            if self.is_shape_line(shape): continue
            if not self.validate_infra_location(shape, (params[0], params[1]), ix):
                collision_list.append(ix)
                collision_flag = False
        if collision_flag: print("collisions: OK")
        else: print("collisions: ERROR", collision_list)
        fails |= set(collision_list)

        length_flag, length_list = True, []
        infra_list = self.battlefield["infrastructure"]
        for ix, (shape, *params) in enumerate(infra_list):
            if not self.is_shape_line(shape): continue
            size = self.library["infrastructure"][shape]["size"]
            n1 = self.battlefield["infrastructure"][params[0]]
            n2 = self.battlefield["infrastructure"][params[1]]
            d2 = (n1[1]-n2[1])**2 + (n1[2]-n2[2])**2
            if not (size[0]**2 <= d2 <= size[1]**2):
                length_list.append(ix)
                length_flag = False
                fails.add(params[0])
                fails.add(params[1])
        if length_flag: print("route lengths: OK")
        else: print("route lengths: ERROR", length_list)
        return fails

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
        if x2o < x1o and x2o > x1e: xstatus = True
        if x2e < x1o and x2e > x1e: xstatus = True        
        if x2o < x1e and x2o > x1o: xstatus = True
        if x2e < x1e and x2e > x1o: xstatus = True

        ystatus = False
        if y1o < y2o and y1o > y2e: ystatus = True
        if y1e < y2o and y1e > y2e: ystatus = True
        if y1o < y2e and y1o > y2o: ystatus = True
        if y1e < y2e and y1e > y2o: ystatus = True
        if y2o < y1o and y2o > y1e: ystatus = True
        if y2e < y1o and y2e > y1e: ystatus = True
        if y2o < y1e and y2o > y1o: ystatus = True
        if y2e < y1e and y2e > y1o: ystatus = True

        return xstatus and ystatus
        
    def validate_infra_location(self, infra, xyloc, optional_index=None):
        if infra is None: return True
        shape_in  = self.library["infrastructure"][infra]["shape"]
        size_in  = self.library["infrastructure"][infra]["size"]
        infra_list = self.battlefield["infrastructure"]
        for ix, (infr, x, y, *params) in enumerate(infra_list):
            if optional_index == ix: continue
            if infr is None: continue
            shape  = self.library["infrastructure"][infr]["shape"]
            size  = self.library["infrastructure"][infr]["size"]
            if shape == shape_in == "box":
                coll = self.boxbox_collision(size_in, xyloc, size, (x, y))
                if coll: return False
            elif "line" in [shape, shape_in]: continue
            else: raise ValueError("unkown collision method!")
        return True

class MultiPainter(list):
    def draw(self, context):
        for item in self: item.draw(context)

class InfraWindow(TerrWindow):
    version = 0
    default_app_controls = {
        "infra-num-to-add": 0,
        "selection-add": False,
        "selection-next": False,
        "current-mode": "navigation",
        "available-modes": {
            "F1": "navigation",
            "F2": "selection",
            "F3": "inserting",
            "F4": "editing",
            "F5": "deleting"
        }
    }

    def __init__(self, config, library, battlefield):
        assert self.version == battlefield["version"]
        assert self.version == library["version"]
        assert self.version == config["version"]

        self.config = config
        self.library = library
        self.battlefield = battlefield
        self.fix_battlefield_infrastructure()

        self.app_controls = copy.deepcopy(self.default_app_controls)        
        self.terr_painter = TerrPainter(config, library, battlefield)
        self.infra_painter = InfraPainter(config, library, battlefield)
        self.graph = InfraGraph(config, library, battlefield)
        self.graph.validate()

        self.painter = MultiPainter()
        self.painter.append(self.terr_painter)
        self.painter.append(self.infra_painter)

        title = config["window-title"]
        width, height = config["window-size"]
        BaseWindow.__init__(self, title, width, height)
        print(f"Window {title} ready to work")

    def fix_battlefield_infrastructure(self):
        length = len(self.library["resources"])

        new_infra_list = []
        infra_list = self.battlefield["infrastructure"]
        for shape, *params in infra_list:
            new_row = [shape, params[0], params[1]]
            new_row += [1.0] + [0.0] * length
            for j, p in enumerate(new_row):
                if j > 2: new_row[j] = float(p)
                else: new_row[j] = p
            new_infra_list.append(new_row)
        self.battlefield["infrastructure"] = new_infra_list

    def on_click(self, widget, event):
        xoffset, yoffset = self.config["window-offset"]
        width, height = self.config["window-size"]
        zoom = self.config["window-zoom"]
        ox = (int(event.x) - xoffset) / zoom
        oy = (int(event.y) - yoffset) / zoom

        if event.button == 1:
            if self.check_mode("selection", "deleting", "editing"):
                selection = self.graph.find_infra(ox, oy)
                if self.app_controls["selection-add"]:
                    for it in selection:
                        if it in self.infra_painter.selected_infrastructure:
                            self.infra_painter.selected_infrastructure.remove(it)
                        else: self.infra_painter.selected_infrastructure.add(it)
                elif self.app_controls["selection-next"]:
                    if len(selection) != 1:
                        self.infra_painter.selected_infrastructure = selection
                        print("Warning! selection next required only 1 item")
                    else:
                        item = next(iter(selection))
                        for infr, x, y, *params in self.battlefield["infrastructure"]:
                            if self.graph.is_shape_line(infr):
                                if item == x: selection.add(y) 
                                if item == y: selection.add(x)
                        self.infra_painter.selected_infrastructure = selection
                else: self.infra_painter.selected_infrastructure = selection
                print(f"({round(ox, 2)}, {round(oy, 2)}) --> {selection}")
                self.draw_content()

            elif self.check_mode("inserting"):
                buildlist = list(sorted(self.library["infrastructure"].keys()))
                build = buildlist[self.app_controls["infra-num-to-add"]]
                xyro = round(ox), round(oy)
                if self.graph.validate_infra_location(build, xyro):
                    if self.graph.is_shape_box(build):
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
            print("No infra selected..."); return

        for ix in self.infra_painter.selected_infrastructure:
            di = self.battlefield["infrastructure"][ix]
            print(f"delete infrastructure element: {di}...")
            self.battlefield["infrastructure"][ix] = None, None, None
            for i, params in enumerate(self.battlefield["infrastructure"]):
                if not self.graph.is_shape_line(params[0]): continue
                if params[1] == ix or params[2] == ix:
                    self.battlefield["infrastructure"][i] = None, None, None
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
            null_counter = 0
            for b, *params in self.battlefield["infrastructure"]:
                if b is None: null_counter += 1
            print("terrian parts:", len(self.battlefield["terrains"]))
            print("infra parts:", len(self.battlefield["infrastructure"]))
            print("null parts:", null_counter)
            self.app_controls = copy.deepcopy(self.default_app_controls)
            self.infra_painter.selected_infrastructure = set()
            for key, name in self.app_controls["available-modes"].items():
                print(key, "-->", name)
            self.draw_content()

        elif key_name in self.app_controls["available-modes"]:
            mode = self.app_controls["available-modes"][key_name]
            self.app_controls["current-mode"] = mode
            print("##> mode", mode)
            if mode == "selection":
                selection = self.infra_painter.selected_infrastructure
                if selection: print("Selection:", selection)
                else: print("Selection: -")
        elif key_name in "sS":
            if self.check_mode("navigation"):
                print("##> save")
                self.save_map("outlib", "outfield")
            else: print("Current mode does not support keys sS")
        elif key_name in "bB":
            if self.check_mode("navigation"):
                print("##> hide background")
                self.infra_painter.background_flag = False
                self.draw_content()
                self.infra_painter.background_flag = True
            else: print("Current mode does not support keys bB")

        elif key_name in "vV":
            if self.check_mode("navigation", "inserting", "editing"):
                print("##> validate")
                selection = self.graph.validate()
                self.infra_painter.selected_infrastructure = selection
                self.draw_content()
            else: print("Current mode does not support keys vV")

        elif key_name == "Insert":
            if self.check_mode("inserting", "editing"):
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

        elif key_name in "qQ":
            if self.check_mode("deleting"):
                print("##> clean")
                self.graph.clean_null_infra()
            else: print("Current mode does not support keys qQ")
    
        elif key_name in "aA":
            if self.check_mode("selection", "editing"):
                new_val = not self.app_controls["selection-add"]
                self.app_controls["selection-add"] = new_val
                self.app_controls["selection-next"] = False
                print("##> selection-add", new_val)
            else: print("Current mode does not support keys aA")
        elif key_name in "nN":
            if self.check_mode("selection", "editing"):
                new_val = not self.app_controls["selection-next"]
                self.app_controls["selection-next"] = new_val
                self.app_controls["selection-add"] = False
                print("##> selection-next", new_val)
            else: print("Current mode does not support keys nN")

        elif key_name in "oO":
            if self.check_mode("selection", "editing"):
                if len(self.infra_painter.selected_infrastructure) > 1:
                    it = next(iter(self.infra_painter.selected_infrastructure))
                    self.infra_painter.selected_infrastructure = {it}
                    self.draw_content()
                print("##> selection-reduce")
            else: print("Current mode does not support keys oO")

        elif key_name in "cC":
            if self.check_mode("editing", "inserting"):
                buildlist = list(sorted(self.library["infrastructure"].keys()))
                build = buildlist[self.app_controls["infra-num-to-add"]]
                shape = self.library["infrastructure"][build]["shape"]
                if shape != "line": print("##> cannot connect - no line!")
                elif len(self.infra_painter.selected_infrastructure) == 2:
                    n1, n2 = list(self.infra_painter.selected_infrastructure)
                    connect, itemrow = True, (build, n1, n2, 1.0)
                    for b, j1, j2, *params in self.battlefield["infrastructure"]:
                        if b is None: continue
                        if self.library["infrastructure"][b]["shape"] == "line":
                            if (j1 == n1 and j2 == n2) or (j1 == n2 and j2 == n1):
                                connect = False
                    if connect:
                        self.battlefield["infrastructure"].append(itemrow)
                        print("##> connect", n1, n2)
                        self.draw_content()
                    else: print("##> cannot connect - connection exists?")
                else: print("##> cannot connect - no 2 items selected!")
            else: print("Current mode does not support keys cC")

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
        "version": 0,
        "window-title": "infra-window",
        "window-zoom": 0.0366,
        "window-size": (1800, 820),
        "window-offset": (500, 100),
        "selection-color": (0.8, 0, 0.8),
        "selection-radius2": 2500,
        "move-sensitive": 50,
        "move-editing": 2
    }
    
    from MapExamples import library0
    from MapExamples import battlefield0

    if len(sys.argv) >= 3:
        library_json = sys.argv[1]
        battlefield_json = sys.argv[2]
        print(f"load library: {library_json}")
        with open(library_json, "r") as fd1:
            library0 = json.load(fd1)
        print(f"load battlefield: {battlefield_json}")
        with open(battlefield_json, "r") as fd2:
            battlefield0 = json.load(fd2)        
    InfraWindow(example_config, library0, battlefield0)

    try: Gtk.main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
if __name__ == "__main__": run_example()
        

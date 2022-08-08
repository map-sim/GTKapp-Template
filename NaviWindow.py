#!/usr/bin/python3

from ExampleSave import example_config 
from ExampleSave import example_library
from BaseWindow import BaseWindow
from RawGraph import RawGraph
from math import pi, sqrt, atan2
import os, json, gi, cairo, random

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

class NaviPainter:
    def __init__(self, config, library):
        self.pointed_infra_index = None
        self.selection_color = 0.75, 0.1, 1
        self.library = library
        self.config = config
        
    @staticmethod
    def is_convex_polygon(polygon):
        """
        taken from:
        https://stackoverflow.com/questions/471962/how-do-i-efficiently-
        determine-if-a-polygon-is-convex-non-convex-or-complex
        """
        TWO_PI = 2 * pi

        try:  # needed for any bad points or direction changes
            # Check for too few points
            if len(polygon) < 3: return False
            # Get starting information
            old_x, old_y = polygon[-2]
            new_x, new_y = polygon[-1]
            new_direction = atan2(new_y - old_y, new_x - old_x)
            angle_sum = 0.0
            # Check each point (the side ending there, its angle) and accum. angles
            for ndx, newpoint in enumerate(polygon):
                # Update point coordinates and side directions, check side length
                old_x, old_y, old_direction = new_x, new_y, new_direction
                new_x, new_y = newpoint
                new_direction = atan2(new_y - old_y, new_x - old_x)
                if old_x == new_x and old_y == new_y: return False
                # Calculate & check the normalized direction-change angle
                angle = new_direction - old_direction
                if angle <= -pi: angle += TWO_PI  # make it in half-open interval (-Pi, Pi]
                elif angle > pi: angle -= TWO_PI
                if ndx == 0:  # if first time through loop, initialize orientation
                    if angle == 0.0: return False
                    orientation = 1.0 if angle > 0.0 else -1.0
                else:  # if other time through loop, check orientation is stable
                    if orientation * angle <= 0.0: return False # not both pos. or both neg.
	            # Accumulate the direction-change angle
                angle_sum += angle
            # Check that the total number of full turns is plus-or-minus 1
            return abs(round(angle_sum / TWO_PI)) == 1
        except (ArithmeticError, TypeError, ValueError):
            return False  # any exception means not a proper convex polygon

    def draw_base(self, context, terrain):
        width, height = self.config["window-size"]
        color = self.library["terrains"][terrain]["color"]
        context.set_source_rgba(*color)
        context.rectangle(0, 0, width, height)
        context.fill()

    def draw_polygon(self, context, terrain, params):
        zoom = self.config["window-zoom"]
        xoffset, yoffset = self.config["window-offset"]
        color = self.library["terrains"][terrain]["color"]

        if not NaviPainter.is_convex_polygon(params):
            print("WARNING! Polygon is not convex!")
            color = 1, 0, 0
        context.set_source_rgba(*color)
        
        start_x, start_y = params[-1]
        start_x, start_y = start_x*zoom, start_y*zoom
        start_x, start_y = start_x + xoffset, start_y + yoffset
        context.move_to (start_x, start_y)
        for point in params:    
            stop_x, stop_y = point
            stop_x, stop_y = stop_x*zoom, stop_y*zoom
            stop_x, stop_y = stop_x + xoffset, stop_y + yoffset
            context.line_to (stop_x, stop_y)
        context.fill()
        context.stroke()
        
    def draw_rect(self, context, terrain, params):
        zoom = self.config["window-zoom"]
        xoffset, yoffset = self.config["window-offset"]
        color = self.library["terrains"][terrain]["color"]
        context.set_source_rgba(*color)
        xloc, yloc, wbox, hbox = params
        xloc, yloc = xloc*zoom, yloc*zoom
        xloc, yloc = xloc + xoffset, yloc + yoffset
        context.rectangle(xloc, yloc, wbox*zoom, hbox*zoom)

    def draw_xrect(self, context, terrain, params):
        xloc, yloc, wbox, hbox, multi, xdelta, ydelta = params
        for index in range(multi):
            rparams = xloc + index*xdelta, yloc + index*ydelta, wbox, hbox
            self.draw_rect(context, terrain, rparams)
        context.fill()

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
        if index == self.pointed_infra_index:
            color = self.selection_color
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
        if index == self.pointed_infra_index:
            color = self.selection_color
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
        if index == self.pointed_infra_index:
            color = self.selection_color
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
        if index == self.pointed_infra_index:
            color = self.selection_color
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
        if index == self.pointed_infra_index:
            color = self.selection_color
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

    def draw_bridge_0(self, context, params, index):
        outs = self.get_infrastructure_params("bridge-0", *params)
        color, zoom, xloc, yloc, wbox, hbox = outs
        if index == self.pointed_infra_index:
            color = self.selection_color
        xloc =  xloc - wbox / 2
        yloc =  yloc - hbox / 2
        
        sq = 10*zoom
        context.set_source_rgba(*color)
        context.rectangle(xloc, yloc, wbox, sq)
        context.rectangle(xloc, yloc, sq, hbox)
        context.rectangle(xloc, yloc + hbox - sq, wbox, sq)
        context.rectangle(xloc + wbox - sq, yloc, sq, hbox)
        context.rectangle(xloc, yloc + (hbox - sq) / 2, wbox, sq)
        context.rectangle(xloc, yloc + (hbox - sq) / 4, wbox, sq)
        context.rectangle(xloc, yloc + 3 * (hbox - sq) / 4, wbox, sq)
        context.fill()

    def draw_bridge_1(self, context, params, index):
        outs = self.get_infrastructure_params("bridge-1", *params)
        color, zoom, xloc, yloc, wbox, hbox = outs
        if index == self.pointed_infra_index:
            color = self.selection_color
        xloc =  xloc - wbox / 2
        yloc =  yloc - hbox / 2

        sq = 10*zoom
        context.set_source_rgba(*color)
        context.rectangle(xloc, yloc, wbox, sq)
        context.rectangle(xloc, yloc, sq, hbox)
        context.rectangle(xloc, yloc + hbox - sq, wbox, sq)
        context.rectangle(xloc + wbox - sq, yloc, sq, hbox)
        context.rectangle(xloc + (wbox - sq) / 2, yloc, sq, hbox)
        context.rectangle(xloc + (wbox - sq) / 4, yloc, sq, hbox)
        context.rectangle(xloc + 3 * (wbox - sq) / 4, yloc, sq, hbox)
        context.fill()

    def draw_route_0(self, context, params, name, index):
        outs = self.get_infrastructure_params(name, *params)
        color, zoom, xloc, yloc, wbox, hbox = outs
        if index == self.pointed_infra_index:
            color = self.selection_color
        yloc =  yloc - hbox / 2
        r = wbox/2

        context.set_source_rgba(*color)
        context.set_line_width(5*zoom)
        context.move_to (xloc+wbox/2, yloc)
        context.line_to (xloc+wbox/2, yloc+hbox)
        context.stroke()

        context.move_to (xloc-wbox/2, yloc)
        context.line_to (xloc-wbox/2, yloc+hbox)
        context.stroke()

        context.arc(xloc, yloc, r, 0, 2 * pi)
        context.stroke()
        context.arc(xloc, yloc+hbox, r, 0, 2 * pi)
        context.stroke()

    def draw_route_1(self, context, params, name, index):
        outs = self.get_infrastructure_params(name, *params)
        color, zoom, xloc, yloc, wbox, hbox = outs
        if index == self.pointed_infra_index:
            color = self.selection_color
        xloc =  xloc - wbox / 2
        r = hbox/2

        context.set_source_rgba(*color)
        context.set_line_width(5*zoom)
        context.move_to (xloc,      yloc+hbox/2)
        context.line_to (xloc+wbox, yloc+hbox/2)
        context.stroke()

        context.move_to (xloc,      yloc-hbox/2)
        context.line_to (xloc+wbox, yloc-hbox/2)
        context.stroke()

        context.arc(xloc, yloc, r, 0, 2 * pi)
        context.stroke()
        context.arc(xloc+wbox, yloc, r, 0, 2 * pi)
        context.stroke()

    def draw_route_2(self, context, params, name, index):
        outs = self.get_infrastructure_params(name, *params)
        color, zoom, xloc, yloc, wbox, hbox = outs
        if index == self.pointed_infra_index:
            color = self.selection_color

        r = hbox/2
        d = hbox/(2*sqrt(2))
        b = wbox/sqrt(2)

        context.set_source_rgba(*color)
        context.set_line_width(5*zoom)
         
        context.move_to (xloc - d - b/2, yloc + d - b/2)
        context.line_to (xloc - d + b/2, yloc + d + b/2)
        context.stroke()
        
        context.move_to (xloc + d - b/2, yloc - d - b/2)
        context.line_to (xloc + d + b/2, yloc - d + b/2)
        context.stroke()

        context.arc(xloc - b/2, yloc - b/2, r, 0, 2 * pi)
        context.stroke()
        context.arc(xloc + b/2, yloc + b/2, r, 0, 2 * pi)
        context.stroke()

    def draw_route_3(self, context, params, name, index):
        outs = self.get_infrastructure_params(name, *params)
        color, zoom, xloc, yloc, wbox, hbox = outs
        if index == self.pointed_infra_index:
            color = self.selection_color

        r = hbox/2
        d = hbox/(2*sqrt(2))
        b = wbox/sqrt(2)

        context.set_source_rgba(*color)
        context.set_line_width(5*zoom)
        
        context.move_to (xloc + d + b/2, yloc + d - b/2)
        context.line_to (xloc + d - b/2, yloc + d + b/2)
        context.stroke()
        
        context.move_to (xloc - d - b/2, yloc - d + b/2)
        context.line_to (xloc - d + b/2, yloc - d - b/2)
        context.stroke()

        context.arc(xloc - b/2, yloc + b/2, r, 0, 2 * pi)
        context.stroke()
        context.arc(xloc + b/2, yloc - b/2, r, 0, 2 * pi)
        context.stroke()

    def draw(self, context):
        for shape, ter, *params in self.config["battle-field"]["terrains"]:
            color = self.library["terrains"][ter]["color"]
            if shape == "base": self.draw_base(context, ter)
            elif shape == "rect": self.draw_rect(context, ter, params)
            elif shape == "xrect": self.draw_xrect(context, ter, params)
            elif shape == "polygon": self.draw_polygon(context, ter, params)
            else: raise ValueError(f"Not supported shape: {shape}")
        infra_list = self.config["battle-field"]["infrastructure"]
        for index, (shape, *params) in enumerate(infra_list):
            assert shape in self.library["infrastructure"]

            if shape == "building-0": self.draw_building_0(context, params, index)
            elif shape == "seeport-0": self.draw_seeport_0(context, params, index)
            elif shape == "seeport-1": self.draw_seeport_1(context, params, index)
            elif shape == "airport-0": self.draw_airport_0(context, params, index)
            elif shape == "fortress-0": self.draw_fortress_0(context, params, index)
            elif shape == "bridge-0": self.draw_bridge_0(context, params, index)
            elif shape == "bridge-1": self.draw_bridge_1(context, params, index)
            elif shape == "route-0": self.draw_route_0(context, params, shape, index)
            elif shape == "route-1": self.draw_route_1(context, params, shape, index)
            elif shape == "route-2": self.draw_route_2(context, params, shape, index)
            elif shape == "route-3": self.draw_route_3(context, params, shape, index)
            else: raise ValueError(f"Not supported shape: {shape}")

            xloc, yloc = params[0], params[1]
            xoffset, yoffset = self.config["window-offset"]
            zoom = self.config["window-zoom"]
            xloc, yloc = xloc*zoom, yloc*zoom
            xloc, yloc = xloc + xoffset, yloc + yoffset
            
class NaviWindow(BaseWindow):    
    def __init__(self, config=None, library=None):
        if config is not None: self.config = config
        else: self.config = example_config
        if library is not None: self.library = library
        else: self.library = example_library
        self.painter = NaviPainter(self.config, self.library)
        self.graph = RawGraph(self.config, self.library)

        title = self.config["window-title"]
        width, height = self.config["window-size"]
        BaseWindow.__init__(self, title, width, height)

    def assert_config_and_libraty(self):
        # self.library
        # self.config
        pass
    
    def init_window(self):
        self.surface = None
        self.draw_content()
        self.show_all()

    def on_press(self, widget, event):
        key_name = Gdk.keyval_name(event.keyval)
        if key_name == "Return":
            print("##> move center & redraw")
            self.config["window-offset"] = 0, 0
            self.draw_content()
        elif key_name == "Up":
            print("##> move up & redraw")
            hop = self.config["move-sensitive"]
            xoffset, yoffset = self.config["window-offset"]
            self.config["window-offset"] = xoffset, yoffset + hop
            self.draw_content()
        elif key_name == "Down":
            print("##> move down & redraw")
            hop = self.config["move-sensitive"]
            xoffset, yoffset = self.config["window-offset"]
            self.config["window-offset"] = xoffset, yoffset - hop
            self.draw_content()
        elif key_name == "Left":
            print("##> move left & redraw")
            hop = self.config["move-sensitive"]
            xoffset, yoffset = self.config["window-offset"]
            self.config["window-offset"] = xoffset + hop, yoffset
            self.draw_content()
        elif key_name == "Right":
            print("##> move right & redraw")
            hop = self.config["move-sensitive"]
            xoffset, yoffset = self.config["window-offset"]
            self.config["window-offset"] = xoffset - hop, yoffset
            self.draw_content()
        elif key_name in ("minus", "KP_Subtract"):
            print("##> zoom out & redraw")
            self.config["window-zoom"] *= 0.75
            self.draw_content()
        elif key_name in ("plus", "KP_Add"):
            print("##> zoom in & redraw")
            self.config["window-zoom"] *= 1.25
            self.draw_content()
        elif key_name == "Escape":
            print("##> deselect")
            self.painter.pointed_infra_index = None            
            self.draw_content()
        elif key_name in ("s", "S"):
            print("##> save")
            self.save_battlefield("save.navi")
        else:
            print("not supported key:")
            print("\tkey name:", Gdk.keyval_name(event.keyval))
            print("\tkey value:", event.keyval)
        return True

    def save_battlefield(self, directory_name):
        if not os.path.exists(directory_name):
            os.mkdir(directory_name)

        library_string = json.dumps(self.library)
        library_path = os.path.join(directory_name, "library.json")
        with open(library_path, "w") as fd:
            json.dump(library_string, fd)
            
        config_string = json.dumps(self.config)
        config_path = os.path.join(directory_name, "config.json")
        with open(config_path, "w") as fd:
            json.dump(config_string, fd)

    @BaseWindow.double_buffering
    def draw_content(self, context):
        self.painter.draw(context)
        context.stroke()

    def on_scroll(self, widget, event):
        xoffset, yoffset = self.config["window-offset"]
        width, height = self.config["window-size"]
        zoom = self.config["window-zoom"]
        ox = (event.x - xoffset) / zoom
        oy = (event.y - yoffset) / zoom
        
        if event.direction == Gdk.ScrollDirection.DOWN:
            self.config["window-zoom"] *= 0.75
        elif event.direction == Gdk.ScrollDirection.UP:
            self.config["window-zoom"] *= 1.25

        zoom2 = self.config["window-zoom"]
        xoffset = event.x - ox * zoom2
        yoffset = event.y - oy * zoom2
        self.config["window-offset"] = xoffset, yoffset
        self.draw_content()
        return True

    def on_click(self, widget, event):
        xoffset, yoffset = self.config["window-offset"]
        width, height = self.config["window-size"]
        zoom = self.config["window-zoom"]
        ox = (int(event.x) - xoffset) / zoom
        oy = (int(event.y) - yoffset) / zoom

        if event.button == 1:
            print(f"({round(ox, 2)}, {round(oy, 2)}),")
        elif event.button == 3:
            print(f"\n-->> {round(ox, 2)}  {round(oy, 2)} --")
            terr = self.graph.check_terrain(ox, oy)
            infra, distance, index = self.graph.check_infra(ox, oy)
            self.painter.pointed_infra_index = index

            print("terrain:", terr)
            print("infra:", infra, distance)
            self.draw_content()
        return True

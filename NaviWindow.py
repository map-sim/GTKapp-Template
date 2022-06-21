#!/usr/bin/python3

from ExampleSave import example_config 
from ExampleSave import example_library
from BaseWindow import BaseWindow
import gi, cairo, random

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk


class NaviPainter:
    def __init__(self, config, library):
        self.library = library
        self.config = config

    def draw_base(self, context, terrain):
        width, height = self.config["window-size"]
        color = self.library["terrains"][terrain]["color"]
        context.set_source_rgba(*color)
        context.rectangle(0, 0, width, height)

    def draw_polygon(self, context, terrain, params):
        zoom = self.config["window-zoom"]
        xoffset, yoffset = self.config["window-offset"]
        color = self.library["terrains"][terrain]["color"]
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

    def get_infrastructure_params(self, name, xloc, yloc, *args):
        color = self.library["infrastructure"][name]["color"]
        wbox, hbox = self.library["infrastructure"][name]["size"]
        xoffset, yoffset = self.config["window-offset"]
        zoom = self.config["window-zoom"]
        xloc, yloc = xloc*zoom, yloc*zoom
        xloc, yloc = xloc + xoffset, yloc + yoffset
        wbox, hbox = wbox*zoom, hbox*zoom
        return color, zoom, xloc, yloc, wbox, hbox
    
    def draw_building_0(self, context, params):
        outs = self.get_infrastructure_params("building-0", *params)
        color, zoom, xloc, yloc, wbox, hbox = outs

        context.set_source_rgba(*color)
        context.rectangle(xloc, yloc, wbox, 5*zoom)
        context.rectangle(xloc, yloc+hbox-5*zoom, wbox, 5*zoom)
        context.rectangle(xloc, yloc, 5*zoom, hbox)
        context.rectangle(xloc+wbox-5*zoom, yloc, 5*zoom, hbox)
        context.rectangle(xloc+10*zoom, yloc+10*zoom, 25*zoom, 25*zoom)
        context.rectangle(xloc+50*zoom, yloc+20*zoom, 20*zoom, 20*zoom)
        context.rectangle(xloc+40*zoom, yloc+50*zoom, 20*zoom, 20*zoom)
        context.rectangle(xloc+10*zoom, yloc+60*zoom, 25*zoom, 25*zoom)
        context.rectangle(xloc+65*zoom, yloc+70*zoom, 20*zoom, 20*zoom)
        
    def draw_fortress_0(self, context, params):
        outs = self.get_infrastructure_params("fortress-0", *params)
        color, zoom, xloc, yloc, wbox, hbox = outs
        
        sq = 10*zoom
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

    def draw_bridge_0(self, context, params):
        outs = self.get_infrastructure_params("bridge-0", *params)
        color, zoom, xloc, yloc, wbox, hbox = outs
        
        sq = 10*zoom
        context.rectangle(xloc, yloc, wbox, sq)
        context.rectangle(xloc, yloc, sq, hbox)
        context.rectangle(xloc, yloc + hbox - sq, wbox, sq)
        context.rectangle(xloc + wbox - sq, yloc, sq, hbox)
        context.rectangle(xloc, yloc + (hbox - sq) / 2, wbox, sq)
        context.rectangle(xloc, yloc + (hbox - sq) / 4, wbox, sq)
        context.rectangle(xloc, yloc + 3 * (hbox - sq) / 4, wbox, sq)

    def draw_bridge_1(self, context, params):
        outs = self.get_infrastructure_params("bridge-1", *params)
        color, zoom, xloc, yloc, wbox, hbox = outs
        
        sq = 10*zoom
        context.rectangle(xloc, yloc, wbox, sq)
        context.rectangle(xloc, yloc, sq, hbox)
        context.rectangle(xloc, yloc + hbox - sq, wbox, sq)
        context.rectangle(xloc + wbox - sq, yloc, sq, hbox)
        context.rectangle(xloc + (wbox - sq) / 2, yloc, sq, hbox)
        context.rectangle(xloc + (wbox - sq) / 4, yloc, sq, hbox)
        context.rectangle(xloc + 3 * (wbox - sq) / 4, yloc, sq, hbox)

    def draw_route_01(self, context, params, name):
        outs = self.get_infrastructure_params(name, *params)
        color, zoom, xloc, yloc, wbox, hbox = outs

        sq = 5*zoom
        context.rectangle(xloc, yloc, wbox, sq)
        context.rectangle(xloc, yloc, sq, hbox)
        context.rectangle(xloc, yloc + hbox - sq, wbox, sq)
        context.rectangle(xloc + wbox - sq, yloc, sq, hbox)

    def draw(self, context):
        for shape, ter, *params in self.config["battle-field"]["terrains"]:
            color = self.library["terrains"][ter]["color"]
            if shape == "base": self.draw_base(context, ter)
            elif shape == "rect": self.draw_rect(context, ter, params)
            elif shape == "xrect": self.draw_xrect(context, ter, params)
            elif shape == "polygon": self.draw_polygon(context, ter, params)
            else: raise ValueError(f"Not supported shape: {shape}")
            context.fill()
        for shape, *params in self.config["battle-field"]["infrastructure"]:
            if shape == "building-0": self.draw_building_0(context, params)
            elif shape == "fortress-0": self.draw_fortress_0(context, params)
            elif shape == "bridge-0": self.draw_bridge_0(context, params)
            elif shape == "bridge-1": self.draw_bridge_1(context, params)
            elif shape == "route-0": self.draw_route_01(context, params, shape)
            elif shape == "route-1": self.draw_route_01(context, params, shape)
            else: raise ValueError(f"Not supported shape: {shape}")
            context.fill()
            
class NaviWindow(BaseWindow):    
    def __init__(self, config=None, library=None):
        if config is not None: self.config = config
        else: self.config = example_config
        if library is not None: self.library = library
        else: self.library = example_library
        self.painter = NaviPainter(self.config, self.library)

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
        else:
            print("not supported key:")
            print("\tkey name:", Gdk.keyval_name(event.keyval))
            print("\tkey value:", event.keyval)
        return True

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
        if event.button == 1:
            xoffset, yoffset = self.config["window-offset"]
            width, height = self.config["window-size"]
            zoom = self.config["window-zoom"]
            ox = (int(event.x) - xoffset) / zoom
            oy = (int(event.y) - yoffset) / zoom
            print(round(ox, 2), round(oy, 2))
        return True

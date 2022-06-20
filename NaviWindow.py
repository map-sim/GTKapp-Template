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
        context.fill()

    def draw_rect(self, context, terrain, params):
        zoom = self.config["window-zoom"]
        xoffset, yoffset = self.config["window-offset"]
        color = self.library["terrains"][terrain]["color"]
        context.set_source_rgba(*color)
        xloc, yloc, wbox, hbox = params
        xloc, yloc = xloc*zoom, yloc*zoom
        xloc, yloc = xloc + xoffset, yloc + yoffset
        context.rectangle(xloc, yloc, wbox*zoom, hbox*zoom)
        context.fill()

    def draw_xrect(self, context, terrain, params):
        xloc, yloc, wbox, hbox, multi, xdelta, ydelta = params
        for index in range(multi):
            rparams = xloc + index*xdelta, yloc + index*ydelta, wbox, hbox
            self.draw_rect(context, terrain, rparams)

    def draw_building_0(self, context, params):
        color = self.library["infrastructure"]["building-0"]["color"]
        context.set_source_rgba(*color)
        wbox, hbox = self.library["infrastructure"]["building-0"]["size"]
        xoffset, yoffset = self.config["window-offset"]
        zoom = self.config["window-zoom"]
        xloc, yloc = params
        xloc, yloc = xloc*zoom, yloc*zoom
        xloc, yloc = xloc + xoffset, yloc + yoffset
        context.rectangle(xloc, yloc, wbox*zoom, 5*zoom)
        context.rectangle(xloc, yloc+(hbox-5)*zoom, wbox*zoom, 5*zoom)
        context.rectangle(xloc, yloc, 5*zoom, hbox*zoom)
        context.rectangle(xloc+(wbox-5)*zoom, yloc, 5*zoom, hbox*zoom)

        context.rectangle(xloc+10*zoom, yloc+10*zoom, 25*zoom, 25*zoom)
        context.rectangle(xloc+50*zoom, yloc+20*zoom, 20*zoom, 20*zoom)
        context.rectangle(xloc+40*zoom, yloc+50*zoom, 20*zoom, 20*zoom)
        context.rectangle(xloc+10*zoom, yloc+60*zoom, 25*zoom, 25*zoom)
        context.rectangle(xloc+65*zoom, yloc+70*zoom, 20*zoom, 20*zoom)

        context.fill()
        
    def draw(self, context):
        for shape, ter, *params in self.config["battle-field"]["terrains"]:
            color = self.library["terrains"][ter]["color"]
            if shape == "base": self.draw_base(context, ter)
            elif shape == "rect": self.draw_rect(context, ter, params)
            elif shape == "xrect": self.draw_xrect(context, ter, params)
            elif shape == "ribb": self.draw_ribb(context, ter, params)
            else: raise ValueError(f"Not supported shape: {shape}")
        for shape, *params in self.config["battle-field"]["infrastructure"]:
            if shape == "building-0": self.draw_building_0(context, params)
            else: raise ValueError(f"Not supported shape: {shape}")

            
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

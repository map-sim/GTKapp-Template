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

    def draw(self, context):
        for shape, ter, *params in self.config["battle-field"]["terrains"]:
            color = self.library["terrains"][ter]["color"]
            if shape == "base": self.draw_base(context, ter)
            elif shape == "rect": self.draw_rect(context, ter, params)
            elif shape == "ribb": self.draw_ribb(context, ter, params)
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
        elif key_name == "minus":
            print("##> zoom out & redraw")
            self.config["window-zoom"] *= 0.75
            self.draw_content()
        elif key_name == "plus":
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

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

    def draw(self, context):
        for fig, ter, *params in self.config["battle-field"]["terrains"]:
            print(fig, ter, params)

        
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
        if event.keyval == 65293:
            self.draw_content()
            print("RETURN", self.background)
        else:
            print("key name:", Gdk.keyval_name(event.keyval))
            print("key value:", event.keyval)
        return True

    @BaseWindow.double_buffering
    def draw_content(self, context):
        # context.set_source_rgba(*self.background)
        # context.rectangle (0, 0, self.width, self.height)
        # context.fill()

        self.painter.draw(context)
        context.stroke()

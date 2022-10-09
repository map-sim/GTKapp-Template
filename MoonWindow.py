#!/usr/bin/python3

import os, json, gi, cairo, random

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

from BaseWindow import BaseWindow
from MoonSystem import MoonSystem
from MoonPainters import MoonPainter
from MoonPainters import MoonDistPainter

from MoonExamples import example_library
from MoonExamples import example_state
from MoonExamples import example_setup

        
class MoonWindow(BaseWindow):    
    def __init__(self, setup=None, state=None, library=None):
        if library is not None: self.library = librar
        else: self.library = example_library
        if state is not None: self.state = state
        else: self.state = example_state
        if setup is not None: self.setup = setup
        else: self.setup = example_setup

        self.selected_node = None
        
        title = self.setup["window-title"]
        width, height = self.setup["window-size"]
        self.system = MoonSystem(self.state, self.library)
        self.painter = MoonPainter(self.setup, self.state)
        self.painter_dist = MoonDistPainter(self.setup, self.system)
        BaseWindow.__init__(self, title, width, height)

    @BaseWindow.double_buffering
    def draw_content(self, context):
        self.painter.draw(context, self.selected_node)
    @BaseWindow.double_buffering
    def draw_distribution(self, context):
        self.painter_dist.draw(context, *self.draw_distribution_args)

    def on_scroll(self, widget, event):
        xoffset, yoffset = self.setup["window-offset"]
        width, height = self.setup["window-size"]
        zoom = self.setup["window-zoom"]
        ox = (event.x - xoffset) / zoom
        oy = (event.y - yoffset) / zoom
        
        if event.direction == Gdk.ScrollDirection.DOWN:
            self.setup["window-zoom"] *= 0.75
        elif event.direction == Gdk.ScrollDirection.UP:
            self.setup["window-zoom"] *= 1.25

        zoom2 = self.setup["window-zoom"]
        xoffset = event.x - ox * zoom2
        yoffset = event.y - oy * zoom2
        self.setup["window-offset"] = xoffset, yoffset
        self.draw_content()
        return True

    def on_click(self, widget, event):
        xoffset, yoffset = self.setup["window-offset"]
        width, height = self.setup["window-size"]
        zoom = self.setup["window-zoom"]
        ox = (int(event.x) - xoffset) / zoom
        oy = (int(event.y) - yoffset) / zoom
        print("=====================")
        print(f"({round(ox, 2)}, {round(oy, 2)}):")

        sources = self.system.check_sources(ox, oy)
        print("Sources", sources, "\n")

        node, r2 = self.system.find_element(ox, oy)
        if node is not None and r2 < self.setup["max-selection-range"]:
            print("selection --> ", node)
            print("connections --> ", len(node.ios))
            
            self.selected_node = node
            self.draw_content()
        elif self.selected_node is not None:            
            self.selected_node = None
            self.draw_content()

        return True

    def on_press(self, widget, event):
        key_name = Gdk.keyval_name(event.keyval)
        if key_name == "Home":
            print("##> move center & redraw")
            self.setup["window-offset"] = 0, 0
            self.setup["window-zoom"] = 30.0
            self.draw_content()
        elif key_name == "Up":
            print("##> move up & redraw")
            hop = self.setup["move-sensitive"]
            xoffset, yoffset = self.setup["window-offset"]
            self.setup["window-offset"] = xoffset, yoffset + hop
            self.draw_content()
        elif key_name == "Down":
            print("##> move down & redraw")
            hop = self.setup["move-sensitive"]
            xoffset, yoffset = self.setup["window-offset"]
            self.setup["window-offset"] = xoffset, yoffset - hop
            self.draw_content()
        elif key_name == "Left":
            print("##> move left & redraw")
            hop = self.setup["move-sensitive"]
            xoffset, yoffset = self.setup["window-offset"]
            self.setup["window-offset"] = xoffset + hop, yoffset
            self.draw_content()
        elif key_name == "Right":
            print("##> move right & redraw")
            hop = self.setup["move-sensitive"]
            xoffset, yoffset = self.setup["window-offset"]
            self.setup["window-offset"] = xoffset - hop, yoffset
            self.draw_content()
        elif key_name in ("minus", "KP_Subtract"):
            print("##> zoom out & redraw")
            self.setup["window-zoom"] *= 0.75
            self.draw_content()
        elif key_name in ("plus", "KP_Add"):
            print("##> zoom in & redraw")
            self.setup["window-zoom"] *= 1.25
            self.draw_content()
        elif key_name == "Escape":
            print("##> deselect")
            self.selected_node = None
            self.draw_content()
        elif key_name == "space":
            self.system.run(10.0)
        elif key_name == "X":
            print("##> X & redraw")
            self.draw_distribution_args = "source", "X"
            self.draw_distribution()
        else:
            print("not supported key:")
            print("\tkey name:", Gdk.keyval_name(event.keyval))
            print("\tkey value:", event.keyval)
        return True


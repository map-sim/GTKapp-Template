#!/usr/bin/python3

from math import pi, sqrt, atan2
import os, json, gi, cairo, random
from BaseWindow import BaseWindow

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

class NaviPainter:
    def __init__(self, config):
        self.config = config

    def draw_base(self, context):
        width, height = self.config["window-size"]
        color = self.config["background-color"]
        context.set_source_rgba(*color)
        context.rectangle(0, 0, width, height)
        context.fill()

    def draw_rect(self, context, params):
        zoom = self.config["window-zoom"]
        xoffset, yoffset = self.config["window-offset"]
        color = self.config["foreground-color"]
        context.set_source_rgba(*color)
        xloc, yloc, wbox, hbox = params
        xloc, yloc = xloc*zoom, yloc*zoom
        xloc, yloc = xloc + xoffset, yloc + yoffset
        context.rectangle(xloc, yloc, wbox*zoom, hbox*zoom)
        context.fill()

    def draw(self, context):
        self.draw_base(context)
        self.draw_rect(context, self.config["primary-rect"])
        self.draw_rect(context, self.config["secondary-rect"])
        
class NaviWindow(BaseWindow):
    def __init__(self, config=None):
        self.painter = NaviPainter(config)
        self.config = config

        title = config["window-title"]
        width, height = config["window-size"]
        BaseWindow.__init__(self, title, width, height)

    def init_window(self):
        self.surface = None
        self.draw_content()
        self.show_all()

    def on_press(self, widget, event):
        key_name = Gdk.keyval_name(event.keyval)
        if key_name == "Return":
            print("##> move center & redraw")
            self.config["window-offset"] = 0, 0
            self.config["window-zoom"] = 1.0
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
        xoffset, yoffset = self.config["window-offset"]
        width, height = self.config["window-size"]
        zoom = self.config["window-zoom"]
        ox = (int(event.x) - xoffset) / zoom
        oy = (int(event.y) - yoffset) / zoom

        print(f"({round(ox, 2)}, {round(oy, 2)}),")
        return True

def run_example():
    example_config = {
        "window-title": "navi-window",
        "window-size": (600, 400),
        "window-offset": (100, 50),
        "window-zoom": 1.333,
        "move-sensitive": 50,
        
        "primary-rect": (0, 0, 200, 100),
        "secondary-rect": (200, 100, 100, 50),
        "foreground-color": (1, 0, 0),
        "background-color": (1, 1, 1)
    }
    
    NaviWindow(example_config)
    try: Gtk.main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
if __name__ == "__main__": run_example()
        

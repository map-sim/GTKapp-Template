#!/usr/bin/python3

import gi, cairo, random
from BaseWindow import BaseWindow

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk


class ColorWindow(BaseWindow):
    def __init__(self, title, width, height):
        BaseWindow.__init__(self, title, width, height)

    @staticmethod
    def rand_rgb():
        r = random.uniform(0, 1)
        g = random.uniform(0, 1)
        b = random.uniform(0, 1)
        return r, g, b

    def init_window(self):
        self.background = ColorWindow.rand_rgb()
        self.surface = None
        self.show_all()

    def on_press(self, widget, event):
        if event.keyval == 65293:
            self.background = ColorWindow.rand_rgb()
            self.draw_content()
            print("RETURN", self.background)
        else:
            print("key name:", Gdk.keyval_name(event.keyval))
            print("key value:", event.keyval)
        return True

    @BaseWindow.double_buffering
    def draw_content(self, context=None):
        context.set_source_rgba(*self.background)
        context.rectangle (0, 0, self.width, self.height)
        context.fill()
        context.stroke()

def run_example():
    ColorWindow("color-window", 600, 400)
    try: Gtk.main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
if __name__ == "__main__": run_example()

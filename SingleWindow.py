#!/usr/bin/python3

import gi, cairo, random

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

class SingleWindow(Gtk.Window):    
    def __init__(self, title, width, height):
        assert int(height) > 0, "height <= 0"
        assert int(width) > 0, "width <= 0"

        self.width = int(width)
        self.height = int(height)
        self.background = 0, 0, 0

        Gtk.Window.__init__(self, title=str(title))
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.connect("key-press-event",self.on_key_press)

        fix = Gtk.Fixed()
        self.add(fix)

        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_size_request(width, height)
        fix.put(self.drawing_area, 0, 0)

        self.surface = None
        self.drawing_area.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.drawing_area.connect("button-press-event",self.on_button_click)
        self.drawing_area.connect("configure-event", self.on_configure)   
        self.drawing_area.connect("draw", self.on_draw)

        self.show_all()
        self.draw_content()

    def on_key_press(self, widget, event):
        ### add implementation for keyboard input
        ### e.g.
        if event.keyval == 65293:
            r = random.uniform(0, 1)
            g = random.uniform(0, 1)
            b = random.uniform(0, 1)
            self.background = r, g, b
            self.draw_content()
            print("RETURN", r, g, b)
        else:
            print("key name:", Gdk.keyval_name(event.keyval))
            print("key value:", event.keyval)

    def on_button_click(self, widget, event):        
        ### add implementation for mouse input
        ### e.g.
        print("click", event.x, event.y)

    def on_configure(self, area, event, data=None):
        self.draw_content()
        return False

    def on_draw(self, area, context):
        context.set_source_surface(self.surface, 0.0, 0.0)            
        context.paint()

    def draw_content(self):
        if self.surface is not None:
            self.surface.finish()
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)        
        context = cairo.Context(self.surface)

        ### draw here using context
        ### e.g.

        context.set_source_rgba(*self.background)
        context.rectangle (0, 0, self.width, self.height)
        context.fill()
        context.stroke()

        self.surface.flush()
        self.on_draw(self.drawing_area, context)
        self.drawing_area.queue_draw()

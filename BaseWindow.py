#!/usr/bin/python3

import gi, cairo

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

class BaseWindow(Gtk.Window):    
    def __init__(self, title, width, height):
        assert int(height) > 0, "height <= 0"
        assert int(width) > 0, "width <= 0"

        self.width = int(width)
        self.height = int(height)

        Gtk.Window.__init__(self, title=str(title))
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.connect("key-press-event",self.on_press)

        fix = Gtk.Fixed()
        self.add(fix)

        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_size_request(width, height)
        fix.put(self.drawing_area, 0, 0)

        event_mask = Gdk.EventMask.BUTTON_PRESS_MASK
        event_mask |= Gdk.EventMask.SCROLL_MASK
        self.drawing_area.set_events(event_mask)

        self.drawing_area.connect("scroll-event",self.on_scroll)
        self.drawing_area.connect("button-press-event",self.on_click)
        self.drawing_area.connect("configure-event", self.on_configure)   
        self.drawing_area.connect("draw", self.on_draw)
        self.init_window()

    def on_configure(self, area, event, data=None):
        self.draw_content()
        return True

    def on_draw(self, area, context):
        context.set_source_surface(self.surface, 0.0, 0.0)            
        context.paint()
        return True

    def init_window(self):
        ### add implementation for window init
        ### e.g.

        self.surface = None
        self.show_all()

    def double_buffering(func):
        def inner(self):
            if self.surface is not None:
                self.surface.finish()
            self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)        
            context = cairo.Context(self.surface)
        
            func(self, context)    

            self.surface.flush()
            self.on_draw(self.drawing_area, context)
            self.drawing_area.queue_draw()
        return inner

    @double_buffering
    def draw_content(self, context=None):
        ### add implementation for drawing using context
        ### e.g.

        context.set_source_rgba(0.2, 0.5, 0.8)
        context.rectangle (0, 0, self.width, self.height)
        context.fill()
        context.stroke()

    double_buffering = staticmethod(double_buffering)

    def on_press(self, widget, event):
        ### add implementation for keyboard input
        ### e.g.

        print("key name:", Gdk.keyval_name(event.keyval))
        print("key value:", event.keyval)
        return True

    def on_scroll(self, widget, event):        
        ### add implementation for mouse scroll input
        ### e.g.

        if event.direction == Gdk.ScrollDirection.DOWN: direction = -1
        elif event.direction == Gdk.ScrollDirection.UP: direction = 1
        else: direction = 0
        print("scroll", event.x, event.y, direction)
        return True

    def on_click(self, widget, event):
        ### add implementation for mouse click input
        ### e.g.

        print("click", event.button, event.x, event.y)
        return True


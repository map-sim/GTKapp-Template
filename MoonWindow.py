#!/usr/bin/python3

from math import pi, sqrt, atan2
import os, json, gi, cairo, random


from BaseWindow import BaseWindow
from MoonSystem import MoonSystem

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk


example_library = {
    "infra": {
        "pipeX": {
            "cost": 0.5,
            "cover": 0.55,
            "radius": 0.0,
            "capacity": 0.0,
            "bandwidth": 0.75,
            "switch": 3,
            "type": "pipe",
            "good": "X"
        },
        "pipeY": {
            "cost": 0.75,
            "cover": 0.55,
            "radius": 0.0,
            "capacity": 0.0,
            "bandwidth": 0.75,
            "switch": 3,
            "type": "pipe",
            "good": "Y"
        },
        "ndX": {
            "io": 2,
            "cost": 1.0,
            "radius": 2.0,
            "capacity": 0.0,
            "bandwidth": 0.75,
            "type": "node",
            "good": "X"
        },
        "ndY": {
            "io": 2,
            "cost": 1.0,
            "radius": 2.0,
            "capacity": 0.0,
            "bandwidth": 0.75,
            "type": "node",
            "good": "Y"
        },
        "in0": {
            "io": 1,
            "cost": 3.5,
            "cover": 0.3,
            "radius": 5.0,
            "capacity": 7.5,
            "bandwidth": 0.5,
            "type": "inner"
        },
        "out0": {
            "io": 2,
            "cost": 3.5,
            "cover": 0.7,
            "radius": 5.0,
            "capacity": 1.0,
            "bandwidth": 0.5,
            "type": "outer",
            "goods": ["Y"]
        },
        "bar0": {
            "io": 1,
            "cost": 12.5,
            "cover": 0.6,
            "radius": 7.0,
            "capacity": 3.5,
            "bandwidth": 1.6,
            "type": "barrier",
            "goods": ["Y"]
        },
        "acc0": {
            "io": 2,
            "cost": 4.0,
            "cover": 0.9,
            "radius": 2.5,
            "capacity": 5.0,
            "bandwidth": 1.8,
            "type": "accelerator"
        },
        "mix0": {
            "io": 3,
            "cost": 4.5,
            "cover": 0.9,
            "radius": 5.0,
            "capacity": 5.0,
            "bandwidth": 0.8,
            "type": "mixer"
        },
        "str0": {
            "io": 4,
            "cost": 3.0,
            "cover": 0.95,
            "radius": 5.0,
            "capacity": 15.0,
            "bandwidth": 1.2,
            "type": "store"            
        },
        "src0": {
            "io": 1,
            "cost": 1.5,
            "cover": 0.5,
            "radius": 3.0,
            "capacity": 3.5,
            "bandwidth": 0.4,
            "type": "source",
            "goods": ["X"]
        },
        "ex0": {
            "io": 0,
            "cost": 1.5,
            "cover": 0.0,
            "radius": 2.0,
            "capacity": 0.0,
            "bandwidth": 0.0,
            "type": "explorer"
        },
        "sn0": {
            "io": 0,
            "cost": 1.5,
            "cover": 0.0,
            "radius": 2.0,
            "capacity": 0.0,
            "bandwidth": 0.0,
            "switch": 3,
            "type": "sensor"
        }
    },
    "goods": {
        "X": {
            "ground-source": True,
            "disintegration": 0.05,
            "sensitivity": 0.1,
            "stickiness": 2.4,
            "score": 0.02,
            "process": {}
        },
        "Y": {
            "ground-source": False,
            "disintegration": 0.01,
            "sensitivity": 0.033,
            "stickiness": 1.2,
            "score": 0.666,
            "process": {"X": 4.88}
        }
    },
    "radiation": {
        "method": "rand-cones",
        "max-amplitude": 2.0,
        "min-amplitude": 0.1,
        "max-radius": 50,
        "min-radius": 1,
        "frequency": 2
    }
}

example_state = {
    "source": {
        "X": {
            "method": "additive-cones",
            "max-amplitude": 2.2,
            "points": [
                # x, y, amplitude, radius
                (0, 1, 3.0, 20.0),
                (7, 2, 1.5, 5.0),
                (3, -4, 1.2, 5.0)
            ]
        }
    },
    "connections": [
        ("pipeX", ("src0", -8, 0), ("str0", -8, 6), {"switch": 1}),
        ("pipeX", ("src0", -13, 2), ("str0", -8, 6), {"switch": 1}),
        ("pipeX", ("str0", -8, 6), ("acc0", -3.5, 9), {"switch": 1}),
        ("pipeX", ("acc0", -3.5, 9), ("str0", 1, 7), {"switch": 1}),
        ("pipeX", ("src0", 1, 1), ("str0", 1, 7), {"switch": 1}),
        ("pipeX", ("str0", 1, 7), ("ndX", 3, 12), {"switch": 1}),
        ("pipeX", ("ndX", 3, 12), ("mix0", 9, 15), {"switch": 1}),
        ("pipeY", ("mix0", 9, 15), ("str0", 10, 10), {"switch": 1}),
        ("pipeY", ("str0", 10, 10), ("bar0", 9, 2.5), {"switch": 1}),
        ("pipeY", ("str0", 10, 10), ("out0", 14.5, 7.5), {"switch": 1}),
        ("pipeY", ("mix0", 9, 15), ("in0", 13, 19), {"switch": 1}),
        ("pipeX", ("str0", -8, 6), ("str0", -10, 11), {"switch": 1})
    ],    
    "elements": [
        (("ex0", 3, -2), {}),
        (("ex0", -3, -2), {}),
        (("ex0", -9, -3), {}),
        (("ex0", -15, -1), {}),
        (("sn0", -12, -1), {}),
        (("sn0", -3.5, 0), {}),

        (("src0", -8, 0), {"X": 0.0, "Y": 0.0}),
        (("src0", -13, 2), {"X": 0.0, "Y": 0.0}),
        (("str0", -8, 6), {"X": 0.0, "Y": 0.0}),
        (("acc0", -3.5, 9), {"X": 0.0, "Y": 0.0}),
        (("src0", 1, 1), {"X": 0.0, "Y": 0.0}),
        (("str0", 1, 7), {"X": 0.0, "Y": 0.0}),

        (("ndX", 3, 12), {}),
        (("ndY", 3, 18), {}),
        (("mix0", 9, 15), {"X": 0.0, "Y": 0.0}),
        (("str0", 10, 10), {"X": 0.0, "Y": 0.0}),
        (("bar0", 9, 2.5), {"X": 0.0, "Y": 0.0}),
        (("in0", 13, 19), {"X": 0.0, "Y": 0.0}),
        (("out0", 14.5, 7.5), {"X": 0.0, "Y": 0.0}),
        (("str0", -10, 11), {"X": 0.0, "Y": 0.0}),
        (("sn0", 14, 13), {}),
        (("sn0", 6, 8), {}),
    ]
}

example_setup = {
    "window-title": "demo moon",
    "window-size": (1600, 1000),
    "window-offset": (800, 300),
    "window-zoom": 21.5,
    "move-sensitive": 50,
    "color-selection": (1.0, 0.0, 0.0),
    "color-background": (0.9, 0.95, 0.95),
    "color-pipe": (0.0, 0.66, 0.5),
    "color-base": (1.0, 1.0, 0.0),
    "color-node": (0.4, 0, 0.4),
    "max-selection-range": 25
}


class MoonPainter:
    def __init__(self, setup, state):
        self.setup = setup
        self.state = state

    def calc_render_params(self, xloc, yloc, wbox=0, hbox=0):
        xoffset, yoffset = self.setup["window-offset"]
        zoom = self.setup["window-zoom"]

        xloc, yloc = xloc * zoom, yloc * zoom
        xloc, yloc = xloc + xoffset, yloc + yoffset
        wbox, hbox = wbox * zoom, hbox * zoom
        return xloc, yloc, wbox, hbox

    def draw_polygon(self, context, color, points):
        context.set_source_rgba(*color)        
        start_x, start_y = points[-1]
        context.move_to (start_x, start_y)
        for point in points:    
            stop_x, stop_y = point
            context.line_to (stop_x, stop_y)
        context.fill()
        context.stroke()

    def draw_pipe(self, context, node1, node2, state, mark):
        (_, xi, yi), (_, xe, ye) =  node1, node2
        xi, yi, width, _ = self.calc_render_params(xi, yi, 0.3)
        xe, ye, _, _ = self.calc_render_params(xe, ye)

        if mark: context.set_source_rgba(*self.setup["color-selection"])
        else: context.set_source_rgba(*self.setup["color-pipe"])

        context.set_line_width(width)
        context.move_to(xi, yi)
        context.line_to(xe, ye) 
        context.stroke()
        
    def draw_ex0(self, context, xloc, yloc, state, mark):
        xloc, yloc, wbox, hbox = self.calc_render_params(xloc, yloc, 1.2, 0.25)
        xi = xloc - hbox/2
        xe = xloc + hbox/2
        yi = yloc + hbox/2
        ye = yloc - hbox/2
        if mark: context.set_source_rgba(*self.setup["color-selection"])
        else: context.set_source_rgba(*self.setup["color-node"])
        context.set_line_width(wbox)
        context.move_to(xi, yloc)
        context.line_to(xe, yloc) 
        context.stroke()
        context.move_to(xloc, yi)
        context.line_to(xloc, ye) 
        context.stroke()
        
    def draw_nd(self, context, xloc, yloc, state, mark):
        xloc, yloc, wbox, _ = self.calc_render_params(xloc, yloc, 0.4, 0)

        if mark: context.set_source_rgba(*self.setup["color-selection"])
        else: context.set_source_rgba(*self.setup["color-node"])
        context.arc(xloc, yloc, wbox, 0, 2 * pi)
        context.fill()

    def draw_sn0(self, context, xloc, yloc, state, mark):
        xloc, yloc, wbox, hbox = self.calc_render_params(xloc, yloc, 1.2, 1.2)

        xo, yo = xloc, yloc
        points = [(xo-wbox/2, yo), (xo, yo-hbox/2),
                  (xo+wbox/2, yo), (xo, yo+hbox/2)]
        color = self.setup["color-selection"] if mark else self.setup["color-node"]
        self.draw_polygon(context, color, points)        

    def draw_str0(self, context, xloc, yloc, state, mark):
        xloc, yloc, wbox, hbox = self.calc_render_params(xloc, yloc, 1.75, 1.75)
        
        if mark: context.set_source_rgba(*self.setup["color-selection"])
        else: context.set_source_rgba(*self.setup["color-node"])
        context.rectangle(xloc-wbox/2, yloc-hbox/2, wbox, hbox)
        context.fill()

        context.set_source_rgba(*self.setup["color-base"])
        context.rectangle(xloc-wbox/4, yloc-hbox/4, wbox/2, hbox/2)
        context.fill()

    def draw_src0(self, context, xloc, yloc, state, mark):
        xloc, yloc, r, _ = self.calc_render_params(xloc, yloc, 0.75, 0)
        
        if mark: context.set_source_rgba(*self.setup["color-selection"])
        else: context.set_source_rgba(*self.setup["color-node"])
        context.arc(xloc, yloc, r, 0, 2 * pi)
        context.fill()
        
        context.set_source_rgba(*self.setup["color-base"])
        context.arc(xloc, yloc, r/2, 0, 2 * pi)
        context.fill()

    def draw_bar0(self, context, xloc, yloc, state, mark):
        xloc, yloc, wbox, hbox = self.calc_render_params(xloc, yloc, 1, 1)

        if mark: context.set_source_rgba(*self.setup["color-selection"])
        else: context.set_source_rgba(*self.setup["color-node"])
        context.arc(xloc, yloc, wbox, 0, 2 * pi)
        context.fill()
        
        context.set_source_rgba(*self.setup["color-base"])
        context.arc(xloc, yloc, 2*wbox/3, 0, 2 * pi)
        context.fill()

        if mark: context.set_source_rgba(*self.setup["color-selection"])
        else: context.set_source_rgba(*self.setup["color-node"])
        context.set_line_width(wbox/4)
        context.move_to(xloc-wbox, yloc-hbox)
        context.line_to(xloc+wbox, yloc+hbox) 
        context.stroke()
        context.move_to(xloc+wbox, yloc-hbox)
        context.line_to(xloc-wbox, yloc+hbox) 
        context.stroke()

        
    def draw_acc0(self, context, xloc, yloc, state, mark):
        xloc, yloc, wbox, hbox = self.calc_render_params(xloc, yloc, 2, 2)
        
        if mark: context.set_source_rgba(*self.setup["color-selection"])
        else: context.set_source_rgba(*self.setup["color-node"])
        context.rectangle(xloc-wbox/2, yloc-hbox/2, wbox, hbox)
        context.fill()

        context.set_source_rgba(*self.setup["color-base"])
        context.arc(xloc, yloc, 2*wbox/5, 0, 2 * pi)
        context.fill()

        if mark: context.set_source_rgba(*self.setup["color-selection"])
        else: context.set_source_rgba(*self.setup["color-node"])
        context.arc(xloc, yloc, wbox/7, 0, 2 * pi)
        context.fill()

    def draw_mix0(self, context, xloc, yloc, state, mark):
        xloc, yloc, wbox, hbox = self.calc_render_params(xloc, yloc, 2, 2)
        
        if mark: context.set_source_rgba(*self.setup["color-selection"])
        else: context.set_source_rgba(*self.setup["color-node"])
        context.rectangle(xloc-wbox/2, yloc-hbox/2, wbox, hbox)
        context.fill()

        context.set_source_rgba(*self.setup["color-base"])
        context.rectangle(xloc-3*wbox/8, yloc-3*hbox/8, 3*wbox/4, 3*hbox/4)
        context.fill()

        if mark: context.set_source_rgba(*self.setup["color-selection"])
        else: context.set_source_rgba(*self.setup["color-node"])
        context.set_line_width(wbox/8)
        
        context.move_to(xloc, yloc-hbox/2)
        context.line_to(xloc, yloc+hbox/2) 
        context.stroke()

        context.move_to(xloc-wbox/2, yloc)
        context.line_to(xloc+wbox/2, yloc) 
        context.stroke()

        
    def draw_in0(self, context, xloc, yloc, state, mark):
        xloc, yloc, wbox, hbox = self.calc_render_params(xloc, yloc, 1.6, 1.6)
        
        if mark: context.set_source_rgba(*self.setup["color-selection"])
        else: context.set_source_rgba(*self.setup["color-node"])
        context.arc(xloc, yloc, 2.2*wbox/3, 0, 2 * pi)
        context.fill()

        xo, yo = xloc, yloc + hbox/5
        points = [(xo, yo), (xo + 2*wbox/5, yo - hbox/4),
                  (xo, yo+hbox/4), (xo - 2*wbox/5, yo - hbox/4)]
        self.draw_polygon(context, self.setup["color-base"], points)
        xo, yo = xloc, yloc - hbox/5
        points = [(xo, yo), (xo + 2*wbox/5, yo - hbox/4),
                  (xo, yo+hbox/4), (xo - 2*wbox/5, yo - hbox/4)]
        self.draw_polygon(context, self.setup["color-base"], points)

    def draw_out0(self, context, xloc, yloc, state, mark):
        xloc, yloc, wbox, hbox = self.calc_render_params(xloc, yloc, 1.6, 1.6)
        
        if mark: context.set_source_rgba(*self.setup["color-selection"])
        else: context.set_source_rgba(*self.setup["color-node"])
        context.arc(xloc, yloc, 2.2*wbox/3, 0, 2 * pi)
        context.fill()

        xo, yo = xloc, yloc - hbox/5
        points = [(xo, yo), (xo + 2*wbox/5, yo + hbox/4),
                  (xo, yo - hbox/4), (xo - 2*wbox/5, yo + hbox/4)]
        self.draw_polygon(context, self.setup["color-base"], points)
        xo, yo = xloc, yloc + hbox/5
        points = [(xo, yo), (xo + 2*wbox/5, yo + hbox/4),
                  (xo, yo - hbox/4), (xo - 2*wbox/5, yo + hbox/4)]
        self.draw_polygon(context, self.setup["color-base"], points)

    def draw(self, context, selection=None):
        context.set_source_rgba(*self.setup["color-background"])
        context.rectangle (0, 0, *self.setup["window-size"])
        context.fill()

        for pipe, n1, n2, state in self.state["connections"]:
            if selection is None: mark = False
            else:
                keys = [io.key for io in selection.ios]
                mark = n1 in keys and n2 in keys 
            if pipe in ["pipeX", "pipeY"]:
                self.draw_pipe(context, n1, n2, state, mark)
            else: raise ValueError(f"Not supported shape: {pipe}")

        for (element, x, y), state in self.state["elements"]:
            if selection is None: mark = False
            else: mark = (element, x, y) == selection.key

            if element == "str0": self.draw_str0(context, x, y, state, mark)
            elif element == "in0": self.draw_in0(context, x, y, state, mark)
            elif element == "out0": self.draw_out0(context, x, y, state, mark)
            elif element == "ex0": self.draw_ex0(context, x, y, state, mark)
            elif element in ["ndX", "ndY"]: self.draw_nd(context, x, y, state, mark)
            elif element == "sn0": self.draw_sn0(context, x, y, state, mark)
            elif element == "mix0": self.draw_mix0(context, x, y, state, mark)
            elif element == "src0": self.draw_src0(context, x, y, state, mark)
            elif element == "acc0": self.draw_acc0(context, x, y, state, mark)
            elif element == "bar0": self.draw_bar0(context, x, y, state, mark)
            else: raise ValueError(f"Not supported shape: {element}")
            
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
        self.painter = MoonPainter(self.setup, self.state)
        self.system = MoonSystem(self.state, self.library)
        BaseWindow.__init__(self, title, width, height)

    @BaseWindow.double_buffering
    def draw_content(self, context):
        self.painter.draw(context, self.selected_node)

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
            if self.selected_node is not None:            
                self.selected_node = None
                self.draw_content()
        elif key_name == "space":
            self.system.run(1.0)
        else:
            print("not supported key:")
            print("\tkey name:", Gdk.keyval_name(event.keyval))
            print("\tkey value:", event.keyval)
        return True


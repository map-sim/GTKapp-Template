#!/usr/bin/python3

import os, json, gi, cairo, random


from BaseWindow import BaseWindow
from MoonSystem import MoonSystem
from MoonPainters import MoonPainter
from MoonPainters import MoonDistPainter

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
        "nd0": {
            "io": 2,
            "cost": 1.0,
            "radius": 2.0,
            "capacity": 0.0,
            "bandwidth": 0.75,
            "type": "node"
        },
        "in0": {
            "io": 1,
            "cost": 3.5,
            "cover": 0.3,
            "radius": 5.0,
            "capacity": 7.5,
            "bandwidth": 0.5,
            "type": "inner",
            "goods": ["Y"]
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
        "frequency": 2,
        "process": "Y"
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
        ("pipeX", ("str0", 1, 7), ("nd0", 3, 12), {"switch": 1}),
        ("pipeX", ("nd0", 3, 12), ("mix0", 9, 15), {"switch": 1}),
        ("pipeY", ("mix0", 9, 15), ("str0", 10, 10), {"switch": 1}),
        ("pipeY", ("str0", 10, 10), ("bar0", 9, 2.5), {"switch": 1}),
        ("pipeY", ("str0", 10, 10), ("out0", 14.5, 7.5), {"switch": 1}),
        ("pipeY", ("mix0", 9, 15), ("in0", 13, 19), {"switch": 1}),
        ("pipeX", ("str0", -8, 6), ("str0", -10, 11), {"switch": 1}),

        ("pipeX", ("str0", -10, 11), ("nd0", -8, 16), {"switch": 1}),
        ("pipeX", ("str0", -4, 18), ("nd0", -8, 16), {"switch": 1}),

        ("pipeX", ("str0", -10, 11), ("nd0", -15, 14), {"switch": 1}),
        ("pipeX", ("nd0", -18, 8), ("nd0", -15, 14), {"switch": 1})
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

        (("nd0", -15, 14), {}),
        (("nd0", -18, 8), {}),
        (("nd0", -8, 16), {}),
        (("str0", -4, 18), {"X": 0.0, "Y": 0.0}),

        (("nd0", 3, 12), {}),
        (("nd0", 16, 16), {}),
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
    "window-size": (1200, 800),
    "window-offset": (800, 300),
    "window-zoom": 21.5,
    "move-sensitive": 50,
    "color-selection": (1.0, 0.0, 0.0),
    "color-background": (0.8, 0.9, 0.9),
    "color-pipe": (0.0, 0.66, 0.5),
    "color-base": (1.0, 1.0, 0.0),
    "color-node": (0.4, 0, 0.4),
    "max-selection-range": 25
}


        
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
            self.system.run(1.0)
        elif key_name == "X":
            print("##> X & redraw")
            self.draw_distribution_args = "source", "X"
            self.draw_distribution()
        else:
            print("not supported key:")
            print("\tkey name:", Gdk.keyval_name(event.keyval))
            print("\tkey value:", event.keyval)
        return True


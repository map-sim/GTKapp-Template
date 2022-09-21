#!/usr/bin/python3

from math import pi, sqrt, atan2
import os, json, gi, cairo, random


from BaseWindow import BaseWindow
from RawGraph import RawGraph

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk



example_library = {
    "infra": {
        "pipe0": {
            "cost": 0.5,
            "cover": 0.55,
            "radius": 0.0,
            "capacity": 0.0,
            "bandwidth": 0.5,
            "type": "pipe"
        },
        "nd0": {
            "io": 2,
            "cost": 1.0,
            "cover": 0.55,
            "radius": 0.5,
            "capacity": 0.0,
            "bandwidth": 0.5,
            "type": "node"
        },
        "in0": {
            "io": 1,
            "cost": 3.5,
            "cover": 0.3,
            "radius": 2.0,
            "capacity": 7.5,
            "bandwidth": 0.5,
            "type": "inner"
        },
        "out0": {
            "io": 2,
            "cost": 3.5,
            "cover": 0.7,
            "radius": 1.0,
            "capacity": 1.0,
            "bandwidth": 0.5,
            "type": "outer"
        },
        "bar0": {
            "io": 1,
            "cost": 12.5,
            "cover": 0.6,
            "radius": 3.0,
            "capacity": 3.5,
            "bandwidth": 1.5,
            "type": "barrier",
            "goods": ["Y"]
        },
        "mix0": {
            "io": 3,
            "cost": 4.5,
            "cover": 0.9,
            "radius": 1.0,
            "capacity": 5.0,
            "bandwidth": 0.7,
            "type": "mixer"
        },
        "src0": {
            "io": 1,
            "cost": 1.5,
            "cover": 0.5,
            "radius": 2.5,
            "capacity": 0.5,
            "bandwidth": 0.4,
            "type": "source",
            "goods": ["X"]
        },
        "ex0": {
            "io": 0,
            "cost": 1.5,
            "cover": 0.0,
            "radius": 0.5,
            "capacity": 0.0,
            "bandwidth": 0.0,
            "type": "explorer"
        },
        "sn0": {
            "io": 0,
            "cost": 1.5,
            "cover": 0.0,
            "radius": 0.5,
            "capacity": 0.0,
            "bandwidth": 0.0,
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
    }
}

example_state = {
    
}

example_setup = {
    "window-title": "demo moon",
    "window-size": (800, 600)
}


class MoonWindow(BaseWindow):    
    def __init__(self, setup=None, state=None, library=None):
        if library is not None: self.library = librar
        else: self.library = example_library
        if state is not None: self.state = state
        else: self.state = example_state
        if setup is not None: self.setup = setup
        else: self.setup = example_setup

        title = self.setup["window-title"]
        width, height = self.setup["window-size"]
        BaseWindow.__init__(self, title, width, height)


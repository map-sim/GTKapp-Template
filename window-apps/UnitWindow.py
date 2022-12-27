#!/usr/bin/python3

from InfraWindow import InfraWindow
from InfraWindow import load_and_run

class UnitPainter:
    def __init__(self, config, library, battlefield):
        self.battlefield = battlefield
        self.selected_units = set()
        self.library = library
        self.config = config

    def get_unit_params(self, index, unit):
        xoffset, yoffset = self.config["window-offset"]
        wbox, hbox = self.config["unit-size"]
        zoom = self.config["window-zoom"]
        xloc, yloc = unit["location"]        
        xloc, yloc =  xloc - wbox / 2, yloc - hbox / 2
        xloc, yloc = xloc * zoom, yloc * zoom
        xloc, yloc = xloc + xoffset, yloc + yoffset
        wbox, hbox = wbox * zoom, hbox * zoom
        if index in self.selected_units:
            color = self.battlefield["owners"][unit["owner"]]["color2"]
        else: color = self.battlefield["owners"][unit["owner"]]["color"]
        return color, zoom, xloc, yloc, wbox, hbox

        
    def draw(self, context):
        for index, unit in enumerate(self.battlefield["units"]):
            outs = self.get_unit_params(index, unit)
            color, zoom, xloc, yloc, wbox, hbox = outs
            context.set_line_width(zoom * self.config["unit-line"])
            context.set_source_rgba(*color)

            context.rectangle(xloc, yloc, wbox, hbox)
            context.move_to(xloc + wbox, yloc+hbox) 
            context.line_to(xloc, yloc)
            context.move_to(xloc + wbox, yloc) 
            context.line_to(xloc, yloc+hbox)
            context.stroke()


class UnitAbilities:
    properties = [
        "location",
        "landing-space"
    ],
    abilities = {
	"people-living": { "when": "always", "support": ["cost"]},        
	"foot-movement": {"when": "movment", "support": ["max-speed"]},
	"wheel-movement": {"when": "movment", "support": ["cost", "max-speed"]},
	"track-movement": {"when": "movment", "support": ["cost", "max-speed"]},
        "amphibia-movement": {"when": "movment", "support": ["cost", "max-speed"]},

	"transportation": {"when": "transport", "support": ["cost", "max-speed", "space"]},
	"supply": {"when": "transport", "support": ["cost", "max-speed", "space", "volume"]},
	"point-shot": {"when": "shot-point", "support": ["cost", "deviation", "line-of-sight"]},
	"react-shot": {"when": "shot-react", "support": ["cost", "deviation", "line-of-sight"]},
    }
    
    def __init__(self): pass

class UnitWindow(InfraWindow):
    def init_painters(self, config, library, battlefield):
        self.painter = InfraWindow.init_painters(self, config, library, battlefield)
        self.unit_painter = UnitPainter(config, library, battlefield)
        self.painter.append(self.unit_painter)
        return self.painter


if __name__ == "__main__":
    example_config = {
        "version": 0,
        "window-title": "infra-window",
        "window-zoom": 0.0366,
        "window-size": (1800, 820),
        "window-offset": (500, 100),
        "selection-color": (0.8, 0, 0.8),
        "selection-radius2": 2500,
        "plot-radius-scale": 3.5,
        "move-sensitive": 50,
        "move-editing": 2,
        "person-space": 2,
        "unit-size": (50, 35),
        "unit-line": 6
    }
    load_and_run(example_config, UnitWindow)


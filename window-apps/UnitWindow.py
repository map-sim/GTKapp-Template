#!/usr/bin/python3

import gi

# gi.require_version('Gtk', '3.0')
# from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

from InfraWindow import InfraWindow
from InfraWindow import load_and_run

class UnitPainter:
    def __init__(self, config, library, battlefield):
        self.battlefield = battlefield
        self.object_flag = "units"
        self.selected_units = set()
        self.library = library
        self.config = config

    def get_unit_params(self, index, unit):
        xoffset, yoffset = self.config["window-offset"]
        wbox, hbox = self.config["unit-size"]
        zoom = self.config["window-zoom"]
        if type(unit["location"]) is int:
            params = self.battlefield["infrastructure"][unit["location"]]
            if params is None: print(f"Warning! Unit {index} in null infra")
            else: xloc, yloc = params[1:3]
        else: xloc, yloc = unit["location"]
        try: xloc, yloc =  xloc - wbox / 2, yloc - hbox / 2
        except TypeError: xloc, yloc =  -wbox / 2, -hbox / 2
        xloc, yloc = xloc * zoom, yloc * zoom
        xloc, yloc = xloc + xoffset, yloc + yoffset
        wbox, hbox = wbox * zoom, hbox * zoom
        if index in self.selected_units:
            color = self.battlefield["owners"][unit["owner"]]["color2"]
        else: color = self.battlefield["owners"][unit["owner"]]["color"]
        return color, zoom, xloc, yloc, wbox, hbox

    def draw(self, context):
        if self.object_flag == "no-units": return

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


class UnitValidator:
    def __init__(self, name, conf):
        self.name = name
        self.validate(conf)
    def validate(self, conf):
        counter = 0
        for key, val in conf.items():
            if key in self.required:
                if self.required[key] is dict:
                    assert type(val) is dict
                if self.required[key] is list:
                    assert type(val) is list
                counter += 1
            elif key in self.optional: pass
            else: raise ValueError(key)
        assert len(conf) >= counter
        print(f"{self.prefix} {self.name} ... OK")

class UnitWeapon(UnitValidator):
    optional = ["construction", "destruction"]    
    prefix = "Weapon"
    required = {
        "size": None,
	"view-range": None,
	"fire-range": None,
	"fire-power": None,
	"preparing-delay": None,
	"accuracy": None,
	"abilities": list,
	"cost": dict
    }

class UnitActor(UnitValidator):
    optional = []
    prefix = "Actor"
    required = {
        "size": None,
	"armor": None,
	"aperture": None,
	"personel": None,
	"max-velocity": None,
	"preparing-delay-factor": None,
	"velocity-factors": dict,
	"inactive-cost": dict,
	"active-cost": dict,
	"init-weapons": dict,
	"capacity": dict
    }


class UnitWindow(InfraWindow):
    version = 0
    default_app_controls = {
        "resource-num": 0,
        "infra-num": 0,
        "selection-add": False,
        "selection-next": False,
        "current-mode": "navigation",
        "available-modes": {
            "F1": "navigation",
            "F2": "selection",
            "F3": "inserting",
            "F4": "editing",
            "F5": "modifying",
            "F6": "deleting",
            "F7": "designation"
        }
    }

    
    def __init__(self, config, library, battlefield):
        InfraWindow.__init__(self, config, library, battlefield)
        for name, actor in library["actors"].items(): UnitActor(name, actor)
        for name, weapon in library["weapons"].items(): UnitWeapon(name, weapon)

    def init_painters(self, config, library, battlefield):
        self.painter = InfraWindow.init_painters(self, config, library, battlefield)
        self.unit_painter = UnitPainter(config, library, battlefield)
        self.painter.append(self.unit_painter)
        return self.painter

    def on_press(self, widget, event):
        key_name = Gdk.keyval_name(event.keyval)
        if key_name == "Escape":
            InfraWindow.on_press(self, widget, event)
            units_counter = {}
            for uconf in self.battlefield["units"]:
                try: units_counter[uconf["owner"]] += 1
                except KeyError: units_counter[uconf["owner"]] = 1
            for owner, count in units_counter.items():
                print(f"Owner: {owner} has {count} unit(s)")

        elif key_name in "aA":
            if self.check_mode("selection", "editing", "modifying", "designation"):
                new_val = not self.app_controls["selection-add"]
                self.app_controls["selection-add"] = new_val
                self.app_controls["selection-next"] = False
                print("##> selection-add", new_val)
            else: print("Current mode does not support keys aA")

        elif key_name == "9":
            if self.unit_painter.object_flag != "no-units":
                self.unit_painter.object_flag = "no-units"
            else: self.unit_painter.object_flag = "units"
            self.draw_content()
        else: InfraWindow.on_press(self, widget, event)

    def find_units(self, xloc, yloc):
        selection = set()
        unit_list = self.battlefield["units"]
        for ix, unit in enumerate(unit_list):
            if type(unit["location"]) is int:
                params = self.battlefield["infrastructure"][unit["location"]]
                if params is None: print(f"Warning! Unit {ix} in null infra")
                else: xo, yo = params[1:3]
            else: xo, yo = unit["location"]
            d2 = (xloc-xo)**2 + (yloc-yo)**2
            if d2 < self.config["selection-radius2"]:
                selection.add(ix)
        return selection

    def on_click(self, widget, event):
        ox, oy = self.get_click_location(event)
        if event.button == 1:
            if self.check_mode("designation"):
                selection = self.find_units(ox, oy)                
                if self.app_controls["selection-add"]:
                    for it in selection:
                        if it in self.unit_painter.selected_units:
                            self.unit_painter.selected_units.remove(it)
                        else: self.unit_painter.selected_units.add(it)
                else: self.unit_painter.selected_units = selection
                
                print("Unit selection:")
                for unitid in self.unit_painter.selected_units:
                    unit = self.battlefield["units"][unitid]
                    owner, loc, line= unit["owner"], unit["location"], ""
                    for key, val in unit.items():
                        if key in self.library["actors"]:
                            line += f" {key}: {val['number']}"
                    print(f"{owner}/{loc}: {line}")
                self.draw_content()
            else: InfraWindow.on_click(self, widget, event)
        else: InfraWindow.on_click(self, widget, event)
        
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


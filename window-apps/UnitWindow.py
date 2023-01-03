#!/usr/bin/python3

import gi, math

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

from InfraWindow import InfraWindow
from InfraWindow import InfraGraph
from InfraWindow import load_and_run

class UnitHandler:
    def __init__(self, uid, config, library, battlefield):
        assert uid < len(battlefield["units"])
        self.battlefield = battlefield
        self.library = library
        self.config = config
        self.uid = uid

    def count_orders(self):
        unit = self.battlefield["units"][self.uid]
        if "orders" not in unit: return 0
        return len(unit["orders"])

    def __str__(self):
        unit = self.battlefield["units"][self.uid]
        owner, loc = unit["owner"], unit["location"]
        if type(loc) is int:
            shape = self.battlefield["infrastructure"][loc][0]
            loc = f"{loc}({shape})"
        resources, line = unit["resources"], ""
        for key, val in unit.items():
            if key in self.library["actors"]:
                line += f"{key}: {val['number']} | "
        ol = self.count_orders()
        return f"{self.uid}. {owner}/{loc}/{resources} (orders: {ol}): {line}"

    def update_infra_nodes(self, changelog):
        unit = self.battlefield["units"][self.uid]
        if "orders" in unit:            
            for order in unit["orders"]:
                if order[0] == "transfer": continue
                elif order[0] == "move": gix = range(2, len(order))
                elif order[0] == "landing": gix = range(3, len(order))
                elif order[0] == "supply": gix = range(3, len(order)-1)
                elif order[0] == "store": gix = range(3, len(order))
                elif order[0] == "take": gix = range(3, len(order))
                elif order[0] == "demolish": gix = [len(order)-1]
                elif order[0] == "destroy": gix = [len(order)-1]
                else: raise ValueError(order[0])
                for ix in gix:
                    if order[ix] not in changelog: continue
                    order[ix] = changelog[order[ix]]

        if type(unit["location"]) is not int: return
        if unit["location"] not in changelog: return
        unit["location"] = changelog[unit["location"]]
        
class UnitPainter:
    def __init__(self, config, library, battlefield):
        self.battlefield = battlefield
        self.object_flag = "units"
        self.selected_units = set()
        self.library = library
        self.config = config
        self.measurement = None

    def get_unit_params(self, index, unit):
        xoffset, yoffset = self.config["window-offset"]
        wbox, hbox = self.config["unit-size"]
        zoom = self.config["window-zoom"]
        if type(unit["location"]) is int:
            params = self.battlefield["infrastructure"][unit["location"]]
            if params is None: print(f"Warning! Unit {index} in null infra")
            else: xloc, yloc = params[1:3]
        else: xloc, yloc = unit["location"]
        xloc, yloc =  xloc - wbox / 2, yloc - hbox / 2
        xloc, yloc = xloc * zoom, yloc * zoom
        xloc, yloc = xloc + xoffset, yloc + yoffset
        wbox, hbox = wbox * zoom, hbox * zoom
        if index in self.selected_units:
            color = self.battlefield["owners"][unit["owner"]]["color2"]
        else: color = self.battlefield["owners"][unit["owner"]]["color"]
        color2 = self.battlefield["owners"][unit["owner"]]["color3"]
        return color, color2, zoom, xloc, yloc, wbox, hbox

    def draw_unit(self, context, unit, index):
        outs = self.get_unit_params(index, unit)
        color, color2, zoom, xloc, yloc, wbox, hbox = outs

        context.set_line_width(zoom * 1.5 * self.config["unit-line"])
        context.set_source_rgba(*color2)

        context.rectangle(xloc, yloc, wbox, hbox)
        context.rectangle(xloc, yloc, wbox, hbox)
        context.move_to(xloc + wbox, yloc+hbox) 
        context.line_to(xloc, yloc)
        context.move_to(xloc + wbox, yloc) 
        context.line_to(xloc, yloc+hbox)
        context.stroke()

        context.set_line_width(zoom * self.config["unit-line"])
        context.set_source_rgba(*color)

        context.rectangle(xloc, yloc, wbox, hbox)
        context.move_to(xloc + wbox, yloc+hbox) 
        context.line_to(xloc, yloc)
        context.move_to(xloc + wbox, yloc) 
        context.line_to(xloc, yloc+hbox)
        context.stroke()

    def deduce_loc(self, pt, render=True):
        if type(pt) is int:
            params = self.battlefield["infrastructure"][pt]
            xloc, yloc = params[1:3]
        else: xloc, yloc = pt
        if not render: return xloc, yloc
        xoffset, yoffset = self.config["window-offset"]
        zoom = self.config["window-zoom"]
        xloc, yloc = xloc * zoom, yloc * zoom
        xloc, yloc = xloc + xoffset, yloc + yoffset
        return xloc, yloc

    def draw_line(self, context, xyo, xye, color, width,
                  start=True, stop=True, style="solid"):
        context.set_source_rgba(*color)
        if style == "solid":
            context.set_line_width(width)
            context.move_to(*xyo)
            context.line_to(*xye)
            context.stroke()
        else: raise ValueError(style)
        if start:
            context.arc(*xyo, width, 0, 2*math.pi)
            context.fill()
        if stop:
            context.arc(*xye, width, 0, 2*math.pi)
            context.fill()
            
    def draw_hops(self, context, unit, nodes, last_unit=False):
        #context.set_source_rgba(*)
        zoom = self.config["window-zoom"]
        width = zoom * self.config["unit-line"]
        context.set_line_width(width)
        xyo = self.deduce_loc(unit["location"])
        context.arc(*xyo, width, 0, 2 * math.pi)
        context.fill()

        for i, node in enumerate(nodes):
            if type(node) is int:
                if last_unit and i == len(nodes) - 1:
                    unit2 = self.battlefield["units"][node]
                    xye = self.deduce_loc(unit2["location"])
                else: xye = self.deduce_loc(node)
            else: xye = self.deduce_loc(node)

            color = self.battlefield["owners"][unit["owner"]]["color2"]
            self.draw_line(context, xyo, xye, color, width, start=False)
            xyo = xye

    def draw_arrow(self, context, xyo, xye, color, width):
        zoom = self.config["window-zoom"]
        dx, dy = xye[0] - xyo[0], xye[1] - xyo[1]
        arrow_angle = math.atan(dy/dx) #- math.pi
        if dx < 0: arrow_angle -= math.pi
        arrowhead_angle = math.pi/6
        arrowhead_length = 30 * zoom
        arrow_length = 0 * zoom
        
        context.move_to(*xye)
        context.rel_line_to(arrow_length * math.cos(arrow_angle), arrow_length * math.sin(arrow_angle))
        context.rel_move_to(-arrowhead_length * math.cos(arrow_angle - arrowhead_angle), -arrowhead_length * math.sin(arrow_angle - arrowhead_angle))
        context.rel_line_to(arrowhead_length * math.cos(arrow_angle - arrowhead_angle), arrowhead_length * math.sin(arrow_angle - arrowhead_angle))
        context.rel_line_to(-arrowhead_length * math.cos(arrow_angle + arrowhead_angle), -arrowhead_length * math.sin(arrow_angle + arrowhead_angle))

        context.set_source_rgb(*color)
        context.set_line_width(width)
        context.stroke()
        
    def draw_move(self, context, unit, order):
        self.draw_hops(context, unit, order[2:], last_unit=False)

    def draw_landing(self, context, unit, order):
        self.draw_hops(context, unit, order[3:], last_unit=False)

    def draw_transfer(self, context, unit, order):
        self.draw_hops(context, unit, [order[2]], last_unit=True)

    def draw_take(self, context, unit, order):
        self.draw_hops(context, unit, order[3:], last_unit=False)

    def draw_store(self, context, unit, order):
        self.draw_hops(context, unit, order[3:], last_unit=False)

    def draw_supply(self, context, unit, order):        
        self.draw_hops(context, unit, order[3:], last_unit=True)
        
    def draw_demolish(self, context, unit, order):
        xyo = self.deduce_loc(unit["location"])
        xye = self.deduce_loc(order[-1])

        zoom = self.config["window-zoom"]
        width = zoom * self.config["unit-line"]
        color = self.battlefield["owners"][unit["owner"]]["color3"]
        self.draw_line(context, xyo, xye, color, width, stop=False)        
        self.draw_arrow(context, xyo, xye, color, width)
        color2 = self.battlefield["owners"][unit["owner"]]["color"]
        self.draw_line(context, xyo, xye, color2, width*0.5, stop=False)
        self.draw_arrow(context, xyo, xye, color2, width*0.5)
        
    def draw_destroy(self, context, unit, order):
        xyo = self.deduce_loc(unit["location"])
        unit2 = self.battlefield["units"][order[-1]]
        xye = self.deduce_loc(unit2["location"])

        zoom = self.config["window-zoom"]
        width = zoom * self.config["unit-line"]
        color = self.battlefield["owners"][unit["owner"]]["color3"]
        self.draw_line(context, xyo, xye, color, width, stop=False)
        self.draw_arrow(context, xyo, xye, color, width)
        color2 = self.battlefield["owners"][unit["owner"]]["color"]
        self.draw_line(context, xyo, xye, color2, width*0.5, stop=False)
        self.draw_arrow(context, xyo, xye, color2, width*0.5)

    def draw_measurement(self, context):
        if self.measurement is None: return
        xo, yo, xe, ye = self.measurement
        d = math.sqrt((xo-xe)**2 + (yo-ye)**2)
        if d < 1: return
        dd = d * 0.001 * self.battlefield["scale"]
        print(f"Distance: {round(dd, 3)} km")
        xoo, yoo = self.deduce_loc([xo, yo])
        xee, yee = self.deduce_loc([xe, ye])

        context.set_line_width(0.9 * self.config["unit-line"])
        context.set_source_rgba(0, 0, 0)
        context.move_to(xoo, yoo) 
        context.line_to(xee, yee)
        context.stroke()

        context.set_line_width(0.6 * self.config["unit-line"])
        context.set_source_rgba(1, 1, 0.5)
        context.move_to(xoo, yoo) 
        context.line_to(xee, yee)
        context.stroke()

        context.set_source_rgba(0, 0, 0)
        context.arc(xee, yee, 3, 0, 2 * math.pi)
        context.fill()
        context.set_source_rgba(1, 1, 0.5)
        context.arc(xee, yee, 2.4, 0, 2 * math.pi)
        context.fill()
        context.set_source_rgba(0, 0, 0)
        dx = (xee - xoo) / dd
        dy = (yee - yoo) / dd
        for di in range(int(dd)+1):
            xii = xoo + di * dx 
            yii = yoo + di * dy 
            context.arc(xii, yii, 3, 0, 2 * math.pi)
            context.fill()

    def draw_unit_orders(self, context, unit):
        if "orders" not in unit: return 
        for order in unit["orders"]:
            if order[0] == "move": self.draw_move(context, unit, order)
            elif order[0] == "transfer": self.draw_transfer(context, unit, order)
            elif order[0] == "landing": self.draw_landing(context, unit, order)
            elif order[0] == "supply": self.draw_supply(context, unit, order)
            elif order[0] == "store": self.draw_store(context, unit, order)
            elif order[0] == "take": self.draw_take(context, unit, order)
            elif order[0] == "demolish": self.draw_demolish(context, unit, order)
            elif order[0] == "destroy": self.draw_destroy(context, unit, order)
            else: raise ValueError(f"not supported order: {order[0]}")
            
    def draw(self, context):
        if self.object_flag == "no-units": return
        for index, unit in enumerate(self.battlefield["units"]):
            self.draw_unit(context, unit, index)

        for unit in self.battlefield["units"]:
            self.draw_unit_orders(context, unit)
        for index in self.selected_units:
            unit = self.battlefield["units"][index]
            self.draw_unit_orders(context, unit)            
        self.draw_measurement(context)

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
    optional = ["allowed-infra"]
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

class UnitGraph(InfraGraph):
    required_keys = ["owner", "location", "resources"]
    
    def __init__(self, config, library, battlefield):
        InfraGraph.__init__(self, config, library, battlefield)
        for name, actor in library["actors"].items(): UnitActor(name, actor)
        for name, weapon in library["weapons"].items(): UnitWeapon(name, weapon)
        self.validate_orders()

    def clean_null_infra(self):
        torm_counter, changelog = 0, {}
        infra_list = self.battlefield["infrastructure"]
        for ix, (shape, *params) in enumerate(infra_list):
            if shape is None:
                # changelog[ix] = None
                torm_counter += 1
            else: changelog[ix] = ix - torm_counter
        for ix in range(len(self.battlefield["units"])):
            uh = UnitHandler(ix, self.config, self.library, self.battlefield)
            uh.update_infra_nodes(changelog)
        InfraGraph.clean_null_infra(self)

    def check_los(self, xyo, xye):
        print("los", xyo, xye)
        r = self.config["map-resolution"]
        dx, dy = xye[0] - xyo[0], xye[1] - xyo[1]
        d = math.sqrt(dy**2 + dx**2)

        for i in range(int(d/r)):
            f = float(i) / d
            xy = xyo[0] + f*dx, xyo[1] + f*dy
            t = self.check_terrain(*xy)
        t = self.check_terrain(*xye)
        print(int(d/r))

    def validate_orders(self):
        unit_list = self.battlefield["units"]
        for index, unit in enumerate(unit_list):
            for key in self.required_keys:
                assert key in unit, key

        # number of orders
        # distance of orders

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
        self.graph = UnitGraph(config, library, battlefield)
        self.measurement_base = None

    def init_painters(self, config, library, battlefield):
        self.painter = InfraWindow.init_painters(self, config, library, battlefield)
        self.unit_painter = UnitPainter(config, library, battlefield)
        self.painter.append(self.unit_painter)
        return self.painter

    def delete_selection(self):
        if not self.infra_painter.selected_infra:
            print("No infra selected..."); return
        for unit in self.battlefield["units"]:
            if type(unit["location"]) is int:
                if unit["location"] in self.infra_painter.selected_infra:
                    params = self.battlefield["infrastructure"][unit["location"]]
                    unit["location"] = [params[1], params[2]]
        for unit in self.battlefield["units"]:
            if "orders" not in unit: continue
            torm = set()
            for ix, order in enumerate(unit["orders"]):
                for bid in self.infra_painter.selected_infra:
                    if order[0] == "transfer": continue
                    elif order[0] == "move": nodes = list(order[2:])
                    elif order[0] == "landing": nodes = list(order[3:])
                    elif order[0] == "supply": nodes = list(order[3:-1])
                    elif order[0] == "store": nodes = list(order[3:])
                    elif order[0] == "take": nodes = list(order[3:])
                    elif order[0] == "demolish": nodes = [order[-1]]
                    elif order[0] == "destroy": nodes = [order[-1]]
                    else: raise ValueError(order[0])
                    if bid in nodes: torm.add(ix)
            for ix in list(reversed(sorted(torm))):
                del unit["orders"][ix]
        InfraWindow.delete_selection(self)

    def on_press(self, widget, event):
        key_name = Gdk.keyval_name(event.keyval)
        if key_name == "Escape":
            units_counter = {}
            self.measurement_base = None
            self.unit_painter.measurement = None
            for uconf in self.battlefield["units"]:
                try: units_counter[uconf["owner"]] += 1
                except KeyError: units_counter[uconf["owner"]] = 1
            for owner, count in units_counter.items():
                print(f"Owner: {owner} has {count} unit(s)")
            self.unit_painter.object_flag = "units"
            self.unit_painter.selected_units = set()
            InfraWindow.on_press(self, widget, event)

        elif key_name in "aA":
            if self.check_mode("selection", "editing", "modifying", "designation"):
                new_val = not self.app_controls["selection-add"]
                self.app_controls["selection-add"] = new_val
                self.app_controls["selection-next"] = False
                print("##> selection-add", new_val)
            else: print("Current mode does not support keys aA")

        elif key_name == "0":
            if self.check_mode("navigation", "modifying"):
                print("##> show routes only distribution")
                self.infra_painter.object_flag = "route"
                self.unit_painter.object_flag = "no-units"
                self.draw_content()
            else: print("Current mode does not support key 0")
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
                xo, yo = params[1:3]
            else: xo, yo = unit["location"]
            d2 = (xloc-xo)**2 + (yloc-yo)**2
            if d2 < self.config["selection-radius2"]:
                selection.add(ix)
        return selection

    def on_click(self, widget, event):
        ox, oy = self.get_click_location(event)
        if event.button == 1:
            if self.check_mode("navigation"):
                if self.measurement_base is not None:
                    self.unit_painter.measurement = *self.measurement_base, ox, oy
                    self.graph.check_los(self.measurement_base, (ox, oy))
                    self.draw_content()
                elif self.infra_painter.selected_infra:
                    bid = next(iter(self.infra_painter.selected_infra))
                    ex, ey = self.battlefield["infrastructure"][bid][1:3]
                    self.unit_painter.measurement = ex, ey, ox, oy
                    self.draw_content()

            if self.check_mode("designation"):
                selection = self.find_units(ox, oy)                
                if self.app_controls["selection-add"]:
                    for it in selection:
                        if it in self.unit_painter.selected_units:
                            self.unit_painter.selected_units.remove(it)
                        else: self.unit_painter.selected_units.add(it)
                else: self.unit_painter.selected_units = selection
                ex = ":" if self.unit_painter.selected_units else ": -"
                print(f"Unit selection{ex}")
                for unitid in self.unit_painter.selected_units:
                    args = unitid, self.config, self.library, self.battlefield
                    print(UnitHandler(*args))
                self.draw_content()
            else: InfraWindow.on_click(self, widget, event)
        else:
            if self.check_mode("navigation"):
                if event.button == 3:
                    self.measurement_base = ox, oy
                    print("New measurement base:", self.measurement_base)
            InfraWindow.on_click(self, widget, event)

if __name__ == "__main__":
    example_config = {
        "version": 0,
        "window-title": "infra-window",
        "window-zoom": 0.0366,
        "window-size": (1800, 820),
        "window-offset": (500, 100),
        "selection-color": (0.8, 0, 0.8),
        "order-max-distance2": 45500,
        "selection-radius2": 2500,
        "plot-radius-scale": 3.5,
        "move-sensitive": 50,
        "move-editing": 2,
        "person-space": 2,
        "unit-size": (50, 35),
        "map-resolution": 3.333,
        "unit-line": 6
    }
    load_and_run(example_config, UnitWindow)


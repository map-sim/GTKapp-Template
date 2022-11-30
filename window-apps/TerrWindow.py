#!/usr/bin/python3

import gi, cairo, math
from NaviWindow import NaviWindow
from BaseWindow import BaseWindow
from MapExamples import library0 as terr_library
from MapExamples import battlefield0 as terr_battlefield

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

class TerrPainter:
    def __init__(self, config, library, battlefield):
        self.battlefield =  battlefield
        self.library = library
        self.config = config

    @staticmethod
    def is_convex_polygon(polygon):
        """
        taken from:
        https://stackoverflow.com/questions/471962/how-do-i-efficiently-
        determine-if-a-polygon-is-convex-non-convex-or-complex
        """
        TWO_PI = 2 * math.pi
        try:
            if len(polygon) < 3: return False
            old_x, old_y = polygon[-2]
            new_x, new_y = polygon[-1]
            new_direction = math.atan2(new_y - old_y, new_x - old_x)
            angle_sum = 0.0
            for ndx, newpoint in enumerate(polygon):
                old_x, old_y, old_direction = new_x, new_y, new_direction
                new_x, new_y = newpoint
                new_direction = math.atan2(new_y - old_y, new_x - old_x)
                if old_x == new_x and old_y == new_y: return False
                angle = new_direction - old_direction
                if angle <= -math.pi: angle += TWO_PI
                elif angle > math.pi: angle -= TWO_PI
                if ndx == 0 and angle == 0.0: return False
                elif ndx == 0: orientation = 1.0 if angle > 0.0 else -1.0
                elif orientation * angle <= 0.0: return False	            
                angle_sum += angle
            return abs(round(angle_sum / TWO_PI)) == 1
        except (ArithmeticError, TypeError, ValueError):
            return False

    def draw_base(self, context, terrain):
        width, height = self.config["window-size"]
        color = self.library["terrains"][terrain]["color"]
        context.set_source_rgba(*color)
        context.rectangle(0, 0, width, height)
        context.fill()

    def draw_rect(self, context, terrain, params):
        zoom = self.config["window-zoom"]
        xoffset, yoffset = self.config["window-offset"]
        color = self.library["terrains"][terrain]["color"]
        context.set_source_rgba(*color)
        xloc, yloc, wbox, hbox = params
        xloc, yloc = xloc*zoom, yloc*zoom
        xloc, yloc = xloc + xoffset, yloc + yoffset
        context.rectangle(xloc, yloc, wbox*zoom, hbox*zoom)
        context.fill()
        context.stroke()

    def draw_polygon(self, context, terrain, params):
        zoom = self.config["window-zoom"]
        xoffset, yoffset = self.config["window-offset"]
        color = self.library["terrains"][terrain]["color"]

        if not TerrPainter.is_convex_polygon(params):
            print("WARNING! Polygon is not convex!")
            color = 1, 0, 0
        context.set_source_rgba(*color)

        start_x, start_y = params[-1]
        start_x, start_y = start_x*zoom, start_y*zoom
        start_x, start_y = start_x + xoffset, start_y + yoffset
        context.move_to (start_x, start_y)
        for point in params:    
            stop_x, stop_y = point
            stop_x, stop_y = stop_x*zoom, stop_y*zoom
            stop_x, stop_y = stop_x + xoffset, stop_y + yoffset
            context.line_to (stop_x, stop_y)
        context.fill()
        context.stroke()
        
    def draw(self, context):
        for shape, ter, *params in self.battlefield["terrains"]:
            color = self.library["terrains"][ter]["color"]
            if shape == "base": self.draw_base(context, ter)
            elif shape == "rect": self.draw_rect(context, ter, params)
            elif shape == "polygon": self.draw_polygon(context, ter, params)
            else: raise ValueError(f"Not supported shape: {shape}")

class TerrGraph:
    def __init__(self, battlefield):
        self.infrastructure = list()
        self.battlefield = battlefield

    def check_in_polygon(self, xyloc, xypoints):
        (x, y), pos, neg = xyloc, 0, 0
        for index in range(len(xypoints)):
            x1, y1 = xypoints[index]
            if x == x1 and y == y1: return True
            index2 = (index + 1) % len(xypoints)
            x2, y2 = xypoints[index2]
            d = (x-x1)*(y2-y1) - (y-y1)*(x2-x1)
            if d > 0: pos += 1
            if d < 0: neg += 1
            if pos > 0 and neg > 0:
                return False
        return True
        
    def check_terrain(self, xloc, yloc):
        output_terr, output_row = None, None
        for shape, terr, *params in self.battlefield["terrains"]:
            if shape == "base":
                output_terr = terr
                output_row = shape, terr, params
            elif shape == "rect":
                xo, yo = params[0], params[1]
                polygon = [(xo, yo), (xo+params[2], yo),
                           (xo+params[2], yo+params[3]), (xo, yo+params[3])]                
                if self.check_in_polygon((xloc, yloc), polygon):
                    output_row = shape, terr, params
                    output_terr = terr
            elif shape == "polygon":
                if self.check_in_polygon((xloc, yloc), params):
                    output_row = shape, terr, params
                    output_terr = terr
            else: raise ValueError(f"not supported: {shape}")
        return output_terr, output_row
        
class TerrWindow(NaviWindow):
    def __init__(self, config, library, battlefield):
        self.painter = TerrPainter(config, library, battlefield)
        self.graph = TerrGraph(battlefield)
        
        self.battlefield =  battlefield
        self.library = library
        self.config = config

        title = config["window-title"]
        width, height = config["window-size"]
        BaseWindow.__init__(self, title, width, height)

    def on_click(self, widget, event):
        xoffset, yoffset = self.config["window-offset"]
        width, height = self.config["window-size"]
        zoom = self.config["window-zoom"]
        ox = (int(event.x) - xoffset) / zoom
        oy = (int(event.y) - yoffset) / zoom

        if event.button == 1:
            print(f"({round(ox, 2)}, {round(oy, 2)}),")
        elif event.button == 3:
            terr = self.graph.check_terrain(ox, oy)
            print(f"({round(ox, 2)}, {round(oy, 2)}) --> {terr}")
        return True
        
def run_example():
    example_config = {
        "window-title": "terr-window",
        "window-size": (1800, 820),
        "window-offset": (500, 100),
        "window-zoom": 0.0366,
        "move-sensitive": 50
    }
    
    TerrWindow(example_config, terr_library, terr_battlefield)
    try: Gtk.main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
if __name__ == "__main__": run_example()
        

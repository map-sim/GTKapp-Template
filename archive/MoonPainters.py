from math import pi

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
        
    def draw_nd0(self, context, xloc, yloc, state, mark):
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
            elif element == "nd0": self.draw_nd0(context, x, y, state, mark)
            elif element == "sn0": self.draw_sn0(context, x, y, state, mark)
            elif element == "mix0": self.draw_mix0(context, x, y, state, mark)
            elif element == "src0": self.draw_src0(context, x, y, state, mark)
            elif element == "acc0": self.draw_acc0(context, x, y, state, mark)
            elif element == "bar0": self.draw_bar0(context, x, y, state, mark)
            else: raise ValueError(f"Not supported shape: {element}")

class MoonDistPainter:
    def __init__(self, setup, system):
        self.system = system
        self.setup = setup

    def draw(self, context, kind, param):
        context.set_source_rgba(1, 1, 1)
        context.rectangle (0, 0, *self.setup["window-size"])
        context.fill()

        xoffset, yoffset = self.setup["window-offset"]
        width, height = self.setup["window-size"]
        zoom = self.setup["window-zoom"]

        if kind == "source":
            vmax = self.system.state["source"][param]["max-amplitude"]
            #dist =             

            for x in range(width):
                for y in range(height):
                    ox = (x - xoffset) / zoom
                    oy = (y - yoffset) / zoom
                    src_dict = self.system.check_sources(ox, oy)
                    f = float(src_dict.get(param))/vmax
                    if not f: continue
                    context.set_source_rgba(1.0, 1.0-f, 1.0-f)
                    context.arc(x, y, 0.75, 0, 2 * pi)
                    context.fill()
        else: raise ValueError("dist kind")
        

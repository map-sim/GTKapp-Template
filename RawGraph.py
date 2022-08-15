import math

class RawGraph:
    def __init__(self, config, library, battle_field):
        self.infrastructure = list()
        self.battle_field = battle_field
        self.library = library
        self.config = config

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

    def check_infra(self, xloc, yloc):
        smallest_d2, smallest_row, smallest_index = math.inf, None, None
        infra_list = self.battle_field["infrastructure"]
        radius2 = self.config["pointer-radius"] ** 2
        for index, (infra_type, x, y) in enumerate(infra_list):
            d2 = (xloc-x)**2 + (yloc-y)**2
            if d2 > radius2: continue
            if d2 < smallest_d2:
                smallest_d2 = d2
                smallest_index = index
                smallest_row = infra_type, x, y
        return smallest_row, round(math.sqrt(smallest_d2), 1), smallest_index
        
    def check_terrain(self, xloc, yloc):
        output_terr, output_row = None, None
        for shape, terr, *params in self.battle_field["terrains"]:
            if shape == "base":
                output_terr = terr
                output_row = shape, terr, params
            elif shape == "polygon":
                if self.check_in_polygon((xloc, yloc), params):
                    output_row = shape, terr, params
                    output_terr = terr
            else: raise ValueError(f"not supported: {shape}")
        return output_terr, output_row


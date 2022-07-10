

class InfraNode:
    def __init__(self, config, library):
        self.library = library
        self.config = config
        
class RawGraph:
    def __init__(self, config, library):
        self.infrastructure = list()
        self.library = library
        self.config = config

        for config in self.config["battle-field"]["infrastructure"]:
            node = InfraNode(config, self.library)
            
        
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
        return "--"
        
    def check_terrain(self, xloc, yloc):
        output_terr = None
        for shape, terr, *params in self.config["battle-field"]["terrains"]:
            if shape == "base":
                output_terr = terr
            elif shape == "polygon":
                if self.check_in_polygon((xloc, yloc), params):
                    output_terr = terr
            else: raise ValueError(f"not supported: {shape}")
        return output_terr

    def get_info(self, xloc, yloc):
        outstr = f" -- {round(xloc, 2)}  {round(yloc, 2)} --\n"
        outstr += f"terrain: " + self.check_terrain(xloc, yloc)
        outstr += f"\ninfra: " + self.check_infra(xloc, yloc)
        return outstr

import math

class MoonNode(dict):
    def __init__(self, key, state, definition):
        self.definition = definition
        dict.__init__(self, state)
        self.key = key
        self.io = []
        
class MoonSystem(dict):
    def __init__(self, state, library):
        dict.__init__(self)
        self.library = library
        self.state = state

        for key, st in state["elements"]:
            name, xloc, yloc = key
            print(xloc, yloc, "-->", name)            
            definition = self.library["infra"][name]
            radius = definition["radius"]
            for (n, x, y), nd in self.items():
                d2 = (xloc - x) ** 2 + (yloc - y) ** 2
                r2 = nd.definition["radius"] * radius
                
                info =  f"{name}({xloc},{yloc}) -- {n}({x},{y})"
                assert d2 > r2, f"{info} -- {math.sqrt(d2)} > {math.sqrt(r2)}"
            self[key] = MoonNode(key, st, definition)

    def run(self):
        print("RUN....")
        

import math

class MoonNode(dict):
    def __init__(self, key, state, definition):
        self.definition = definition
        dict.__init__(self, state)
        self.connection = set()
        self.io = list()
        self.key = key
        
    def save_connection(self, key1, key2):
        self.connection.add(key1)
        self.connection.add(key2)

    def __str__(self):
        out = f"{self.key[0]}({self.key[1]},{self.key[2]})"
        return out

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

        for name, key1, key2, st in state["connections"]:
            assert key1 in self, f"no node found:{key1}"
            assert key2 in self, f"no node found:{key2}"
            xy = (key1[1] + key2[1]) / 2, (key1[2] + key2[2]) / 2
            definition = self.library["infra"][name]
            node = MoonNode((name, *xy), st, definition)
            node.save_connection(key1, key2)
            node.io.append(self[key1])
            node.io.append(self[key2])
            self[key1].io.append(node)
            self[key2].io.append(node)

    def find_element(self, x, y):
        min_r2, min_node = math.inf, None
        for key, node in self.items():
            r2 = (x-key[1]) ** 2 + (y-key[2]) ** 2
            if r2 < min_r2: min_node, min_r2 = node, r2
            for nd in node.io:
                r2 = (x-nd.key[1]) ** 2 + (y-nd.key[2]) ** 2
                if r2 < min_r2: min_node, min_r2 = nd, r2
        return min_node, min_r2

    def run(self):
        for val in self.values(): print(val)
        print("RUN....")
        

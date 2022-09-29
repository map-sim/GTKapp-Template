import math

class MoonNode(dict):
    def __init__(self, key, state, definition):
        self.definition = definition
        dict.__init__(self, state)
        self.__newvals = {}
        self.ios = list()
        self.key = key
        
    def commit(self):
        total_goods = 0
        keys = self.__newvals.keys() | self.keys()
        for key in keys:
            vol = self.__newvals.get(key, 0)
            if vol == 0: vol = self[key]
            total_goods += vol        
        capacity = self.definition["capacity"]
        if total_goods > capacity:
            factor = capacity / total_goods
        else: factor = 1.0
        for key in keys:
            vol = self.__newvals.get(key, 0)
            if vol == 0: vol = self[key]
            dict.__setitem__(self, key, vol * factor)
        self.__newvals = {}

    def __setitem__(self, key, value):
        self.__newvals[key] = value

    def __str__(self):
        out = f"{self.key[0]}({self.key[1]},{self.key[2]}) --> "
        for key, value in self.items():
            out += f"{key}: {round(value, 2)} "
        return f"{out}"

class MoonSystem(dict):
    def __init__(self, state, library):
        dict.__init__(self)
        self.library = library
        self.state = state

        for key, st in state["elements"]:
            name, xloc, yloc = key
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
            node.ios.append(self[key1])
            node.ios.append(self[key2])
            self[key1].ios.append(node)
            self[key2].ios.append(node)

    def find_element(self, x, y):
        min_r2, min_node = math.inf, None
        for key, node in self.items():
            r2 = (x-key[1]) ** 2 + (y-key[2]) ** 2
            if r2 < min_r2: min_node, min_r2 = node, r2
            for nd in node.ios:
                r2 = (x-nd.key[1]) ** 2 + (y-nd.key[2]) ** 2
                if r2 < min_r2: min_node, min_r2 = nd, r2
        return min_node, min_r2
    
    def check_sources(self, xloc, yloc):
        output = dict()
        for good, config in self.state["source"].items():
            if config["method"] == "additive-cones":
                max_value = config["max-amplitude"]
                output[good] = 0.0  
                for point in config["points"]:
                    x, y, a, r = point
                    d2 = (xloc-x)**2 + (yloc-y)**2
                    d = math.sqrt(d2)
                    if d > r: continue
                    output[good] += a * d / r
                if output[good] > max_value:
                    output[good] = max_value
            else: raise ValueError("unknown good-method")
        return output

    def fill_source(self, node, dtime):
        assert node.definition["type"] == "source"
        sources = self.check_sources(node.key[1], node.key[2])
        for good, value in sources.items():
            if "goods" in node.definition:
                goods = node.definition["goods"]
                if good not in goods: continue
            node[good] += value * dtime

    def fuse_pipelines(self, connections):
        analyzed = set()
        for key, pipe in connections.items():
            if len(pipe.ios) != 2: continue
            if key in analyzed: continue
            analyzed.add(key)
            blind = False

            pipe_key = key
            node = pipe.ios[0]
            start_pipeline = [node]
            while node.definition["type"] == "node":
                if len(node.ios) < 2: blind = True; break
                if pipe_key != node.ios[0].key: n_pipe = node.ios[0]
                elif pipe_key != node.ios[1].key: n_pipe = node.ios[1]
                else: raise ValueError("internal error!")
                start_pipeline.append(n_pipe)
                analyzed.add(n_pipe.key)
                pipe_key = n_pipe.key

                if len(n_pipe.ios) < 2: blind = True; break
                if n_pipe.ios[0].key != node.key: node = n_pipe.ios[0]
                elif n_pipe.ios[1].key != node.key: node = n_pipe.ios[1]
                else: raise ValueError("internal error!")
                start_pipeline.append(node)

            pipe_key = key
            node = pipe.ios[1]
            stop_pipeline = [node]                        
            while node.definition["type"] == "node":
                if len(node.ios) < 2: blind = True; break
                if pipe_key != node.ios[0].key: n_pipe = node.ios[0]
                elif pipe_key != node.ios[1].key: n_pipe = node.ios[1]
                else: raise ValueError("internal error!")
                stop_pipeline.append(n_pipe)
                analyzed.add(n_pipe.key)
                pipe_key = n_pipe.key

                if len(n_pipe.ios) < 2: blind = True; break
                if n_pipe.ios[0].key != node.key: node = n_pipe.ios[0]
                elif n_pipe.ios[1].key != node.key: node = n_pipe.ios[1]
                else: raise ValueError("internal error!")
                stop_pipeline.append(node)
            
            pipeline = list(reversed(start_pipeline))
            pipeline += [pipe] + stop_pipeline
            if not blind: yield pipeline
            
    def run(self, dtime):
        print("RUN....")

        connections = {}
        for key, node in self.items():
            if not node.ios: continue
            # print("node", key, f"has {len(node.ios)} connection(s)")
            for io in node.ios: assert io.definition["type"] == "pipe"
            for io in node.ios: connections[io.key] = io
        print("found uniq connections:", len(connections))
        for pipeline in self.fuse_pipelines(connections):
            print("p-l", [n.key for n in pipeline])
        
        for node in self.values():
            if node.definition["type"] == "source":
                self.fill_source(node, dtime)
        for node in self.values():
            node.commit()

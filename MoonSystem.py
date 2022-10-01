import math

class MoonNode(dict):
    def __init__(self, key, state, definition):
        self.definition = definition
        dict.__init__(self, state)
        self.__newvals = {}
        self.ios = list()
        self.key = key

    def is_pipe(self):
        return self.get_def("type") == "pipe"
    def get_def(self, key):
        return self.definition[key]

    # def commit(self):
    #     total_goods = 0
    #     keys = self.__newvals.keys() | self.keys()
    #     for key in keys:
    #         vol = self.__newvals.get(key, 0)
    #         if vol == 0: vol = self[key]
    #         total_goods += vol        
    #     capacity = self.definition["capacity"]
    #     if total_goods > capacity:
    #         factor = capacity / total_goods
    #     else: factor = 1.0
    #     for key in keys:
    #         vol = self.__newvals.get(key, 0)
    #         if vol == 0: vol = self[key]
    #         dict.__setitem__(self, key, vol * factor)
    #     self.__newvals = {}
    # 
    # def __setitem__(self, key, value):
    #     self.__newvals[key] = value

    def __str__(self):
        out = f"{self.key[0]}({self.key[1]},{self.key[2]}) --> "
        for key, value in self.items():
            out += f"{key}: {round(value, 2)} "
        return f"{out}"

class MoonPipeline(list):
    def __init__(self, system, pipeline):
        list.__init__(self, pipeline)
        self.system = system

        self.length = 0.0
        self.bandwidth = math.inf
        for item in self:
            if item.get_def("type") in ["pipe", "node"]:
                if item.get_def("bandwidth") < self.bandwidth:
                    self.bandwidth = item.get_def("bandwidth")
            if item.is_pipe():
                self.good = item.get_def("good")
                xyo, xye = item.ios[0].key[1:], item.ios[1].key[1:]
                d2 = (xye[0] - xyo[0]) ** 2 + (xye[1] - xyo[1]) ** 2
                self.length += math.sqrt(d2)
        assert self.bandwidth > 0.0
        assert self.length > 0.0

        good_definition = system.library["goods"][self.good]
        self.stickiness = good_definition["stickiness"]

    def __str__(self):
        lstr = round(self.length, 2)
        bwstr = round(self.bandwidth, 2)
        start, stop = self[0].key, self[-1].key
        output = f"PIPELINE({len(self)})  len-{lstr}"
        output += f" bw-{bwstr} ({start} <--> {stop}"
        return output

    def estimate_transfer(self):
        # if item.get_def("type") == ""
        return 0.0
    
class MoonSystem(dict):
    def __init__(self, state, library):
        dict.__init__(self)
        self.library = library
        self.state = state

        for (name, xloc, yloc), st in state["elements"]:
            newdef = self.library["infra"][name]
            radius = newdef["radius"]
            for (n, x, y), nd in self.items():
                d2 = (xloc - x) ** 2 + (yloc - y) ** 2
                r2 = nd.get_def("radius") * radius                
                info =  f"{name}({xloc},{yloc}) -- {n}({x},{y})"
                assert d2 > r2, f"{info} -- {math.sqrt(d2)} > {math.sqrt(r2)}"
            self[name, xloc, yloc] = MoonNode((name, xloc, yloc), st, newdef)

        for name, key1, key2, st in state["connections"]:
            assert key1 in self, f"no node found:{key1}"
            assert key2 in self, f"no node found:{key2}"
            xy = (key1[1] + key2[1]) / 2, (key1[2] + key2[2]) / 2
            node = MoonNode((name, *xy), st, self.library["infra"][name])
            node.ios.extend([self[key1], self[key2]])
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
        assert node.get_def("type") == "source"
        sources = self.check_sources(node.key[1], node.key[2])
        for good, value in sources.items():
            if "goods" in node.definition:
                goods = node.get_def("goods")
                if good not in goods: continue
            node[good] += value * dtime

    def find_elementary_connections(self):
        connections = {}
        for key, node in self.items():
            if not node.ios: continue
            for io in node.ios: assert io.is_pipe()
            for io in node.ios: connections[io.key] = io
        print("found uniq connections:", len(connections))
        return connections

    def fuse_pipelines(self, connections):
        analyzed = set()
        for key, pipe in connections.items():
            if len(pipe.ios) != 2: continue
            if key in analyzed: continue
            good = pipe.get_def("good")
            analyzed.add(key)
            blind = False
            
            pipe_key = key
            node = pipe.ios[0]
            start_pipeline = [node]
            while node.get_def("type") == "node":
                if len(node.ios) < 2: blind = True; break
                if pipe_key != node.ios[0].key: n_pipe = node.ios[0]
                elif pipe_key != node.ios[1].key: n_pipe = node.ios[1]
                else: raise ValueError("internal error!")
                if good != n_pipe.get_def("good"): blind = True; break
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
            while node.get_def("type") == "node":
                if len(node.ios) < 2: blind = True; break
                if pipe_key != node.ios[0].key: n_pipe = node.ios[0]
                elif pipe_key != node.ios[1].key: n_pipe = node.ios[1]
                else: raise ValueError("internal error!")
                if good != n_pipe.get_def("good"): blind = True; break
                stop_pipeline.append(n_pipe)
                analyzed.add(n_pipe.key)
                pipe_key = n_pipe.key

                if len(n_pipe.ios) < 2: blind = True; break
                if n_pipe.ios[0].key != node.key: node = n_pipe.ios[0]
                elif n_pipe.ios[1].key != node.key: node = n_pipe.ios[1]
                else: raise ValueError("internal error!")
                stop_pipeline.append(node)            
            if blind: continue

            pipeline = list(reversed(start_pipeline))
            pipeline += [pipe] + stop_pipeline
            yield MoonPipeline(self, pipeline)
            
    def run(self, dtime):
        print("RUN....")

        connections = self.find_elementary_connections()
        for pipeline in self.fuse_pipelines(connections):
            print(pipeline)
            print(pipeline.estimate_transfer())

        for node in self.values():
            if node.get_def("type") == "source":
                self.fill_source(node, dtime)

        # for node in self.values():
        #     node.commit()

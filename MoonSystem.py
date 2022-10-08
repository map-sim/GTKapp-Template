import math

class MoonNode(dict):
    def __init__(self, key, state, definition):
        self.definition = definition
        dict.__init__(self, state)
        self.ios = list()
        self.key = key

    def is_accelerator(self):
        return self.get_def("type") == "accelerator"
    def is_pipe(self):
        return self.get_def("type") == "pipe"
    def get_def(self, key):
        return self.definition[key]
    def has_def(self, key):
        return key in self.definition
    def get_capacity(self):
        return self.definition["capacity"]
    def get_empty_space(self):
        total_goods = 0
        for key in self.keys():
            vol = self.get(key, 0)
            total_goods += vol
        capacity = self.definition["capacity"]
        return capacity - total_goods

    def __str__(self):
        out = f"{self.key[0]}({self.key[1]},{self.key[2]}) --> "
        for key, value in self.items():
            out += f"{key}: {round(value, 2)} "
        return f"{out}"

class MoonPipeline(list):
    node_transfer_types = {
        "accelerator": ["active", "dynamic"],
        "source": ["passive", "source"],
        "inner": ["passive", "sink"],
        "outer": ["passive", "sink"],
        "barrier": ["passive", "sink"],
        "mixer": ["passive", "mixer"],
        "store": ["passive", "dynamic"]
    }
        
    def __init__(self, system, pipeline):
        list.__init__(self, pipeline)
        self.system = system

        self.length = 0.0
        self.bandwidth = math.inf
        for item in self:
            if item.get_def("type") == "node":
                if item.get_def("bandwidth") < self.bandwidth:
                    self.bandwidth = item.get_def("bandwidth")
            if item.is_pipe():
                max_switch = item.get_def("switch") - 1                
                dbw = item.get_def("bandwidth") / max_switch
                bandwitch = dbw * item["switch"]
                if bandwitch < self.bandwidth:
                    self.bandwidth = bandwitch                
            if item.is_pipe():
                self.good = item.get_def("good")
                xyo, xye = item.ios[0].key[1:], item.ios[1].key[1:]
                d2 = (xye[0] - xyo[0]) ** 2 + (xye[1] - xyo[1]) ** 2
                self.length += math.sqrt(d2)
        assert 0.0 <= self.bandwidth < math.inf
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
        if self[0].has_def("goods"):
            if self.good not in self[0].get_def("goods"):
                self.estimated_transfer = 0.0
                return self.estimated_transfer
        if self[-1].has_def("goods"):
            if self.good not in self[-1].get_def("goods"):
                self.estimated_transfer = 0.0
                return self.estimated_transfer
            
        type_o =  self[0].get_def("type")
        type_e = self[-1].get_def("type")
        gain_o, role_o = self.node_transfer_types[type_o]
        gain_e, role_e = self.node_transfer_types[type_e]

        ond, end = "dynamic", "dynamic"
        if role_o == "source": ond = "in"
        elif role_o == "sink": ond = "out"
        elif role_o == "mixer":
            proc_good = self[0].get_def("process")
            in_goods = self.system.library["goods"][proc_good]["process"].keys()
            if self.good in in_goods: ond = "out"
            elif proc_good == self.good: ond = "in"
            else:
                self.estimated_transfer = 0.0
                return self.estimated_transfer
        
        if role_e == "source": end = "in"
        elif role_e == "sink": end = "out"
        elif role_e == "mixer":
            proc_good = self[-1].get_def("process")
            in_goods = self.system.library["goods"][proc_good]["process"].keys()
            if self.good in in_goods: end = "out"
            elif proc_good == self.good: end = "in"
            else:
                self.estimated_transfer = 0.0
                return self.estimated_transfer
        if ond == end != "dynamic":
            self.estimated_transfer = 0.0
            return self.estimated_transfer

        o_volume = self[0][self.good]
        e_volume = self[-1][self.good]        
        o_empty = self[0].get_empty_space()
        e_empty = self[-1].get_empty_space()
        o_cap = self[0].get_capacity()
        e_cap = self[-1].get_capacity()

        o_frac = o_empty / o_cap
        e_frac = e_empty / e_cap

        st = self.system.library["goods"][self.good]["stickiness"]
        factor1 = self.bandwidth / (1.0 + self.length * st)
        if "dynamic" == ond == end:
            if e_frac > o_frac: direction = 1
            else: direction = -1
        elif ond == "in": direction = 1
        elif ond == "out": direction = -1
        elif end == "in": direction = -1
        elif end == "out": direction = 1
        else: raise ValueError("internal-error")

        if direction == 1:
            factor2 = (e_frac / o_frac) / (1.0 + e_frac / o_frac)
        else: factor2 = (o_frac / e_frac) / (1.0 + o_frac / e_frac)
        self.estimated_transfer = direction * factor1 * factor2
        if gain_o == "active":
            self.estimated_transfer *= self[0].get_def("factor")
        if gain_e == "active":
            self.estimated_transfer *= self[-1].get_def("factor")
        return self.estimated_transfer

    
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
                    output[good] += a * (r-d) / r
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
            pipe_obj= MoonPipeline(self, pipeline)
            yield pipe_obj

    def run(self, dtime):
        print("RUN....")

        connections = self.find_elementary_connections()
        for pipeline in self.fuse_pipelines(connections):
            print(pipeline, "----", pipeline.estimate_transfer())

        for node in self.values():
            if node.get_def("type") == "source":
                self.fill_source(node, dtime)

        # for node in self.values():
        #     node.commit()

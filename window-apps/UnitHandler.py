#!/usr/bin/python3

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

    def get_order_nodes(self, order_id=None):
        unit = self.battlefield["units"][self.uid]
        if "orders" not in unit: return []
        setnodes, nodes = set(), list()
        for ix, order in enumerate(unit["orders"]):
            if order_id is not None and order_id != ix: continue
            if order[0] == "destroy": nodes = [order[-1]]
            elif order[0] == "move": nodes = list(order[2:])
            elif order[0] == "landing": nodes = list(order[3:])
            elif order[0] == "supply": nodes = list(order[3:-1])
            elif order[0] == "store": nodes = list(order[3:])
            elif order[0] == "take": nodes = list(order[3:])
            elif order[0] == "demolish": nodes = [order[-1]]
            elif order[0] == "transfer": continue
            else: raise ValueError(order[0])
            for node in nodes: setnodes.add(node)
        return list(setnodes)

import math

def load_data(filename):
    products = {}
    with open(filename) as file:
        for line in file.readlines():
            p = dict()
            [precursors, product] = line.split("=>")
            [min_order, product_name] = product.strip().split(" ")
            precursors = precursors.strip()
            p["min_order"] = int(min_order)
            p["on_hand"] = 0
            pre = []
            for i in [x.strip() for x in precursors.split(",")]:
                qty, pre_name = i.split(" ")
                pre.append((pre_name, int(qty)))
            p["precursors"] = pre
            products[product_name] = p
    return products

def request(products, product_name, requested_qty, depth = 0):
    debug = 0
    ore_mined = 0
    depth += 1
    if debug:
        print(" " * depth + "requesting %d %s" % (requested_qty, product_name))
    if product_name == "ORE":
        if debug:
            print(" " * depth + "mining ORE")
        #ore_mined += requested_qty
        return requested_qty
    p = products[product_name]

    #if we have enough on hand, use it
    if p["on_hand"] >= requested_qty:
        if debug:
            print(" " * depth + "using %d onhand" % p["on_hand"])
        p["on_hand"] -= requested_qty
        return 0
    else:
        #otherwise, figure out how much we need to request
        required_qty = requested_qty - p["on_hand"]

    #round up order to closest orderable amount
    orderable_qty = math.ceil(required_qty/p["min_order"]) * p["min_order"]
    multiplier = orderable_qty // p["min_order"]

    if debug:
        print(" " * depth + "%d (x%d) %s requires:" % (orderable_qty, multiplier, product_name))
    for pre, pre_qty in products[product_name]["precursors"]:
        if debug:
            print(" " * depth + " %d %s" % (pre_qty * multiplier, pre))
        ore_mined += request(products, pre, pre_qty * multiplier, depth)
    p["on_hand"] += orderable_qty
    p["on_hand"] -= requested_qty
    return ore_mined

def part2():
    fuel = 1
    closest_under = None
    closest_over = None

    while True:
        ore = request(products, "FUEL", fuel)
        if ore == 1e12:
            return fuel
        elif ore < 1e12:
            if closest_under is None or fuel > closest_under:
                closest_under = fuel
        else:
            if closest_over is None or fuel < closest_over:
                closest_over = fuel
        if closest_over is None:
            fuel *= 2
        else:
            last = fuel
            fuel = (closest_under + closest_over) // 2
            if fuel == last:
                return fuel

products = load_data("14.txt")
print(request(products, "FUEL", 1))
print(part2())

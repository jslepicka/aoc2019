view = {}
#k=name
#v=[locs]
portal_locs = {}

#k=loc
#v=(name,dir)
portal_info = {}

NORTH = 0
SOUTH = 1
WEST = 2
EAST = 3

start_loc = (0,0)
end_loc = (0,0)
half_x = 0
half_y = 0

def print_view(view):
    max_x = max([x for x, y in view])
    max_y = max([y for x, y in view])
    min_x = min([x for x, y in view])
    min_y = min([y for x, y in view])
    for y in range(min_y, max_y + 1):
        line = ""
        for x in range(min_x, max_x + 1):
            if (x,y) not in view:
                line += " "
            else:
                line += view[(x,y)]
        print(line)

def is_portal(loc, dir):
    #if this is a portal location, return the destination
    if loc in portal_info:
        (name, d) = portal_info[loc]
        if d == dir:
            #find opposite
            dests = portal_locs[name]
            if dests[0] == loc:
                return dests[1]
            else:
                return dests[0]
    return None

def get_portal_dest(loc):
    print("looking up destination for %d" % loc)

def get_neighbors(view, loc, level = None):
    #given a location, loc, return a list of all traversable neighbors
    
    #(loc, level_adjust)
    neighbors = []
    x, y = loc
    check_dirs = {
        NORTH:  (x, y-1),
        SOUTH:  (x, y+1),
        WEST:   (x-1, y),
        EAST:   (x+1, y)
    }
    for dir in range(4):
        next_loc = check_dirs[dir]
        if view.get(next_loc) == ".":
            if level is not None:
                neighbors.append((next_loc, 0))
            else:
                neighbors.append(next_loc)
        elif view[loc] == '.':
            p = is_portal(loc, dir)
            if p:
                level_adjust = 0
                p_x = loc[0]
                p_y = loc[1]
                if dir == NORTH:
                    level_adjust = -1 if p_y < half_y else 1
                elif dir == SOUTH:
                    level_adjust = 1 if p_y < half_y else -1
                elif dir == WEST:
                    level_adjust = -1 if p_x < half_x else 1
                elif dir == EAST:
                    level_adjust = 1 if p_x < half_x else -1
                #print("portal %d %s at %d, %d %d" % (dir, portal_info[(p_x, p_y)][0], p_x, p_y, level_adjust))
                if not (level == 0 and level_adjust == -1):
                    if level is not None:
                        neighbors.append((p, level_adjust))
                    else:
                        neighbors.append(p)
    return neighbors

def load_map(filename):
    global view, start_loc, end_loc, half_x, half_y
    with open(filename) as file:
        y = 0
        for l in file.readlines():
            for x, c in enumerate(l.rstrip()):
                view[(x, y)] = c
            y += 1
    for v in view:
        if view[v] == '.':
            (x,y) = v
            #direction to travel to enter portal
            check_dirs = {
                WEST:   [(x-2, y), (x-1, y)],
                EAST:   [(x+1, y), (x+2, y)],
                NORTH:  [(x, y-2), (x, y-1)],
                SOUTH:  [(x, y+1), (x, y+2)]
            }
            for dir in check_dirs:
                a = view.get(check_dirs[dir][0])
                b = view.get(check_dirs[dir][1])
                if a is None or b is None:
                    continue
                if a.isalpha() and b.isalpha():
                    pname = a + b
                    if pname == "AA":
                        start_loc = (x,y)
                    elif pname == "ZZ":
                        end_loc = (x,y)
                    else:
                        if pname not in portal_locs:
                            portal_locs[pname] = [(x,y)]
                        else:
                            portal_locs[pname].append((x,y))
                        portal_info[(x,y)] = (pname,dir)

    half_x = max(k[0] for k in view) // 2
    half_y = max(k[1] for k in view) // 2

def part1(view, start_loc, end_loc):
    visited = {}
    queue = []
    queue.append((start_loc, 0))
    while (queue):
        loc, depth = queue.pop(0)
        if loc == end_loc:
            return depth
        visited[loc] = 1
        for n in get_neighbors(view, loc):
            if n not in visited:
                visited[loc] = 1
                queue.append((n, depth + 1))

def part2(view, start_loc, end_loc):
    visited = {}
    queue = []
    level = 0
    depth = 0
    queue.append((start_loc, level, depth))
    visited[(start_loc,level)] = 1
    while (queue):
        loc, level, depth = queue.pop(0)
        if loc == end_loc and level == 0:
            return depth
        for n, level_adjust in get_neighbors(view, loc, level):
            new_level = level
            if level_adjust != 0:
                new_level = level + level_adjust
            if (n, new_level) not in visited:
                visited[(n, new_level)] = 1
                queue.append((n, new_level, depth + 1))
    return depth

load_map("20.txt")
print(part1(view, start_loc, end_loc))
print(part2(view, start_loc, end_loc))
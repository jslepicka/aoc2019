import re
import os

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



view = {}
with open("20.txt") as file:
    y = 0
    for l in file.readlines():
        for x, c in enumerate(l.rstrip()):
            view[(x, y)] = c
        y += 1


print_view(view)
#k=name
#v=[locs]
portal_locs = {}

#k=loc
#v=(name,dir)
portal_info = {}

seen = {}

NORTH = 0
SOUTH = 1
WEST = 2
EAST = 3

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


def get_neighbors(loc):
    #given a location, loc, return a list of all traversable neighbors
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
            neighbors.append(next_loc)
        else:
            p = is_portal(loc, dir)
            if p:
                neighbors.append(p)
    return neighbors

def part1():
    start_loc = (0,0)
    end_loc = (0,0)
    for v in view:
        if view[v] == '.':
            (x,y) = v
            #direction to travel to enter portal
            check_dirs = {
                WEST:     [(x-2, y), (x-1, y)],
                EAST:    [(x+1, y), (x+2, y)],
                NORTH:       [(x, y-2), (x, y-1)],
                SOUTH:     [(x, y+1), (x, y+2)]
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
                        print("%s portal %s at %d, %d" % (dir, pname, x, y))
    print(portal_locs)
    print(portal_info)
    visited = {}
    queue = []
    queue.append((start_loc, 0))
    while (queue):
        loc, depth = queue.pop(0)
        visited[loc] = 1
        for n in get_neighbors(loc):
            if n not in visited:
                queue.append((n, depth + 1))
        view[loc] = 'X'
        if loc == end_loc:
            return depth

print(part1())

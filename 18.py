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

def load_map(filename):
    view = {}
    start = (0,0)
    num_keys = 0
    with open(filename) as f:
        for y, l in enumerate(f.readlines()):
            for x, c in enumerate(l.strip()):
                view[(x, y)] = c
                if c == '@':
                    start = (x,y)
                elif c.islower():
                    num_keys += 1
    return view, start, num_keys

view, start, num_keys = load_map("18.txt")
print ("start at %d, %d %d keys" % (start[0], start[1], num_keys))
print_view(view)

def part1(view, start, num_keys):
    ALL_KEYS = 2**num_keys - 1
    visited = {}
    keys = 0
    depth = 0
    queue = []
    queue.append((start, keys, depth))
    visited[(start, keys)] = 1
    while (queue):
        loc, keys, depth = queue.pop(0)
        #print(loc, keys)
        #print_view(view)
        if keys == ALL_KEYS:
            print("done at %d" % depth)
            return depth
        #now check if neighbors are traversible.
        #up, down, left, right
        dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for d in dirs:
            x = loc[0] + d[0]
            y = loc[1] + d[1]
            c = view.get((x,y))
            next_loc = None
            next_keys = keys
            if c == '.' or c == '@':
                next_loc = (x,y)
            elif c.islower(): #key
                k = 1 << (ord(c) - ord('a'))
                new_keys = keys | k
                #print("found key %s, new_keys: %d" % (c, new_keys))
                next_loc = (x,y)
                next_keys = new_keys
            elif c.isupper():
                #print("found door %s" % (c))
                door = 1 << (ord(c) - ord('A'))
                #print("%d %d" % (door, keys))
                if door & keys:
                    #print("we have the key")
                    next_loc = (x,y)
            if next_loc is not None:
                if (next_loc, next_keys) not in visited:
                    queue.append((next_loc, next_keys, depth+1))
                    visited[(next_loc, next_keys)] = 1
                


print(part1(view, start, num_keys))
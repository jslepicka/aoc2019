from intcode_machine import intcode_machine

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

class decision:
    def __init__(self, entered_from):
        self.choices = [1, 2, 3, 4]
        self.entered_from = entered_from
        if entered_from is not None:
            self.choices.remove(entered_from)
    def get_choice(self):
        if len(self.choices) > 0:
            #print(self.choices)
            d = self.choices.pop(0)
            #print("d: %d" % d)
            return d
        else:
            return self.entered_from

def part1():
    view = {}
    decisions = {}
    nodes = {}

    im = intcode_machine()
    im.load_mem("15.txt")
    x = 0
    y = 0
    last_x = 0
    last_y = 0
    view[(x,y)] = '\u2593'
    decisions[(x,y)] = decision(None)
    o2_coord = (0,0)
    nodes[(0,0)] = []
    while not im.halted:
        ret, val = im.run()

        if ret == im.OPCODE_INPUT:
            #N = 1, S = 2, W = 3, E = 4
            i = decisions[(x,y)].get_choice()
            if i is None:
                break
            #print("loc: %d, %d, decision: %i" % (x,y,i))
            last_x = x
            last_y = y
            if i == 1:
                y -= 1
            elif i == 2:
                y += 1
            elif i == 3:
                x -= 1
            elif i == 4:
                x += 1
            if (x,y) not in decisions:
                ef = 0
                if i & 1:
                    ef = i + 1
                else:
                    ef = i - 1
                decisions[(x,y)] = decision(ef)
                #view[(x,y)] = '?'
            im.add_input(i)
        elif ret == im.OPCODE_OUTPUT:
            #print(val)
            #print((x,y))
            if val == 0: #hit a wall
                #print("hit wall at %d, %d, moving back to %d, %d" % (x, y, last_x, last_y))
                view[(x,y)] = '#'
                x = last_x
                y = last_y
            elif val == 1 or val == 2 and (x,y) not in view:
                view[(x,y)] = '.'
                if val == 2:
                    view[(x,y)] = '\u2588'
                    o2_coord = (x,y)
                if (x,y) not in nodes:
                    nodes[(x,y)] = [(last_x, last_y)]
                    nodes[(last_x, last_y)].append((x,y))

            #print_view(view)
    print(len(view))
    print_view(view)
    return view, nodes, o2_coord

def part2(coord, limit = None):
    visited = {}
    queue = []
    queue.append((coord, 0))
    visited[coord] = 1
    depth = 0
    while queue:
        s, d = queue.pop(0)
        if limit is not None and s == limit:
            return d
        if d > depth:
            depth = d
        for n in nodes[s]:
            if n not in visited:
                queue.append((n, d + 1))
                visited[n] = 1
    return depth

view, nodes, o2_coord = part1()
print(part2((0,0), o2_coord))
print(part2(o2_coord))


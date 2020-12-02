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

def load_data(filename):
    view = {}
    with open(filename) as file:
        for y, l in enumerate(file.readlines()):
            for x, c in enumerate(l.rstrip()):
                view[(x,y)] = c
    return view


def get_adjacent_bug_count(view, x, y):
    #up, down, left, right
    offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    count = 0
    for i, offset in enumerate(offsets):
        x2 = x + offset[0]
        y2 = y + offset[1]
        c = view.get((x2, y2), '.')
        if c == '#':
            count += 1
    return count

def get_biodiversity(view):
    b = 0
    for y in range(5):
        for x in range(5):
            shift = y * 5 + x
            v = 1 if view[(x,y)] == '#' else 0
            b |= (v << shift)
    return b


def part1():
    view = load_data("24.txt")
    history = {}

    m = 0
    while True:
        next_view = {}
        print("minute %d" % (m))
        print_view(view)
        b = get_biodiversity(view)
        print("biodiversity %d" % (b))
        if b in history:
            when = history[b]
            print("saw layout before at minute %d" % (when))
            return b
        else:
            history[b] = m
        print("\n")
        for y in range(5):
            for x in range(5):
                k = (y * 5) + x
                adj_count = get_adjacent_bug_count(view, x, y)
                if view[(x,y)] == '#' and adj_count != 1:
                    next_view[(x,y)] = '.'
                elif view[(x,y)] == '.' and (adj_count > 0 and adj_count < 3):
                    next_view[(x,y)] = '#'
                else:
                    next_view[(x,y)] = view[(x,y)]
        view = next_view
        m += 1

print(part1())
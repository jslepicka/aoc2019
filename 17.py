from intcode_machine import intcode_machine

def part1():
    im = intcode_machine()
    im.load_mem("17.txt")
    x = 0
    y = 0
    view = {}
    line = ""
    while not im.halted:
        ret, data = im.run()
        if ret == im.OPCODE_OUTPUT:
            if data == 10: #newline
                y += 1
                x = 0
            else:
                view[(x,y)] = chr(data)
                x += 1

    max_x = max([x for x, y in view])
    max_y = max([y for x, y in view])
    min_x = min([x for x, y in view])
    min_y = min([y for x, y in view])
    intersections = []
    for y in range(min_y, max_y + 1):
        line = ""
        for x in range(min_x, max_x):
            if view[(x,y)] == '#' and x > min_x and x < max_x and y > min_y and y < max_y:
                if view[(x-1,y)] == '#' and view[(x+1, y)] == '#' and view[(x, y-1)] == '#' and view[(x, y+1)] == '#':
                    line += 'O'
                    intersections.append((x,y))
                else:
                    line += view[(x,y)]
            else:
                line += view[(x,y)]
        print(line)
    print(sum([x * y for x,y in intersections]))

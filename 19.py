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

def check_loc(x, y):
    im = intcode_machine("19.txt")
    im.reset()
    input_phase = 0
    while not im.halted:
        ret, data = im.run()
        if ret == im.OPCODE_INPUT:
            im.add_input((x,y)[input_phase])
            input_phase ^= 1
        elif ret == im.OPCODE_OUTPUT:
            return True if data == 1 else False

def part1():
    view = {}

    for y in range(50):
        for x in range(50):
            view[(x,y)] = "#" if check_loc(x, y) else "."

    print_view(view)
    affected_count = list(view.values()).count("#")
    return affected_count

#instead of searching whole space, travel down the left side,
#incrementing x if the space is empty, and checking up and to the right
#99 units to see if the beam exists there
#
#I spent hours attempting to solve with trig.  The beam doesn't behave
#as expected

def part2():
    x = 0
    #start at 10 since first few rows are flaky
    for y in range(10,5000):
        input_phase = 0
        inside_beam = 0
        found = 0
        while not inside_beam:
            inside_beam = check_loc(x,y)
            if inside_beam:
                if check_loc(x+99, y-99):
                    return x * 10000 + (y-99)
            else:
                x += 1

print(part1())
print(part2())

                



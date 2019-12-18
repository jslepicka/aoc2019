from intcode_machine import intcode_machine

view = {}

def part1():
    im = intcode_machine()
    im.load_mem("17.txt")
    x = 0
    y = 0

    line = ""
    while not im.halted:
        ret, data = im.run()
        if ret == im.OPCODE_OUTPUT:
            if data == 10:  # newline
                y += 1
                x = 0
            else:
                view[(x, y)] = chr(data)
                x += 1

    max_x = max([x for x, y in view])
    max_y = max([y for x, y in view])
    min_x = min([x for x, y in view])
    min_y = min([y for x, y in view])
    intersections = []
    for y in range(min_y, max_y + 1):
        line = ""
        for x in range(min_x, max_x + 1):
            if view[(x, y)] == '#' and x > min_x and x < max_x and y > min_y and y < max_y:
                if view[(x-1, y)] == '#' and view[(x+1, y)] == '#' and view[(x, y-1)] == '#' and view[(x, y+1)] == '#':
                    line += 'O'
                    intersections.append((x, y))
                else:
                    line += view[(x, y)]
            else:
                line += view[(x, y)]
        print(line)

    alignment_sum = sum([x * y for x, y in intersections])
    return alignment_sum


def find_robot():
    r = {'^': 0, '>': 1, 'v': 2, '<': 3}
    for k in view:
        if view[k] in r:
            return k, r[view[k]]
    return None


move_change = {
    0: (0, -1),  # North, check up
    1: (1, 0),  # East, check right
    2: (0, 1),  # South check down
    3: (-1, 0),  # West, check left)
}

#given a pos and a dir, can the robot move there?
#return next_pos if possible, otherwise False
def moveable(pos, dir):
    next_pos = (pos[0] + move_change[dir][0], pos[1] + move_change[dir][1])
    if next_pos in view and view[next_pos] == '#':
        return next_pos
    else:
        return False

def get_funcs(string):
    for a in range(1, 21):
        for b in range(1, 21):
            for c in range(1, 21):
                groups = []
                s = string
                for x in [a, b, c]:
                    #take the first x occurences of the string
                    #aaabbbccccaaaa
                    test_str = s[0:x]
                    #e.g., if x is 3, test_str is aaa
                    #replace all occurences of that in the string with blanks, string becomes:
                    #bbbcccca
                    s = s.replace(test_str, "")
                    #store the group
                    groups.append(test_str)
                    #do this for all 3 test strings, a, b, c
                #if a, b, and c have matched all characters, we've found our solution
                if s == "":
                    print(groups)
                    repl_chars = ["A,", "B,", "C,"]
                    main = string
                    for i in range(3):
                        main = main.replace(groups[i], repl_chars[i])
                    main = main[0:-1]
                    groups = [g[0:-1] for g in groups]
                    return main, groups

def part2():
    pos, dir = find_robot()
    print(pos, dir)
    move_string = ""
    #can the robot move forward?

    move_count = 0
    deadend = 0

    #move forward while possible
    while not deadend:
        while True:
            next_pos = moveable(pos, dir)
            if next_pos:
                move_count += 1
                pos = (pos[0] + move_change[dir][0], pos[1] + move_change[dir][1])
                print("moved to %d %d" % pos)
            else:
                if move_count > 0:
                    move_string += "%d," % move_count
                    move_count = 0
                break

        next_pos = moveable(pos, (dir-1) % 4)
        if next_pos:
            print("Robot can turn left")
            dir = (dir - 1) % 4
            move_string += "L,"
        else:
            next_pos = moveable(pos, (dir + 1) % 4)
            if next_pos:
                print("Robot can turn right")
                move_string += "R,"
                dir = (dir + 1) % 4
            else:
                print("Robot at dead end")
                deadend = 1

    print(move_string)

    main, funcs = get_funcs(move_string)

    im = intcode_machine()
    im.load_mem("17.txt")
    im.mem[0] = 2

    #inputs will be main, then functions a, b, c, then n for live video feed
    inputs = []
    for x in [main, funcs[0], funcs[1], funcs[2], "n"]:
        x += chr(10)
        inputs.append(list(x))

    last_in = ""
    input_phase = 0
    output_phase = 0
    dust = 0
    while not im.halted:
        ret, data = im.run()
        if ret == im.OPCODE_OUTPUT:
            if output_phase == 3:
                dust = data
            if data == 10 and last_in == 10:
                output_phase += 1
            last_in = data
        elif ret == im.OPCODE_INPUT:
            im.add_input(ord(inputs[input_phase].pop(0)))
            if len(inputs[input_phase]) == 0:
                input_phase += 1
    return dust

print(part1())
print(part2())

from intcode_machine import intcode_machine

def paint(start_color):
    BLACK = 0
    WHITE = 1
    DIR_N = 0
    DIR_E = 1
    DIR_S = 2
    DIR_W = 3
    PHASE_COLOR = 0
    PHASE_DIRECTION = 1

    hull = {}
    painted = {}
    x = 0
    y = 0
    color = BLACK
    dir = DIR_N
    output_phase = PHASE_COLOR

    first = 1
    im = intcode_machine()
    im.load_mem("11.txt")
    while im.halted == 0:
        (ret, param) = im.run()
        if ret == im.OPCODE_INPUT:
            #provide panel color
            hull_color = 0
            if (x,y) in hull:
                hull_color = hull[(x,y)]
            else:
                hull_color = start_color if first == 1 else 0
                first = 0
            #print("hull color: %d" % hull_color)
            im.add_input(hull_color)
        elif ret == im.OPCODE_OUTPUT:
            if output_phase == PHASE_COLOR:
                color = param
                output_phase = PHASE_DIRECTION
                #print("color: %d" % color)
            elif output_phase == PHASE_DIRECTION:
                turn = param
                #print("turn: %d" % turn)
                if turn == 0:
                    turn = 3
                dir = (dir + turn) % 4
                #print("dir: %d" % dir)
                #print("painting %d, %d color %d" % (x, y, color))
                painted[(x,y)] = 1
                hull[(x,y)] = color
                if dir == DIR_N:
                    y -= 1
                elif dir == DIR_E:
                    x += 1
                elif dir == DIR_S:
                    y += 1
                elif dir == DIR_W:
                    x -= 1
                #print("now pos: %d, %d" % (x, y))
                output_phase = PHASE_COLOR
    return (hull, painted)

def part1():
    _, painted = paint(0)
    return len(painted)

def part2():
    hull, _ = paint(1)
    min_x = min(hull, key=lambda k:k[0])[0]
    max_x = max(hull, key=lambda k:k[0])[0]
    min_y = min(hull, key=lambda k:k[1])[1]
    max_y = max(hull, key=lambda k:k[1])[1]

    for y in range(min_y, max_y+1):
        char_width = 2
        line = ""
        for x in range(min_x, max_x + 1):
            pix = hull.get((x,y), None)
            char = " "
            if pix == 1:
                char = "#"
            line += char * char_width
        print(line)

print(part1())
part2()

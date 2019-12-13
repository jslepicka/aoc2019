from intcode_machine import intcode_machine
import os, sys, getopt

def part1():
    vram = {}
    im = intcode_machine()
    im.load_mem("13.txt")
    out_phase = 0
    x = 0
    y = 0
    while not im.halted:
        (ret, o) = im.run()
        if (ret == im.OPCODE_OUTPUT):
            if out_phase == 0: #x
                x = o
                out_phase += 1
            elif out_phase == 1: #y
                y = o
                out_phase += 1
            elif out_phase == 2: #tile
                vram[(x,y)] = o
                out_phase = 0
    return list(vram.values()).count(2)

SCREEN_X = 43
SCREEN_Y = 21

def draw_screen(vram, score):
    tile_chars = {
        0: ' ',
        1: '\u2591',
        2: '\u2588',
        3: '=',
        4: 'o'
    }
    os.system('cls')
    for y in range(SCREEN_Y):
        line = ""
        for x in range(SCREEN_X):
            line += tile_chars[vram[y * SCREEN_X + x]]
        print(line)
    print("SCORE: %d" % score)

def part2(draw):
    #screen is 43x21
    vram = [0] * (SCREEN_X * SCREEN_Y)
    im = intcode_machine()
    im.load_mem("13.txt")
    out_phase = 0
    x = 0
    y = 0
    im.mem[0] = 2 #free play
    ball_x = 0
    paddle_x = 0
    score = 0
    while not im.halted:
        (ret, o) = im.run()
        if (ret == im.OPCODE_OUTPUT):
            #draw_screen(vram)
            if out_phase == 0: #x
                x = o
                out_phase += 1
            elif out_phase == 1: #y
                y = o
                out_phase += 1
            elif out_phase == 2: #tile
                if x == -1: #score
                    score = o
                else:
                    if o == 4:
                        ball_x = x
                    elif o == 3:
                        paddle_x = x
                    vram[y * SCREEN_X  + x] = o
                out_phase = 0
        elif (ret == im.OPCODE_INPUT):
            if draw:
                draw_screen(vram, score)
            joy = 0
            if (paddle_x < ball_x):
                joy = 1
            elif (paddle_x > ball_x):
                joy = -1
            im.add_input(joy)
    return score

draw = False
try:
    args, _ = getopt.getopt(sys.argv[1:], "d")
    for arg, _ in args:
        if arg == '-d':
            draw = True
except getopt.GetoptError:
    pass

print(part1())
print(part2(draw))
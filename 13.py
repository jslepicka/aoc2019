from collections import deque
import os, getopt, sys

class intcode_machine:
    OPCODE_HALT = 99
    OPCODE_INPUT = 3
    OPCODE_OUTPUT = 4

    def __init__(self, mem_size = 4096):
        self.opcodes = {
            1: self.op_sum,
            2: self.op_mul,
            self.OPCODE_INPUT: self.op_input,
            self.OPCODE_OUTPUT: self.op_output,
            5: self.op_jmp_true,
            6: self.op_jmp_false,
            7: self.op_store_lt,
            8: self.op_store_eq,
            9: self.op_adj_rel_base,
            self.OPCODE_HALT: self.op_halt
        }
        self.mem_size = mem_size
        self.outp = 0
        self.reset()

    def reset(self):
        self.mem = [0] * self.mem_size
        self.input_queue = deque()
        self.pc = 0
        self.mode1 = 0
        self.mode2 = 0
        self.mode3 = 0
        self.rel_base = 0
        self.halted = 0

    def read(self, address, mode):
        a = self.mem[address]
        if mode == 0: #position (indirect)
            return self.mem[a]
        elif mode == 1: #immediate
            return a
        elif mode == 2: #relative
            return self.mem[self.rel_base + a]
        else:
            print("Invalid address mode %d in read" % mode)
            quit()
    
    def write(self, value, address, mode):
        a = self.mem[address]
        if mode == 0: #position (indirect)
            self.mem[a] = value
        elif mode == 2: #relative
            self.mem[self.rel_base + a] = value
        else:
            print("Invalid address mode %d in write" % mode)
            quit()

    def op_sum(self):
        a = self.read(self.pc+1, self.mode1)
        b = self.read(self.pc+2, self.mode2)
        self.write(a+b, self.pc+3, self.mode3)
        self.pc += 4

    def op_mul(self):
        a = self.read(self.pc+1, self.mode1)
        b = self.read(self.pc+2, self.mode2)
        self.write(a*b, self.pc+3, self.mode3)
        self.pc += 4

    def op_input(self):
        self.write(self.input_queue.popleft(), self.pc+1, self.mode1)
        self.pc += 2

    def op_output(self):
        v = self.read(self.pc+1, self.mode1)
        self.outp = v
        self.pc += 2

    def op_jmp_true(self):
        test = self.read(self.pc+1, self.mode1)
        target = self.read(self.pc+2, self.mode2)
        if test != 0:
            self.pc = target
        else:
            self.pc += 3

    def op_jmp_false(self):
        test = self.read(self.pc+1, self.mode1)
        target = self.read(self.pc+2, self.mode2)
        if test == 0:
            self.pc = target
        else:
            self.pc += 3

    def op_store_lt(self):
        a = self.read(self.pc+1, self.mode1)
        b = self.read(self.pc+2, self.mode2)
        dest = self.pc+3
        if a < b:
            self.write(1, dest, self.mode3)
        else:
            self.write(0, dest, self.mode3)
        self.pc += 4

    def op_store_eq(self):
        a = self.read(self.pc+1, self.mode1)
        b = self.read(self.pc+2, self.mode2)
        dest = self.pc+3
        if a == b:
            self.write(1, dest, self.mode3)
        else:
            self.write(0, dest, self.mode3)
        self.pc += 4

    def op_adj_rel_base(self):
        self.rel_base += self.read(self.pc+1, self.mode1)
        self.pc += 2

    def op_halt(self):
        return

    def decode_opcode(self, opcode):
            op = int(opcode % 100)
            self.mode1 = int((opcode / 100) % 10)
            self.mode2 = int((opcode / 1000) % 10)
            self.mode3 = int((opcode / 10000) % 10)
            return op

    def load_mem(self, filename):
        with open(filename) as f:
            x = f.readline()
        i = 0
        for b in x.rstrip().split(","):
            self.mem[i] = int(b)
            i += 1
    
    def add_input(self, i):
        self.input_queue.append(i)

    def run(self):
        if self.halted:
            return None
        while True:
            op = self.decode_opcode(self.mem[self.pc])
            #print("PC = %d raw = %d opcode = %d modes = %d %d %d" % (self.pc, self.mem[self.pc], op, self.mode1, self.mode2, self.mode3))
            if op == self.OPCODE_HALT:
                self.halted = 1
                return (None, None)
            elif op == self.OPCODE_INPUT and len(self.input_queue) == 0:
                return (self.OPCODE_INPUT, None)
            self.opcodes[op]()
            if op == 4:
                return (self.OPCODE_OUTPUT, self.outp)

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
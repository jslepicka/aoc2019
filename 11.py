from collections import deque

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

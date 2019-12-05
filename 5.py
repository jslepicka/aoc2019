class intcode_machine:
    OPCODE_HALT = 99

    def __init__(self):
        self.opcodes = {
            1: self.op_sum,
            2: self.op_mul,
            3: self.op_input,
            4: self.op_output,
            5: self.op_jmp_true,
            6: self.op_jmp_false,
            7: self.op_store_lt,
            8: self.op_store_eq,
            99: self.op_halt
        }
        self.reset()

    def reset(self):
        self.mem = [0] * 4096
        self.pc = 0
        self.mode1 = 0
        self.mode2 = 0
        self.mode3 = 0

    def read(self, a, mode):
        if mode == 0: #position (indirect)
            v = self.mem[a]
            print("read %d from %d" % (v, a))
            return v
        elif mode == 1: #immediate
            print("direct read %d" % a)
            return a
        print("ERR")
    
    def write(self, value, a, mode):
        if mode == 0: #position (indirect)
            print("indirect write %d to %d" % (value, a))
            self.mem[a] = value
            return
        elif mode == 1: #immediate -- invalid for writes
            print("Invalid mode!")
            quit()

    def op_sum(self):
        a = self.read(self.mem[self.pc+1], self.mode1)
        b = self.read(self.mem[self.pc+2], self.mode2)
        self.write(a+b, self.mem[self.pc+3], self.mode3)
        self.pc += 4

    def op_mul(self):
        a = self.read(self.mem[self.pc+1], self.mode1)
        b = self.read(self.mem[self.pc+2], self.mode2)
        self.write(a*b, self.mem[self.pc+3], self.mode3)
        self.pc += 4

    def op_input(self):
        print("Input:")
        i = int(input())
        print("User input %d" % (i))
        self.write(i, self.mem[self.pc+1], self.mode1)
        self.pc += 2

    def op_output(self):
        v = self.read(self.mem[self.pc+1], self.mode1)
        print("Output: %d" % (v))
        self.pc += 2

    def op_jmp_true(self):
        test = self.read(self.mem[self.pc+1], self.mode1)
        target = self.read(self.mem[self.pc+2], self.mode2)
        if test != 0:
            self.pc = target
        else:
            self.pc += 3

    def op_jmp_false(self):
        test = self.read(self.mem[self.pc+1], self.mode1)
        target = self.read(self.mem[self.pc+2], self.mode2)
        if test == 0:
            self.pc = target
        else:
            self.pc += 3

    def op_store_lt(self):
        a = self.read(self.mem[self.pc+1], self.mode1)
        b = self.read(self.mem[self.pc+2], self.mode2)
        dest = self.mem[self.pc+3]
        if a < b:
            self.write(1, dest, self.mode3)
        else:
            self.write(0, dest, self.mode3)
        self.pc += 4

    def op_store_eq(self):
        a = self.read(self.mem[self.pc+1], self.mode1)
        b = self.read(self.mem[self.pc+2], self.mode2)
        dest = self.mem[self.pc+3]
        if a == b:
            self.write(1, dest, self.mode3)
        else:
            self.write(0, dest, self.mode3)
        self.pc += 4

    def op_halt(self):
        return

    def decode_opcode(self, opcode):
            op = int(opcode % 100)
            self.mode1 = int((opcode / 100) % 2)
            self.mode2 = int((opcode / 1000) % 2)
            self.mode3 = int((opcode / 10000) % 2)
            return op

    def load_mem(self, filename):
        with open(filename) as f:
            x = f.readline()
            i = 0
        for b in x.rstrip().split(","):
            self.mem[i] = int(b)
            i += 1

    def run(self):
        while True:
            op = self.decode_opcode(self.mem[self.pc])
            print("PC = %d raw = %d opcode = %d modes = %d %d %d" % (self.pc, self.mem[self.pc], op, self.mode1, self.mode2, self.mode3))
            if op == self.OPCODE_HALT:
                break
            self.opcodes[op]()

im = intcode_machine()
im.load_mem("5.txt")
im.run()

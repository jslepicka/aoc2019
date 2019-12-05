mem = []

def load_mem():
    global mem
    mem = [0] * 4096
    with open("5.txt") as f:
        x = f.readline()
        i = 0
        for b in x.rstrip().split(","):
            mem[i] = int(b)
            i += 1

def read(a, mode):
    if mode == 0: #position (indirect)
        v = mem[a]
        print("read %d from %d" % (v, a))
        return v
    elif mode == 1: #immediate
        print("direct read %d" % a)
        return a
    print("ERR")
    return
def write(value, a, mode):
    if mode == 0: #position (indirect)
        print("indirect write %d to %d" % (value, a))
        mem[a] = value
        return
    elif mode == 1: #immediate -- invalid for writes
        print("Invalid mode!")
        quit()

    return

def run():
    global mem
    pc = 0
    while True:
            raw = int(mem[pc])
            opcode = int(raw % 100)
            mode1 = int((raw / 100) % 2)
            mode2 = int((raw / 1000) % 2)
            mode3 = int((raw / 10000) % 2)
            print("PC = %d raw = %d opcode = %d modes = %d %d %d" % (pc, raw, opcode, mode1, mode2, mode3))
            if opcode == 1:
                a = read(mem[pc+1], mode1)
                b = read(mem[pc+2], mode2)
                write(a+b, mem[pc+3], mode3)
                #mem[mem[pc+3]] = mem[mem[pc+1]] + mem[mem[pc+2]]
                pc += 4
            elif opcode == 2:
                a = read(mem[pc+1], mode1)
                b = read(mem[pc+2], mode2)
                write(a*b, mem[pc+3], mode3)
                pc += 4
            elif opcode == 3: #input
                print("Enter ID of system to test:")
                i = input()
                i = int(i)
                print("User input %d" % (i))
                write(i, mem[pc+1], mode1)
                print(pc)
                pc += 2
                print(pc)
            elif opcode == 4: #output
                v = read(mem[pc+1], mode1)
                print("Output: %d" % (v))
                pc += 2
            elif opcode == 5: #jump if true
                test = read(mem[pc+1], mode1)
                target = read(mem[pc+2], mode2)
                if test != 0:
                    pc = target
                else:
                    pc += 3
            elif opcode == 6: #jump if false
                test = read(mem[pc+1], mode1)
                target = read(mem[pc+2], mode2)
                if test == 0:
                    pc = target
                else:
                    pc += 3
            elif opcode == 7: #if less than, store 1 in 3rd
                a = read(mem[pc+1], mode1)
                b = read(mem[pc+2], mode2)
                dest = mem[pc+3]
                if a < b:
                    write(1, dest, mode3)
                else:
                    write(0, dest, mode3)
                pc += 4
            elif opcode == 8: #if equals, store 1 in 3rd
                a = read(mem[pc+1], mode1)
                b = read(mem[pc+2], mode2)
                dest = mem[pc+3]
                if a == b:
                    write(1, dest, mode3)
                else:
                    write(0, dest, mode3)
                pc += 4
            elif opcode == 99:
                #print("halt")
                break
            else:
                print("Invalid opcode: %d" % (opcode))
                break

def part1():
    global mem
    load_mem()
    run()

part1()

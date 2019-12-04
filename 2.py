mem = []

def load_mem():
    global mem
    mem = [0] * 256
    with open("2.txt") as f:
        x = f.readline()
        i = 0
        for b in x.rstrip().split(","):
            mem[i] = int(b)
            i += 1

def run():
    global mem
    pc = 0
    while True:
            opcode = int(mem[pc])
            #print("PC = %d opcode = %d" % (pc, opcode))
            if opcode == 1:
                mem[mem[pc+3]] = mem[mem[pc+1]] + mem[mem[pc+2]]
                pc += 4
            elif opcode == 2:
                mem[mem[pc+3]] = mem[mem[pc+1]] * mem[mem[pc+2]]
                pc += 4
            elif opcode == 99:
                #print("halt")
                break
            else:
                print("Invalid opcode")
                break

def part1():
    global mem
    load_mem()
    mem[1] = 12
    mem[2] = 2
    run()
    return mem[0]

def part2():
    global mem
    for noun in range(100):
        for verb in range(100):
            load_mem()
            mem[1] = noun
            mem[2] = verb
            run()
            if mem[0] == 19690720:
                return (noun, verb)

    return None

print(part1())
ans = part2()
print(ans)
print(100*ans[0] + ans[1])
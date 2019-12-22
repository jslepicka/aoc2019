from intcode_machine import intcode_machine

def part1():
    im = intcode_machine("21.txt")

    commands = [
        "NOT A T",
        "NOT B J",
        "OR T J",
        "NOT C T",
        "OR T J",
        "AND D J",
        "WALK",
        ]
    command_queue = []
    for command in commands:
        for c in command:
            command_queue.append(c)
        command_queue.append("\n")
    line = ""
    while not im.halted:
        ret, data = im.run()
        if ret == im.OPCODE_INPUT:
            c = command_queue.pop(0)
            print(c, end='')
            im.add_input(ord(c))
        elif ret == im.OPCODE_OUTPUT:
            if data == 10:
                print(line)
                line = ""
            else:
                if data < 128:
                    line += chr(data)
                else:
                    print(data)

def part2():
    im = intcode_machine("21.txt")

    commands = [
        "NOT A T",
        "NOT B J",
        "OR T J",
        "NOT C T",
        "OR T J",
        "AND D J",
        "NOT E T",
        "NOT T T",
        "OR H T",
        "AND T J",
        "RUN",
        ]
    command_queue = []
    for command in commands:
        for c in command:
            command_queue.append(c)
        command_queue.append("\n")
    line = ""
    while not im.halted:
        ret, data = im.run()
        if ret == im.OPCODE_INPUT:
            c = command_queue.pop(0)
            print(c, end='')
            im.add_input(ord(c))
        elif ret == im.OPCODE_OUTPUT:
            if data == 10:
                print(line)
                line = ""
            else:
                if data < 128:
                    line += chr(data)
                else:
                    print(data)

part1()
part2()
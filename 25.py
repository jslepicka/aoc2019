from intcode_machine import intcode_machine

im = intcode_machine("25.txt", mem_size=16384)


def bf_puzzle():
    items = [
    "spool of cat6",
    "space law space brochure",
    "asterisk",
    "jam",
    "shell",
    "astronaut ice cream",
    "space heater",
    "klein bottle"
    ]

    drop = ""
    for i in items:
        drop += ("drop %s\n" % i)
    
    for i in range(256):
        take = ""
        for b in range(8):
            x = 1 << b
            if i & x:
                take += "take " + items[b] + "\n"
        print(drop)
        print(take)
        print("south")


bf_puzzle()

while not im.halted:
    ret, data = im.run()
    if ret == im.OPCODE_INPUT:
        command = input()
        for c in command:
            im.add_input(ord(c))
        im.add_input(10)
    elif ret == im.OPCODE_OUTPUT:
        print(chr(data), end="")
from intcode_machine import intcode_machine
from collections import deque

def print_view(view):
    max_x = max([x for x, y in view])
    max_y = max([y for x, y in view])
    min_x = min([x for x, y in view])
    min_y = min([y for x, y in view])
    for y in range(min_y, max_y + 1):
        line = ""
        for x in range(min_x, max_x + 1):
            line += view[(x,y)]
        print(line)

class decision:
    def __init__(self, entered_from):
        self.n = None
        self.s = None
        self.e = None
        self.w = None
        self.choice = 0
        self.choices = [1, 2, 3, 4]
        self.entered_from = entered_from
        if entered_from is not None:
            print("removing %d" % entered_from)
            self.choices.remove(entered_from)
            self.choices.append(entered_from)
    def get_choice(self):
        if len(self.choices) > 0:
            d = self.choices.pop(0)
            print("d: %d" % d)
            return self.choices.pop(0)
        else:
            return None

    


view = {}
decisions = {}


im = intcode_machine()
im.load_mem("15.txt")
x = 0
y = 0
view[(x,y)] = '.'
decisions[(x,y)] = decision(None)
while not im.halted:
    ret, val = im.run()
    i = 0
    last_x = 0
    last_y = 0
    if ret == im.OPCODE_INPUT:
        #N = 1, S = 2, W = 3, E = 4
        i = decisions[(x,y)].get_choice()
        if i is None:
            print("out of choices")
            quit()
        last_x = x
        last_y = y
        if i == 1:
            y -= 1
        elif i == 2:
            y += 1
        elif i == 3:
            x -= 1
        elif i == 4:
            x += 1
        if (x,y) not in decisions:
            decisions[(x,y)] = decision(i ^ 1)
        im.add_input(i)
    elif ret == im.OPCODE_OUTPUT:
        print(val)
        if val == 0: #hit a wall
            view[(x,y)] = '#'
            x = last_x
            y = last_y
        elif val == 1:
            view[(x,y)] = '.'
        elif val == 2:
            view[(x,y)] = 'o'
        print_view(view)

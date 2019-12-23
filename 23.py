from intcode_machine import intcode_machine
class computer():
    def __init__(self, id, network):
        self.id = id
        self.im = intcode_machine("23.txt")
        #send id to computer as first input
        self.input_queue = [id, None]
        self.output_queue = []
        self.network = network
    def run(self, num_cycles):
        #print("%d running for %d cycles" % (self.id, num_cycles))
        if self.im.halted:
            return
        cycles = num_cycles
        while cycles > 0:
            cycles -= 1
            (ret, data) = self.im.run(single_step=True)
            if ret == self.im.OPCODE_INPUT:
                if len(self.input_queue) > 1: # queue is not empty, rx words are 2 bytes
                    while self.input_queue:
                        data = self.input_queue.pop(0)
                        if data is not None:
                            print("%d received %s" % (self.id, data))
                            self.im.add_input(data)
                else:
                    self.im.add_input(-1)
            elif ret == self.im.OPCODE_OUTPUT:
                self.output_queue.append(data)
                if len(self.output_queue) == 3:
                    self.send_packet()
    def send_packet(self):
        if len(self.output_queue) > 2:
            dest = self.output_queue.pop(0)
            data = []
            for _ in range(2):
                data.append(self.output_queue.pop(0))
            print("%d sending %s to %d" % (self.id, data, dest))

            if dest == 255:
                print(data)
                quit()

            self.network.rx(dest, data)

class network():
    def __init__(self):
        self.num_computers = 50
        self.computers = []
        for i in range(self.num_computers):
            self.computers.append(computer(i, self))
    #receive data from computer
    def rx(self, dest, data):
        while data:
            self.computers[dest].input_queue.append(data.pop(0))
    #transmit data to computer
    def tx(self, dest, data):
        1
    def run(self):
        halted = 0
        for c in self.computers:
            if not c.im.halted:
                c.run(10)
            else:
                halted += 1
        if halted == self.num_computers:
            print("All computers halted")

net = network()
while True:
    net.run()


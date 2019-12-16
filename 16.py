
def read_input():
    with open("16.txt") as file:
        return file.readline().rstrip()

def part1(input_signal):
    input_signal = "19617804207202209144916044189917"
    input_len = len(input_signal)
    print("input signal length: %d" % input_len)
    pattern = [0, 1, 0, -1]
    total = input_signal
    for phase in range(100):
        input_signal = total
        total = ""
        for offset in range(len(input_signal)):
            digit = offset
            sum = 0
            for i in input_signal[digit:]:
                coeff_offset = (((digit+1) // (offset+1)) % 4)
                #print("coeff: %d" % coeff_offset)
                sum += int(i) * pattern[coeff_offset]
                digit += 1
            total += str(abs(sum) % 10)
        #print("%d" % phase)
    return total[:8]

input_signal = read_input()
print(part1(input_signal))
#print(part1(input_signal * 10000))
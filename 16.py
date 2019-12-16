
def read_input():
    with open("16.txt") as file:
        return file.readline().rstrip()

def part1(input_signal):
    input_signal = [int(x) for x in input_signal]
    input_len = len(input_signal)
    pattern = [0, 1, 0, -1]
    for phase in range(100):
        for offset in range(len(input_signal)):
            digit = offset
            sum = 0
            for i in input_signal[digit:]:
                coeff_offset = ((digit+1) // (offset+1)) % 4
                sum += i * pattern[coeff_offset]
                digit += 1
            input_signal[offset] = abs(sum) % 10
    return "".join([str(i) for i in input_signal[:8]])

def part2(input_signal):
    #at the halfway point, all of the coefficients change to 1
    #the offset is in the second half
    #calculate sum of second half of digits
    input_signal *= 10000
    input_len = len(input_signal)
    offset = int(input_signal[:7])
    input_signal = [int(x) for x in input_signal[offset:]]
    for phase in range(100):
        input_signal_sum = sum(input_signal)
        for i in range(0, len(input_signal)):
            temp = input_signal[i]
            input_signal[i] = input_signal_sum % 10
            input_signal_sum -= temp
    return "".join([str(i) for i in input_signal[:8]])

input_signal = read_input()
print(part1(read_input()))
print(part2(read_input()))




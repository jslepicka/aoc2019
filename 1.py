data = []

def calc_fuel(weight):
    return int(int(weight)/3) - 2

def part1():
    s = 0
    for l in data:
        s += calc_fuel(l)
    return s

def part2():
    total = 0
    for l in data:
        fuel = calc_fuel(l)
        fuelfuel = calc_fuel(fuel)
        while fuelfuel > 0:
            fuel += fuelfuel
            fuelfuel = calc_fuel(fuelfuel)
        total += fuel
    return total

with open("1.txt") as file:
    data = file.readlines()


print(part1())
print(part2())

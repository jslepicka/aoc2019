import re
import math

class Moon:
    def __init__(self, x, y, z):
        self.coords = [x, y, z]
        self.veloc = [0, 0, 0]
        self.init_coords = self.coords.copy()
        self.init_veloc = self.veloc.copy()
    def get_energy(self):
        potential = sum([abs(c) for c in self.coords])
        kinetic = sum([abs(v) for v in self.veloc])
        return potential * kinetic

def load_moons(filename):
    moons = []
    with open(filename) as file:
        for line in file.readlines():
            matches = re.search(r"x=(-*\d+).+y=(-*\d+).+z=(-*\d+)", line)
            if matches:
                x = int(matches[1])
                y = int(matches[2])
                z = int(matches[3])
                moons.append(Moon(x,y,z))
    return moons

def part1(moons):
    for _ in range(1000):
        for i in range(len(moons) - 1):
            for j in range(i+1, len(moons)):
                for c in range(3):
                    if moons[i].coords[c] == moons[j].coords[c]:
                        continue
                    elif moons[i].coords[c] < moons[j].coords[c]:
                        moons[i].veloc[c] += 1
                        moons[j].veloc[c] -= 1
                    else:
                        moons[i].veloc[c] -= 1
                        moons[j].veloc[c] += 1

        for moon in moons:
            for c in range(3):
                moon.coords[c] += moon.veloc[c]

    print(sum([moon.get_energy() for moon in moons]))

def lcm(a, b):
    return a * b // math.gcd(a,b)

def part2(moons):
    periods = []
    for c in range(3): #for each coordinate
        iter = 1
        while True:
            for i in range(len(moons) - 1):
                for j in range(i+1, len(moons)):
                    if moons[i].coords[c] == moons[j].coords[c]:
                        continue
                    elif moons[i].coords[c] < moons[j].coords[c]:
                        moons[i].veloc[c] += 1
                        moons[j].veloc[c] -= 1
                    else:
                        moons[i].veloc[c] -= 1
                        moons[j].veloc[c] += 1
            for moon in moons:
                moon.coords[c] += moon.veloc[c]
            if not False in [moon.coords[c] == moon.init_coords[c] and moon.veloc[c] == moon.init_veloc[c] for moon in moons]:
                periods.append(iter)
                break
            iter += 1
    print(lcm(periods[0], lcm(periods[1], periods[2])))
        
part1(load_moons("12.txt"))
part2(load_moons("12.txt"))


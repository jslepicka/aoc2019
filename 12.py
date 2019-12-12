import re

class moon:
    def __init__(self, x, y, z):
        self.coords = [x, y, z]
        self.veloc = [0, 0, 0]
    def get_energy(self):
        potential = sum([abs(c) for c in self.coords])
        kinetic = sum([abs(v) for v in self.veloc])
        return potential * kinetic
    def get_state(self):
        state = ""
        for c in self.coords:
            state += ("%d" % c)
        for v in self.veloc:
            state += ("%d" % v)
        return state

moons = []

with open("12.txt") as file:
    for line in file.readlines():
        matches = re.search(r"x=(-*\d+).+y=(-*\d+).+z=(-*\d+)", line)
        if matches:
            x = int(matches[1])
            y = int(matches[2])
            z = int(matches[3])
            moons.append(moon(x, y, z))

def print_moons():
    for moon in moons:
        print("%d %d %d  %d %d %d" % (moon.coords[0],moon.coords[1], moon.coords[2], moon.veloc[0], moon.veloc[1], moon.veloc[2]))

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

print_moons()
print(sum([moon.get_energy() for moon in moons]))
state_string = ""
for moon in moons:
    state_string += moon.get_state()
print(state_string)
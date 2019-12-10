import math
class asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visibility = 0
        self.distances = {}
        self.angles = {}

asteroids = {}

with open("10.txt") as file:
    y = 0
    for line in file.readlines():
        x = 0
        for c in line:
            if c == '#':
                asteroids[(x,y)] = asteroid(x, y)
            x += 1
        y += 1
print("found %d asteroids" % len(asteroids))

def get_distance(p1x, p1y, p2x, p2y):
    return math.sqrt(math.pow(p2x-p1x, 2) + math.pow(p2y-p1y, 2))

def get_angle(x0, y0, x1, y1):
    y = y1-y0
    x = x1-x0
    angle = math.atan2(y,x)
    angle = angle * (180/math.pi)
    angle = (angle + 360 + 90) % 360
    return angle

#for each asteroid, find distance and angle to every other asteroid
for s in asteroids:
    for e in asteroids:
        if s is e: #ignore self
            continue
        else:
            d = get_distance(asteroids[s].x, asteroids[s].y, asteroids[e].x, asteroids[e].y)
            asteroids[s].distances[e] = d
            asteroids[s].angles[e] = get_angle(asteroids[s].x, asteroids[s].y, asteroids[e].x, asteroids[e].y)

print("computed distances and angles")

def part1():
    counts = {}
    for a in asteroids:
        ast = asteroids[a]
        angles = sorted(ast.angles, key=lambda k:ast.angles[k])
        last_angle = None
        count = 0
        for ang in angles:
            if last_angle is None or abs(ast.angles[ang] - last_angle) > .0001:
                count += 1
            last_angle = ast.angles[ang]
        counts[a] = count
    max_a = max(counts, key=lambda k:counts[k])
    max_count = counts[max_a]
    return (max_a, max_count)

def part2(best, kill):
    kill_order = {}
    best = asteroids[best]
    best_angles = sorted(best.angles, key=lambda k:best.angles[k])

    paths = []
    path = None
    last_a = None
    for a in best_angles:
        if last_a is not None and abs(best.angles[a] - last_a) < .00001:
            path.append(a)
        else:
            if path is not None:
                paths.append(sorted(path, key=lambda k:best.distances[k]))
            path = []
            path.append(a)
        last_a = best.angles[a]
    if len(path) > 0:
        paths.append(sorted(path, key=lambda k:best.distances[k]))

    found = 0
    while sum(len(p) for p in paths) > 0:
        for p in range(len(paths)):
            if len(paths[p]) > 0:
                x = paths[p].pop(0)
                found += 1
                kill_order[found] = x
    k = kill_order[kill]
    return k[0] * 100 + k[1]

(best, max_count) = part1()
print(max_count)
print(part2(best, 200))

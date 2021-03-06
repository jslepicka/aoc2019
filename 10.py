import math
class asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
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

def equalish(a, b):
    return True if abs(a-b) < .00001 else False

#sort asteroids by angle
#get count of each "unique" angle
#return highest unique count
def part1():
    counts = {}
    for ast_coord in asteroids:
        ast = asteroids[ast_coord]
        angles = sorted(ast.angles, key=lambda k:ast.angles[k])
        last_angle = None
        count = 0
        for angle in angles:
            if last_angle is None or not equalish(ast.angles[angle], last_angle):
                count += 1
            last_angle = ast.angles[angle]
        counts[ast_coord] = count
    max_ast_coord = max(counts, key=lambda k:counts[k])
    max_count = counts[max_ast_coord]
    return (max_ast_coord, max_count)

#sort asteroids by angle
#for each angle, create a list of all the asteroids on that angle
#sort those lists by distance order
#then, iterate over list of path lists
#pop (kill) the first asteroid off of each list
#repeat as long as there are asteroids left
def part2(ast, kill):
    kill_order = {}
    ast = asteroids[ast]
    ast_coords = sorted(ast.angles, key=lambda k:ast.angles[k])

    paths = []
    path = None
    last_coord = None
    for ast_coord in ast_coords:
        if last_coord is not None and equalish(ast.angles[ast_coord], last_coord):
            path.append(ast_coord)
        else:
            if path is not None:
                paths.append(sorted(path, key=lambda k:ast.distances[k]))
            path = []
            path.append(ast_coord)
        last_coord = ast.angles[ast_coord]
    if len(path) > 0:
        paths.append(sorted(path, key=lambda k:ast.distances[k]))

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

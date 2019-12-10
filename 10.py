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

#now we have distances between every asteroid.  find all the cases where
#distance start<->end == distance start<->point + distance end<->point

def part1():
    for s in asteroids:
        start = asteroids[s]
        #print("start point is %d, %d" % (start.x, start.y))
        for e in start.distances:
            end = asteroids[e]
            #print(" end point is %d, %d distance: %f" % (end.x, end.y, start.distances[e]))
            #for every asteroid p that is not start and not end
            #find sum of distances between p and start and p and end
            blocked = 0
            for x in asteroids:
                p = asteroids[x]
                if p is not start and p is not end:
                    d_start = p.distances[s]
                    d_end = p.distances[e]
                    d_sum = d_start + d_end
                    #print("  %d %d %.4f %.4f %.4f" % (p.x, p.y, d_start, d_end, d_sum))
                    if abs(d_sum - start.distances[e]) < .00001:
                        blocked = 1
                        break
            if blocked == 0:
                start.visibility += 1
    best = max(asteroids, key=lambda x:asteroids[x].visibility)
    #print("%s can see %d asteroids" % (best, asteroids[best].visibility))
    return best

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

best = part1()
print(asteroids[best].visibility)
print(part2(best, 200))

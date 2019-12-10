import math
class asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visibility = 0
        self.distances = {}

asteroids = {}

with open("10.txt") as file:
    y = 0
    for line in file.readlines():
        x = 0
        for c in line:
            if c == '#':
                print("found asteroid at %d, %d" % (x,y))
                asteroids[(x,y)] = asteroid(x, y)
            x += 1
        y += 1
print("found %d asteroids" % len(asteroids))

print(asteroids)

def distance(p1x, p1y, p2x, p2y):
    return math.sqrt(math.pow(p2x-p1x, 2) + math.pow(p2y-p1y, 2))

#for each asteroid, find distance to every other asteroid
for s in asteroids:
    for e in asteroids:
        if s is e: #ignore self
            continue
        else:
            d = distance(asteroids[s].x, asteroids[s].y, asteroids[e].x, asteroids[e].y)
            asteroids[s].distances[e] = d

#now we have distances between every asteroid.  find all the cases where
#distance start<->end == distance start<->point + distance end<->point

print("computed distances")

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
                d_start = distance(p.x, p.y, start.x, start.y)
                d_end = distance(p.x, p.y, end.x, end.y)
                d_sum = d_start + d_end
                #print("  %d %d %.4f %.4f %.4f" % (p.x, p.y, d_start, d_end, d_sum))
                if abs(d_sum - start.distances[e] < .00000001):
                    blocked = 1
                    break
        if blocked == 0:
            start.visibility += 1

print(asteroids[max(asteroids, key=lambda x:asteroids[x].visibility)].visibility)


            

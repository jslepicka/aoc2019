import time
grid = {}
path1 = []
path2 = []

with open("3.txt") as file:
    path1 = file.readline().rstrip().split(",")
    path2 = file.readline().rstrip().split(",")

# print(path1)
# print(path2)

start = time.time()
x = 0
y = 0
for p in path1:
    dir = p[:1]
    distance = int(p[1:])
    for i in range(distance):
        if dir == "U":
            y += 1
        elif dir == "D":
            y -= 1
        elif dir == "L":
            x -= 1
        elif dir == "R":
            x += 1
        grid[(x,y)] = 1

x = 0
y = 0

matches = []
for p in path2:
    dir = p[:1]
    distance = int(p[1:])
    for i in range(distance):
        if dir == "U":
            y += 1
        elif dir == "D":
            y -= 1
        elif dir == "L":
            x -= 1
        elif dir == "R":
            x += 1
        if (x,y) in grid:
            matches.append((x,y))

best = None
shortest = 9999999
for m in matches:
    distance = abs(m[0]) + abs(m[1])
    if distance < shortest:
        shortest = distance
        best = m
print(best)
print(shortest)

print(min([abs(m[0]) + abs(m[1]) for m in matches]))

#print(matches)

lengths = {}

x = 0
y = 0
travelled = 0
for p in path1:
    dir = p[:1]
    distance = int(p[1:])

    for i in range(distance):
        travelled += 1
        if dir == "U":
            y += 1
        elif dir == "D":
            y -= 1
        elif dir == "L":
            x -= 1
        elif dir == "R":
            x += 1
        if (x,y) in matches:
            if (x,y) not in lengths:
                lengths[(x,y)] = (travelled, -1)

x = 0
y = 0
travelled = 0
for p in path2:
    dir = p[:1]
    distance = int(p[1:])
    for i in range(distance):
        travelled += 1
        if dir == "U":
            y += 1
        elif dir == "D":
            y -= 1
        elif dir == "L":
            x -= 1
        elif dir == "R":
            x += 1
        if (x,y) in matches:
            if lengths[(x,y)][1] == -1:
                lengths[(x,y)] = (lengths[(x,y)][0], travelled)

best = 999999999
for l in lengths:
    distance = lengths[l][0] + lengths[l][1]
    if distance < best:
        best = distance
print(best)

print(min([lengths[l][0] + lengths[l][1] for l in lengths]))

print("end")

end = time.time()

print(end-start)

### revised below ###

start = time.time()

def get_points(a):
    x = 0
    y = 0
    travelled = 0
    points = {}
    moves = {"U": (0,1), "D": (0,-1), "L": (-1,0), "R": (1,0)}
    for p in a:
        dir = p[0]
        distance = int(p[1:])
        move_x = moves[dir][0]
        move_y = moves[dir][1]
        for i in range(distance):
            x += move_x
            y += move_y
            travelled += 1
            if (x,y) not in points:
                points[(x,y)] = travelled
    return points

points1 = get_points(path1)
points2 = get_points(path2)
matches = set(points1.keys()) & set(points2.keys())

print(min([abs(x) + abs(y) for (x,y) in matches]))

print(min([(points1[p]+points2[p]) for p in matches]))

end = time.time()
print(end-start)
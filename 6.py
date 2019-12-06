parents = {}

def get_path_to_root(start):
    path = []
    x = start
    while x in parents:
        x = parents[x]
        path.append(x)
    return path
    
def get_transfer_count(planet1, planet2):
    path1 = get_path_to_root(planet1)
    path2 = get_path_to_root(planet2)
    for p in path1:
        if p in path2:
            return path1.index(p) + path2.index(p)
    return None

with open("6.txt") as file:
    for line in file.readlines():
        line = line.rstrip()
        (parent, p) = line.split(")")
        parents[p] = parent

orbit_count = 0
for p in parents:
    orbit_count += len(get_path_to_root(p))

print("%d orbits" % orbit_count)
print("%d transfers between YOU and SAN" % get_transfer_count("YOU", "SAN"))

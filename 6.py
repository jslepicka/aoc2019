class planet:
    def __init__(self, name, parent_name):
        self.name = name
        self.parent_name = parent

planets = {}
with open("6.txt") as file:
    for line in file.readlines():
        line = line.rstrip()
        (parent, p) = line.split(")")
        planets[p] = planet(p, parent)

def get_path_to_root(start):
    path = []
    x = planets[start].name
    while x in planets and planets[x].parent_name is not None:
        x = planets[x].parent_name
        path.append(x)
    return path
    
def get_transfer_count(planet1, planet2):
    path1 = get_path_to_root(planet1)
    path2 = get_path_to_root(planet2)
    for p in path1:
        if p in path2:
            return path1.index(p) + path2.index(p)
    return None

orbit_count = 0
for p in planets:
    orbit_count += len(get_path_to_root(planets[p].name))

print("%d orbits" % orbit_count)
print("%d transfers between YOU and SAN" % get_transfer_count("YOU", "SAN"))

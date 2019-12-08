from collections import Counter

def read_image(filename):
    image = []
    with open(filename) as file:
        image = [int(f) for f in file.readline().rstrip()]
    return image

def get_layers(image, width, height):
    layers = []
    input_len = len(image)
    layer_len = width * height
    start = 0
    end = layer_len
    while end <= input_len:
        layer = image[start:end]
        start = end
        end = start + layer_len
        layers.append(layer)
    return layers

def merge_layers(layers):
    layer_len = len(layers[0])
    merged = [None] * layer_len
    for l in layers:
        for i in range(layer_len):
            if l[i] != 2 and merged[i] is None:
                merged[i] = l[i]
    return merged

def print_image(image, width, height):
    start = 0
    end = width
    while end <= width * height:
        print("".join(["XX" if s == 1 else "  " for s in image[start:end]]))
        start += width
        end += width

def part1(image):
    layers = get_layers(image, 25, 6)
    layer_stats = [Counter(l) for l in layers]
    layer_stats.sort(key=lambda k: k[0])
    return layer_stats[0][1] * layer_stats[0][2]

def part2(image):
    layers = get_layers(image, 25, 6)
    merged = merge_layers(layers)
    print_image(merged, 25, 6)

image = read_image("8.txt")
print(part1(image))
part2(image)
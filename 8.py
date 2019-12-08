def read_image(filename):
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
    char_width = 2
    fill_char = "#" * char_width
    empty_char = " " * char_width
    start = 0
    end = width
    while end <= width * height:
        print("".join([fill_char if s == 1 else empty_char for s in image[start:end]]))
        start = end
        end += width

def part1(image):
    layers = get_layers(image, 25, 6)
    least0 = min(layers, key=lambda layer: layer.count(0))
    return least0.count(1) * least0.count(2)

def part2(image):
    layers = get_layers(image, 25, 6)
    merged = merge_layers(layers)
    print_image(merged, 25, 6)

image = read_image("8.txt")
print(part1(image))
part2(image)
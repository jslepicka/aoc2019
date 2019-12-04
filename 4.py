import time
start = 178416
end = 676461


def test1(a):
    for i in range(len(a) - 1):
        if a[i] == a[i+1]:
            return True
    return False


def test1a(a):
    for i in range(10):
        count = 0
        for char in a:
            if char == str(i):
                count += 1
        if count == 2:
            return True
    return False

def test1b(a):
    prev_char = None
    count = 0
    for i in range(len(a)):
        if prev_char == a[i]:
            count += 1
        else:
            if count == 2:
                return True
            count = 1
        prev_char = a[i]
    if count == 2:
        return True
    return False

def test1c(a):
    chars = {}
    for i in a:
        chars[i] = chars.get(i, 0) + 1
    if 2 in chars.values():
        return True
    return False

def test2(a):
    for i in range(len(a)-1):
        if a[i+1] < a[i]:
            return False
    return True

start_time = time.time()
count1 = 0
count2 = 0
for i in range(start, end+1):
    a = str(i)
    if test2(a):
        if test1(a):
            count1 += 1
        if test1c(a):
            count2 += 1
print(count1)
print(count2)
end_time = time.time()
print(end_time-start_time)
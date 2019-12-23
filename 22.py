import re

def deal_into_new_stack(deck):
    return list(reversed(deck))

def cut_cards(deck, n):
    return deck[n:] + deck[:n]
    

def deal_with_increment(deck, n):
    deck_len = len(deck)
    table = [0] * deck_len
    dest = 0
    for source in range(deck_len):
        table[dest] = deck[source]
        dest = (dest + n) % deck_len
    return table

deck = list(range(10007))
#print(deck)
# print(deck)
# print("deal with increment 8")
# d = deal_with_increment(deck, 8)
# print(d)
# print(d.index(1))

# print("cut 2")
# d = cut_cards(deck, 3)
# print(d)
# print(d.index(1))
# print("cut -2")
# print(cut_cards(deck, -2))
# print("deal into stack")
# print(deal_into_new_stack(deck))
# cut_sum = 0
last = 0
x = 0

with open("22.txt") as file:
    for l in file.readlines():
        matches = re.search("^deal with increment (\d+)", l)
        if matches:
            n = int(matches[1])
            #print(n)
            deck = deal_with_increment(deck, n)
        matches = re.search("^cut (-?\d+)", l)
        if matches:
            n = int(matches[1])
            #print(n)
            deck = cut_cards(deck, n)
        matches = re.search("^deal into new stack", l)
        if matches:
            deck = deal_into_new_stack(deck)

i = deck.index(2019)
if i == 6831:
    print(x)
x += 1
print("card 2019 is at position: %d" % i)

def rev_deal_into_new_stack(deck_len, pos):
    new_pos = (deck_len - 1) - pos
    #print("rev new stack: %d -> %d" % (pos, new_pos))
    return new_pos

def rev_cut_cards(deck_len, n, pos):
    new_pos = (pos + n) % deck_len
    #print("rev cut cards %d: %d -> %d" % (n, pos, new_pos))
    return new_pos
    

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def rev_deal_with_increment(deck_len, n, pos):
    mi = modinv(n, deck_len)
    new_pos = (pos * mi) % deck_len
    #print("reversing deal with inc %d: %d -> %d" % (n, pos, new_pos))
    return new_pos


position = 2020 #2020
deck_len = 119315717514047
results = {}
i = 0
last = 0

while True:
    with open("22.txt") as file:
        for l in reversed(file.readlines()):
            #print(position)
            matches = re.search("^deal with increment (\d+)", l)
            if matches:
                n = int(matches[1])
                #print(n)
                position = rev_deal_with_increment(deck_len, n, position)
            matches = re.search("^cut (-?\d+)", l)
            if matches:
                n = int(matches[1])
                #print(n)
                position = rev_cut_cards(deck_len, n, position)
            matches = re.search("^deal into new stack", l)
            if matches:
                position = rev_deal_into_new_stack(deck_len, position)
    #print(position)
    if position in results:
        print("found dupe %d at %d" % (position, results))
    results[position] = 1
    i += 1




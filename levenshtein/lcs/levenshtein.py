import numpy as np

ADD = 1
SWAP = 2
REMOVE = -1
EQUAL = 0


def path(p):
    n, m = p.shape
    i, j = n - 1, m - 1
    route = []

    while i != 0 or j != 0:
        if j == 0:
            i -= 1
            route.append(REMOVE)
        elif i == 0:
            j -= 1
            route.append(ADD)
        elif p[i, j] == ADD:
            j -= 1
            route.append(ADD)
        elif p[i, j] == REMOVE:
            i -= 1
            route.append(REMOVE)
        elif p[i, j] == SWAP:
            i -= 1
            j -= 1
            route.append(SWAP)
        else:  # EQUAL
            i -= 1
            j -= 1
            route.append(EQUAL)

    return reversed(route)


def levenshtein(a, b):
    n = len(a) + 1
    m = len(b) + 1
    d = np.zeros(shape=(n, m))
    p = np.zeros(shape=(n, m))

    for i in range(1, n):
        d[i, 0] = i
        p[i, 0] = REMOVE

    for j in range(1, m):
        d[0, j] = j
        p[0, j] = ADD

    for j in range(1, m):
        for i in range(1, n):

            cost = 0 if a[i - 1] == b[j - 1] else 1

            d[i, j] = min(d[i - 1, j] + 1, d[i, j - 1] + 1, d[i - 1, j - 1] + cost)

            if d[i, j] == d[i - 1, j - 1] and cost == 0:
                p[i, j] = EQUAL
            elif d[i, j] == d[i - 1, j - 1] + 1 and cost == 1:
                p[i, j] = SWAP
            elif d[i, j] == d[i - 1, j] + 1:
                p[i, j] = REMOVE
            else:
                p[i, j] = ADD

    return d[n - 1, m - 1], path(p)


def show(a, b, path):
    tmp = a
    j = 0
    
    print(a)

    for i, move in enumerate(path):
        if move == EQUAL:
            print(tmp[: i + j] + f"*{tmp[i+j]}*" + tmp[i + j + 1 :], "EQUAL")
        elif move == SWAP:
            print(tmp[: i + j] + f"*{b[i+j]}*" + tmp[i + j + 1 :], "SWAP")
            tmp = tmp[: i + j] + b[i + j] + tmp[i + j + 1 :]
        elif move == REMOVE:
            print(tmp[: i + j] + "**" + tmp[i + j + 1 :], "REMOVE")
            tmp = tmp[: i + j] + tmp[i + j + 1 :]
            j -= 1
        elif move == ADD:
            print(tmp[: i + j] + f"*{b[i+j]}*" + tmp[i + j :], "ADD")
            tmp = tmp[: i + j] + b[i + j] + tmp[i + j :]
    
    print(b)

    return tmp

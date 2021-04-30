import numpy as np

UP = 1
EQUAL = 0
LEFT = -1


def extract(array, p):

    stack = []

    i, j = p.shape
    i, j = i - 1, j - 1

    while i != 0 and j != 0:
        if p[i, j] == EQUAL:
            stack.append(array[i - 1])
            i, j = i - 1, j - 1
        elif p[i, j] == UP:
            i = i - 1
        elif p[i, j] == LEFT:
            j = j - 1
        else:
            raise Exception(f"Illegal argument: {p[i, j]}")

    return "".join(reversed(stack)) if isinstance(array, str) else list(reversed(stack))


def lcs(a, b):
    d, p = lcs_(a, b)
    return d[len(a), len(b)], extract(a, p)


def lcs_(a, b):
    n = len(a) + 1
    m = len(b) + 1
    d = np.zeros(shape=(n, m))
    p = np.zeros(shape=(n, m))

    for j in range(1, m):
        for i in range(1, n):
            if a[i - 1] == b[j - 1]:
                d[i, j] = d[i - 1, j - 1] + 1
                p[i, j] = EQUAL
            elif d[i - 1, j] > d[i, j - 1]:
                d[i, j] = d[i - 1, j]
                p[i, j] = UP
            else:
                d[i, j] = d[i, j - 1]
                p[i, j] = LEFT

    return d, p

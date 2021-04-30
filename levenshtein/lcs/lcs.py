import numpy as np

UP = 1
EQUAL = 0
LEFT = -1


def extract(string, p, i=None, j=None, acc=None):
    if i is None:
        i = p.shape[0] - 1
    if j is None:
        j = p.shape[1] - 1
    if acc is None:
        acc = []

    if i == 0 or j == 0:
        return acc if acc else ""

    if p[i, j] == EQUAL:
        extract(string, p, i - 1, j - 1, acc)
        acc.append(string[i - 1])
    elif p[i, j] == UP:
        extract(string, p, i - 1, j, acc)
    else:
        extract(string, p, i, j - 1, acc)

    return "".join(acc)


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

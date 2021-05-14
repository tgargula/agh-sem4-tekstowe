import numpy as np
from .helpf import parse, vectors, norm
from numba import jit


def cosine(i, j, data, length):
    x, y = parse(i, j, data, length)
    v, u = vectors(x, y)

    return 1 - np.sum(v * u) / (np.sum(v) + np.sum(u))


def dice(i, j, data, length):
    x, y = parse(i, j, data, length)
    s, t = set(x), set(y)

    return 1 - 2 * len(s & t) / (len(s) + len(t))


def euclidean(i, j, data, length):
    x, y = parse(i, j, data, length)
    v, u = vectors(x, y)
    v, u = norm(v), norm(u)

    return np.sqrt(np.sum((v - u) ** 2))


def lcs(i, j, data):
    i, j = int(i[0]), int(j[0])
    x, y = data[i], data[j]

    mlen = max(len(x), len(y))
    lcs_value = np.max(lcs_array(x, y))

    return 1 - lcs_value / mlen

def lcs_array(a, b):
    n = len(a) + 1
    m = len(b) + 1
    d = np.zeros(shape=(n, m))

    for j in range(1, m):
        for i in range(1, n):
            if a[i - 1] == b[j - 1]:
                d[i, j] = d[i - 1, j - 1] + 1

    return d


def levenshtein(i, j, data):
    i, j = int(i[0]), int(j[0])
    x, y = data[i], data[j]

    mlen = max(len(x), len(y))

    return levenshtein_array(x, y)[len(x), len(y)] / mlen

@jit(nopython=True)
def levenshtein_array(a, b):
    n = len(a) + 1
    m = len(b) + 1
    d = np.zeros(shape=(n, m))

    for i in range(1, n):
        d[i, 0] = i

    for j in range(1, m):
        d[0, j] = j

    for j in range(1, m):
        for i in range(1, n):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            d[i, j] = min(
                d[i - 1, j] + 1,
                d[i, j - 1] + 1,
                d[i - 1, j - 1] + cost
            )

    return d

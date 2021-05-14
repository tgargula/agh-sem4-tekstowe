import numpy as np
from .ngrams import ngrams, ngrams_text
from functools import reduce

def vectors(x, y):
    keys = set(x) | set(y)

    v = np.array([x.get(key, 0) for key in keys])
    u = np.array([y.get(key, 0) for key in keys])

    return v, u


def vector(keys, x):
    return np.array([x.get(key, 0) for key in keys])


def cluster_vector(keys, ngrams):
    return np.array([np.array([line.get(key, 0) for key in keys]) for line in ngrams])
    V = np.array()
    for line in ngrams:
        V.append(np.array([line.get(key, 0) for key in keys]))
    return V


def parse(i, j, data, length):
    i, j = int(i[0]), int(j[0])
    x, y = data[i], data[j]
    x, y = ngrams(x, length), ngrams(y, length)
    return x, y


def norm(v):
    return v / np.sum(v)
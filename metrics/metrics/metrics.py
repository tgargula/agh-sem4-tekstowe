from .ngrams import ngrams
import numpy as np


def vectors(x, y):
    keys = set(x) | set(y)

    v = np.array([x.get(key, 0) for key in keys])
    u = np.array([y.get(key, 0) for key in keys])

    return v, u


def norm(v):
    return v / np.sum(v)


def cosine(x, y):
    v, u = vectors(x, y)

    return 1 - np.sum(v * u) / (np.sum(v) + np.sum(u))


def dice(x, y):
    s, t = set(x), set(y)

    return 1 - 2 * len(s & t) / (len(s) + len(t))


def euclidean(x, y):
    v, u = vectors(x, y)
    v, u = norm(v), norm(u)

    return np.sqrt(np.sum((v - u) ** 2))

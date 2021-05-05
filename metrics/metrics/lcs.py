import numpy as np

def lcs(a, b):
    return np.max(lcs_array(a, b))


def lcs_array(a, b):
    n = len(a) + 1
    m = len(b) + 1
    d = np.zeros(shape=(n, m))

    for j in range(1, m):
        for i in range(1, n):
            if a[i - 1] == b[j - 1]:
                d[i, j] = d[i - 1, j - 1] + 1
                
    return d

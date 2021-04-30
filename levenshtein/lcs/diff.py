from .lcs import lcs_, EQUAL, UP, LEFT


def extract(a, b, p):
    (n, m) = p.shape

    result = []
    for j in range(1, m):
        for i in range(1, n):
            if p[i, j] == 0:
                break
            if i == n - 1:
                result.append((b[j-1], '<'))

    for i in range(1, n):
        for j in range(1, m):
            if p[i, j] == 0:
                break
            if j == m - 1:
                result.append((a[i-1], '>'))

    return result


def diff(filename1, filename2):
    with open(filename1, 'r') as f:
        lines1 = f.readlines()
    with open(filename2, 'r') as f:
        lines2 = f.readlines()
    return diff_(lines1, lines2)


def diff_(s, t):
    _, p = lcs_(s, t)
    return extract(s, t, p)

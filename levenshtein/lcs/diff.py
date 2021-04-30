from .lcs import lcs_tokens, lcs_text, EQUAL, UP, LEFT
from .tokenizer import tokenize_from_file, lines

def extract(a, b, p):
    (n, m) = p.shape

    result = {}
    for j in range(1, m):
        for i in range(1, n):
            if p[i, j] == 0:
                break
            if i == n - 1:
                if "<" in result:
                    result["<"].append(b[j - 1])
                else:
                    result["<"] = [b[j - 1]]

    for i in range(1, n):
        for j in range(1, m):
            if p[i, j] == 0:
                break
            if j == m - 1:
                if ">" in result:
                    result[">"].append(a[i - 1])
                else:
                    result[">"] = [a[i - 1]]

    return result


def diff(filename1, filename2):
    tokens1 = lines(tokenize_from_file(filename1))
    tokens2 = lines(tokenize_from_file(filename2))

    result = {}
    for i, (line1, line2) in enumerate(zip(tokens1, tokens2)):
        d = diff_tokens(line1, line2)
        if d:
            result[i] = d

    return result


def diff_tokens(s, t):
    _, p = lcs_tokens(s, t)
    return extract(s, t, p)


def diff_text(s, t):
    _, p = lcs_text(s, t)
    return extract(s, t, p)
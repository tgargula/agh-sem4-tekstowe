def naive(data, pattern):
    n = len(data)
    m = len(pattern)
    result = []
    
    for s in range(n - m + 1):
        if pattern == data[s:s+m]:
            result.append(s)

    return result


def transition_table(pattern):
    Q = range(len(pattern) + 1)
    Sigma = set(pattern)
    delta = []

    for q in Q:
        delta.append({})
        for letter in Sigma:
            k = min(len(Q), q + 2) - 1
            text = pattern[:q] + letter
            while not text.endswith(pattern[:k]):
                k -= 1

            delta[q][letter] = k
    
    return delta


def fa(data, pattern):
    delta = transition_table(pattern)
    return fa_preprocessed(data, delta)


def fa_preprocessed(data, delta):
    q = 0
    result = []

    for s, letter in enumerate(data):
        q = delta[q].get(letter, 0)
        if q + 1 == len(delta):
            result.append(s - q + 1)

    return result


def prefix_function(pattern):
    m = len(pattern)
    pi = [0] * m
    k = 0
    
    for q in range(1, m):
        while k > 0 and pattern[k] != pattern[q]: # check back
            k = pi[k - 1]
        if pattern[k] == pattern[q]: # letters match
            k += 1
        pi[q] = k
    
    return pi


def kmp(data, pattern, pi=None):
    pi = prefix_function(pattern)
    return kmp_preprocessed(data, pattern, pi)


def kmp_preprocessed(data, pattern, pi):
    n = len(data)
    m = len(pattern)
    q = 0               # number of matching symbols
    result = []
    for i, letter in enumerate(data):
        while q > 0 and pattern[q] != letter:
            q = pi[q - 1]
        if pattern[q] == letter:
            q += 1
        if q == m:
            result.append(i - m + 1)
            q = pi[q - 1]

    return result

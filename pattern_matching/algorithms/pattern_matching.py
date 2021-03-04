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


def transition_function(pattern):
    return None


def kmp(data, pattern, pi=None):
    pi = transition_function(pattern)
    return kmp_preprocessed(data, pi)


def kmp_preprocessed(data, pi):
    return None
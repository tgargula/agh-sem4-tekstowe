from time import time

def test(f, data, pattern):
    start = time()
    f(data, pattern)
    return time() - start

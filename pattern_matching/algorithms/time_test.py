from time import time

def test(f, *args):
    start = time()
    f(*args)
    return time() - start

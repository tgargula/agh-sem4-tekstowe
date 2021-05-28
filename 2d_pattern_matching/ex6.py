from ahocorasick import Automaton2d
from letters.image import Haystack
import numpy as np
import csv

import time


def benchmark(f, *args):
    start = time.time()
    result = f(*args)
    end = time.time()
    return result, end - start


if __name__ == "__main__":
    haystack = Haystack()
    pattern = haystack.get("pattern")
    e = haystack.get("e")

    pattern_times, e_times = [], []
    results = [pattern_times, e_times]
    elapsed = [0] * 2

    for j in range(3):
        div = 2 ** (j+1)
        print(f"*** div = {div} ***")
        print()
        width = haystack.image.shape[1]
        images = [haystack.image[ : , int(width / div * i) : int(width / div * (i+1))] for i in range(div)]
        elapsed = [0] * 2
        A, elapsed[0] = benchmark(lambda patterns: Automaton2d.images(patterns), [pattern])
        
        for image in images:
            _, el =  benchmark(lambda image: A.search2d(image), image)
            elapsed[1] += el
            

        print("pattern:")
        print(f"\tCreating automata: {elapsed[0]}")
        print(f"\tSearching: {elapsed[1]}")
        
        elapsed = [0] * 2
        B, elapsed[0] = benchmark(lambda patterns: Automaton2d.images(patterns), [e])
        for image in images:
            _, el = benchmark(lambda image: B.search2d(image), image)
            elapsed[1] += el
           
        print("e:")
        print(f"\tCreating automata: {elapsed[0]}")
        print(f"\tSearching: {elapsed[1]}")
        
        print()
        print()
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

    for i in range(10):
        A, elapsed[0] = benchmark(
            lambda patterns: Automaton2d.images(patterns), [pattern]
        )
        _, elapsed[1] = benchmark(lambda image: A.search2d(image), haystack.image)

        print("pattern:")
        print(f"\tCreating automata: {elapsed[0]}")
        print(f"\tSearching: {elapsed[1]}")
        pattern_times.append(tuple(elapsed))

    for i in range(10):
        B, elapsed[0] = benchmark(lambda patterns: Automaton2d.images(patterns), [e])
        _, elapsed[1] = benchmark(lambda image: B.search2d(image), haystack.image)

        print("e:")
        print(f"\tCreating automata: {elapsed[0]}")
        print(f"\tSearching: {elapsed[1]}")
        e_times.append(tuple(elapsed))

    results = [
        (
            np.array([t[0] for t in l]).mean(),
            np.array([t[0] for t in l]).std(),
            np.array([t[1] for t in l]).mean(),
            np.array([t[1] for t in l]).std(),
        )
        for l in results
    ]
    results[0] = ("pattern", *results[0])
    results[1] = ("e", *results[1])

    with open("results.csv", "w") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(
            [
                "pattern",
                "Creating automata (mean)",
                "Creating automata (std)",
                "Searching (mean)",
                "Searching (std)",
            ]
        )
        for result in results:
            writer.writerow(result)
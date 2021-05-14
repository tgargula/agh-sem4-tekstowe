from metrics.metrics import dice, cosine, lcs, levenshtein
from metrics.cluster import cluster

metrics = [
    (dice, 0.4, {'length': 2}),
    (cosine, 0.6, {'length': 2}),
    (lcs, 0.85, {}),
    (levenshtein, 0.7, {})
]

if __name__ == '__main__':

    with open('lines.txt', 'r') as f:
        lines = f.readlines()

    lines = lines[:500]
    csv = 'out.csv'

    # cluster(lines, metrics, verbose=True, csv=csv, index=1)
    # cluster(lines, metrics, stoplist_freq=30, verbose=True, csv=csv, index=2)
    cluster(lines, metrics, stoplist_freq=50, verbose=True, csv=csv, index=3)

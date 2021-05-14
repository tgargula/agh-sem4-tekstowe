from itertools import combinations
import numpy as np


def centroid(cluster, metric, **kwargs):
    dist = np.zeros(shape=(len(cluster)))

    for i, j in combinations(range(len(cluster)), 2):
        d = metric([0], [1], [cluster[i], cluster[j]], **kwargs)
        dist[i] += d
        dist[j] += d

    return cluster[np.argmin(dist)]


def cluster_len(cluster, metric, **kwargs):
    d = 0

    n = len(cluster)

    for i, j in combinations(range(n), 2):
        d += metric([0], [1], [cluster[i], cluster[j]], **kwargs)

    return d / (n * (n - 1)) * 2 if n > 1 else 0


def mindist(clusters, metric, **kwargs):
    d = 1

    for i, j in combinations(range(len(clusters)), 2):
        d = min(d, metric([0], [1], [clusters[i], clusters[j]], **kwargs))

    return d


def davies_bouldin_index(clusters, metric, **kwargs):
    def centrdist(x, y):
        return metric([0], [1], [x, y], **kwargs)

    n = len(clusters)

    sigma = np.array([cluster_len(clusters[i], metric, **kwargs)
                     for i in range(n)])
    centr = np.array([centroid(clusters[i], metric, **kwargs)
                     for i in range(n)])

    M = np.array([max([(sigma[i] + sigma[j]) / centrdist(centr[i], centr[j])
                 for j in range(n) if j != i]) for i in range(n)])

    return np.mean(M)


def dunn_index(clusters, metric, **kwargs):
    mlen = max([cluster_len(cluster, metric, **kwargs)
               for cluster in clusters])

    centroids = []
    for cluster in clusters:
        centroids.append(centroid(cluster, metric, **kwargs))

    return mindist(centroids, metric, **kwargs) / mlen

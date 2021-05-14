import numpy as np

from .stoplist import filtered, stoplist
from sklearn.cluster import DBSCAN
from .quality import davies_bouldin_index, dunn_index
    

def cluster(lines, metrics, stoplist_freq=None, verbose=False, csv=None, index=None):
    
    if verbose:
        print(f'### {index} ###')
        
    X = np.arange(len(lines)).reshape(-1, 1)

    if stoplist_freq:
        stop = stoplist(lines, stoplist_freq)

    for metric, eps, kwargs in metrics:
        kwargs['data'] = filtered(lines, stop) if stoplist_freq else lines

        if verbose:
            print(f'{metric.__name__}: Computation started...')

        db = DBSCAN(
            metric=metric,
            metric_params=kwargs,
            algorithm='brute',
            min_samples=1,
            eps=eps
        ).fit(X)

        if verbose:
            print(f'{metric.__name__}: Computation ended...')

        with open(f'out/{metric.__name__}{index}.txt', 'w') as f:
            clusters = zip(db.labels_, lines)
            clusters = sorted(clusters)

            result = [[]]
            prev = 0
            for label, line in clusters:
                if prev < label:
                    result.append([])
                    f.write('\n\n#########################\n')
                    prev = label
                result[-1].append(line)
                f.write(line)

            del kwargs['data']
            
            db_index = davies_bouldin_index(result, metric, **kwargs)
            d_index = dunn_index(result, metric, **kwargs)
            if verbose:
                print(f"Davies-Bouldin index: {db_index}")
                print(f"Dunn index: {d_index}")
            
        if csv:
            with open(f'out/{csv}', 'a') as f:
                f.write(f"{metric.__name__};{stoplist_freq if stoplist_freq else '-'};{db_index};{d_index}\n")

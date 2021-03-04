from algorithms.pattern_matching import fa_preprocessed as fa
from algorithms.pattern_matching import kmp_preprocessed as kmp
from algorithms.pattern_matching import (naive, transition_function,
                                         transition_table)
from algorithms.time_test import test
from data.cache import transition_table as tt

if __name__ == '__main__':
    text = ('abb' * 1000 + 'c') * 1000
    pattern = 'abb' * 10000
    result = {}

    delta = tt.get(pattern, transition_table(pattern))
    pi = transition_function(pattern)

    result['naive'] = test(naive, text, pattern)
    result['fa'] = test(fa, text, delta)
    
    print(result)

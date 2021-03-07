from pprint import pprint

from algorithms.pattern_matching import fa_preprocessed as fa
from algorithms.pattern_matching import kmp_preprocessed as kmp
from algorithms.pattern_matching import naive, prefix_function, transition_table
from algorithms.time_test import test

if __name__ == '__main__':
    text = ('a' * 10000 + 'b' + 'a' * 100 + 'c') * 100
    pattern = 'a' * 7000 + 'b'
    result = {}

    delta = transition_table(pattern)
    pi = prefix_function(pattern)

    result['naive'] = test(naive, text, pattern)
    result['fa'] = test(fa, text, delta)
    result['kmp'] = test(kmp, text, pattern, pi)

    print(result['naive'] / result['fa'] > 5 and result['naive'] / result['kmp'] > 5)
    
    pprint(result)

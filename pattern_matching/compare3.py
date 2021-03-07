from algorithms.pattern_matching import transition_table, prefix_function
from algorithms.time_test import test


if __name__ == '__main__':

    pattern = 'Wstawaj samuraju!'

    result = {}

    result['transition_table'] = test(transition_table, pattern)
    result['prefix_function'] = test(prefix_function, pattern)

    print(result['transition_table'] / result['prefix_function'] > 5)
    print(result)
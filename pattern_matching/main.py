if __name__ == '__main__':

    from algorithms.pattern_matching import transition_table
    open('f.py', 'w').write(str(transition_table('abb' * 10000)))
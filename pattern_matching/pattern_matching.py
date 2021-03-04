import re

def naive_pattern_matching(data, pattern):
    n = len(data)
    m = len(pattern)
    for s in range(n - m + 1):
        if pattern == data[s:s+m]:
            print(f'Przesunięcie {s} jest poprawne')


def transition_table(pattern):
    Q = range(len(pattern) + 1)
    Sigma = set(pattern)
    delta = [{key: 0 for key in Sigma} for _ in Q]

    for q in Q:
        for letter in Sigma:
            k = min(len(Q), q + 2) - 1
            while not re.search(
                    f'{pattern[:k]}$', 
                    pattern[:q] + letter):
                k -= 1
            delta[q][letter] = k
    
    return delta


def finite_automata(data, pattern):
    delta = transition_table(pattern)
    q = 0
    for s, letter in enumerate(data):
        q = delta[q].get(letter, 0)
        if q + 1 == len(delta):
            print(f'Przesunięcie {s - q + 1} jest poprawne')



if __name__ == '__main__':

    naive_pattern_matching('abaaaaabaaadasbaba', 'aba')

    # print(transition_table('aba'))
    finite_automata('abaaaaabaaadasbaba', 'aba')
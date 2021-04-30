from lcs import levenshtein, show

pairs = [
    ('los', 'kloc'),
    ('Łódź', 'Lodz'),
    ('quintessence', 'kwintesencja'),
    ('ATGAATCTTACCGCCTCG', 'ATGAGGCTCTGGCCCCTG')
]

if __name__ == '__main__':

    for a, b in pairs:
        d, route = levenshtein(a, b)
        print(d)
        show(a, b, route)

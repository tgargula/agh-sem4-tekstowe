from ahocorasick import Automaton2d
from ahocorasick.stats import TextStats
from ahocorasick.parser import parse_letter

if __name__ == '__main__':
    with open('haystack.txt', 'r') as f:
        lines = f.readlines()
    
    ts = TextStats(lines)
    letters = TextStats(ts.letters)
    A = Automaton2d(letters)
    
    array = A.search_array(lines)
    
    for i in range(1, len(array)):
        # Note: zip has length of the smallest of zipped elements!
        for j, (x, y) in enumerate(zip(array[i-1], array[i])):
            if x == y:
                letter = parse_letter(ts.letters[x-1])
                print(f"{i}-{i+1}:{j} \t{letter}")
                
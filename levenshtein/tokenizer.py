from spacy.lang.pl import Polish
from spacy.tokens.span import Span
from spacy.tokens import Doc
from random import randrange

nlp = Polish()

def tokenize(filename):
    tokenizer = Polish().tokenizer
    with open(filename, 'r') as f:
        tokens = [tokenizer(line) for line in f.readlines()]
    return tokens


def punch(tokens, level=0.03):
    copy = [nlp(' '.join([token.text for token in line])) for line in tokens]
    size = sum([len(token) for token in copy])
    to_remove = round(level * size)

    while to_remove:
        index = randrange(len(copy))
        line = copy[index]
        if len(line) > 0:
            i = randrange(len(line))
            print(line[:i].text)
            print(line[i+1:].text)
            print(type(line))
            copy[index] = nlp(line[:i].text + line[i+1:].text)
            to_remove -= 1
    
    return copy


if __name__ == '__main__':
    tokens = tokenize('data/romeo-i-julia-700.txt')
    punched = punch(tokens)
    print(1 - sum([len(token) for token in punched]) / sum([len(token) for token in tokens]))

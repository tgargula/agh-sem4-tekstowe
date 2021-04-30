from spacy.lang.pl import Polish
from random import randrange

nlp = Polish()

def tokenize_from_file(filename):
    return tokenize(open(filename, 'r').read())


def tokenize(text):
    return list(nlp.tokenizer(text))


def punch(tokens, level=0.03):
    copy = tokens.copy()
    size = len(copy)
    to_remove = round(level * size)

    while to_remove:
        index = randrange(len(copy))
        if '\n' in copy[index].text_with_ws:
            continue
        copy[index:] = copy[index + 1:]
        to_remove -= 1
    
    return copy


def decompose(tokens):
    return [token.text_with_ws for token in tokens]
    
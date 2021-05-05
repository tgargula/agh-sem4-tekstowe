def ngrams(string, length=2):
    result = {}
    for i in range(len(string) - length + 1):
        ngram = string[i:i+length]
        result[ngram] = result.get(ngram, 0) + 1
    return result


def ngrams_text(text, length=2, delimiter=' '):
    tokens = tuple(text.split(delimiter))
    result = {}
    for i in range(len(tokens) - length + 1):
        ngram = delimiter.join(tokens[i:i+length])
        result[ngram] = result.get(ngram, 0) + 1
    return result

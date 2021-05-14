from collections import Counter

def stoplist(lines, freq):
    words = [word for line in lines for word in line.split(' ') if word != '']
    c = Counter()
    for word in words:
        c[word] += 1
    return {key for key, value in c.items() if value >= freq}

def filtered(lines, stoplist):
    return [' '.join([word for word in line.split(' ') if word not in stoplist]) for line in lines]
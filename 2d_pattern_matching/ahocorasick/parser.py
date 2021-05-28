PARSER = {
    ' ': '<space>',
    '\n': '<newline>'
}

def parse_letter(letter):
    return PARSER.get(letter, letter)
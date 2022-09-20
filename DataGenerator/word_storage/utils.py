def filter_uniq(text):
    words = text.split()
    uniq_words = list(set(words))
    return uniq_words

def save_words(words, file):
    with open(file, 'w') as f:
        for line in words:
            f.write(f"{line}\n")
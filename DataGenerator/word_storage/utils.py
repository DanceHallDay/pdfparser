def filter_uniq(text):
    words = text.split()
    uniq_words = list(set(words))
    return uniq_words


def save_words(words, file):
    with open(file, "w") as f:
        for line in words:
            f.write(f"{line}\n")


def get_text(path):
    with open(path, "r") as text_file:
        text = text_file.read()
    return text


def calc_frequency(text, vocab):
    result = {v: text.count(v) for v in vocab}
    return result


if __name__ == "__main__":
    from DataGenerator.const import VOCABS
    import matplotlib.pyplot as plt
    import os

    vocab_eng = VOCABS["eng_tesseract"]

    folders = os.listdir("legal_doc")
    freq = {k: 0 for k in vocab_eng}
    for f in folders:
        if f.split(".")[-1] == "wl":
            path = "legal_doc/" + f
            with open(path, "r") as file:
                text = file.read().replace("\n", "")

            _freq = calc_frequency(text, vocab_eng)
            for k in freq:
                freq[k] += _freq[k]

    plt.bar(freq.keys(), freq.values(), 3, color="g")
    plt.show()

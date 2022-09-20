from DataGenerator.word_storage.utils import filter_uniq, save_words

def get_text(path):
    with open(path, "r") as text_file:
        text = text_file.read()
    return text


if __name__ == '__main__':
    path_train = 'WikiQA-train.txt'
    path_test = 'WikiQA-test.txt'
    path_dev = 'WikiQA-dev.txt'

    paths = [path_train, path_test, path_dev]

    texts = []
    for path in paths:
        text = get_text(path)
        texts.append(text)

    text = ' '.join(texts)
    words = filter_uniq(text)

    save_words(words, 'wiki_qa.wl')

    print(len(words))


from DataGenerator.word_storage.utils import filter_uniq, save_words, get_text
import os
import gc


def parse_files(files_list: list, path: str, bs=int(1e7)):
    words_set = set()
    for f in files_list:
        text = get_text(f)
        words = filter_uniq(text)
        words_set = words_set.union(set(words))

    words_list = list(words_set)
    save_words(words_list, path)

    del words_set
    gc.collect()


if __name__ == "__main__":
    path_train = "/storage/ocr/cuad/"
    folders = os.listdir(path_train)
    folders = [f for f in folders if f.isdigit()]

    path = "/storage/ocr/cuad/"
    to_save = "/storage/ocr/cuad/words/"
    for f in folders:
        path = path_train + f
        files = os.listdir(path)
        files = [path + "/" + f for f in files]
        print(path.split("/")[-1])
        # if path.split('/')[-1] != '2000':
        #     continue
        words = parse_files(files, to_save + path.split("/")[-1] + ".wl")
        gc.collect()

    # folder_path = '/storage/ocr/cuad/2000'
    # files = os.listdir(folder_path)
    # files = [folder_path + '/' + f for f in files]

    # words = parse_files(files, folder_path + '.wl')
    # print(len(words))

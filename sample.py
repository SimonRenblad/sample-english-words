import random

sample_words = 250
file_path_name = "words_alpha.txt"
out_path_name = "sample.txt"

with open(file_path_name) as f:
    word_list = f.read().splitlines()

sample_list = random.sample(word_list, sample_words)

with open(out_path_name, "w") as out_f:
    for word in sample_list:
        out_f.write(word + " ")
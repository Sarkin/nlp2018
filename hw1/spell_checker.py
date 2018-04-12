from collections import Counter
from collections import defaultdict
import re
import sys


def text_to_wordlist(sentence):
    regexp = "[^а-яА-Яё]"
    sentence = re.sub(regexp, " ", sentence)
    result = sentence.lower().split()
    return result


def get_trigram_frequencies(text):
    words = list(map(embellish_word, text_to_wordlist(text)))

    trigrams = [w[i:i+3] for w in words for i in range(len(w) - 2)]

    trigram_cnt = Counter(trigrams)
    n_trigrams = sum(trigram_cnt.values())

    p_trigram = defaultdict(float)
    for k in trigram_cnt:
        p_trigram[k] = trigram_cnt[k] / n_trigrams

    return p_trigram


def embellish_word(w):
    return "##" + w + "##"


def check_spelling(word, p_threshold, p_trigram):
    mword = embellish_word(word)

    for i in range(len(mword) - 2):
        if p_trigram[mword[i:i+3]] < p_threshold:
            return False

    return True


def main():
    with open("wp.txt", "r") as fin:
        text = fin.read()

    p_trigram = get_trigram_frequencies(text)

    print(check_spelling("ABCDEF", 0.00001, p_trigram))
    print(check_spelling("делал", 0.00001, p_trigram))


if __name__ == "__main__":
    sys.exit(main())

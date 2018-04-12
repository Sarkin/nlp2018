import re
import sys
from collections import Counter

import pymorphy2


def pymorphy_test():
    analyzer = pymorphy2.MorphAnalyzer()

    print(analyzer.normal_forms("руки"))

    print('\n'.join(["score {} for tags: {}".format(p.score, p.tag) for p in analyzer.parse("руки")]))

    print('\n'.join(["normal form: {} score: {} tag: {}".format(p.normal_form, p.score, p.tag) for p in analyzer.parse("три")]))

    print(analyzer.parse("руки")[0].lexeme)

    grammems = frozenset(("ablt", "plur"))
    print(analyzer.parse("турок")[0].inflect(grammems).word)

    print("POS for майню: {}".format(analyzer.parse("майню")[0].tag.POS))


def text_to_wordlist(sentence):
    regexp = "[^а-яА-Яё]"
    sentence = re.sub(regexp, " ", sentence)
    result = sentence.lower().split()
    return result


def text_stats():
    with open("wp.txt", "r") as fin:
        text = fin.read()
    words = text_to_wordlist(text)

    print("Word count {}".format(len(words)))

    analyzer = pymorphy2.MorphAnalyzer()

    noun_lemmas = list()
    verb_lemmas = list()
    for w in words:
        p = analyzer.parse(w)[0]
        if 'NOUN' in p.tag:
            noun_lemmas.append(p.normal_form)
        elif 'VERB' in p.tag:
            verb_lemmas.append(p.normal_form)

    print(Counter(noun_lemmas).most_common(10))
    print(Counter(verb_lemmas).most_common(10))

def main():
    pymorphy_test()
    text_stats()

if __name__ == "__main__":
    sys.exit(main())

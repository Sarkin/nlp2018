from collections import defaultdict
import re
import sys


class Trie:
    def __init__(self, words, costs):
        self.root = dict()

        for w in words:
            self.add(w)

        self.costs = costs


    def create_node(self):
        return dict()


    def get_node(self, node, nxt):
        if nxt in node:
            return node[nxt]

        return None

    def get_or_create_node(self, node, nxt):
        if nxt not in node:
            node[nxt] = self.create_node()

        return node[nxt]


    def add(self, w, root=None):
        if root is None:
            root = self.root

        w += "$"
        for c in w:
            root = self.get_or_create_node(root, c)

    def find_closest_rec(self, w, budget, root, cur_word):
        if budget < 0:
            return []

        if not w:
            return [(budget, cur_word)]

        candidates = []

        if len(w) > 1:
            candidates += self.find_closest_rec(w[1:], budget - self.costs["delete"], root, cur_word)
            for key in root:
                candidates += self.find_closest_rec(w[1:], budget - self.costs["change"], root[key], cur_word + key)

        for key in root:
            candidates += self.find_closest_rec(w, budget - self.costs["delete"], root[key], cur_word + key)

        if len(w) > 2:
            candidates += self.find_closest_rec(w[1:2] + w[0:1] + w[2:], budget - self.costs["swap"], root, cur_word)

        if w[0] in root:
            candidates += self.find_closest_rec(w[1:], budget, root[w[0]], cur_word + w[0])

        return candidates


    def find_closest(self, w, budget):
        return list(set((budget - x, y) for (x, y) in self.find_closest_rec(w, budget, self.root, "")))




def text_to_wordlist(sentence):
    regexp = "[^а-яА-Яё]"
    sentence = re.sub(regexp, " ", sentence)
    result = sentence.lower().split()
    return result


def main():
    with open("wp.txt", "r") as fin:
        text = fin.read()

    words = text_to_wordlist(text)

    trie = Trie(words, {"delete": 1, "change": 1, "swap": 1})

    print(trie.find_closest("княжь", 1))



if __name__ == "__main__":
    sys.exit(main())

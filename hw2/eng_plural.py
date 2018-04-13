import re
import sys


def get_exception_plural(lemma):
    exceptions = {"cactus" : ["cacti", "cactuses"], "mouse" : ["mice"], "goose" : ["geese"], "index" : ["indices", "indexes"], "formula" : ["formulas", "formulae"]}
    if lemma in exceptions:
        return exceptions[lemma]

    return None


def get_category(s):
    m = re.match("^([a-z]+)\+(N)\+(Sg|Pl)$", s)

    if not m:
        return None

    return m.group(1), m.group(2), m.group(3)


def has_siblant_ending(lemma):
    return re.match("^[a-z]*(s|x|z|ch|sh)$", lemma) is not None


def has_cy_ending(lemma):
    return re.match("^[a-z]*[^aeoiuy]y$", lemma) is not None

def produce_form(s):
    category = get_category(s)

    if category is None:
        return ["Wrong Input"]

    lemma, tag, number = category
    forms = []

    if number == "Sg":
        return [lemma]
    else:
        exception_forms = get_exception_plural(lemma)

        if exception_forms is not None:
            return exception_forms

        if has_siblant_ending(lemma):
            return [lemma + "es"]

        if has_cy_ending(lemma):
            return [lemma[:-1] + "ies"]
        return [lemma + "s"]


def main():
    for line in sys.stdin:
        print(produce_form(line))


if __name__ == "__main__":
    sys.exit(main())

from random import randint


def _shuffle(cards: list[str]):
    n = len(cards)
    for i in range(n):
        j = randint(i, n-1)
        cards[i], cards[j] = cards[j], cards[i]
    return cards


def shuffle(cards: list[str]):
    for i in range(3):
        _shuffle(cards)
    return cards

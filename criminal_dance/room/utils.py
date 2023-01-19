from random import randint
from ayaka import AyakaChannel
from ..cat import cat


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


async def send_private(uid: str, msg: str):
    await cat.base_send(channel=AyakaChannel(type="private", id=uid), msg=msg)

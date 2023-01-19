from random import choice, sample, randint
from ayaka import AyakaChannel
from ..cat import cat

unique_3 = ["第一发现人", "犯人", "侦探", "不在场证明"]
unique_4 = ["第一发现人", "犯人", "侦探", "不在场证明", "共犯"]
unique_5 = ["第一发现人", "犯人", "侦探", "不在场证明", "不在场证明", "共犯"]
unique_6 = ["第一发现人", "犯人", "侦探", "侦探", "不在场证明", "不在场证明", "共犯", "共犯"]
unique_7 = ["第一发现人", "犯人", "侦探", "侦探", "不在场证明", "不在场证明", "不在场证明", "共犯", "共犯"]
unique_8 = [
    "第一发现人", "犯人", "侦探", "侦探", "侦探", "不在场证明", "不在场证明", "不在场证明", "不在场证明", "不在场证明", "共犯", "共犯"
]

unique = [
    0, 0, 0,
    unique_3,
    unique_4,
    unique_5,
    unique_6,
    unique_7,
    unique_8,
]


def get_unique(n: int) -> list[str]:
    return unique[n]


normal = [
    "普通人", "普通人", "谣言", "谣言", "谣言", "谣言", "情报交换", "情报交换", "情报交换", "情报交换", "目击者", "目击者", "目击者", "目击者", "交易", "交易", "交易", "交易"
]

normal_n = [
    0, 0, 0,
    8,
    11,
    14,
    15,
    17,
    18,
]


def get_normal(n: int):
    return sample(normal, normal_n[n])


pro = ["神犬", "警部"]


def get_pro(n: int):
    if n < 6:
        return []
    if n == 6:
        return [choice(pro)]
    return pro


def get_cards(n: int):
    # ---- 临时调试 ----
    return [
        "第一发现人", "目击者", "普通人", "犯人",
        "共犯", "普通人", "神犬", "侦探",
        "交易", "谣言", "情报交换", "共犯"
    ]
    # ---- 临时调试 ----

    return get_normal(n) + get_unique(n) + get_pro(n)


def _shuffle(cards: list[str]):
    n = len(cards)
    for i in range(n):
        j = randint(i, n-1)
        cards[i], cards[j] = cards[j], cards[i]
    return cards


def shuffle(cards: list[str]):
    # ---- 临时调试 ----
    return cards
    # ---- 临时调试 ----

    for i in range(3):
        _shuffle(cards)
    return cards


async def send_private(uid: str, msg: str):
    await cat.base_send(channel=AyakaChannel(type="private", id=uid), msg=msg)

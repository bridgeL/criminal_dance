from random import sample
from ..config import R


# 独特池
unique_3 = [R.第一发现人, R.犯人, R.侦探, R.不在场证明]
unique_4 = [R.第一发现人, R.犯人, R.侦探, R.不在场证明, R.共犯]
unique_5 = [R.第一发现人, R.犯人, R.侦探, R.不在场证明, R.不在场证明, R.共犯]
unique_6 = [R.第一发现人, R.犯人, R.侦探, R.侦探, R.不在场证明, R.不在场证明, R.共犯, R.共犯]
unique_7 = [R.第一发现人, R.犯人, R.侦探, R.侦探, R.不在场证明, R.不在场证明, R.不在场证明, R.共犯, R.共犯]
unique_8 = [
    R.第一发现人, R.犯人, R.侦探, R.侦探, R.侦探, R.不在场证明, R.不在场证明, R.不在场证明, R.不在场证明, R.不在场证明, R.共犯, R.共犯
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

# 普通池
normal = [
    R.普通人, R.普通人, R.谣言, R.谣言, R.谣言, R.谣言, R.情报交换, R.情报交换, R.情报交换, R.情报交换, R.目击者, R.目击者, R.目击者, R.目击者, R.交易, R.交易, R.交易, R.交易
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

# 加强池
pro = [R.神犬, R.警部]
pro_n = [
    0, 0, 0,
    0,
    0,
    0,
    1,
    2,
    2,
]


def get_cards(n: int):
    # ---- 临时调试
    return [
        "第一发现人", "神犬", "普通人", "普通人",
        "共犯", "普通人", "普通人", "普通人",
        "普通人", "普通人", "普通人", "犯人",
    ]
    
    return unique[n] + sample(normal, normal_n[n]) + sample(pro, pro_n[n])

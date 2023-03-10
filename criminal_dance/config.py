'''配置'''
from pydantic import BaseModel
from ayaka import AyakaConfig


class Rename(BaseModel):
    第一发现人: str = "第一发现人"
    犯人: str = "犯人"
    神犬: str = "神犬"
    警部: str = "警部"
    共犯: str = "共犯"
    普通人: str = "普通人"
    不在场证明: str = "不在场证明"
    目击者: str = "目击者"
    侦探: str = "侦探"
    谣言: str = "谣言"
    交易: str = "交易"
    情报交换: str = "情报交换"


class Config(AyakaConfig):
    __config_name__ = "犯人在跳舞"
    overtime: int = 90
    auto_card_help: bool = True
    '''每打一张牌，就自动发送该牌的帮助'''
    rename: Rename = Rename()


config = Config()
'''配置'''

R = config.rename
'''config.rename的缩写'''

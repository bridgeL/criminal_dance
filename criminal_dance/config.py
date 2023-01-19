'''配置'''
from ayaka import AyakaConfig
from .cat import cat


class Config(AyakaConfig):
    __config_name__ = cat.name
    overtime: int = 90


config = Config()

'''配置'''
from ayaka import AyakaConfig
from .cat import cat


class Config(AyakaConfig):
    __config_name__ = cat.name
    # overtime: int = 90
    overtime: int = 2


config = Config()

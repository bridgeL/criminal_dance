import asyncio
from random import choice
from typing import TYPE_CHECKING
from .config import config

if TYPE_CHECKING:
    from .model import Player


def set_overtime_task(player: "Player"):
    '''设置超时任务'''
    loop = asyncio.get_event_loop()
    player.fut = loop.create_future()
    loop.create_task(overtime(player))


async def overtime(player: "Player"):
    try:
        print("开启计时器")
        await asyncio.wait_for(player.fut, config.overtime)
    except asyncio.exceptions.TimeoutError:
        print("超时了")
        card = choice(player.cards)
        player.cards.remove(card)
        await player.game.send(f"{player.index_name} 被系统强制丢弃了{card}")
        if card == "犯人":
            player.is_good = False
            await player.game.end(True)
        else:
            await player.game.turn_next()
    else:
        print("关闭计时器")

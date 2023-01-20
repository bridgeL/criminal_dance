'''第一发现人超时'''
import asyncio
from ..model import Player
from ..config import config, R


def set_overtime_task(player: Player):
    '''设置超时任务'''
    loop = asyncio.get_event_loop()
    player.fut = loop.create_future()
    loop.create_task(overtime(player))


async def overtime(player: Player):
    try:
        await asyncio.wait_for(player.fut, config.overtime)
    except asyncio.exceptions.TimeoutError:
        card = R.第一发现人
        player.cards.remove(card)
        player.game.first = True
        await player.game.send(f"{player.index_name} 被系统强制丢弃了{card}")
        await player.game.turn_next()
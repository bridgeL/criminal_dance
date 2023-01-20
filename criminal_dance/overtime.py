'''打牌超时'''
import asyncio
from random import choice
from typing import TYPE_CHECKING
from .config import config, R

if TYPE_CHECKING:
    from .model import Player


def set_overtime_task(player: "Player"):
    '''设置超时任务'''
    loop = asyncio.get_event_loop()
    player.fut = loop.create_future()
    loop.create_task(overtime(player))


async def overtime(player: "Player"):
    try:
        await asyncio.wait_for(player.fut, config.overtime)
    except asyncio.exceptions.TimeoutError:
        game = player.game
        async with game.lock:
            card = choice(player.cards)
            player.cards.remove(card)
            await game.send(f"{player.index_name} 被系统强制丢弃了{card}")
            if card == R.犯人:
                player.is_good = False
                await game.end(True)
            else:
                await game.turn_next()

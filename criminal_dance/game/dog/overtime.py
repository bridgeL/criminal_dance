'''神犬超时'''
import asyncio
from random import choice
from ...model import Player
from ...config import config, R


def set_overtime_task(player: Player):
    '''设置超时任务'''
    loop = asyncio.get_event_loop()
    player.fut = loop.create_future()
    loop.create_task(overtime(player))


async def overtime(player: Player):
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
                owner = game.get_player(game.dog.owner_id)
                owner.is_good = True
                return await game.end(True)

            player.cards.append(R.神犬)
            await game.send(f"{player.index_name} 获得{R.神犬}牌")

            game.set_state("game")
            await game.turn_next()

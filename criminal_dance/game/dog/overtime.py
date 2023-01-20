import asyncio
from random import choice
from ...model import Player
from ...config import config


def set_overtime_task(player: Player):
    '''设置超时任务'''
    loop = asyncio.get_event_loop()
    player.fut = loop.create_future()
    loop.create_task(overtime(player))


async def overtime(player: Player):
    try:
        print("开启计时器")
        await asyncio.wait_for(player.fut, config.overtime)
    except asyncio.exceptions.TimeoutError:
        print("超时了")
        game = player.game
        card = choice(player.cards)
        player.cards.remove(card)
        await game.send(f"{player.index_name} 被系统强制丢弃了{card}")

        if card == "犯人":
            player.is_good = False
            owner = game.get_player(game.dog.owner_id)
            owner.is_good = True
            return await game.end(True)

        player.cards.append("神犬")
        await game.send(f"{player.index_name} 获得神犬牌")

        game.set_state("game")
        await game.turn_next()
    else:
        print("关闭计时器")

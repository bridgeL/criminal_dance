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
        give = game.round_give.get_give(player.id)
        async with game.lock:
            card = choice(player.cards)
            give.card = card
            await player.send(f"您被系统强制交出了{card}")
            await game.send(f"{give.giver.index_name} 已决定好卡牌")

            # 判断是否完成
            if game.round_give.all_given:
                # 私聊 互相给牌
                game.round_give.set_receivers()
                await game.round_give.convey_all()
                await asyncio.sleep(2)
                
                game.set_state("game")
                await game.turn_next()

    else:
        print("关闭计时器")

import asyncio
from random import choice
from ..cat import cat
from ..model import Game
from ..config import config


async def check_first():
    '''检查第一发现人是否已打出'''
    game = cat.get_data(Game)
    if not game.first:
        await cat.send("第一张牌必须是第一发现人")
        return False
    return True


async def check_player():
    '''检查是否在游戏中，是否轮到其行动'''
    game = cat.get_data(Game)
    player = game.get_player(cat.user.id)
    if not player:
        await cat.send("你没参与游戏")
        return False
    if player != game.current_player:
        await cat.send("没轮到你")
        return False
    return True


async def check_card(card: str):
    '''检查是否有此牌'''
    game = cat.get_data(Game)
    player = game.current_player
    if card not in player.cards:
        await cat.send(f"[{player.name}] 没有 [{card}]")
        return False
    return True


async def play_card(card: str):
    '''打出一张牌并通知'''
    game = cat.get_data(Game)
    player = game.current_player
    player.cards.remove(card)
    await cat.send(f"[{player.name}] 打出 [{card}]")
    await stop_timer()


async def turn_next():
    '''移交行动权并通知'''
    game = cat.get_data(Game)
    game.turn_next()
    await cat.send(f"现在轮到 [{game.current_player.name}] 出牌")
    await start_timer()


async def start_timer():
    '''超时会被系统强制弃牌（防止挂机）'''
    game = cat.get_data(Game)
    game.fut = asyncio.get_event_loop().create_future()
    try:
        await asyncio.wait_for(game.fut, config.overtime)
    except asyncio.exceptions.TimeoutError:
        player = game.current_player
        card = choice(player.cards)
        player.cards.remove(card)
        await cat.send(f"[{player.name}] 被系统强制丢弃了 [{card}]")
        if card == "犯人":
            player.good_person = False
            goods, bads = game.end()
            items = [
                "，".join(goods) + "赢了",
                "，".join(bads) + "输了",
            ]
            await cat.send("\n".join(items))

            cat.state = "room"
            await cat.send("已返回房间")
        else:
            await turn_next()


async def stop_timer():
    game = cat.get_data(Game)
    game.fut.set_result(True)


async def refresh_timer():
    await stop_timer()
    await start_timer()

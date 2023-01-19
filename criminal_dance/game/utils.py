import asyncio
from random import choice
from ..cat import cat
from ..model import Game, Player
from ..config import config


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


async def check_first():
    '''检查 第一发现人是否已打出'''
    game = cat.get_data(Game)
    if not game.first:
        await cat.send("第一张牌必须是第一发现人")
        stop_timer()
        start_timer()
        return False
    return True


async def check_card(card: str, player: Player | None = None):
    '''检查 player 是否有此牌'''
    if not player:
        game = cat.get_data(Game)
        player = game.current_player
    if card not in player.cards:
        await cat.send(f"[{player.name}] 没有 [{card}]")
        stop_timer()
        start_timer()
        return False
    return True


async def play_card(card: str, player: Player | None = None):
    '''player 打出一张牌并通知'''
    if not player:
        game = cat.get_data(Game)
        player = game.current_player
    player.cards.remove(card)
    await cat.send(f"[{player.name}] 打出 [{card}]")
    stop_timer()


async def turn_next():
    '''game.current_player 移交行动权并通知'''
    game = cat.get_data(Game)
    game.turn_next()
    await cat.send(f"现在轮到 [{game.current_player.name}] 出牌")
    start_timer()


async def overtime(player: Player):
    game = cat.get_data(Game)
    try:
        await asyncio.wait_for(game.fut, config.overtime)
    except asyncio.exceptions.TimeoutError:
        if not game.first:
            card = "第一发现人"
            game.first = True
        else:
            card = choice(player.cards)
        player.cards.remove(card)
        await cat.send(f"[{player.name}] 被系统强制丢弃了 [{card}]")
        if card == "犯人":
            player.good_person = False
            await game_end(True)
        else:
            await turn_next()


def start_timer(player: Player | None = None):
    '''超时会被系统强制弃牌（防止挂机）'''
    game = cat.get_data(Game)
    game.fut = asyncio.get_event_loop().create_future()
    if not player:
        player = game.current_player
    asyncio.create_task(overtime(player))


def stop_timer():
    game = cat.get_data(Game)
    game.fut.set_result(True)


async def check_at_one_player():
    '''指定一位玩家'''
    game = cat.get_data(Game)
    player = game.get_player(cat.event.at)
    if not player:
        await cat.send("你需要at一个游戏中的玩家")
        stop_timer()
        start_timer()
        return False
    return True


async def game_end(good_win: bool):
    '''游戏结束，返回房间'''
    game = cat.get_data(Game)
    if good_win:
        winners, losers = game.end()
    else:
        losers, winners = game.end()
    items = [
        "，".join(winners) + "赢了",
        "，".join(losers) + "输了",
    ]
    await cat.send("\n".join(items))
    await cat.send("已返回房间")
    cat.state = "room"

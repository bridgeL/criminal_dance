'''谣言'''
from asyncio import sleep
from random import choice
from ..cat import cat
from ..model import Game
from ..config import R


@cat.on_cmd(cmds=R.谣言, states="game", auto_help=False)
async def rumor():
    # 排除私聊发送的消息
    if cat.event.origin_channel:
        return

    game = cat.get_data(Game)

    # 排除未参加游戏的人
    player = game.get_player(cat.user.id)
    if not player:
        return

    async with game.lock:
        card = cat.cmd
        if not await player.check(card):
            return

        await player.play_card(card)

        # 所有有牌的人
        ps = [p for p in game.players if p.cards]
        game.round_give.init(ps)

        # 被随机抽一张牌
        for g in game.round_give.gives:
            g.card = choice(g.giver.cards)

        # 设置接收方为上家
        game.round_give.set_receivers()

        await cat.send("谣言抽取中...")

        await game.round_give.convey_all()
        await sleep(2)
        await game.turn_next()

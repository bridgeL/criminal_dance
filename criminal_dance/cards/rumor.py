'''谣言'''
from asyncio import sleep
from random import choice
from ..model import on_cmd, Game
from ..config import R


@on_cmd(cmds=R.谣言, states="game")
async def rumor(game: Game):
    # 所有有牌的人
    ps = [p for p in game.players if p.cards]
    game.round_give.init(ps)

    # 被随机抽一张牌
    for g in game.round_give.gives:
        g.card = choice(g.giver.cards)

    # 设置接收方为上家
    game.round_give.set_receivers()

    await game.send(f"{R.谣言}抽取中...")
    await game.round_give.convey_all()
    await sleep(2)

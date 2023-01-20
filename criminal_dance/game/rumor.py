'''谣言'''
from asyncio import sleep
from random import choice
from ..cat import cat
from ..model import Game, Give
from .utils import turn_next, check_player, check_card, play_card, check_first
from ..room.cards import send_private


@cat.on_cmd(cmds="谣言", states="game")
async def rumor():
    game = cat.get_data(Game)
    async with game.lock:

        if not await check_player():
            return

        if not await check_first():
            return

        card = cat.cmd
        if not await check_card(card):
            return

        await play_card(card)

        # 所有有牌的人随机抽一张牌
        ps = [p for p in game.players if p.cards]
        gs = [Give(giver=p, card=choice(p.cards)) for p in ps]

        # 设置接收方为上家
        ps = [ps[-1], *ps[:-1]]
        for p, g in zip(ps, gs):
            g.recver = p

        await cat.send("谣言抽取中...")

        for g in gs:
            g.convey()
            await send_private(g.recver.id, f"你抽到了 下家 [{g.giver.name}] 的 [{g.card}]")
            items = ["你的手牌", *g.recver.cards]
            await send_private(g.recver.id, "\n".join(items))

        await sleep(2)
        await turn_next()

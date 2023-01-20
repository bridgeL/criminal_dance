'''谣言'''
from asyncio import sleep
from random import choice
from ..cat import cat
from ..model import Game, GiveAction
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

        # 所有有牌的人被随机抽一张牌
        ps = [p for p in game.players if p.cards]
        gs = [GiveAction(giver=p, card=choice(p.cards)) for p in ps]

        # 设置接收方为上家
        ps = [ps[-1], *ps[:-1]]
        for p, g in zip(ps, gs):
            g.receiver = p

        await cat.send("谣言抽取中...")

        for g in gs:
            g.convey()
            await g.giver.send(f"您的上家 {g.receiver.index_name} 抽走了您的{g.card}")

        for g in gs:
            await g.receiver.send(f"您抽到了下家 {g.giver.index_name} 的{g.card}")
            items = ["您当前的手牌\n", *g.receiver.cards]
            await g.receiver.send("\n".join(items))

        await sleep(2)
        await game.turn_next()

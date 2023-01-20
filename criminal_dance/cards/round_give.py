'''交易'''
import asyncio
from random import choice
from ..model import on_cmd, on_overtime, set_rg_cmd, Game, Player
from ..config import R


@on_cmd(cmds=R.情报交换, states="game", auto_turn_next=False)
async def round_give(game: Game):
    # 所有有牌的人
    ps = [p for p in game.players if p.cards]
    game.round_give.init(ps)
    await game.send(f"{R.情报交换}进行中...\n请参与者通过私聊告知bot要给出的手牌")

    # 私聊通知
    for g in game.round_give.gives:
        await g.giver.send("请在这里发送您要给出的牌")
        # 设置超时任务
        overtime(g.giver)

    game.set_state("round_give")


set_rg_cmd(
    cmds=[
        R.共犯, R.普通人, R.不在场证明, R.目击者, R.侦探, R.交易,
        R.谣言, R.情报交换, R.警部, R.犯人, R.神犬
    ],
    states="round_give",
    name="set_round_give"
)


@on_overtime
async def overtime(player: Player):
    game = player.game
    give = game.round_give.get_give(player.id)
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

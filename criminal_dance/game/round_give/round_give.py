'''交易'''
from .overtime import set_overtime_task
from ...on import on_cmd, set_rg_cmd, Game
from ...config import R


@on_cmd(cmds=R.情报交换, states="game")
async def round_give(game: Game):
    # 所有有牌的人
    ps = [p for p in game.players if p.cards]
    game.round_give.init(ps)
    await game.send(f"{R.情报交换}进行中...\n请参与者通过私聊告知bot要给出的手牌")

    # 私聊通知
    for g in game.round_give.gives:
        await g.giver.send("请在这里发送您要给出的牌")
        # 设置超时任务
        set_overtime_task(g.giver)

    game.set_state("round_give")


set_rg_cmd(
    cmds=[
        R.共犯, R.普通人, R.不在场证明, R.目击者, R.侦探, R.交易,
        R.谣言, R.情报交换, R.警部, R.犯人, R.神犬
    ],
    states="round_give"
)

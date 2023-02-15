'''侦探'''
from ..model import on_cmd, Game, Player, AtPlayer
from ..config import R


@on_cmd(cmds=R.侦探, states="game", max_num=2, at_require=True, auto_turn_next=False)
async def detect(game: Game, player: Player, p2: AtPlayer):
    await game.send(f"目标是 {p2.index_name}！")

    # 侦探排查中...
    if R.犯人 in p2.cards and R.不在场证明 not in p2.cards:
        player.is_good = True
        p2.is_good = False
        return await game.end(True)

    await game.send(f"{p2.index_name} 不是{R.犯人}~")
    await game.turn_next()

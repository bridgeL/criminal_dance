'''警部'''
from ..model import on_cmd, Game, Player, AtPlayer
from ..config import R


@on_cmd(cmds=R.警部, states="game", max_num=2, at_require=True)
async def police(game: Game, player: Player, p2: AtPlayer):
    await game.send(f"目标是 {p2.index_name}！")
    game.police.target_id = p2.id
    game.police.owner_id = player.id

'''共犯'''
from ..model import on_cmd, Player
from ..config import R


@on_cmd(cmds=R.共犯, states="game")
async def accomplice(player: Player):
    player.is_good = False

'''不在场证明'''
from ..on import on_cmd, Game
from ..config import R


@on_cmd(cmds=R.不在场证明, states="game")
async def cert(game: Game):
    game.cert_num -= 1
    await game.turn_next()

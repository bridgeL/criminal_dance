'''第一发现人'''
from ..on import on_cmd, Game
from ..config import R


@on_cmd(cmds=R.第一发现人, states="game")
async def first(game: Game):
    game.first = True
    await game.turn_next()

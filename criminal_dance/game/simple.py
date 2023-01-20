'''普通人'''
from ..on import on_cmd, Game
from ..config import R


@on_cmd(cmds=R.普通人, states="game")
async def simple(game: Game):
    await game.turn_next()

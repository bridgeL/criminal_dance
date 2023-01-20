'''第一发现人'''
from ..model import on_cmd, Game
from ..config import R


@on_cmd(cmds=R.第一发现人, states="game")
async def first(game: Game):
    game.first = True

'''普通人'''
from ..model import on_cmd
from ..config import R


@on_cmd(cmds=R.普通人, states="game")
async def simple():
    pass

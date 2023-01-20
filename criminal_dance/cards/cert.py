'''不在场证明'''
from ..model import on_cmd
from ..config import R


@on_cmd(cmds=R.不在场证明, states="game")
async def cert():
    pass

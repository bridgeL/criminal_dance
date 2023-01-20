'''共犯'''
from ..on import on_cmd, Game, Player
from ..config import R


@on_cmd(cmds=R.共犯, states="game")
async def accomplice(game: Game, player: Player):
    player.is_good = False
    await game.turn_next()

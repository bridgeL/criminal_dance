'''目击者'''
from asyncio import sleep
from ..on import on_cmd, Game, Player, AtPlayer
from ..config import R


@on_cmd(cmds=R.目击者, states="game", at_require=True)
async def watch(game: Game, player: Player, p2: AtPlayer):
    items = [f"{p2.index_name} 的手牌是\n", *p2.cards]
    await player.send("\n".join(items))

    await game.send(f"{R.目击者}观察中...")
    await sleep(2)

    await game.turn_next()

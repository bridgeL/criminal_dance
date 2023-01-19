'''普通人'''
from ..cat import cat
from ..model import Game
from .utils import turn_next, check_player, check_card, play_card, check_first


@cat.on_cmd(cmds="普通人", states="game")
async def simple():
    game = cat.get_data(Game)
    async with game.lock:
        
        if not await check_player():
            return

        if not await check_first():
            return

        card = cat.cmd
        if not await check_card(card):
            return

        await play_card(card)
        await turn_next()

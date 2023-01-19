'''第一发现人'''
from ..cat import cat
from ..model import Game
from .utils import turn_next, check_player, check_card, play_card


@cat.on_cmd(cmds="第一发现人", states="game")
async def first_one():
    '''打出第一发现人'''
    if not await check_player():
        return

    card = cat.cmd
    if not await check_card(card):
        return

    await play_card(card)
    
    game = cat.get_data(Game)
    game.first = True

    await turn_next()

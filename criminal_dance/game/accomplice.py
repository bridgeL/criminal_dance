'''共犯'''
from ..cat import cat
from ..model import Game
from .utils import turn_next, check_player, check_card, play_card


@cat.on_cmd(cmds="共犯", states="game")
async def accomplice():
    if not await check_player():
        return

    card = cat.cmd
    if not await check_card(card):
        return

    await play_card(card)

    game = cat.get_data(Game)
    game.current_player.good_person = False

    await turn_next()

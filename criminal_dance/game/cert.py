'''不在场证明'''
from ..cat import cat
from ..model import Game
from .utils import turn_next, check_player, check_card, play_card, check_first


@cat.on_cmd(cmds="不在场证明", states="game")
async def cert():
    game = cat.get_data(Game)
    async with game.lock:
    
        if not await check_player():
            return

        if not await check_first():
            return

        card = cat.cmd
        if not await check_card(card):
            return

        game.cert_num -= 1

        await play_card(card)
        await turn_next()

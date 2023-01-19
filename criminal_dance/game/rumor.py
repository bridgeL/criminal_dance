'''谣言'''
from ..cat import cat
from ..model import Game
from .utils import turn_next, check_player, check_card, play_card, check_first


@cat.on_cmd(cmds="谣言", states="game")
async def rumor():
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

        # 所有有手牌的人，寻找有手牌的下家，同时、同步抽取一张牌

        #

        await turn_next()

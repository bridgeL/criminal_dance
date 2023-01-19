'''谣言'''
from random import choice
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

        ps = [p for p in game.players if p.cards]

        cs = []
        for p in ps:
            c = choice(p.cards)
            p.cards.remove(c)
            cs.append(c)

        cs = [*cs[1:], cs[0]]
        for c, p in zip(cs, ps):
            p.cards.append(c)

        await turn_next()

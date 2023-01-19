'''临时'''
from ..cat import cat
from .utils import turn_next, check_player, check_card, play_card, check_first


@cat.on_cmd(cmds=["谣言", "情报交换", "交易", "警部"], states="game")
async def temp():
    if not await check_player():
        return

    if not await check_first():
        return

    card = cat.cmd
    if not await check_card(card):
        return

    await play_card(card)
    await turn_next()

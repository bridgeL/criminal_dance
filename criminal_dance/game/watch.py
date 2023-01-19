'''目击者'''
from asyncio import sleep
from ..cat import cat
from ..model import Game
from ..room.utils import send_private
from .utils import turn_next, check_player, check_card, play_card, check_at_one_player, check_first


@cat.on_cmd(cmds="目击者", states="game")
async def watch():
    game = cat.get_data(Game)
    async with game.lock:

        if not await check_player():
            return

        if not await check_first():
            return

        card = cat.cmd
        if not await check_card(card):
            return

        if not await check_at_one_player():
            return

        await play_card(card)

        p2 = game.get_player(cat.event.at)
        items = [f"[{p2.name}]的手牌是", *p2.cards]
        await send_private(cat.user.id, "\n".join(items))
        
        await cat.send("目击者观察中...")
        await sleep(2)

        await turn_next()

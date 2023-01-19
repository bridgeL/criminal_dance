'''目击者'''
from asyncio import sleep
from ..cat import cat
from ..model import Game
from ..room.utils import send_private
from .utils import turn_next, check_player, check_card, play_card, refresh_timer, check_first


@cat.on_cmd(cmds="目击者", states="game")
async def watch():
    if not await check_player():
        return

    if not await check_first():
        return 

    card = cat.cmd
    if not await check_card(card):
        return

    if not cat.event.at:
        await refresh_timer()
        await cat.send("你需要at一个对象")
        return

    game = cat.get_data(Game)
    p2 = game.get_player(cat.event.at)
    if not p2:
        await refresh_timer()
        await cat.send("你需要at一个游戏中的对象")
        return

    await play_card(card)

    items = [f"[{p2.name}]的手牌是", *p2.cards]
    await send_private(cat.user.id, "\n".join(items))
    await cat.send("...")
    await sleep(2)
    await turn_next()

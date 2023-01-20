'''目击者'''
from asyncio import sleep
from ..cat import cat
from ..model import Game
from ..config import R


@cat.on_cmd(cmds=R.目击者, states="game", auto_help=False)
async def watch():
    # 排除私聊发送的消息
    if cat.event.origin_channel:
        return

    game = cat.get_data(Game)

    # 排除未参加游戏的人
    player = game.get_player(cat.user.id)
    if not player:
        return

    async with game.lock:
        card = cat.cmd
        if not await player.check(card, at_require=True):
            return

        await player.play_card(card)

        p2 = game.get_player(cat.event.at)
        items = [f"{p2.index_name} 的手牌是\n", *p2.cards]

        await player.send("\n".join(items))
        await game.send(f"{R.目击者}观察中...")
        await sleep(2)
        await game.turn_next()

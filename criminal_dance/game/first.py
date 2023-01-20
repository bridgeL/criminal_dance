'''第一发现人'''
from ..cat import cat
from ..model import Game
from ..config import R


@cat.on_cmd(cmds=R.第一发现人, states="game", auto_help=False)
async def first():
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
        if not await player.check(card):
            return

        game.first = True
        await player.play_card(card)
        await game.turn_next()

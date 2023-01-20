'''犯人'''
from ..cat import cat
from ..model import Game
from ..config import R


@cat.on_cmd(cmds=R.犯人, states="game", auto_help=False)
async def criminal():
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
        if not await player.check(card, max_num=1):
            return

        await player.play_card(card)

        # 被警部抓到了
        if game.police.target_id == player.id:
            p2 = game.get_player(game.police.owner_id)
            p2.is_good = True
            return await game.end(True)

        await game.end(False)

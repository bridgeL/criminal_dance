'''侦探'''
from ..cat import cat
from ..model import Game
from ..config import R


@cat.on_cmd(cmds=R.侦探, states="game", auto_help=False)
async def detect():
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
        if not await player.check(card, max_num=2, at_require=True):
            return

        game.detect_num -= 1
        await player.play_card(card)
        
        p2 = game.get_player(cat.event.at)
        await game.send(f"目标是 {p2.index_name}！")

        # 侦探排查中...
        if R.犯人 in p2.cards and R.不在场证明 not in p2.cards:
            player.is_good = True
            return await game.end(True)

        await game.send(f"{p2.index_name} 不是{R.犯人}~")
        await game.turn_next()

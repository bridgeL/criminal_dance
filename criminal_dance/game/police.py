'''警部'''
'''犯人'''




from ..cat import cat
from ..model import Game
from ..config import R
@cat.on_cmd(cmds=R.警部, states="game", auto_help=False)
async def police():
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

        await player.play_card(card)
        
        game.police.target_id = cat.event.at
        game.police.owner_id = cat.user.id
        p2 = game.get_player(cat.event.at)

        await game.send(f"目标是 {p2.index_name}！")
        await game.turn_next()

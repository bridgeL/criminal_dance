'''游戏局势'''
from ..cat import cat
from ..model import Game
from ..config import R


@cat.on_cmd(cmds="局势", states="*")
async def show_game_info():
    '''查看场面局势'''
    # 排除私聊发送的消息
    if cat.event.origin_channel:
        return

    game = cat.get_data(Game)

    if not game.start:
        return

    items = ["所有玩家剩余手牌数"]
    for p in game.players:
        items.append(f"{p.index_name} {len(p.cards)}张")

    if game.detect_num:
        items.append(f"剩余{R.侦探}牌 {game.detect_num}张")

    if game.cert_num:
        items.append(f"剩余{R.不在场证明}牌 {game.cert_num}张")

    items.append(f"目前轮到 {game.current_player.index_name}")

    await cat.send("\n".join(items))


@cat.on_cmd(cmds="手牌", states="*")
async def show_cards():
    '''私聊展示手牌'''
    # 只接受私聊发送的消息
    if not cat.event.origin_channel:
        return

    game = cat.get_data(Game)

    if not game.start:
        return

    player = game.get_player(cat.event.origin_channel.id)
    items = ["您的手牌\n", *player.cards]
    await player.send("\n".join(items))

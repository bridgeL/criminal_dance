'''游戏局势'''
from ..cat import cat
from ..model import Game


@cat.on_cmd(cmds="局势", states="game")
async def show_game_info():
    '''查看场面局势'''
    # 排除私聊发送的消息
    if cat.event.origin_channel:
        return

    game = cat.get_data(Game)

    items = ["所有玩家剩余手牌数"]
    for p in game.players:
        items.append(f"{p.index_name} {len(p.cards)}张")

    if game.detect_num:
        items.append(f"剩余侦探牌 {game.detect_num}张")

    if game.cert_num:
        items.append(f"剩余不在场证明牌 {game.cert_num}张")

    items.append(f"目前轮到 [{game.current_player.name}]")

    await cat.send("\n".join(items))


@cat.on_cmd(cmds="手牌", states="game")
async def show_cards():
    '''私聊展示手牌'''
    # 只接受私聊发送的消息
    if not cat.event.origin_channel:
        return

    game = cat.get_data(Game)
    player = game.get_player(cat.event.origin_channel.id)
    items = ["您的手牌\n", *player.cards]
    await player.send("\n".join(items))

'''游戏局势'''
from .cat import cat, get_uid
from .model import Game
from .config import R


@cat.on_cmd(cmds="局势", states="*")
async def show_game_info():
    '''查看场面局势'''
    game = cat.get_data(Game)
    if not game.start:
        return

    items = ["所有玩家剩余手牌数"]
    for p in game.players:
        items.append(f"{p.index_name} {len(p.cards)}张")

    # 统计牌数
    detect_num = 0
    cert_num = 0
    for p in game.players:
        for card in p.cards:
            if card == R.侦探:
                detect_num += 1
            elif card == R.不在场证明:
                cert_num += 1

    if detect_num:
        items.append(f"剩余{R.侦探}牌 {detect_num}张")

    if cert_num:
        items.append(f"剩余{R.不在场证明}牌 {cert_num}张")

    items.append(f"目前轮到 {game.current_player.index_name}")

    await cat.send("\n".join(items))


@cat.on_cmd(cmds="手牌", states="*")
async def show_cards():
    '''展示手牌'''
    game = cat.get_data(Game)
    if not game.start:
        return
    
    uid = get_uid()
    
    player = game.get_player(uid)
    if not player:
        return

    items = ["您的手牌\n", *player.cards]
    await player.send("\n".join(items))

'''游戏局势'''
from ..cat import cat
from ..model import Game


@cat.on_cmd(cmds="局势", states="game")
async def show_game_info():
    game = cat.get_data(Game)

    # ---- 临时调试 ----
    for p in game.players:
        items = [f"[{p.name}]", *p.cards]
        await cat.send("\n".join(items))
    return
    # ---- 临时调试 ----

    items = ["所有玩家剩余手牌数"]
    for p in game.players:
        items.append(f"[{p.name}] {len(p.cards)}张")
    if game.detect_num:
        items.append(f"剩余侦探牌 {game.detect_num}张")
    if game.cert_num:
        items.append(f"剩余不在场证明牌 {game.cert_num}张")
    items.append(f"目前轮到 [{game.current_player.name}]")
    await cat.send("\n".join(items))

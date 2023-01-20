'''神犬'''
from .overtime import set_overtime_task
from ...on import on_cmd, Game, Player, AtPlayer
from ...config import R


@on_cmd(cmds=R.神犬, states="game", at_require=True, auto_play_card=False)
async def dog(game: Game, player: Player, p2: AtPlayer, card: str):
    if p2.id == player.id:
        return await game.send(f"{R.神犬}不咬主人")

    if not p2.cards:
        return await game.send(f"{R.神犬}只能扑向有手牌的玩家")

    game.dog.target_id = p2.id
    game.dog.owner_id = player.id

    await player.play_card(card)
    await game.send(f"目标是 {p2.index_name}！请TA丢弃一张牌")

    game.set_state("dog")

    # 设置超时任务
    set_overtime_task(p2)


@on_cmd(cmds=[R.共犯, R.普通人, R.不在场证明, R.目击者, R.侦探, R.交易, R.谣言, R.情报交换, R.警部, R.犯人], states="dog", auto_play_card=False, auto_check_card=False)
async def dog_bite(game: Game, player: Player, card: str):
    if game.dog.target_id != player.id:
        return

    if card not in player.cards:
        return await game.send(f"{player.index_name} 没有{card}")

    await player.play_card(card)

    if card == R.犯人:
        player.is_good = False
        owner = game.get_player(game.dog.owner_id)
        owner.is_good = True
        return await game.end(True)

    player.cards.append(R.神犬)
    await game.send(f"{player.index_name} 获得{R.神犬}牌")

    game.set_state("game")
    await game.turn_next()

'''神犬'''
from .overtime import set_overtime_task
from ...cat import cat
from ...model import Game
from ...config import R


@cat.on_cmd(cmds=R.神犬, states="game", auto_help=False)
async def dog():
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

        if cat.event.at == player.id:
            return await game.send(f"{R.神犬}不咬主人")

        p2 = game.get_player(cat.event.at)
        if not p2.cards:
            return await game.send(f"{R.神犬}只能扑向有手牌的玩家")

        game.dog.target_id = p2.id
        game.dog.owner_id = cat.user.id

        await player.play_card(card)
        await game.send(f"目标是 {p2.index_name}！请TA丢弃一张牌")

        game.set_state("dog")

        # 设置超时任务
        set_overtime_task(p2)


@cat.on_cmd(cmds=[R.共犯, R.普通人, R.不在场证明, R.目击者, R.侦探, R.交易, R.谣言, R.情报交换, R.警部, R.犯人], states="dog", auto_help=False)
async def dog_bite():
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

'''交易'''
import asyncio
from random import choice
from ..cat import cat
from ..model import on_cmd, overtime_wrapper, Game, Player, AtPlayer
from ..config import R


@on_cmd(cmds=R.交易, states="game", at_require=True, auto_play_card=False, auto_turn_next=False)
async def exchange(game: Game, player: Player, p2: AtPlayer, card: str):
    if p2.id == player.id:
        return await game.send(f"不能和自己{R.交易}")

    if not p2.cards:
        return await game.send(f"{p2.index_name} 没有可{R.交易}的手牌")

    await player.play_card(card)
    await game.send(f"目标是 {p2.index_name}！")

    if not player.cards:
        await game.send(f"{player.index_name} 没有可{R.交易}的手牌，此牌仍打出，但无效果")
        return await game.turn_next()

    # 记录两人
    game.round_give.init([player, p2])
    await game.send(f"{R.交易}进行中...\n请参与者通过私聊告知bot要给出的手牌")

    # 私聊通知
    for g in game.round_give.gives:
        await g.giver.send("请在这里发送您要给出的牌")
        # 设置超时任务
        overtime(g.giver)

    game.set_state("exchange")


@cat.on_cmd(
    cmds=[
        R.共犯, R.普通人, R.不在场证明, R.目击者, R.侦探, R.交易,
        R.谣言, R.情报交换, R.警部, R.犯人, R.神犬
    ],
    states="exchange",
    auto_help=False
)
async def set_exchange():
    '''
    - 只接受私聊发送的消息
    - 排除give.giver玩家
    - 排除打牌失败
    - 交换牌
    '''
    # 只接受私聊发送的消息
    if not cat.event.private_forward_id:
        return await cat.send("请在私聊里做决定")

    game = cat.get_data(Game)

    # 排除不参与情报交换的
    give = game.round_give.get_give(cat.user.id)
    if not give:
        return

    async with game.lock:
        card = cat.cmd
        if card not in give.giver.cards:
            items = ["你没有这张牌，你当前的手牌是\n", *give.giver.cards]
            return await give.giver.send("\n".join(items))

        give.card = card
        give.giver.fut.set_result(True)
        await game.send(f"{give.giver.index_name} 已决定好卡牌")

        # 判断是否完成
        if game.round_give.all_given:
            # 私聊 互相给牌
            game.round_give.set_receivers()
            await game.round_give.convey_all()
            await asyncio.sleep(2)

            game.set_state("game")
            await game.turn_next()


@overtime_wrapper
async def overtime(player: Player):
    game = player.game
    give = game.round_give.get_give(player.id)
    card = choice(player.cards)
    give.card = card
    await player.send(f"您被系统强制交出了{card}")
    await game.send(f"{give.giver.index_name} 已决定好卡牌")

    # 判断是否完成
    if game.round_give.all_given:
        # 私聊 互相给牌
        game.round_give.set_receivers()
        await game.round_give.convey_all()
        await asyncio.sleep(2)

        game.set_state("game")
        await game.turn_next()

'''交易'''
from asyncio import sleep
from .overtime import set_overtime_task
from ...cat import cat
from ...model import Game
from ...config import R


@cat.on_cmd(cmds=R.情报交换, states="game", auto_help=False)
async def round_give():
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
        if not await player.check(card):
            return

        await player.play_card(card)

        # 所有有牌的人
        ps = [p for p in game.players if p.cards]
        game.round_give.init(ps)
        await game.send(f"{R.情报交换}进行中...\n请参与者通过私聊告知bot要给出的手牌")

        # 私聊通知
        for g in game.round_give.gives:
            await g.giver.send("请在这里发送您要给出的牌")
            # 设置超时任务
            set_overtime_task(g.giver)

        game.set_state("round_give")


@cat.on_cmd(cmds=[R.共犯, R.普通人, R.不在场证明, R.目击者, R.侦探, R.交易, R.谣言, R.情报交换, R.警部, R.犯人, R.神犬], states="round_give", auto_help=False)
async def set_round_give():
    # 只接受私聊发送的消息
    if not cat.event.origin_channel:
        return

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
        await game.send(f"{give.giver.index_name} 已决定好卡牌")

        # 判断是否完成
        if game.round_give.all_given:
            # 私聊 互相给牌
            game.round_give.set_receivers()
            await game.round_give.convey_all()
            await sleep(2)

            game.set_state("game")
            await game.turn_next()

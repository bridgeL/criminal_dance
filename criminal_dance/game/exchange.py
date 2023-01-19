'''交易'''
from asyncio import sleep
from ..cat import cat
from ..model import Game, Player
from .utils import check_player, play_card, check_at_one_player, check_first, turn_next
from .utils import check_card as _check_card
from ..room.utils import send_private


async def check_card(card: str, player: Player):
    '''检查 player 是否有此牌'''
    if card not in player.cards:
        await cat.send(f"[{player.name}] 没有 [{card}]")
        return False
    return True


@cat.on_cmd(cmds="交易", states="game")
async def exchange():
    game = cat.get_data(Game)
    async with game.lock:

        if not await check_player():
            return

        if not await check_first():
            return

        card = cat.cmd
        if not await _check_card(card):
            return

        player = game.get_player(cat.user.id)

        if len(player.cards) == 1:
            await play_card(card)
            await cat.send(f"[{cat.user.name}] 没有可交易的手牌，此牌无效果")
            await turn_next()
            return

        if not await check_at_one_player():
            return

        p2 = game.get_player(cat.event.at)
        game.round_give.init([player, p2])
        await play_card(card)

        # 私聊通知
        for g in game.round_give.gives:
            await send_private(g.giver.id, "请在这里发送你要交换的牌")
            # 这里还要写一个私聊超时发送的东西
            # ---- 先鸽了 ----

        cat.state = "exchange"


@cat.on_cmd(cmds=["共犯", "普通人", "不在场证明", "目击者", "侦探", "交易", "谣言", "情报交换", "警部", "犯人", "神犬"], states="exchange")
async def set_exchange_card():
    game = cat.get_data(Game)
    async with game.lock:
        uid = cat.user.id

        give = game.round_give.get_give(uid)
        if not give:
            return
        if give.card:
            return

        card = cat.cmd
        if not await check_card(card, give.giver):
            return

        give.card = card

        # 判断是否完成
        if game.round_give.finish:
            # 私聊 互相给牌
            game.round_give.set_recver()
            for g in game.round_give.gives:
                g.convey()
                await send_private(g.recver.id, f"你得到了 [{g.giver.name}] 的 [{g.card}]")

            await sleep(2)
            cat.state = "game"
            await turn_next()

        await cat.base_send(cat.event.channel, f"[{cat.user.name}] 已决定好卡牌")

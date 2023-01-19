'''神犬'''
from ..cat import cat
from ..model import Game
from .utils import check_player, check_card, play_card, at_one_player, check_first, start_timer, turn_next, game_end


@cat.on_cmd(cmds="神犬", states="game")
async def dog():
    if not await check_player():
        return

    if not await check_first():
        return

    card = cat.cmd
    if not await check_card(card):
        return

    if not await at_one_player():
        return

    game = cat.get_data(Game)
    p2 = game.get_player(cat.event.at)
    game.dog_bite = p2.id

    if not p2.cards:
        return await cat.send("神犬牌只能扑向有手牌的玩家")

    await play_card(card)

    await cat.send(f"请 [{p2.name}] 丢弃一张牌")
    start_timer(p2)
    cat.state = "dog"


@cat.on_cmd(cmds=["共犯", "普通人", "不在场证明", "目击者", "侦探", "交易", "谣言", "情报交换", "警部", "犯人"], states="dog")
async def dog_bite_1():
    game = cat.get_data(Game)
    if not game.dog_bite == cat.user.id:
        return

    card = cat.cmd
    if not await check_card(card):
        return

    await play_card(card)

    if card == "犯人":
        player = game.get_player(cat.user.id)
        player.good_person = False
        return await game_end(True)

    await turn_next()

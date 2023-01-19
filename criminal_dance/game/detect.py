'''侦探'''
from ..cat import cat
from ..model import Game
from .utils import turn_next, check_player, check_card, play_card, at_one_player, check_first, game_end


@cat.on_cmd(cmds="侦探", states="game")
async def detect():
    if not await check_player():
        return

    if not await check_first():
        return

    card = cat.cmd
    if not await check_card(card):
        return

    game = cat.get_data(Game)
    if len(game.current_player.cards) > 2:
        return await cat.send("侦探牌只能在手牌<=2时打出")

    if not await at_one_player():
        return

    await play_card(card)

    game.detect_num -= 1
    p2 = game.get_player(cat.event.at)
    if "犯人" in p2.cards and "不在场证明" not in p2.cards:
        game.current_player.good_person = True
        await game_end(True)
        return

    await cat.send(f"[{p2.name}] 不是犯人~")
    await turn_next()

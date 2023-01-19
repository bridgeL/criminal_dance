'''警部'''
from ..cat import cat
from ..model import Game
from .utils import check_player, check_card, play_card, check_first, check_at_one_player, turn_next


@cat.on_cmd(cmds="警部", states="game")
async def police():
    game = cat.get_data(Game)
    async with game.lock:

        if not await check_player():
            return

        if not await check_first():
            return

        card = cat.cmd
        if not await check_card(card):
            return

        if len(game.current_player.cards) > 2:
            return await cat.send("警部牌只能在手牌数<=2时打出")

        if not await check_at_one_player():
            return

        game.police.target_id = cat.event.at
        game.police.owner_id = cat.user.id

        await play_card(card)
        await turn_next()

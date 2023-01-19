'''犯人'''
from ..cat import cat
from ..model import Game
from .utils import check_player, check_card, play_card, check_first, game_end


@cat.on_cmd(cmds="犯人", states="game")
async def accomplice():
    game = cat.get_data(Game)
    async with game.lock:
    
        if not await check_player():
            return

        if not await check_first():
            return

        card = cat.cmd
        if not await check_card(card):
            return

        if len(game.current_player.cards) > 1:
            return await cat.send("犯人牌只能作为最后一张手牌打出~顺便一提，你暴露辣")

        game.current_player.good_person = False
        
        await play_card(card)

        # ---- 部分完成 ----
        # 这里还需要考虑警部的问题
        await game_end(False)
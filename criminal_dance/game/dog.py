'''神犬'''
from ..cat import cat
from ..model import Game
from .utils import check_player, check_card, play_card, check_at_one_player, check_first, start_timer, turn_next, game_end


@cat.on_cmd(cmds="神犬", states="game")
async def dog():
    game = cat.get_data(Game)
    async with game.lock:

        if not await check_player():
            return

        if not await check_first():
            return

        card = cat.cmd
        if not await check_card(card):
            return

        if not await check_at_one_player():
            return

        p2 = game.get_player(cat.event.at)
        game.dog.target_id = p2.id
        game.dog.owner_id = cat.user.id

        if not p2.cards:
            return await cat.send("神犬牌只能扑向有手牌的玩家")

        await play_card(card)

        await cat.send(f"请 [{p2.name}] 丢弃一张牌")
        start_timer(p2)
        cat.state = "dog"


@cat.on_cmd(cmds=["共犯", "普通人", "不在场证明", "目击者", "侦探", "交易", "谣言", "情报交换", "警部", "犯人"], states="dog")
async def dog_bite():
    game = cat.get_data(Game)
    async with game.lock:

        if game.dog.target_id != cat.user.id:
            return

        card = cat.cmd
        player = game.get_player(cat.user.id)
        if not await check_card(card, player):
            return

        await play_card(card, player)

        if card == "犯人":
            player.good_person = False
            owner = game.get_player(game.dog.owner_id)
            owner.good_person = True
            return await game_end(True)

        player.cards.append("神犬")
        await turn_next()

'''犯人'''
from ..on import on_cmd, Game, Player
from ..config import R


@on_cmd(cmds=R.犯人, states="game", max_num=1)
async def criminal(game: Game, player: Player):
    player.is_good = False
    await game.send(f"{R.犯人}是 {player.index_name}！")

    # 被警部抓到了
    if game.police.target_id == player.id:
        p2 = game.get_player(game.police.owner_id)
        p2.is_good = True
        await game.send(f"但是{R.犯人}被 {p2.index_name} 布置的{R.警部}抓到了！")
        return await game.end(True)

    await game.end(False)

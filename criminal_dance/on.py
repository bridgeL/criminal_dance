'''特别定制的注册回调方法'''
from asyncio import sleep
import inspect
from typing import Awaitable, Callable
from .cat import cat
from .model import Game, Player


class AtPlayer(Player):
    '''被at的玩家'''
    pass


def on_cmd(
    cmds: str | list[str] = "",
    states: str | list[str] = "",
    max_num: int = 4,
    at_require: bool = False,
    auto_check_card: bool = True,
    auto_play_card: bool = True,
):
    '''
    - 排除私聊发送的消息
    - 排除非游戏玩家
    - 检查第一发现人、行动权、是否有手牌、是否满足数量要求、是否at玩家
    - 打出牌
    '''
    def decorator(func: Callable[..., Awaitable]):

        # 分析func参数表
        # 参数名:类型
        params = inspect.signature(func).parameters
        params = {k: v.annotation for k, v in params.items()}

        async def _func():
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
                if auto_check_card:
                    if not await player.check(card, max_num, at_require):
                        return

                    if auto_play_card:
                        await player.play_card(card)

                # 依赖注入
                _params = {}

                for key, cls in params.items():
                    if cls is Game:
                        _params[key] = game
                    elif cls is Player:
                        _params[key] = player
                    elif cls is AtPlayer:
                        p2 = game.get_player(cat.event.at)
                        _params[key] = p2
                    elif cls is str:
                        _params[key] = card

                await func(**_params)

        cat.on_cmd(cmds=cmds, states=states, auto_help=False)(_func)
        return func

    return decorator


def set_rg_cmd(
    cmds: str | list[str] = "",
    states: str | list[str] = "",
):
    '''
    - 只接受私聊发送的消息
    - 排除give.giver玩家
    - 排除打牌失败
    - 交换牌
    '''
    async def _func():
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
            give.giver.fut.set_result(True)
            await game.send(f"{give.giver.index_name} 已决定好卡牌")

            # 判断是否完成
            if game.round_give.all_given:
                # 私聊 互相给牌
                game.round_give.set_receivers()
                await game.round_give.convey_all()
                await sleep(2)

                game.set_state("game")
                await game.turn_next()

    cat.on_cmd(cmds=cmds, states=states, auto_help=False)(_func)

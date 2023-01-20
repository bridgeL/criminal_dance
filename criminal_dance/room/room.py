'''房间'''
import asyncio
from ayaka import AyakaChannel
from .cards import get_cards
from .shuffle import shuffle
from ..cat import cat
from ..model import Room, Game, Player
from ..config import R, config


@cat.on_cmd(cmds=f"{R.犯人}在跳舞")
async def wakeup():
    '''唤醒猫猫'''
    await cat.start("room")
    await cat.send_help()
    room = cat.get_data(Room)
    room.users = []
    await join_room()


@cat.on_cmd(cmds="加入", states="room")
async def join_room():
    name = cat.user.name
    room = cat.get_data(Room)
    channel = AyakaChannel(
        type="private",
        id=cat.user.id
    )

    try:
        await cat.base_send(channel, "测试私聊，无需回复")
    except:
        await cat.send(f"{name} 不是bot好友，无法加入游戏")
    else:
        cat.add_listener(channel)

        room.join(cat.user.id, name)
        room.cards = []

        await cat.send(f"{name} 加入房间")
        await cat.send(room.info)


@cat.on_cmd(cmds="离开", states="room")
async def leave_room():
    name = cat.user.name
    room = cat.get_data(Room)
    channel = AyakaChannel(
        type="private",
        id=cat.user.id
    )

    room.leave(cat.user.id)
    room.cards = []

    cat.remove_listener(channel)

    await cat.send(f"{name} 离开房间")
    await cat.send(room.info)

    if not room.users:
        await cat.send("房间为空，游戏结束")
        await cat.rest()


@cat.on_cmd(cmds="房间", states="room")
async def show_room():
    # 排除私聊发送的消息
    if cat.event.origin_channel:
        return

    room = cat.get_data(Room)
    await cat.send(room.info)


@cat.on_cmd(cmds="开始游戏", states="room")
async def start_game():
    # 排除私聊发送的消息
    if cat.event.origin_channel:
        return

    room = cat.get_data(Room)

    # 人数控制
    n = len(room.users)
    if n < 3 or n > 8:
        return await cat.send(f"{R.犯人}在跳舞只能3-8人游玩，现在房间里有{n}人")

    # 生成牌库
    if not room.cards:
        room.cards = get_cards(n)

    # 洗牌
    shuffle(room.cards)

    # 状态转移
    cat.state = "game"

    # 初始化游戏
    game = cat.get_data(Game)
    game.init(room, cat.channel.id)

    # 通知
    await game.send("游戏开始")

    # 发牌
    for player in game.players:
        items = ["您的手牌是\n", *player.cards]
        await player.send("\n".join(items))

    # 第一发现人
    await game.send(f"{R.第一发现人}是 [{game.current_player.name}]")

    # 设置超时任务
    set_overtime_task(game.current_player)


def set_overtime_task(player: Player):
    '''设置超时任务'''
    loop = asyncio.get_event_loop()
    player.fut = loop.create_future()
    loop.create_task(overtime(player))


async def overtime(player: Player):
    try:
        print("开启计时器")
        await asyncio.wait_for(player.fut, config.overtime)
    except asyncio.exceptions.TimeoutError:
        print("超时了")
        card = R.第一发现人
        player.cards.remove(card)
        player.game.first = True
        await player.game.send(f"{player.index_name} 被系统强制丢弃了{card}")
        await player.game.turn_next()
    else:
        print("关闭计时器")

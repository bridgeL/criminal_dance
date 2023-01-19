'''房间'''
from ayaka import AyakaChannel
from ..cat import cat
from ..model import Room, Game
from ..game.utils import start_timer
from .utils import shuffle, send_private, get_cards


@cat.on_cmd(cmds="犯人在跳舞")
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
    try:
        await send_private(cat.user.id, "测试私聊，无需回复")
    except:
        await cat.send(f"[{name}] 不是bot好友，无法加入游戏")
    else:
        cat.add_listener(AyakaChannel(
            type="private",
            id=cat.user.id
        ))
        room.join(cat.user.id, name)
        room.cards = []
        await cat.send(f"[{name}] 加入房间")
        await cat.send(room.info)


@cat.on_cmd(cmds="离开", states="room")
async def leave_room():
    room = cat.get_data(Room)
    room.leave(cat.user.id)
    room.cards = []
    await cat.send(f"[{cat.user.name}] 离开房间")
    cat.remove_listener(AyakaChannel(
        type="private",
        id=cat.user.id
    ))

    if not room.users:
        await cat.send("房间为空，游戏结束")
        return await cat.rest()

    await cat.send(room.info)


@cat.on_cmd(cmds="房间", states="room")
async def show_room():
    room = cat.get_data(Room)
    await cat.send(room.info)


@cat.on_cmd(cmds="开始游戏", states="room")
async def start_game():
    room = cat.get_data(Room)
    n = len(room.users)
    if n < 3 or n > 8:
        return await cat.send(f"犯人在跳舞只能3-8人游玩，现在房间里有{n}人")
    # 生成牌库
    if not room.cards:
        room.cards = get_cards(n)
    # 洗牌
    shuffle(room.cards)
    await cat.send("游戏开始")

    cat.state = "game"
    game = cat.get_data(Game)
    game.init(room)

    # 发牌
    for p in game.players:
        items = ["您的手牌是", *p.cards]
        await send_private(p.id, "\n".join(items))

    await cat.send(f"第一发现人是 [{game.current_player.name}]")
    start_timer()

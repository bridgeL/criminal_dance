import asyncio
from typing import Awaitable, Callable, Optional
from pydantic import BaseModel
from ayaka import AyakaChannel
from .cat import cat
from .config import R
from .overtime import set_overtime_task


class User(BaseModel):
    '''房间成员'''
    id: str
    name: str


class Room(BaseModel):
    '''房间'''
    users: list[User] = []
    cards: list[str] = []

    @property
    def info(self):
        items = ["当前房间人员\n"]
        items.extend(u.name for u in self.users)
        return "\n".join(items)

    def join(self, id: str, name: str):
        for u in self.users:
            if u.id == id:
                return
        else:
            user = User(id=id, name=name)
            self.users.append(user)
            return True

    def leave(self, id: str):
        for u in self.users:
            if u.id == id:
                self.users.remove(u)
                return True


class Player(BaseModel):
    '''玩家'''
    index: int

    id: str
    name: str

    cards: list[str] = []
    '''当前手牌'''

    is_good: bool = True
    '''天生都是好人，打出共犯或犯人后变坏'''

    game: "Game"

    fut: Optional[asyncio.Future]
    '''超时控制'''

    choose_card: Optional[Callable[[str], Awaitable]]
    '''需要执行的任务（放一张卡牌）'''

    class Config:
        arbitrary_types_allowed = True

    @property
    def index_name(self):
        '''座号+名字'''
        return f"[座号{self.index+1}] {self.name}"

    async def send(self, msg: str):
        '''发送私聊消息'''
        await cat.base_send(AyakaChannel(type="private", id=self.id), msg)

    async def send_many(self, msgs: list[str]):
        '''发送私聊消息'''
        await cat.base_send_many(AyakaChannel(type="private", id=self.id), msgs)

    async def check(self, card: str, max_num: int = 4, at_require: bool = False):
        '''大部分情况下使用此方法来检查，神犬、交易、情报交换则需要特殊规则'''
        if card != R.第一发现人 and not self.game.first:
            await self.game.send("第一张牌必须是第一发现人")
            return False
        if self.game.current_player.id != self.id:
            await self.game.send("没轮到你")
            return False
        if card not in self.cards:
            await self.game.send(f"{self.index_name} 没有{card}")
            return False
        if len(self.cards) > max_num:
            await self.game.send(f"{card}只能在手牌<={max_num}时打出")
            return False
        if at_require and not self.game.get_player(cat.event.at):
            await self.game.send("你需要at一个游戏中的玩家")
            return False
        return True

    async def play_card(self, card: str):
        '''打出一张牌并通知'''
        self.cards.remove(card)
        await self.game.send(f"{self.index_name} 打出{card}")

        # 结束超时任务
        if self.fut and not self.fut.done():
            self.fut.set_result(True)


class MarkItem(BaseModel):
    '''标志物'''
    target_id: str = ""
    '''目标id'''
    owner_id: str = ""
    '''主人id'''


class Game(BaseModel):
    '''游戏'''

    players: list[Player] = []
    '''玩家列表'''
    index: int = 0
    '''玩家指针'''
    first: bool = False
    '''第一发现人是否已打出'''

    detect_num: int = 0
    '''剩余侦探数量'''
    cert_num: int = 0
    '''剩余不在场证明数量'''

    dog: MarkItem = MarkItem()
    '''神犬标志物'''
    police: MarkItem = MarkItem()
    '''警部标志物'''

    lock: asyncio.Lock = asyncio.Lock()
    '''同步锁，保证用户操作的原子性，防止一个用户因某种情况连出两牌的情况'''
    group_id: str = ""
    '''群聊号'''

    class Config:
        arbitrary_types_allowed = True

    def init(self, room: Room, group_id: str):
        '''将房间成员转换为游戏玩家'''
        # 保存群号
        self.group_id = group_id

        # 将room成员转换为玩家
        self.players = [
            Player(
                id=u.id, name=u.name,
                index=i, game=self,
                cards=room.cards[i*4:(i+1)*4],
            )
            for i, u in enumerate(room.users)
        ]

        # 统计牌数
        self.detect_num = 0
        self.cert_num = 0
        for card in room.cards:
            if card == R.侦探:
                self.detect_num += 1
            elif card == R.不在场证明:
                self.cert_num += 1

        # 设置玩家指针
        for i, p in enumerate(self.players):
            if R.第一发现人 in p.cards:
                self.index = i
                break

        # 第一发现人未打出
        self.first = False

    async def send(self, msg: str):
        '''发送群聊消息'''
        await cat.base_send(AyakaChannel(type="group", id=self.group_id), msg)

    async def send_many(self, msgs: list[str]):
        '''发送群聊消息'''
        await cat.base_send_many(AyakaChannel(type="group", id=self.group_id), msgs)

    @property
    def current_player(self):
        return self.players[self.index]

    def set_cat_state(self, state: str):
        '''在群聊、私聊均可用'''
        channel = AyakaChannel(type="group", id=self.group_id)
        cat._state_dict[channel.mark] = state

    async def turn_next(self):
        '''转移至下一个有牌的玩家'''
        n = len(self.players)
        for i in range(n):
            self.index = (self.index+1) % n
            if self.current_player.cards:
                break

        await cat.send(f"现在轮到 {self.current_player.index_name} 出牌")
        set_overtime_task(self.current_player)

    def get_player(self, uid: str):
        for p in self.players:
            if p.id == uid:
                return p

    async def end(self, good_win: bool):
        '''游戏终结，给出输赢'''
        goods = []
        bads = []
        for p in self.players:
            if p.is_good:
                goods.append(p.name)
            else:
                bads.append(p.name)

        if good_win:
            winners, losers = goods, bads
        else:
            winners, losers = bads, goods

        items = [
            "，".join(winners) + "赢了",
            "，".join(losers) + "输了",
        ]
        await self.send("\n".join(items))

        # ---- 待修改 这里有问题，因为game.end可能会在私聊中调用
        await self.send("已返回房间")
        cat.state = "room"


Player.update_forward_refs()

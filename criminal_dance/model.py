import asyncio
from typing import Optional
from pydantic import BaseModel


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
        items = ["当前房间人员"]
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
    id: str
    name: str
    cards: list[str] = []
    '''当前手牌'''
    good_person: bool = True
    '''天生都是好人，打出共犯或犯人后变坏'''


class Dog(BaseModel):
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
    fut: Optional[asyncio.Future]
    '''超时控制'''
    dog: Dog = Dog()
    '''神犬'''
    lock: asyncio.Lock = asyncio.Lock()
    '''同步锁，保证用户操作的原子性，防止一个用户因某种情况连出两牌的情况'''

    class Config:
        arbitrary_types_allowed = True

    def init(self, room: Room):
        '''将房间成员转换为游戏玩家'''
        self.players = [
            Player(id=u.id, name=u.name, cards=room.cards[i*4:(i+1)*4])
            for i, u in enumerate(room.users)
        ]

        self.detect_num = 0
        self.cert_num = 0
        for card in room.cards:
            if card == "侦探":
                self.detect_num += 1
            elif card == "不在场证明":
                self.cert_num += 1

        for i, p in enumerate(self.players):
            if "第一发现人" in p.cards:
                self.index = i
                break

        self.first = False

    @property
    def current_player(self):
        return self.players[self.index]

    def turn_next(self):
        '''转移至下一个有牌的玩家'''
        n = len(self.players)
        for i in range(n):
            self.index = (self.index+1) % n
            if self.current_player.cards:
                break

    def get_player(self, uid: str):
        for p in self.players:
            if p.id == uid:
                return p

    def end(self):
        '''游戏终结，给出输赢'''
        goods = []
        bads = []
        for p in self.players:
            if p.good_person:
                goods.append(p.name)
            else:
                bads.append(p.name)
        return goods, bads
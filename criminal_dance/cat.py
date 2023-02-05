'''猫猫'''
from ayaka import AyakaCat, get_adapter
from .config import R, config

cat = AyakaCat(f"{R.犯人}在跳舞")
cat.help = f'''
3-8人游玩，游玩前请先加bot的qq好友，否则无法发牌。{config.overtime}s内不出牌会被系统强制弃牌（防止挂机）
'''

help_dict = {
    R.第一发现人: "一切都是由您开始。打出时没有特别效果",
    R.共犯: f"打出这张牌成为{R.共犯}。当{R.犯人}获胜时，您也获得胜利。当{R.犯人}输掉游戏时，您也跟着输掉游戏",
    R.犯人: f"您是{R.犯人}，不能让其他玩家知道。您只能在只剩下这张手牌时才能打出这张牌，如果您要这么做，您获胜",
    R.不在场证明: f"只要有了这个，您就不是{R.犯人}了。打出时没有特别效果。如果您有{R.犯人}和{R.不在场证明}，{R.侦探}质疑时您可以否认",
    R.侦探: f"您的手牌<=2才能打出这张牌。打出时质疑另一位玩家，如果该玩家持有{R.犯人}，您获胜",
    R.普通人: "打出时没有特别效果",
    R.谣言: "所有玩家随机抽一张他下家玩家的手牌",
    R.情报交换: "所有玩家把一张牌传给他上家玩家",
    R.目击者: "看另一个玩家的手牌",
    R.交易: "和至少还有1张手牌的玩家交换一张手牌。如果这是您打出的最后一张牌，则没有特别效果",
    R.神犬: f"选择一个玩家。该玩家弃掉他其中的一张手牌，并且获得{R.神犬}。如果他弃掉一张{R.犯人}牌，您获胜",
    R.警部: f"手牌<=2时，选定一个玩家放置此牌，若其最终打出{R.犯人}牌，您获得游戏胜利"
}


all_cards_str = f'''
所有手牌种类：{R.共犯}， {R.普通人}，{R.不在场证明}， {R.目击者}， {R.侦探}， {R.交易}， {R.谣言}， {R.情报交换}， {R.警部}， {R.犯人}，{R.神犬}，{R.第一发现人}
'''.strip()


@cat.on_cmd(cmds="卡牌帮助", states="*")
async def _():
    '''<卡牌名> 获取相应的帮助'''
    help = None
    if cat.arg:
        help = help_dict.get(cat.arg)
    if not help:
        await cat.send(all_cards_str)
        return await cat.send_many([f"[{k}] {v}" for k, v in help_dict.items()])
    await cat.send(help)

total_helps = f'''
开局每人4张手牌，轮流出牌，整局游戏的第一张牌必须是{R.第一发现人}（类似扑克规则中的红桃3）

游戏分为好人阵营和坏人阵营，默认都是好人，而最终打出{R.犯人}牌的人作为坏人而胜利
但{R.犯人}牌只有在手牌数为1的时候才能打出，此时打出者作为{R.犯人}而胜利
其他人的目标就是在{R.犯人}逃跑成功之前，通过{R.侦探}、{R.神犬}、{R.警部}等牌抓到{R.犯人}，此时好人阵营胜利
当你打出{R.共犯}牌后，你便加入了坏人阵营，需要协助{R.犯人}获胜
当然，你也可以当个二五仔，若{R.共犯}使用{R.侦探}等牌抓到了{R.犯人}，那么他也视为好人阵营一同胜利

根据参与人数的不同，牌库的牌也不同，具体规则请发送 牌库规则 进一步了解

此外，当游戏进行中时，还有如下命令
局势：获得游戏进行情况等信息
手牌：获得你当前的手牌情况（bot私聊告知）
'''.strip().split("\n\n")


@cat.on_cmd(cmds="详细帮助", states="*")
async def _():
    await cat.send_many(total_helps)


cards_build_helps = f'''
3人局，必须有{R.第一发现人}、{R.犯人}、{R.侦探}、{R.不在场证明}，加其他任意8张牌
4人局，必须有{R.第一发现人}、{R.犯人}、{R.侦探}、{R.不在场证明}、{R.共犯}，加其他任意11张牌
5人局，必须有{R.第一发现人}、{R.犯人}、{R.侦探}、{R.不在场证明}*2、{R.共犯}，加其他任意14张牌
6人局，必须有{R.第一发现人}、{R.犯人}、{R.侦探}*2、{R.不在场证明}*2、{R.共犯}*2，加其他任意16张牌
7人局，必须有{R.第一发现人}、{R.犯人}、{R.侦探}*2、{R.不在场证明}*3、{R.共犯}*2，加其他任意19张牌
8人局，加全部
'''.strip().split("\n")


@cat.on_cmd(cmds="牌库规则", states="*")
async def _():
    await cat.send_many(cards_build_helps)

uid_redirect_dict: dict[str, str] = {}
'''重定向'''


def get_uid():
    '''获取当前发言者的uid'''
    uid = cat.user.id

    if cat.private:
        return uid

    adapter = get_adapter()
    if adapter.name != "nb2.ob11.qqguild_patch":
        return uid

    return uid_redirect_dict[uid]


@cat.on_cmd(cmds="绑定私聊", states="*")
async def _():
    '''<qq uid> 频道用户请使用该命令'''
    uid = cat.user.id
    uid_redirect_dict[uid] = cat.arg
    await cat.send(f"{cat.user.name} - {uid} - {cat.arg} 绑定成功")

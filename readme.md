<div align="center">

# 犯人在跳舞 0.0.1b3

祝各位新年快乐~

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/criminal_dance)
![PyPI - Downloads](https://img.shields.io/pypi/dm/criminal_dance)
![PyPI - License](https://img.shields.io/pypi/l/criminal_dance)
![PyPI](https://img.shields.io/pypi/v/criminal_dance)

基于ayaka的文字版桌游！

</div>

得益于[ayaka](https://github.com/bridgeL/ayaka)，本插件可作为如下机器人框架的插件使用

- [nonebot2](https://github.com/nonebot/nonebot2)(使用[onebot11](https://github.com/nonebot/adapter-onebot)适配器)
- [hoshino](https://github.com/Ice-Cirno/HoshinoBot)
- [nonebot1](https://github.com/nonebot/nonebot)

也可将其作为console程序离线运行

## 猫猫帮助

```
[犯人在跳舞]
3-8人游玩，游玩前请先加bot好友，否则无法发牌
开局4张手牌，轮流出牌，具体帮助请查看 详细帮助、卡牌帮助、牌库规则
若长时间不出牌则会被系统强制弃牌（防止挂机）
- 犯人在跳舞 唤醒猫猫
[*]
- 卡牌帮助 <卡牌名> 获取相应的帮助
- 详细帮助
- 牌库规则
[room]
- 加入
- 离开
- 房间
- 开始游戏
[game]
- 局势 查看场面局势
- 手牌 私聊展示手牌
```

```
[第一发现人] 一切都是由您开始。打出时没有特别效果
[共犯] 打出这张牌成为共犯。当犯人获胜时，您也获得胜利。当犯人输掉游戏时，您也跟着输掉游戏
[犯人] 您是犯人，不能让其他玩家知道。您只能在只剩下这张手牌时才能打出这张牌，如果您要这么做，您获胜
[不在场证明] 只要有了这个，您就不是犯人了。打出时没有特别效果。如果您有犯人和不在场证明，侦探质疑时您可以否认
[侦探] 您的手牌<=2才能打出这张牌。打出时质疑另一位玩家，如果该玩家持有犯人，您获胜
[普通人] 打出时没有特别效果
[谣言] 所有玩家随机抽一张他下家玩家的手牌
[情报交换] 所有玩家把一张牌传给他上家玩家
[目击者] 看另一个玩家的手牌
[交易] 和至少还有1张手牌的玩家交换一张手牌。如果这是您打出的最后一张牌，则没有特别效果
[神犬] 选择一个玩家。该玩家弃掉他其中的一张手牌，并且获得神犬。如果他弃掉一张犯人牌，您获胜
[警部] 手牌<=2时，选定一个玩家放置此牌，若其最终打出犯人牌，您获得游戏胜利
```

```
开局4张手牌，轮流出牌

拥有第一发现人的人优先出牌（类似扑克规则的红桃3），且第一张牌必须是第一发现人

犯人牌只有在手牌数为1的时候才能打出，此时打出者作为犯人而胜利

其他人的目标就是在犯人逃跑成功之前，通过侦探、神犬、警部等牌抓到犯人，此时好人阵营胜利

当你打出共犯牌后，你便加入了坏人阵营，需要协助犯人获胜

当然，你也可以当个二五仔，若共犯使用侦探等牌抓到了犯人，那么他也视为好人阵营一同胜利

根据参与人数的不同，牌库的牌也不同，具体规则请发送 牌库规则 进一步了解

此外，当游戏进行中时

可以在群聊发送 局势，获得游戏进行情况等信息
或在私聊bot发送 手牌，获得你当前的手牌情况
```

```
3人局，必须有第一发现人、犯人、侦探、不在场证明，加其他任意8张牌

4人局，必须有第一发现人、犯人、侦探、不在场证明、共犯，加其他任意11张牌

5人局，必须有第一发现人、犯人、侦探、不在场证明*2、共犯，加其他任意14张牌

6人局，必须有第一发现人、犯人、侦探*2、不在场证明*2、共犯*2，加其他任意16张牌

7人局，必须有第一发现人、犯人、侦探*2、不在场证明*3、共犯*2，加其他任意19张牌

8人局，加全部
```

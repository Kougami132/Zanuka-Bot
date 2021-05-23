from nonebot.plugin import on_command, require
from nonebot.adapters.cqhttp import Bot, Event
from datetime import datetime, timedelta
import requests
import json
import re
import copy

export = require("tools")
Translate = export.translate
DeltaStr = export.deltastr

voidtrader = on_command("奸商")

@voidtrader.handle()
async def _(bot: Bot, event: Event):
    # try:
        response = requests.get(url="https://api.warframestat.us/pc/voidTrader")
        data = json.loads(response.text)
        if not data["active"]:
            content = "距离 " + data["character"] + " 到达 " + Translate(data["location"], "dict") + " 中继站还有 "
            utcTime = datetime.strptime(data["activation"], "%Y-%m-%dT%H:%M:%S.%fZ")
            timeLeft = utcTime + timedelta(hours=8) - datetime.now()
            content += DeltaStr(timeLeft)
            await voidtrader.send(content)
        else:
            nodes = []
            node = {
                "type": "node",
                "data": {
                    "uin": f"{bot.self_id}",
                    "name": "ZANUKA"
                }
            }
            node["data"]["content"] = data["character"] + " 已到达 " + Translate(data["location"], "dict") + " 中继站"
            nodes.append(copy.deepcopy(node))
            content = "——————————————————————————————"
            for i in data["inventory"]:
                content += "\n—{0}   [{1} 杜卡德]   [{2} 现金]".format(Translate(i["item"], "dict"), i["ducats"], i["credits"])
            content += "\n——————————————————————————————"
            node["data"]["content"] = content
            nodes.append(copy.deepcopy(node))

            utcTime = datetime.strptime(data["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
            timeLeft = utcTime + timedelta(hours=8) - datetime.now()
            content = "剩余时间: " + DeltaStr(timeLeft)
            await bot.send_group_forward_msg(group_id=event.group_id, messages=nodes)
    # except Exception as e:
    #     print(e)
    #     await voidtrader.finish("获取失败,请重试!")

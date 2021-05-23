from nonebot import on_command
from nonebot.plugin import require
from nonebot.adapters.cqhttp import Bot, Event
from datetime import datetime, timedelta
import requests
import json
import re
import copy

export = require("tools")
Translate = export.translate

invasions = on_command("入侵")

@invasions.handle()
async def _(bot: Bot, event: Event):
    try:
        response = requests.get(url="https://api.warframestat.us/pc/invasions")
        data = json.loads(response.text)
        nodes = []
        node = {
            "type": "node",
            "data": {
                "uin": f"{bot.self_id}",
                "name": "ZANUKA"
            }
        }
        for i in data:
            if i["completed"]:
                continue
            content = "——————————"
            
            #节点、星球
            content += "\n—节点: {0}".format(Translate(i["node"], "dict"))

            #进攻方进度、派系、奖励
            if len(i["attackerReward"]["countedItems"]):
                i["attackerReward"]["countedItems"][0]["key"] = Translate(i["attackerReward"]["countedItems"][0]["key"], "invasion")
                content += "\n—进攻: {0}% {1}×{2}".format(
                    round(i["completion"], 1), i["attackerReward"]["countedItems"][0]["key"], i["attackerReward"]["countedItems"][0]["count"])
            else:
                content += "\n—进攻: {0}% 无".format(round(i["completion"], 1))

            #防守方进度、派系、奖励
            if len(i["defenderReward"]["countedItems"]):
                i["defenderReward"]["countedItems"][0]["key"] = Translate(i["defenderReward"]["countedItems"][0]["key"], "invasion")
                content += "\n—防守: {0}% {1}×{2}".format(
                    round(100 - round(i["completion"], 1), 1), i["defenderReward"]["countedItems"][0]["key"], i["defenderReward"]["countedItems"][0]["count"])
            else:
                content += "\n—防守: {0}% 无".format(round(100 - round(i["completion"], 1), 1))
            
            content += "\n——————————"
            node["data"]["content"] = content
            nodes.append(copy.deepcopy(node))
        await bot.send_group_forward_msg(group_id=event.group_id, messages=nodes)
    except Exception as e:
        print(e)
        await invasions.finish("获取失败,请重试!")

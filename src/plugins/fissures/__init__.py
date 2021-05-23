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
DeltaStr = export.deltastr

fissures = on_command("裂隙")

@fissures.handle()
async def _(bot: Bot, event: Event):
    try:
        response = requests.get(url="https://api.warframestat.us/pc/fissures")
        data = json.loads(response.text)
        nodes = []
        node = {
            "type": "node",
            "data": {
                "uin": f"{bot.self_id}",
                "name": "ZANUKA"
            }
        }
        for tier in range(5):
            content = "————{0}————".format(("古纪", "前纪", "中纪", "后纪", "安魂")[tier])
            for i in data:
                if not i["active"]:
                    continue
                if i["tierNum"] == tier + 1:
                    
                    #节点
                    content += "\n—节点: {0}".format(Translate(i["node"], "dict"))

                    #模式
                    i["missionType"] = Translate(i["missionType"], "dict")
                    content += "\n—模式: {0} ({1})".format(i["missionType"], i["enemy"])

                    #剩余时间
                    utcTime = datetime.strptime(i["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
                    timeLeft = utcTime + timedelta(hours=8) - datetime.now()
                    content += "\n—剩余时间: " + DeltaStr(timeLeft)
                    
                    content += "\n——————————"
            node["data"]["content"] = content
            nodes.append(copy.deepcopy(node))
        await bot.send_group_forward_msg(group_id=event.group_id, messages=nodes)
    except Exception as e:
        print(e)
        await fissures.finish("获取失败,请重试!")

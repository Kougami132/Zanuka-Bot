import copy
from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.plugin import require
from fuzzywuzzy import fuzz
import requests
from bs4 import BeautifulSoup

export = require("tools")
WF_Dict = export.dict
WF_Riven = export.riven

rm = on_command("rm", aliases={"RM"})

@rm.handle()
async def _(bot: Bot, event: Event):
    try:
        item = event.get_message().__str__().strip()
        if item == "":
            await rm.send("参数不能为空!")
            return

        #相似度匹配
        index = 0
        similar = 0
        for i in range(len(WF_Dict)):
            flag = True
            for j in WF_Riven:
                if WF_Dict[i]["en"] == j["name"]:
                    flag = False
                    break
            if flag:
                continue
            if " " in item:
                s = fuzz.partial_ratio(item, WF_Dict[i]["zh"])
            else:
                s = fuzz.ratio(item, WF_Dict[i]["zh"].replace(" ", ""))
            if s > similar:
                similar = s
                index = i
        if similar < 50:
            await rm.send("未找到该物品,请缩小范围!")
            return
        
        await rm.send("正在查询 [{0}] 紫卡价格,请稍等".format(WF_Dict[index]["zh"]))
        response = requests.get(
            url="https://riven.market/_modules/riven/showrivens.php?platform=PC&limit={1}&onlinefirst=true&polarity=all&rank=all&mastery=16&weapon={0}&stats=Any&neg=all&price=99999&rerolls=-1&sort=price&direction=ASC".format(
                WF_Dict[index]["en"].replace(" ", "_"), 10))
        html = response.text
        bs = BeautifulSoup(html, "html.parser")
        rivens = bs.find_all("div", class_="riven")

        nodes = []
        node = {
            "type": "node",
            "data": {
                "uin": f"{bot.self_id}",
                "name": "ZANUKA"
            }
        }
        node["data"]["content"] = "查价武器: {0} ({1})\n数据来源: https://riven.market/list/PC/{2}".format(
            WF_Dict[index]["zh"], WF_Dict[index]["en"], WF_Dict[index]["en"].replace(" ", "_"))
        nodes.append(copy.deepcopy(node))

        #简略
        content = "——————————————————————————————"
        for i in rivens:
            content += "\n—单价: {0} —次数: {1} —段位: {2} —等级: {3} —卖家: {4}".format(
                i["data-price"], i["data-rerolls"], i["data-mr"], i["data-rank"], i.find("div", class_="attribute seller").string.strip())
        content += "\n——————————————————————————————"
        node["data"]["content"] = content
        nodes.append(copy.deepcopy(node))
        
        #详细
        for i in rivens:
            content = "——————————————————————————————"
            content += "\n—单价: {0} —次数: {1} —段位: {2} —等级: {3} —极性: {4}".format(
                i["data-price"], i["data-rerolls"], i["data-mr"], i["data-rank"], i["data-polarity"])
            content += "\n—卖家: {0} —卡名: {1} {2}".format(
                i.find("div", class_="attribute seller").string.strip(), i["data-weapon"], i["data-name"])
            content += "\n—词条: {0} + {1} | {2} + {3}".format(
                i["data-stat1"], i["data-stat1val"], i["data-stat2"], i["data-stat2val"])
            content += " | {0} + {1}".format(i["data-stat3"], i["data-stat3val"]) if i["data-stat3"] != "" else ""
            content += " | {0} - {1}".format(i["data-stat4"],i["data-stat4val"]) if i["data-stat4"] != "" else ""
            content += "\n——————————————————————————————"
            content += "\n/w {0} Hey! I'd like to buy the {1} {2} Riven that you sell on Riven.market for {3} Platinum!".format(
                i.find("div", class_="attribute seller").string.strip(), i["data-weapon"], i["data-name"], i["data-price"])
            node["data"]["content"] = content
            nodes.append(copy.deepcopy(node))
        
        await bot.send_group_forward_msg(group_id=event.group_id, messages=nodes)
    except Exception as e:
        print(e)
        await rm.finish("获取失败,请重试!")

from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Message, GroupMessageEvent, MessageSegment
import time
import requests
import json

setu = on_command('setu', aliases={'涩图', '色图'})
cd = {}

@setu.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    global cd
    if str(event.group_id) not in cd:
        cd[str(event.group_id)] = int(time.time())
    ## 初始化cd

    if cd[str(event.group_id)] <= int(time.time()):
        keyword = event.get_message().__str__().strip()
        response = requests.get(
            "https://api.lolicon.app/setu/?apikey={0}&r18={1}&keyword={2}&num={3}&proxy=i.pixiv.cat&size1200=false".format(
                "698604975f3623bd7ed1d0", "2", keyword, 3))
        data = json.loads(response.text)
        if data["code"] == 0:
            cd[str(event.group_id)] = int(time.time()) + 60
            quota = data["quota"]
            if keyword == "":
                await setu.send("正在获取涩图,今日剩余可调用 {0} 次".format(quota))
            else:
                await setu.send("正在获取 [{0}] 涩图,今日剩余可调用 {1} 次".format(keyword, quota))
            for i in data["data"]:
                content = "\n标题: {0} (PID: {1})".format(i["title"], i["pid"])
                content += "\n作者: {0} (UID: {1})".format(i["author"], i["uid"])
                try:
                    await setu.send(MessageSegment.image(i["url"]) + content)
                except Exception as e:
                    print(e)
        elif data["code"] == 404:
            await setu.send("没有符合条件的涩图")
        else:
            await setu.send("获取失败")
    else:
        await setu.finish(Message(f"CD还剩 {cd[str(event.group_id)] - int(time.time())} 秒,请节制"))


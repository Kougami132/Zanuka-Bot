from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Message, GroupMessageEvent, MessageSegment
from base64 import b64encode
import os
import random
import time

if not os.path.isdir("./src/data/setu"):
    os.makedirs("./src/data/setu")

setu = on_command('setu', aliases={'涩图', '色图'})
cd = {}

@setu.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    global cd
    if str(event.group_id) not in cd:
        cd[str(event.group_id)] = int(time.time())
    ## 初始化cd

    if cd[str(event.group_id)] <= int(time.time()):
        nodes = []
        for root, dirs, files in os.walk("./src/data/setu/"):
            index = []
            for i in range(5):
                temp = random.randint(0, len(files) - 1)
                while temp in index:
                    temp = random.randint(0, len(files) - 1)
                index.append(temp)
            for i in index:
                node = {
                    "type": "node",
                    "data": {
                        "uin": f"{bot.self_id}",
                        "name": "ZANUKA"
                    }
                }
                with open("./src/data/setu/" + files[i], "rb") as file:
                    data = b64encode(file.read()).decode()
                    node["data"]["content"] = f"[CQ:image,file=base64://{data}]"
                nodes.append(node)
        try:
            await bot.send_group_forward_msg(group_id=event.group_id, messages=nodes)
            cd[str(event.group_id)] = int(time.time()) + 60
        except Exception as e:
            print(e)
            await setu.finish(Message("消息被风控,请重试"))
    else:
        await setu.finish(Message(f"CD还剩 {cd[str(event.group_id)] - int(time.time())} 秒,请节制"))


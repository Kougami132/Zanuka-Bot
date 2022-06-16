from datetime import timedelta
import hashlib
from io import BytesIO
import base64
import os
import configparser
from PIL import Image
import httpx
import json


# 转换 Image 对象图片为 Base64 编码字符串
def img_to_base64(pic: Image.Image) -> str:
  buf = BytesIO()
  pic.save(buf, format="PNG", quality=100)
  base64_str = base64.b64encode(buf.getbuffer()).decode()
  return "base64://" + base64_str

# md5加密
def md5(text: str) -> str:
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()

# 转换网络图片为 Image 对象
async def pic_to_image(url: str):
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url, timeout=20.0)
            userImage = Image.open(BytesIO(res.content))
        except Exception as e:
            print(f"文件下载出错: {e}")
            return None

    # 返回 URL 图片的 Image 对象
    return userImage

# 快速粘贴透明图片
def alpha_paste(image1: Image, image2: Image, position=(0, 0)):
    img = Image.new("RGBA", image1.size)
    img.paste(image2, position)
    image1.alpha_composite(img)
    return image1

# 获取必要资源目录
def get_assets_path():
    return "./src/assets/"

# 获取数据存储目录
def get_data_path():
    return "./src/data/"

# 读取数据
def get_config(name: str, section: str, item: str) -> str:
    path = get_data_path() + "config/"
    cp = configparser.RawConfigParser()
    
    # 检查文件夹是否存在
    if not os.path.isdir(path):
        return ""
    
    file = path + name + ".ini"
    # 检查文件是否存在
    if not os.path.isfile(file):
        return ""
    
    cp.read(file)
    # 检查section是否存在
    if not cp.has_section(section):
        return ""
    
    items = cp.items(section)
    # 遍历item
    for i in items:
        if i[0] == item:
            return i[1]
    # 默认为空
    return ""

# 存储数据
def set_config(name: str, section: str, item: str, content: str):
    path = get_data_path() + "config/"
    cp = configparser.RawConfigParser()

    # 检查文件夹是否存在
    if not os.path.isdir(path):
        os.makedirs(path)

    file = path + name + ".ini"
    # 检查文件是否存在
    if not os.path.isfile(file):
        cp.write(open(file, "w"))

    cp.read(file)
    # 检查section是否存在
    if not cp.has_section(section):
        cp.add_section(section)

    cp.set(section, item, content)
    cp.write(open(file, "w"))

# 消息记录json生成
def forward_msg(messages: list, uid: str, name: str):
    nodes = []
    for i in messages:
        if type(i) == list:
            nodes.append({
                "type": "node",
                "data": {
                    "uin": uid,
                    "name": name,
                    "content": forward_msg(i, uid, name)
                }
            })
        else:
            nodes.append({
                "type": "node",
                "data": {
                    "uin": uid,
                    "name": name,
                    "content": str(i)
                }
            })
    return nodes

# 秒数转倒计时
def count_down(timeLeft: timedelta) -> str:
    days = timeLeft.days
    secondsLeft = timeLeft.seconds
    hours = secondsLeft // 3600
    secondsLeft = secondsLeft - 3600 * hours
    minutes = secondsLeft // 60
    seconds = secondsLeft - 60 * minutes
    return f"{days} 天 {hours} 时 {minutes} 分 {seconds} 秒" if days else f"{hours} 时 {minutes} 分 {seconds} 秒" if hours else f"{minutes} 分 {seconds} 秒" if minutes else f"{seconds} 秒"

# 保存json文件
async def writeJson(data, path):
    if not os.path.isdir(path[:path.rfind("/") + 1]):
        os.makedirs(path[:path.rfind("/") + 1])
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

# 读取json文件
async def readJson(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


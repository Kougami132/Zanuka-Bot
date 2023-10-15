import re
from httpx import AsyncClient


# fiter获取的选项
filterOption = [{
        "title": "英文:",
        "pattern": re.compile(r'英文名：(.*?)）'),
        "index": 1,
        "errTitle": "英文:",
        "err": "未查询到\n",
        "addition": re.compile(r'<h1>(.*?)<\/h1>'),
        "indexAddition": 1,
    },{
        "title": "交易:",
        "pattern": re.compile(r'可交易'),
        "index": 0,
        "errTitle": "交易:",
        "err": "不可交易\n"
    },
]


# 查询存在的词条，用于模糊搜索
async def queryWikiOption(item: str):
    url = f"https://warframe.huijiwiki.com/api.php?action=opensearch&format=json&formatversion=2&search={item}&limit=10&suggest=true"
    async with AsyncClient() as client:
        res = await client.get(url=url, timeout=10)
        return res

# 发送获取wiki的请求
async def queryWarframeWiki(item: str):

    if(item.find("http")==-1):
        url = f"https://warframe.huijiwiki.com/wiki/{item}"
    else:
        url = item

    async with AsyncClient() as client:
        res = await client.get(url=url, timeout=10)
        return res


# 过滤其他内容
def strFiter(data):

    s = data.text
    res = ""
    # 循环获取
    for i in filterOption:
        searchObj = i["pattern"].search(s)
        try:
            res = res + i["title"] + searchObj.group(i["index"])

            if("addition" in i):
                additionObj = i["addition"].search(s)
                res = res + "("+ additionObj.group(i["indexAddition"]) +")" + "\n"
            else:
                res = res + "\n"

        except:
            res = res + i["errTitle"] + i["err"]

    return res + "来源地址："+str(data.url)

async def fetchWiki(item: str):


    resOption = await queryWikiOption(item)
    data = resOption.json()
    # print(data)
    if (len(data[1]) == 0):
        return "未查询到该内容，请更换搜索内容"

    res = "搜索:"+data[0]+"\n"
    res = res + "实际:"+data[1][0]+"\n"

    # 避免简介为空
    if(len(data[2])>0 and len(data[2][0])>0):
        res = res + "简介:"+data[2][0]+"\n"

    res = res + strFiter(await queryWarframeWiki(data[3][0]))

    if(len(data[1])>1):
        res = res +"\n"+ "相似选项:" + " , ".join(data[1])

    return res



# 用于测试
# async def doQuery():
#     res = await fetchWiki("墓沼隐龙")
#     print(res)
#
# import asyncio
#
# asyncio.run(doQuery())
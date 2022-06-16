from httpx import AsyncClient
from bs4 import BeautifulSoup


async def queryRivenMarket(riven: str, num=10):
    url = f"https://riven.market/_modules/riven/showrivens.php?platform=PC&limit={num}&onlinefirst=true&polarity=all&rank=all&mastery=16&weapon={riven}&stats=Any&neg=all&price=99999&rerolls=-1&sort=price&direction=ASC"
    async with AsyncClient() as client:
        res = await client.get(url=url, timeout=10)
        html = res.text
        bs = BeautifulSoup(html, "html.parser")
        rivens = bs.find_all("div", class_="riven")
        result = []
        for i in rivens:
            if i.find("div", class_="offline") != None:
                break
            obj = {
                "price": i["data-price"],
                "rerolls": i["data-rerolls"],
                "mr": i["data-mr"],
                "rank": i["data-rank"],
                "polarity": i["data-polarity"].title(),
                "weapon": i["data-weapon"],
                "name": i["data-name"],
                "stat1": i["data-stat1"],
                "stat1val": i["data-stat1val"],
                "stat2": i["data-stat2"],
                "stat2val": i["data-stat2val"],
                "stat3": i["data-stat3"],
                "stat3val": i["data-stat3val"],
                "stat4": i["data-stat4"],
                "stat4val": i["data-stat4val"],
                "seller": i.find("div", class_="attribute seller").string.strip(),
            }
            result.append(obj)
    return result
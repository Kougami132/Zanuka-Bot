from httpx import AsyncClient


async def queryWarframeMarket(item: str):
    url = f"https://api.warframe.market/v1/items/{item}/orders"
    async with AsyncClient() as client:
        res = await client.get(url=url, timeout=10)
        resJson = res.json()
    return resJson

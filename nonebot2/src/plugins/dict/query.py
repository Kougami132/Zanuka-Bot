from httpx import AsyncClient


async def queryItem():
    url = "https://api.warframe.market/v1/items"
    async with AsyncClient() as client:
        try:
            res = await client.get(url=url, timeout=10)
            resJson = res.json()
        except Exception as e:
            return False, type(e)
    return True, resJson

async def queryRivenItem():
    url = "https://api.warframe.market/v1/riven/items"
    async with AsyncClient() as client:
        try:
            res = await client.get(url=url, timeout=10)
            resJson = res.json()
        except Exception as e:
            return False, type(e)
    return True, resJson

async def queryDict():
    url = "https://warframe.huijiwiki.com/api.php?action=query&format=json&prop=revisions&titles=UserDict&formatversion=2&rvprop=content&rvlimit=1"
    async with AsyncClient() as client:
        try:
            res = await client.get(url=url, timeout=10)
            resJson = res.json()
        except Exception as e:
            return False, type(e)
    return True, resJson



    
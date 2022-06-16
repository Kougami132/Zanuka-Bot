from httpx import AsyncClient


# WFCD接口
async def queryWorldstate(node: str):
    platform = "pc" # "pc" "ps4" "xb1" "swi"
    language = "zh" # "de" "es" "fr" "it" "ko" "pl" "pt" "ru" "zh" "en"
    url = f"https://api.warframestat.us/{platform}/{node}"
    params = {
        "language": language
    }
    headers = {
        "Accept-Language": language
    }
    # 发送请求
    async with AsyncClient() as client:
        res = await client.get(url=url, params=params, headers=headers, timeout=10)
        resJson = res.json()
    return resJson

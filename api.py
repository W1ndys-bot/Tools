import aiohttp
import asyncio
import sys
import os

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from app.api import send_group_msg, send_private_msg


# 快递查询
async def fetch_delivery_info(nu):
    url = f"https://api.oioweb.cn/api/common/delivery?nu={nu}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            if data.get("code") == 200:
                return data
            else:
                return {"error": data.get("msg") + "\n仅支持无需验证的快递查询"}

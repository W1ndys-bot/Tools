import aiohttp
import asyncio
import subprocess
import logging
import chardet

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


# IP地址查询
async def fetch_ip_info(ip):
    url = f"https://api.oioweb.cn/api/ip/ipaddress?ip={ip}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            if data.get("code") == 200:
                return data
            else:
                return {"error": data.get("msg") + "\nIP地址查询失败"}


# 测试ping
async def ping_test(address_or_ip):
    import platform

    if platform.system().lower() == "windows":
        ping_cmd = f"ping -n 4 {address_or_ip}"
    else:
        ping_cmd = f"ping -c 4 {address_or_ip}"

    proc = await asyncio.create_subprocess_shell(
        ping_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()

    # 自动检测编码，使用 'utf-8' 作为默认编码
    stdout_encoding = chardet.detect(stdout).get("encoding") or "utf-8"
    stderr_encoding = chardet.detect(stderr).get("encoding") or "utf-8"

    stdout_decoded = stdout.decode(stdout_encoding, errors="ignore")
    stderr_decoded = stderr.decode(stderr_encoding, errors="ignore")

    if proc.returncode == 0:
        return {"result": stdout_decoded}
    else:
        if (
            "需要具有管理权限" in stderr_decoded
            or "Permission denied" in stderr_decoded
        ):
            return {"error": "执行ping命令需要管理员权限。"}
        return {"error": stderr_decoded}

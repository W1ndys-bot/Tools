import logging
import sys
import os
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api import send_group_msg
from app.scripts.Tools.api import fetch_delivery_info, fetch_ip_info
from app.switch import load_switch, save_switch


async def process_delivery_info(websocket, msg, delivery_number):
    try:
        delivery_info_json = await fetch_delivery_info(delivery_number)
        if delivery_info_json.get("error"):
            asyncio.create_task(
                send_group_msg(
                    websocket,
                    msg.get("group_id"),
                    f"快递查询失败: {delivery_info_json.get('error')}",
                )
            )
        elif delivery_info_json and delivery_info_json.get("result"):
            delivery_status = delivery_info_json.get("result", {}).get("status")
            delivery_info = delivery_info_json.get("result", {}).get("info")
            if delivery_info:
                delivery_last_time = delivery_info[0].get("time")
                delivery_last_context = delivery_info[0].get("context")
                asyncio.create_task(
                    send_group_msg(
                        websocket,
                        msg.get("group_id"),
                        f"快递状态: {delivery_status}\n最后更新时间: {delivery_last_time}\n最后更新内容: {delivery_last_context}",
                    )
                )
            else:
                logging.error("获取快递信息失败，info字段为空")
        else:
            logging.error("获取快递信息失败，返回数据为空或格式不正确")
    except Exception as e:
        logging.error(f"处理快递信息时发生错误: {e}")


async def process_ip_info(websocket, msg, ip):
    try:
        ip_info_json = await fetch_ip_info(ip)
        disp = ip_info_json.get("result", {}).get("disp")
        if disp:
            asyncio.create_task(
                send_group_msg(websocket, msg.get("group_id"), f"IP地址信息: {disp}")
            )  # 使用 create_task
        else:
            logging.error("获取IP信息失败，address字段为空")
    except Exception as e:
        logging.error(f"处理IP信息时发生错误: {e}")


async def handle_group_message(websocket, msg):
    try:
        if msg.get("raw_message").startswith("查快递 "):
            logging.info(f"收到查快递消息: {msg.get('raw_message')}")
            delivery_number = msg.get("raw_message").split(" ")[1]  # 不再转换为整数
            asyncio.create_task(
                process_delivery_info(websocket, msg, delivery_number)
            )  # 使用 create_task
        elif msg.get("raw_message").startswith("查IP "):
            logging.info(f"收到查IP消息: {msg.get('raw_message')}")
            ip = msg.get("raw_message").split(" ")[1]
            asyncio.create_task(process_ip_info(websocket, msg, ip))  # 使用 create_task
    except Exception as e:
        logging.error(f"处理API消息时发生错误: {e}")


async def handle_private_message(websocket, msg):
    pass

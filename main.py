import logging
import sys
import os
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api import send_group_msg
from app.scripts.Tools.api import fetch_delivery_info


async def process_delivery_info(websocket, msg, delivery_number):
    try:
        delivery_info_json = await fetch_delivery_info(delivery_number)
        if delivery_info_json.get("error"):
            await send_group_msg(
                websocket,
                msg.get("group_id"),
                f"快递查询失败: {delivery_info_json.get('error')}",
            )
        elif delivery_info_json and delivery_info_json.get("result"):
            delivery_status = delivery_info_json.get("result", {}).get("status")
            delivery_info = delivery_info_json.get("result", {}).get("info")
            if delivery_info:
                delivery_last_time = delivery_info[0].get("time")
                delivery_last_context = delivery_info[0].get("context")
                await send_group_msg(
                    websocket,
                    msg.get("group_id"),
                    f"快递状态: {delivery_status}\n最后更新时间: {delivery_last_time}\n最后更新内容: {delivery_last_context}",
                )
            else:
                logging.error("获取快递信息失败，info字段为空")
        else:
            logging.error("获取快递信息失败，返回数据为空或格式不正确")
    except Exception as e:
        logging.error(f"处理快递信息时发生错误: {e}")


async def handle_group_message(websocket, msg):
    try:
        if msg.get("raw_message").startswith("查快递 "):
            logging.info(f"收到查快递消息: {msg.get('raw_message')}")
            delivery_number = msg.get("raw_message").split(" ")[1]  # 不再转换为整数
            asyncio.create_task(
                process_delivery_info(websocket, msg, delivery_number)
            )  # 创建一个异步任务来处理快递信息，避免阻塞主线程
    except Exception as e:
        logging.error(f"处理查快递消息时发生错误: {e}")


async def handle_private_message(websocket, msg):
    pass

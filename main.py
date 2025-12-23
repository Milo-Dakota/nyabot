import sys
import asyncio
import json
from websockets import serve
from pymongo import MongoClient
import yaml
import importlib
import re

client = MongoClient("mongodb://localhost:27017")

db = client["Nyabot"]

with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

managers = {}
triggers = {}

for manager_name, manager_config in config['managers'].items():
    if manager_config.get('enabled', True):

            # 动态导入模块（假设文件在managers文件夹下）
            module = importlib.import_module(f'managers.{manager_name}')
            # 获取类（假设类名和文件名一样）
            manager_class = getattr(module, manager_name)
            # 创建实例
            instance = manager_class()
            managers[manager_name] = instance
            

            for pattern in instance.patterns:
                triggers[pattern] = manager_name
            
            instance.groups = manager_config.get('groups', [])

            for group in instance.groups:
                instance.collections[str(group)] = {}
                for header in instance.collectionheaders:
                    instance.collections[str(group)][header] = db[f"{header}_{group}"]

            print(f"✓ 已加载: {manager_name}")

async def handle_websocket(websocket):

    async for message in websocket:

        event = json.loads(message)

        if event.get("post_type") == "message" and event.get("message_type") == "group":
            raw_message = event["raw_message"]
            for pattern, manager_name in triggers.items():
                if re.match(pattern, raw_message):
                    manager = managers[manager_name]
                    response = manager.process(event)
                    await websocket.send(json.dumps(response))

        elif event.get("post_type") == "notice" and event.get("target_id") == event.get("self_id"):
            response = {
                "action": "send_group_msg",
                "params": {
                    "group_id": event["group_id"],
                    "message": "不许戳"
                }
            }
            await websocket.send(json.dumps(response))

async def main():
    async with serve(handle_websocket, "0.0.0.0", 31003):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())

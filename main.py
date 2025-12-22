import sys
import asyncio
import json
from websockets import serve
from pymongo import MongoClient
from manager_summary import manager_summary
#from manager_hash import manager_hash
from manager_debug import manager_debug
from manager_tarot import manager_tarot

client = MongoClient("mongodb://localhost:27017")

db = client["Nyabot"]
group_list=[897830548,979088841,861678361]
debug_list=[0,0,0]
collections_message=[db[str(group_list[0])],db[str(group_list[1])],db[str(group_list[2])]]
collections_image=[db["hash_"+str(group_list[0])],db["hash_"+str(group_list[1])],db["hash_"+str(group_list[2])]]

async def handle_websocket(websocket):

    async for message in websocket:

        event = json.loads(message)

        
        if event.get("post_type") == "message" and event.get("message_type") == "group":
            if event["group_id"] in group_list:
                i=group_list.index(event["group_id"])

                response0,debug = manager_debug(event,debug_list[i])
                debug_list[i]=debug
                if response0: 
                    await websocket.send(json.dumps(response0))               

                response1 = manager_summary(event,collections_message[i])
                if response1: 
                    await websocket.send(json.dumps(response1))

                #response2 = manager_hash(event,collections_image[i])
                #if response2: 
                    #await websocket.send(json.dumps(response2))

                response3 = manager_tarot(event)
                if response3: 
                    await websocket.send(json.dumps(response3))

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
import json
from bson import json_util
from datetime import datetime
from openai import OpenAI
import re

client = OpenAI(
    api_key="sk-cc80ug5d4bm9wdqpe4xybzusgmlothp7otnb9emcv7whf4o9",
    base_url="https://api.xiaomimimo.com/v1"
)

class ManagerSummary:
    def __init__(self):
        self.patterns = [r"^\.总结 (\d+)$"]
        self.collectionheaders = ["default"]
        self.groups = [] 
        self.collections = {}

        self.client = client

    def process(self, event):
        raw_message = event["raw_message"]

        collection = self.collections[event["group_id"]]["default"]

        match = re.match(self.patterns[0], raw_message)
        message_count = int(match.group(1))

        messages = list(collection.find({}, {"_id": 0}).sort("时间", -1).limit(message_count))
        messages.reverse()
        for msg in messages:
            msg['时间'] = msg['时间'].strftime("%m-%d %H:%M")

        summary = ai_summary(messages)
        response = {
            "action": "send_group_msg",
            "params": {
                "group_id": event["group_id"],
                "message": summary
            }
        }
        return response

def ai_summary(content):
    
    response = client.chat.completions.create(
    model="mimo-v2-flash",
    messages=[
        {
            "role": "user", 
            "content": prompt + f"{content}"
        }
    ],
    stream=False
    )
    print(f"{content}")
    return response.choices[0].message.content

prompt = """你是一个专业的QQ群聊内容总结助手。请根据提供的群聊消息数据，生成一份结构清晰、重点突出的纯文本群聊总结报告。

【核心原则】
输出必须是纯文本，仅使用以下符号进行排版：换行、空格、【】、◆、→、`等。严禁使用Markdown

【总结模板】
【🗓️ 总结时段】X月X日 HH:MM 至 X月X日 HH:MM

【🌐 整体氛围】
用一两句话概括群内整体气氛，如“气氛活跃”、“围绕XX话题展开热烈讨论”等。

【🔥 热聊话题】
◆ 话题一：用一句话概括核心事件
   → 时间：昨天 HH:MM - HH:MM
   → 核心成员：成员A，成员B，成员C
   → 详情：描述事件起因、经过、关键对话和结果。关键人物发言或网络用语可用`引号`突出。

◆ 话题二：用一句话概括核心事件
   → 时间：昨天 HH:MM - 今天 HH:MM
   → 核心成员：成员D，成员E
   → 详情：描述讨论的主要内容、不同观点和结论。

【💎 其他亮点】
- 成员F 分享了 [资源/图片/见闻]。
- 成员G 提出了一个关于 [问题] 的疑问。

请严格按照上述格式和要求，对以下群聊消息进行总结：


"""
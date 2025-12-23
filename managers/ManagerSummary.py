import json
from bson import json_util
from datetime import datetime
from openai import OpenAI

client = OpenAI(
    api_key="sk-cc80ug5d4bm9wdqpe4xybzusgmlothp7otnb9emcv7whf4o9",
    base_url="https://api.xiaomimimo.com/v1"
)

class ManagerSummary:
    def __init__(self):
        self.patterns = [r"^\.总结 (\d+)$"]
        self.collectionheaders = ["default"]
        self.groups = [897830548,979088841,861678361] 
        self.collections = []

        self.client = client

    def proccess(self, event):
        raw_message = event["raw_message"]

        i = self.collections[0].index(event["group_id"])
        collection = self.collections[0][i]

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
            "content": prompt + content
        }
    ],
    stream=False
    )
    return response.choices[0].message.content

prompt = """你是一个专业的QQ群聊内容总结助手。请根据提供的群聊消息数据，生成一份结构清晰、重点突出的纯文本群聊总结报告。

【数据字段说明】
- `群友`：发言者的群昵称或备注，这是主要的身份标识
- `群友id`：发言者的QQ号，仅用于理解`@消息`中提及的对象，总结时不要显示此ID
- `消息id`：消息的唯一标识，仅用于理解`回复消息`的对话关系，总结时不要显示此ID
- `发言`：消息的实际内容（已清理CQ码）
- `时间`：消息发送时间

【CQ码处理指南】
- `[CQ:face,id=123]` → 表情符号，总结时忽略或描述为"发表情"
- `[CQ:image,file=xxx.jpg]` → 图片，总结时忽略或总结为"分享图片"或根据上下文推断图片内容
- `[CQ:at,qq=123456]` → @某人，总结时保留"@用户名"的语义
- `[CQ:reply,id=xxx]` → 回复消息，总结时注意对话的连贯性
- `[CQ:share,url=...]` → 分享链接，总结为"分享链接"或根据标题描述内容

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
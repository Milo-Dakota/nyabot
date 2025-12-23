import json
from bson import json_util
from datetime import datetime

class ManagerMessage:
    def __init__(self):
        self.patterns = [r"(?s).*"]
        self.collectionheaders = ["default"]
        self.groups = [] 
        self.collections = {}

    def proccess(self, event):

        i = self.collections[0].index(event["group_id"])
        collection = self.collections[0][i]

        x=event["sender"]["card"]
        if not x:
            x=event["sender"]["nickname"]

        message = extract_info(event)

        new_message = {
            "群友": x,
            "发言": message,
            "时间": datetime.now()
        }
        collection.insert_one(new_message)
        return

def extract_info(event):
    result = []
    message = event["message"]
    for msg in message:

        if msg["type"] == "text":
            result.append({
                "type":"text",
                "text":msg["data"]["text"]
                })

        elif msg["type"] == "face":
            if msg["data"]["raw"]["faceText"]:
                result.append({
                    "type":"face",
                    "faceText":msg["data"]["raw"]["faceText"]
                    })
            elif face_dic[msg["data"]["id"]]:
                result.append({
                    "type":"face",
                    "faceText":face_dic[msg["data"]["id"]]
                    })   
            else:
                result.append({
                    "type":"face",
                    "faceText":"[表情]"
                    })                

        elif msg["type"] == "image":
            if msg["data"]["summary"]:
                result.append({
                    "type":"image",
                    "summary":msg["data"]["summary"]
                    })  
            else:
                result.append({
                    "type":"image",
                    "summary":"image"
                    })  

        elif msg["type"] == "at":
            pass

        elif msg["type"] == "reply":
            pass

        else:
            pass

face_dic = {
    0: "[惊讶]",
    1: "[撇嘴]",
    2: "[色]",
    3: "[发呆]",
    4: "[得意]",
    5: "[流泪]",
    6: "[害羞]",
    7: "[闭嘴]",
    8: "[睡]",
    9: "[大哭]",
    10: "[尴尬]",
    11: "[发怒]",
    12: "[调皮]",
    13: "[呲牙]",
    14: "[微笑]",
    15: "[难过]",
    16: "[酷]",
    18: "[抓狂]",
    19: "[吐]",
    20: "[偷笑]",
    21: "[可爱]",
    22: "[白眼]",
    23: "[傲慢]",
    24: "[饥饿]",
    25: "[困]",
    26: "[惊恐]",
    27: "[流汗]",
    28: "[憨笑]",
    29: "[悠闲]",
    30: "[奋斗]",
    31: "[咒骂]",
    32: "[疑问]",
    33: "[嘘]",
    34: "[晕]",
    35: "[折磨]",
    36: "[衰]",
    37: "[骷髅]",
    38: "[敲打]",
    39: "[再见]",
    41: "[发抖]",
    42: "[爱情]",
    43: "[跳跳]",
    46: "[猪头]",
    49: "[拥抱]",
    53: "[蛋糕]",
    55: "[炸弹]",
    56: "[刀]",
    59: "[便便]",
    60: "[咖啡]",
    63: "[玫瑰]",
    64: "[凋谢]",
    66: "[爱心]",
    67: "[心碎]",
    74: "[太阳]",
    75: "[月亮]",
    76: "[赞]",
    77: "[踩]",
    78: "[握手]",
    79: "[胜利]",
    85: "[飞吻]",
    86: "[怄火]",
    89: "[西瓜]",
    96: "[冷汗]",
    97: "[擦汗]",
    98: "[抠鼻]",
    99: "[鼓掌]",
    100: "[糗大了]",
    101: "[坏笑]",
    102: "[左哼哼]",
    103: "[右哼哼]",
    104: "[哈欠]",
    106: "[委屈]",
    109: "[左亲亲]",
    111: "[可怜]",
    116: "[示爱]",
    118: "[抱拳]",
    120: "[拳头]",
    122: "[爱你]",
    123: "[NO]",
    124: "[OK]",
    125: "[转圈]",
    129: "[挥手]",
    144: "[喝彩]",
    147: "[棒棒糖]",
    171: "[茶]",
    173: "[泪奔]",
    174: "[无奈]",
    175: "[卖萌]",
    176: "[小纠结]",
    179: "[doge]",
    180: "[惊喜]",
    181: "[骚扰]",
    182: "[笑哭]",
    183: "[我最美]",
    201: "[点赞]",
    203: "[托脸]",
    212: "[托腮]",
    214: "[啵啵]",
    219: "[蹭一蹭]",
    222: "[抱抱]",
    227: "[拍手]",
    232: "[佛系]",
    240: "[喷脸]",
    243: "[甩头]",
    246: "[加油抱抱]",
    262: "[脑阔疼]",
    264: "[捂脸]",
    265: "[辣眼睛]",
    266: "[哦哟]",
    267: "[头秃]",
    268: "[问号脸]",
    269: "[暗中观察]",
    270: "[emm]",
    271: "[吃瓜]",
    272: "[呵呵哒]",
    273: "[我酸了]",
    277: "[汪汪]",
    278: "[汗]",
    281: "[无眼笑]",
    282: "[敬礼]",
    284: "[面无表情]",
    285: "[摸鱼]",
    287: "[哦]",
    289: "[睁眼]",
    290: "[敲开心]",
    293: "[摸锦鲤]",
    294: "[期待]",
    297: "[拜谢]",
    298: "[元宝]",
    299: "[牛啊]",
    305: "[右亲亲]",
    306: "[牛气冲天]",
    307: "[喵喵]",
    314: "[仔细分析]",
    315: "[加油]",
    318: "[崇拜]",
    319: "[比心]",
    320: "[庆祝]",
    322: "[拒绝]",
    324: "[吃糖]",
    326: "[生气]"
}
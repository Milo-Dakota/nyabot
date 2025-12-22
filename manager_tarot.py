import re
import random

def manager_tarot(event):
    raw_message = event["raw_message"]

    pattern = r"^\.塔罗牌$"

    if re.match(pattern, raw_message):

        tarot = random.choice(tarots)

        response = {
            "action": "send_group_msg",
            "params": {
                "group_id": event["group_id"],
                "message": [
                    {
                        "type": "reply",
                        "data": {
                            "id": event["message_id"]
                        }
                    },
                    {
                        "type": "text",
                        "data": {
                            "text": f"抽到了：\n『{tarot["card"]}』\n『{tarot["master"]}』的替身『{tarot["name"]}』"
                        }
                    },
                    {
                        "type": "image",
                        "data": {
                            "file": f"file:///app/nyabot/tarots/{tarot["image"]}.png"
                        }
                    },
                    {
                        "type": "text",
                        "data": {
                            "text": f"替身能力：\n{tarot["magic"]}!"
                        }
                    }
                ]
            }
        }
        return response

tarots = [
  {
    "name": "魔术师",
    "master": "穆罕默德·阿布德尔",
    "magic": "能操控火焰进行攻击和防御",
    "card": "魔术师",
    "image": 0
  },
  {
    "name": "女教皇",
    "master": "蜜朵拉",
    "magic": "能融入并操控矿物质，进行变形和攻击",
    "card": "女教皇",
    "image": 1
  },
  {
    "name": "女皇帝",
    "master": "妮娜",
    "magic": "通过亲吻使目标部位增生肉瘤并操控",
    "card": "女皇帝",
    "image": 2
  },
  {
    "name": "皇帝",
    "master": "荷尔·荷斯",
    "magic": "发射能自动追踪目标的子弹",
    "card": "皇帝",
    "image": 3
  },
  {
    "name": "法皇",
    "master": "花京院典明",
    "magic": "可远程操控，发射绿宝石水花，并能布设结界",
    "card": "教皇",
    "image": 4
  },
  {
    "name": "恋人",
    "master": "钢铁阿丹",
    "magic": "植入肉芽操控他人，并能共享伤害与感知",
    "card": "恋人",
    "image": 5
  },
  {
    "name": "战车",
    "master": "J·P·波鲁那雷夫",
    "magic": "手持双剑的银色人形替身，速度与精准度高",
    "card": "战车",
    "image": 6
  },
  {
    "name": "力量",
    "master": "拉巴索",
    "magic": "附身于船只，能操控船体变形与攻击",
    "card": "力量",
    "image": 7
  },
  {
    "name": "隐者之紫",
    "master": "乔瑟夫·乔斯达",
    "magic": "藤蔓状替身，可用于侦查、念写与传导波纹",
    "card": "隐士",
    "image": 8
  },
  {
    "name": "命运之轮",
    "master": "ZZ",
    "magic": "与车辆融合，大幅强化车辆性能并变形攻击",
    "card": "命运之轮",
    "image": 9
  },
  {
    "name": "正义",
    "master": "恩雅婆婆",
    "magic": "制造并操控浓雾，能在雾中形成幻象并实体化攻击",
    "card": "正义",
    "image": 10
  },
  {
    "name": "倒吊人",
    "master": "J·凯尔",
    "magic": "能在镜面或反光物中移动并攻击",
    "card": "吊人",
    "image": 11
  },
  {
    "name": "死神13",
    "master": "曼登·提姆",
    "magic": "在梦境中实体化，对梦中造成的伤害会反映到现实",
    "card": "死神",
    "image": 12
  },
  {
    "name": "黄色节制",
    "master": "橡胶灵魂",
    "magic": "覆盖于体表，可变形伪装，并能吸收冲击与能量",
    "card": "节制",
    "image": 13
  },
  {
    "name": "恶魔",
    "master": "诅咒的迪波",
    "magic": "通过怨恨操控玩偶进行追踪与攻击",
    "card": "恶魔",
    "image": 14
  },
  {
    "name": "灰塔",
    "master": "灰塔",
    "magic": "小型昆虫状替身，以极快速度刺穿目标",
    "card": "塔",
    "image": 15
  },
  {
    "name": "星辰",
    "master": "空条承太郎",
    "magic": "近距离力量型人形替身，拥有超高精度与停止时间的能力",
    "card": "星星",
    "image": 16
  },
  {
    "name": "月亮",
    "master": "恩多尔",
    "magic": "制造逼真的水面幻象，并可用藤壶束缚敌人",
    "card": "月亮",
    "image": 17
  },
  {
    "name": "太阳",
    "master": "阿拉伯胖子",
    "magic": "制造出类似太阳的高热光球，持续灼烧敌人",
    "card": "太阳",
    "image": 18
  },
  {
    "name": "审判",
    "master": "卡梅欧",
    "magic": "利用泥土实现他人愿望，但会扭曲愿望的本质",
    "card": "审判",
    "image": 19
  },
  {
    "name": "世界",
    "master": "DIO",
    "magic": "近距离力量型人形替身，拥有超越星辰的力量与停止时间的能力",
    "card": "世界",
    "image": 20
  },
  {
    "name": "愚者",
    "master": "伊奇",
    "magic": "操控沙子进行防御、移动与攻击",
    "card": "愚者",
    "image": 21
  }
]
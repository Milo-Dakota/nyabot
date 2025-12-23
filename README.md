# Nyabot

一个可以高度自定义的QQ聊天机器人框架

## 基于
- MongoDB
- Napcat(Docker)

## 自定义功能编写指南
1. 编写Manager类
```python
#用你的Manager名字替换ManagerName，比如ManagerChat
class ManagerName:
   def __init__(self):

      #在patterns列表里添加触发该Manager的trigger，请使用正则表达式
      #系统会在检测到trigger时自动执行你编写的process函数
      #如果你希望该Manager在任何情况下都运行，请使用r"(?s).*"作为trigger
      self.patterns = []

      #在collectionheaders列表里添加你需要的数据库集合名称，系统会自动创建并初始化数据库并存入self.collections字典
      #如果你希望该Manager不使用数据库，请留空该列表
      #系统自带的ManagerMessage会将群聊消息存入"default"集合，如果你希望调用它，请在collectionheaders列表里添加"default"
      self.collectionheaders = []

      #如果你想限制Manager管理的群聊，不要在这里修改，而是去config.yaml里修改
      self.groups = [] 

      #你需要用到的数据库集合，系统会自动创建并初始化
      #访问数据库请使用self.collections[group][collectionheader]
      self.collections = {}

      #你可以在这里定义你想用的自定义变量
      self.custom_var = "custom_value"

   def process(self, event):
      #在这里写你的自定义处理逻辑
      #event是一个字典，包含了触发该Manager的事件信息，包括群号、QQ号、消息内容等
      #该函数应当返回一个response，其格式请参照onebotv11的标准
```

2. 在config.yaml里添加Manager
```yaml
managers:
  ManagerDebug:
    enabled: true
    groups:
      - 979088841
      - 897830548
  
  ManagerMessage:
    enabled: true
    groups:
      - 979088841
      - 897830548
```
在这里添加你的Manager，配置是否开启与管理的群聊。

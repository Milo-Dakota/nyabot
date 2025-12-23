import re

class ManagerDebug:
    def __init__(self):
        self.patterns = [r"(?s).*"]
        self.collectionheaders = []
        self.groups = [] 
        self.collections = {}

        self.debug = 0

    def process(self, event):
        patterns = [r"^\.debugon$", r"^\.debugoff$"]
        raw_message = event["raw_message"]
        if any(re.match(pattern, raw_message) for pattern in patterns):
            if re.match(r"^\.debugon$", raw_message):
                self.debug = 1
                response = {
                    "action": "send_group_msg",
                    "params": {
                        "group_id": event["group_id"],
                        "message": "debug on"
                    }
                }
                return response
            
            elif re.match(r"^\.debugoff$", raw_message):
                self.debug = 0
                response = {
                    "action": "send_group_msg",
                    "params": {
                        "group_id": event["group_id"],
                        "message": "debug off"
                    }
                }
                return response
            
        elif self.debug:
            print(event)
            return
import re

def manager_debug(event, debug):
    raw_message = event["raw_message"]

    pattern1 = r"^\.debugon$"
    pattern2 = r"^\.debugoff$"

    if re.match(pattern1, raw_message):
        response = {
            "action": "send_group_msg",
            "params": {
                "group_id": event["group_id"],
                "message": "debug on"
            }
        }
        return response,1
    elif re.match(pattern2, raw_message):
        response = {
            "action": "send_group_msg",
            "params": {
                "group_id": event["group_id"],
                "message": "debug off"
            }
        }
        return response,0
    elif debug:
        print(event)
        return None,1
    return None,0
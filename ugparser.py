import re
import requests
import json

def UserAgentExtractor(log_line):
    useragent = ""
    for i in range(len(log_line)-2,0,-1):
        if(log_line[i] != '"'):
            useragent += log_line[i]
        else:
            break
    return useragent[::-1]

def UserAgentParser(useragent):
    headers = {
        "X-API-KEY": "e4ad241fce428383c8b243a18e2cf68c",
    }
    post_data = {
        "user_agent": useragent,
        "parse_options": {},
    }

    result = requests.post("https://api.whatismybrowser.com/api/v2/user_agent_parse", data=json.dumps(post_data), headers=headers)
    result_json = result.json()
    parse = result_json.get("parse")
    if parse.get("is_abusive"):
        #print("\tMalcious user-agent detected")
        return 1
    else:
        return 0
    
# useragent = "0\\\'XOR(if(now()=sysdate(),sleep(12),0))XOR\\\'Z"
# print(UserAgentParser(useragent))

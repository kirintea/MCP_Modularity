import requests
import json

import sys
import os
# 将上一级目录加入到 Python 搜索路径中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# # 从配置文件 config.py 中导入参数
# from config import LLM_QUESTION_URL_CONFIG, MODEL_NAME, HEADERS

LLM_QUESTION_URL_CONFIG = "https://api.siliconflow.cn/v1/chat/completions"
MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
HEADERS = {
    'Authorization': 'Bearer sk-rmprjadkeedwjibjztyjzwmzxmvzmyjspvlwhpkwgqujzdjs',
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
    'Content-Type': 'application/json'
}

def chat_completions():
    # 使用配置文件中的 API 基础地址和模型名称
    url = LLM_QUESTION_URL_CONFIG

    # 请求体，使用配置中的模型名称
    params = {
    "model": MODEL_NAME,
    "messages": [
        {   "role": "system", 
            "content": "你是一名善解人意的小管家"
        },
        {
            "role": "user",
            "content": "去银川旅行怎么安排行程？用30个字回答"
        }
    ],
    "temperature": 0, 
    "stream": False
}

    # 发送 POST 请求
    r = requests.post(url, json=params, headers=HEADERS)

    return r


if __name__ == '__main__':
    r = chat_completions()
    print(r.status_code)
    print(r)
    response = r.json()
    
    # 处理响应，输出聊天结果
    if 'choices' in response and len(response['choices']) > 0:
        content = response['choices'][0]['message']['content']
        print(content)
    else:
        print(f"Error: {response}")
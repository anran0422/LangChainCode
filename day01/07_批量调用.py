"""
    load_dotenv() —— 负责读取 .env 文件，把里面的键值对写入当前进程的环境变量池。
    os.getenv() —— 负责从环境变量池里取值。
"""

import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model(
    model=os.getenv('MODEL_NAME'),
    model_provider=os.getenv('MODEL_PROVIDER'),
    base_url=os.getenv('DEEPSEEK_BASE_URL'),
    api_key=os.getenv('DEEPSEEK_API_KEY')
)

messages = [
    [
        {"role":"system", "content": "你是一位诗人"},
        {"role":"user", "content": "写一首关于春天的诗"}
    ],
    [
        {"role":"system", "content": "你是一位诗人"},
        {"role":"user", "content": "写一首诗来赞美张家界十里画廊"}
    ],
    [
        {"role":"system", "content": "你是一位诗人"},
        {"role":"user", "content": "写一首诗来赞美张家界国家森林公园"}
    ],
]

resp = llm.batch(messages)
print(resp[0])
print("========================")
print(resp)

# 时间对比还没写！

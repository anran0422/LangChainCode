"""
    API-Ley 管理与使用
    1. 显示读取 .env 文件
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# DeepSeek 说兼容，竟然命名都可以这样搞
client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)

completion = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {"role": "user", "content": "将'你好'翻译成意大利语"}
    ],
)
print(completion.choices[0].message.content)
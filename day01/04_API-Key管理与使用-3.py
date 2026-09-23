"""
    API-Ley 管理与使用
    1. 显示读取 .env 文件
    2. 隐式读取 .env 文件（和1 一样都需要加载 load_dotenv 文件才可以）
    3. 在终端设置临时变量，或者设置 Pycharm 环境变量
    这里通过设置 Pycharm 环境变量
"""
import os
from openai import OpenAI

print("API KEY:", os.getenv("OPENAI_API_KEY"))

client = OpenAI(
    base_url="https://api.deepseek.com",
    # api_key 终端设置临时变量
    api_key=os.getenv("OPENAI_API_KEY")
)

completion = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {"role": "user", "content": "将'你好'翻译成意大利语"}
    ],
)
print(completion.choices[0].message.content)

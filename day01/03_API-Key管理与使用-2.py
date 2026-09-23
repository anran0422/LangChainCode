"""
    API-Ley 管理与使用
    1. 显示读取 .env 文件
    2. 隐式读取 .env 文件（和1 一样都需要加载 load_dotenv 文件才可以）
"""
"""
    load_dotenv() —— 负责读取 .env 文件，把里面的键值对写入当前进程的环境变量池。
    os.getenv() —— 负责从环境变量池里取值。
"""


from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

completion = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {"role": "user", "content": "将'你好'翻译成意大利语"}
    ],
)
print(completion.choices[0].message.content)
"""
    输出解析器常用的有：字符串解析器 和 JSON 解析器
    这里是字符串解析器 StrOutputParser，从 LLM 输出提取 content
"""
import os
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model(
    model=os.getenv('MODEL_NAME'),
    model_provider=os.getenv('MODEL_PROVIDER'),
    base_url=os.getenv('DEEPSEEK_BASE_URL'),
    api_key=os.getenv('DEEPSEEK_API_KEY')
)

messages = [
    {"role": "system", "content": "我是你的专属机器人"},
    {"role": "user", "content": "你好"}
]

resp = llm.invoke(messages)
print(resp)

print("============")

str_parser = StrOutputParser()
# 经过输出解析器解析
# 也可以只直接 StrOutputParser().invoke
str_res = str_parser.invoke(resp)
print(str_res)
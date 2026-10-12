"""
    输出解析器常用的有：字符串解析器 和 JSON 解析器
    这里是字符串解析器 JsonOutputParser，从 LLM 输出提取 content
        1. 将自由输出文本转化为结构化 JSON 数据的工具，特别适用于需要严格输出结构化输出的场景
            API 调用、数据存储、下游任务处理
        2. 要结合 Pydantic 模型进行数据验证，自动验证字段类型和内容（字符串、数字、嵌套对象等）
        3. 使用 get_format_instructions 方法
            get_format_instructions()：根据 OutputParser 定义的输出结构，
            自动生成“要求 LLM 按指定格式输出”的提示词，通常放入 system 消息中。
            字段名决定 JSON 的 key，description 主要是给模型看的语义说明
"""

import os
from typing import List

from pydantic import BaseModel,Field
from langchain_core.output_parsers import JsonOutputParser
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model(
    model=os.getenv('MODEL_NAME'),
    model_provider=os.getenv('MODEL_PROVIDER'),
    base_url=os.getenv('DEEPSEEK_BASE_URL'),
    api_key=os.getenv('DEEPSEEK_API_KEY')
)

# 控制了输出模板
class Prime(BaseModel): # 结构可能不太好，可以把 Prime 封装成对象
    prime: int = Field(description="素数")
    count: int = Field(description="小于素数的素数个数")
    # 字段名决定 JSON 的 key，description 主要是给模型看的语义说明
class PrimeList(BaseModel):
    primes: List[Prime] = Field(description="素数列表")

# 定义根据哪个类进行 JSON 结构化输出
json_parser = JsonOutputParser(pydantic_model=PrimeList)

messages = [
    {"role": "system", "content": json_parser.get_format_instructions()}, # 一句指令：按照指定格式进行输出
    {"role": "user", "content": "生成任意 3 个 在 100-200 之间的素数，并标出小于该素数的素数个数"}
]

res = llm.invoke(messages)
json_res = json_parser.invoke(res)
print(json_res)

# {'primes': [{'素数': 101, '小于该素数的素数个数': 25},
# {'素数': 131, '小于该素数的素数个数': 31},
# {'素数': 199, '小于该素数的素数个数': 45}]}

# 第2次输出
# 因为字段是 prime，描述是中文，如果把字段改成中文，输出就是中文了
# 字段名决定 JSON 的 key，description 主要是给模型看的语义说明。
# {'primes': [{'prime': 101, 'count_of_primes_less_than': 25},
# {'prime': 151, 'count_of_primes_less_than': 35},
# {'prime': 199, 'count_of_primes_less_than': 45}]}
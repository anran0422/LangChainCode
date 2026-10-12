"""
    大模型按照给定的模式格式提供响应
    如果模型没有提供，只能使用 Langchain 自己的，就是前面的
"""
import os
from typing import TypedDict, Annotated

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

llm = init_chat_model(
    model=os.getenv("MODEL_NAME"),
    model_provider=os.getenv("MODEL_PROVIDER"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    extra_body={
            "thinking": {
                "type": "disabled"  # 强制关闭思考模式
            }
        }
)

class Animal(TypedDict):
    animal: Annotated[str, "动物"]
    emoji: Annotated[str, "表情"]

class AnimalList(TypedDict):
    animals: Annotated[list[Animal], "动物与表情列表"]

messages = [
    {"role": "user", "content": "任意生成三种动物，以及他们的 emoji 表情"}
]

# 这个相当于是 system 预设，可以去比较 JsonOutputParser
llm_struct = llm.with_structured_output(AnimalList)

res = llm_struct.invoke(messages)

print(res)
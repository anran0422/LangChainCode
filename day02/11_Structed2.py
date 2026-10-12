"""
    与 10 一样，只是更改类型，带有验证方案
    只是 类型定义问题，和使用输出方式没冲突
"""
import os
# from typing import TypedDict, Annotated
from pydantic import BaseModel, Field
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

class Animal(BaseModel):
    animal: str = Field(description="动物")
    emoji: str = Field(description="表情")

class AnimalList(BaseModel):
    animals: list[Animal] = Field(description="动物与表情列表")

messages = [
    {"role": "user", "content": "任意生成三种动物，以及他们的 emoji 表情"}
]

# 这个相当于是 system 预设，可以去比较 JsonOutputParser
llm_struct = llm.with_structured_output(AnimalList)

res = llm_struct.invoke(messages)

print(res)
"""
    和前面的非流式调用完全一样
"""
import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model(
    model=os.getenv("MODEL_NAME"),
    model_provider=os.getenv("MODEL_PROVIDER"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY")
)

messages = [
    [
        {"role": "system", "content": "你是一个数学家"},
        {"role": "user", "content": "请给出勾股定理的公式"}
    ],
[
        {"role": "system", "content": "你是一个数学家"},
        {"role": "user", "content": "请给九九乘法表，要排列好"}
    ],
]

resp = [llm.invoke(message) for message in messages]
print(resp)
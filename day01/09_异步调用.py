import asyncio
import os
import time
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

async def async_invoke():
    tasks = [llm.ainvoke(message) for message in messages]
    return await asyncio.gather(*tasks)

start_time = time.time()

resp = asyncio.run(async_invoke())

total_time = time.time() - start_time

print(f"执行花费的时间：{total_time} s")
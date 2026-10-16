"""
    传入一个 Python 函数，或者说可执行的一个对象，将其封装成 Runnable 示例
    使得可以使用 invoke 调用
"""

import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda

load_dotenv()

llm = init_chat_model(
    model=os.getenv("MODEL_NAME"),
    model_provider=os.getenv("MODEL_PROVIDER"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY")
)

@RunnableLambda
def total_len(x):
    return len(x["text1"]) + len(x["text2"])

chain = {
    "text1": lambda x: x + "world",
    "text2": lambda x: x + ", how are you"
} | total_len

res = chain.invoke("hello")
print(res) # 28

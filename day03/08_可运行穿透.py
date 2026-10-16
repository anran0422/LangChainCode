"""
    assign 方法向输出中添加键
    RunnablePassthrough 在 LCEL 中的无操作节点
    可以接收输入并且将其原样输出，用于在流水线中透传输入或者保留上下文，也可以向输出中添加键
"""
import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

llm = init_chat_model(
    model=os.getenv("MODEL_NAME"),
    model_provider=os.getenv("MODEL_PROVIDER"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY")
)

chain = {
    "text1": lambda x: x + " world",
    "text2": lambda x: x + ", how are you"
} | RunnablePassthrough.assign(word_count=lambda x: len(x["text1"]) + len(x["text2"]))

res = chain.invoke("hello")
print(res)
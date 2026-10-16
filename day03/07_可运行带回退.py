"""
    Runnable 就有with_fallbacks 方法，直接使用即可，回退
    该方法接收列表，即使一个回退机制也需要 []
"""
import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = init_chat_model(
    model=os.getenv("MODEL_NAME"),
    model_provider=os.getenv("MODEL_PROVIDER"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY")
)

# 这里有填充变量才对
# 这里应该是接收一个 字典 {}
chain = PromptTemplate.from_template("给我讲一个关于 {topic} 的笑话") | llm
chain_with_fallback = chain.with_fallbacks([RunnableLambda(lambda x : "sorry")])

# 它把你传入的字符串，自动包装成了一个‌单键字典‌，键名恰好就是模板里定义的唯一变量名 {topic}。
res = chain_with_fallback.invoke("1")
print(res)
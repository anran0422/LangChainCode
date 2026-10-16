"""
    RunnableParallel
    运行并行：同步使用线程池实现的，异步是用 asyncio.gather 实现的
"""

import os
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableParallel

load_dotenv()

llm = init_chat_model(
    model=os.getenv("MODEL_NAME"),
    model_provider=os.getenv("MODEL_PROVIDER"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY")
)

joke_chain = (
    PromptTemplate.from_template(template="讲一个关于{topic}的笑话") | llm | StrOutputParser()
)

poem_chain = (
    PromptTemplate.from_template(template="讲一个关于{topic}的诗歌") | llm | StrOutputParser()
)

# 这是在构建键值对，保证返回结果，没有也行，但是结果可能混乱
map_chain = RunnableParallel(joke=joke_chain, poem=poem_chain)

res = map_chain.invoke({"topic": "人工智能"})

print(res)
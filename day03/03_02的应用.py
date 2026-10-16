"""
    可以说是对于不同的模型对于同一个问题的回答
"""

import os
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableParallel

load_dotenv()

# 1. 初始化两个模型实例
# 注意：两者都使用 init_chat_model 以确保它们都是 LangChain 的 Runnable 对象
openai_model = init_chat_model(
    model="deepseek-flash",  # 或者从环境变量获取 os.getenv("OPENAI_MODEL_NAME")
    model_provider="deepseek",
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)

deepseek_model = init_chat_model(
    model=os.getenv("MODEL_NAME", "deepseek-chat"),
    model_provider=os.getenv("MODEL_PROVIDER", "deepseek"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY")
)

# 2. 定义 Prompt 模板
messages = [
    ("system", "你是一个艺术家，请用富有想象力的语言回答"),
    ("user", "{user_question}")
]
template = ChatPromptTemplate.from_messages(messages)

# 3. 构建 Chain
# 关键点：
# - template 输出字符串
# - openai_model 和 deepseek_model 接收字符串，输出 AIMessage
# - StrOutputParser() 将 AIMessage 转换为纯字符串
# - RunnableParallel 并行执行两个分支，并将结果合并为字典
chain = template | RunnableParallel({
    "openai_output": openai_model | StrOutputParser(),
    "deepseek_output": deepseek_model | StrOutputParser()
})

# 4. 执行并获取结果
try:
    res = chain.invoke({"user_question": "什么是人工智能？"})

    print("--- OpenAI 回答 ---")
    print(res["openai_output"])

    print("\n--- DeepSeek 回答 ---")
    print(res["deepseek_output"])

except Exception as e:
    print(f"发生错误: {e}")

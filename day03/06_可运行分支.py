"""
    RunnableBranch 对列表和默认分支进行初始化
    像是条件分支
"""
import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_core.runnables import RunnableBranch

load_dotenv()

llm = init_chat_model(
    model=os.getenv("MODEL_NAME"),
    model_provider=os.getenv("MODEL_PROVIDER"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY")
)

branch = RunnableBranch(
    (lambda x : isinstance(x, str), lambda x : x.upper()),
    (lambda x : isinstance(x, int), lambda x :x + 1),
    (lambda x : isinstance(x, float), lambda x : x * 2),
    lambda x : "goodbye"
)

res = branch.invoke(2.5) # 5.0
print(res)

res = branch.invoke(None) # goodbye
print(res)
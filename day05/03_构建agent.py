"""
    这里的给定工具，没有用 llm.bind_tools
    而是直接 from langchain.agents import create_agent 能够指定参数
    create_agent() 创建的 Agent 基于 LangGraph 的状态图运行，
        默认期望输入是一个字典，其中包含 messages 等状态字段。
"""

import os
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
load_dotenv()

print("Tavily Key 是否加载：", bool(os.getenv("TAVILY_API_KEY")))
llm = init_chat_model(
    model=os.getenv('MODEL_NAME'),
    model_provider=os.getenv('MODEL_PROVIDER'),
    base_url=os.getenv('DEEPSEEK_BASE_URL'),
    api_key=os.getenv('DEEPSEEK_API_KEY')
)

# 定义工具
search = TavilySearch()
tools = [search]

# 创建 Agent
agent = create_agent(model=llm, tools=tools,
                     system_prompt="你是一个 AI 助手，请你帮助用户解决问题！")

# 调用 Agent
res = agent.invoke( # 这里必须是字典
    {
        "messages": [
            {"role":"user", "content": "现在北京的天气怎么样？"}
        ]
    }
)
print(res)
print("=============")

# 流式调用，显示进度
for chunk in agent.stream({
    "messages": [
        {"role":"user", "content": "现在北京的天气怎么样？"}
    ]
}):
    print(chunk, end="\n\n")
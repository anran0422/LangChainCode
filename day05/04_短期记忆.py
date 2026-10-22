"""
    携带短期记忆，线程级持久化
    使用的是 LangGraph 的
"""

import os
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
load_dotenv()

print("Tavily Key 是否加载：", bool(os.getenv("TAVILY_API_KEY")))
llm = init_chat_model(
    model=os.getenv('MODEL_NAME'),
    model_provider=os.getenv('MODEL_PROVIDER'),
    base_url=os.getenv('DEEPSEEK_BASE_URL'),
    api_key=os.getenv('DEEPSEEK_API_KEY')
)

# Smith 项目，方便查询
os.environ["LANGSMITH_PROJECT"] = 'agent-with-memory'

# 定义工具
search = TavilySearch()
tools = [search]

# 创建 Agent
agent = create_agent(model=llm, tools=tools,checkpointer=InMemorySaver(),
                     system_prompt="你是一个 AI 助手，请你帮助用户解决问题！")

config = {
    "configurable":{"thread_id":"agent_with_memory"}
}

# 调用 Agent
res = agent.invoke( # 这里必须是字典
    {
        "messages": [
            {"role":"user", "content": "现在北京的天气怎么样？"}
        ]
    },config=config
)
print(res)
print("=============")

# 流式调用，显示进度
for chunk in agent.stream({
    "messages": [
        {"role":"user", "content": "我刚才让你查询过北京的天气了吗？"} # 通过这个问题就可以看到，config的作用了
    ]
}, config=config):
    print(chunk, end="\n\n")

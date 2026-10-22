"""
    配合 MCP 难度也不大，只是阿里云百炼需要充钱
    另外一个全是英文，也不想搞了
    如果后面需要再修改代码好了
"""
# pip install langchain-mcp-adapters langchain langchain-openai

import os
import asyncio
from urllib.parse import urlencode

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient


# ==================== 1. 配置 MCP 客户端 ====================

mcp_client = MultiServerMCPClient(
    {
        "WebSearch": {
            "transport": "sse",
            "url": "https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/sse",
            "headers": {
                "Authorization": f"Bearer {os.getenv('DASHSCOPE_API_KEY')}"
            },
        },
        # 阿里云百炼 WebSearch MCP：
        # https://bailian.console.aliyun.com/?tab=mcp#/mcp-market/detail/WebSearch

        "RailService": {
            "transport": "streamable_http",
            "url": (
                "https://server.smithery.ai/@DeniseLewis200081/rail/mcp"
                f"?{urlencode({'api_key': os.getenv('SMITHERY_API_KEY')})}"
            ),
        },
        # Smithery Rail MCP：
        # https://smithery.ai/server/@DeniseLewis200081/rail
    }
)


# ==================== 2. 定义大模型 ====================

llm = init_chat_model(
    model="z-ai/glm-4.5-air:free",
    model_provider="openai",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


# ==================== 3. 创建 Agent 并调用 ====================

async def main():
    # 获取 MCP 工具
    tools = await mcp_client.get_tools()

    print("已加载的 MCP 工具：")
    for tool in tools:
        print(f"- {tool.name}: {tool.description}")

    # 创建 Agent
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="你是一位助手，需要根据用户需求调用合适的工具来帮助用户。",
    )

    # 调用 Agent 并流式输出执行过程
    async for chunk in agent.astream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "北京今天天气怎么样？"
                        "如果天气还不错，帮我看看今天上海到北京的车票。"
                    ),
                }
            ]
        },
        stream_mode="updates",
    ):
        print(chunk, end="\n\n")


if __name__ == "__main__":
    asyncio.run(main())

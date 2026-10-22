
import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def call_mcp_server(name: str, url: str):
    """连接 MCP 服务并测试工具、资源和提示词。"""
    print(f"\n{'=' * 20} {name} {'=' * 20}")
    print(f"连接地址：{url}")

    async with streamablehttp_client(url) as (read, write, _):
        async with ClientSession(read, write) as session:
            # 初始化连接
            await session.initialize()
            print("MCP 服务连接成功！")

            # 1. 查看工具
            tools = await session.list_tools()
            print("\n【可用工具】")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            # 2. 调用加法工具
            if name == "工具服务":
                result = await session.call_tool(
                    "add",
                    {"a": 1, "b": 2}
                )
                print("\n【工具调用结果】")
                print(result)

            # 3. 查看资源
            resources = await session.list_resources()
            print("\n【可用资源】")
            for resource in resources.resources:
                print(f"- {resource.name}: {resource.uri}")

            # 4. 读取问候语资源
            if name == "资源服务":
                result = await session.read_resource(
                    "greeting://default"
                )
                print("\n【资源读取结果】")
                print(result)

            # 5. 查看提示词
            prompts = await session.list_prompts()
            print("\n【可用提示词】")
            for prompt in prompts.prompts:
                print(f"- {prompt.name}: {prompt.description}")

            # 6. 获取问候提示词
            if name == "提示词服务":
                result = await session.get_prompt(
                    "greet_user",
                    {"name": "Jack"}
                )
                print("\n【提示词调用结果】")
                print(result)


async def main():
    # 依次连接三个 MCP 服务
    servers = [
        (
            "工具服务",
            "http://127.0.0.1:8000/tool/"
        ),
        (
            "资源服务",
            "http://127.0.0.1:8000/resource/"
        ),
        (
            "提示词服务",
            "http://127.0.0.1:8000/prompt/"
        ),
    ]

    for name, url in servers:
        try:
            await call_mcp_server(name, url)
        except Exception as e:
            print(f"\n【{name}连接失败】")
            print(f"错误信息：{e}")


if __name__ == "__main__":
    asyncio.run(main())

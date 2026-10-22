
# pip install mcp
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def streamablehttp_run():
    # MCP 服务端地址
    url = "http://127.0.0.1:8000/mcp"

    # 请求头（仅当服务端配置了对应认证时才需要）
    headers = {
        "Authorization": "Bearer sk-atguigu"
    }

    # 建立 Streamable HTTP 连接
    async with streamablehttp_client(url, headers=headers) as (
        read,
        write,
        _
    ):
        async with ClientSession(read, write) as session:
            # 初始化连接
            await session.initialize()

            # 获取可用工具
            tools = await session.list_tools()
            print("可用工具：")
            print(tools)
            print()

            # 调用工具
            call_res = await session.call_tool(
                "add",
                {"a": 1, "b": 2}
            )
            print("工具调用结果：")
            print(call_res)
            print()

            # 获取可用资源
            resources = await session.list_resources()
            print("可用资源：")
            print(resources)
            print()

            # 读取资源
            read_res = await session.read_resource(
                "greeting://default"
            )
            print("资源读取结果：")
            print(read_res)
            print()

            # 获取可用提示词
            prompts = await session.list_prompts()
            print("可用提示词：")
            print(prompts)
            print()

            # 调用提示词
            get_res = await session.get_prompt(
                "greet_user",
                {"name": "Jack"}
            )
            print("提示词调用结果：")
            print(get_res)
            print()


if __name__ == "__main__":
    asyncio.run(streamablehttp_run())
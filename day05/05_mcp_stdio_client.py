"""
    修改这个 args 的文件名称，才能运行
    # 配置 MCP 服务端启动参数
    server_params = StdioServerParameters( # 这里本质是个命令，所以后面就被抛弃了
        command="python",
        args=["05_mcp_stdio_server.py"],
    )
"""

import asyncio
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters


async def stdio_run():
    # 配置 MCP 服务端启动参数
    server_params = StdioServerParameters( # 这里本质是个命令，所以后面就被抛弃了
        command="python",
        args=["05_mcp_stdio_server.py"],
    )

    # 建立标准输入输出连接
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化连接
            await session.initialize()

            # 获取可用工具
            tools = await session.list_tools()
            print(tools)
            print()

            # 调用工具
            call_res = await session.call_tool(
                "add",
                {"a": 1, "b": 2}
            )
            print(call_res)
            print()

            # 获取可用资源
            resources = await session.list_resources()
            print(resources)
            print()

            # 读取资源
            read_res = await session.read_resource(
                "greeting://default"
            )
            print(read_res)
            print()

            # 获取可用提示词
            prompts = await session.list_prompts()
            print(prompts)
            print()

            # 调用提示词
            get_res = await session.get_prompt(
                "greet_user",
                {"name": "Jack"}
            )
            print(get_res)
            print()


asyncio.run(stdio_run())

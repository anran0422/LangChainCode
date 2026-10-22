
# pip install mcp fastapi uvicorn

import contextlib
import uvicorn
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP


# 1. 创建三个独立的 MCP 实例
tool_mcp = FastMCP("tool server")
resource_mcp = FastMCP("resource server")
prompt_mcp = FastMCP("prompt server")


# 2. 注册工具
@tool_mcp.tool()
def add(a: int, b: int) -> int:
    return a + b


# 3. 注册资源
@resource_mcp.resource("greeting://default")
def get_greeting() -> str:
    return "Hello from static resource!"


# 4. 注册提示词
@prompt_mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    styles = {
        "friendly": "写一句友善的问候",
        "formal": "写一句正式的问候",
        "casual": "写一句轻松的问候",
    }
    return f"为{name}{styles.get(style, styles['friendly'])}"


# 5. 设置每个 MCP 服务内部的 HTTP 路径
tool_mcp.settings.streamable_http_path = "/"
resource_mcp.settings.streamable_http_path = "/"
prompt_mcp.settings.streamable_http_path = "/"


# 6. 统一管理三个 MCP 服务的生命周期
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(
            tool_mcp.session_manager.run()
        )
        await stack.enter_async_context(
            resource_mcp.session_manager.run()
        )
        await stack.enter_async_context(
            prompt_mcp.session_manager.run()
        )
        yield


# 7. 创建 FastAPI 应用
app = FastAPI(lifespan=lifespan)


# 8. 将三个 MCP 服务挂载到不同路径
app.mount("/tool", tool_mcp.streamable_http_app())
app.mount("/resource", resource_mcp.streamable_http_app())
app.mount("/prompt", prompt_mcp.streamable_http_app())


# 9. 启动 ASGI 服务器
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

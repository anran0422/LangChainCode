"""
    这个也有上一个代码中的 MCP 就不搞了
    再就是这个核心就是那个 多 Agent 架构，其实我是搞过的
        之前的项目中学过多Agent架构，有哪些而已
"""
import os
import asyncio
import smtplib

from email.mime.text import MIMEText
from email.utils import formataddr
from urllib.parse import urlencode

from langchain.tools import tool
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient


# ==================== 1. 配置大模型 ====================

llm = init_chat_model(
    model="z-ai/glm-4.5-air:free",
    model_provider="openai",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


# ==================== 2. 创建搜索子 Agent ====================

class SearchSubAgent:
    """具有网页搜索和火车票查询功能的子 Agent。"""

    def __init__(self, tools):
        self.agent = create_agent(
            model=llm,
            tools=tools,
            system_prompt=(
                "你是一个搜索助手，可以调用网页搜索和火车票查询工具。"
                "请根据用户需求调用合适的工具，并准确总结查询结果。"
                "如果工具没有返回相关信息，不要编造结果。"
            ),
        )

    async def __call__(self, input: str) -> str:
        result = await self.agent.ainvoke(
            {
                "messages": [
                    {"role": "user", "content": input}
                ]
            }
        )

        return result["messages"][-1].content


# ==================== 3. 创建邮件发送工具 ====================

@tool
async def send_email(to: list[str], subject: str, body: str) -> str:
    """
    发送电子邮件。

    Args:
        to: 收件人邮箱地址列表。
        subject: 邮件主题。
        body: 邮件正文。
    """
    smtp_host = "smtp.qq.com"
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    if not smtp_user or not smtp_pass:
        return "邮件发送失败：未配置 SMTP_USER 或 SMTP_PASS。"

    if not to:
        return "邮件发送失败：收件人列表为空。"

    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = formataddr(("邮件助手", smtp_user))
    msg["To"] = ", ".join(to)
    msg["Subject"] = subject

    try:
        # smtplib 是同步库，放到线程中执行，避免阻塞事件循环。
        await asyncio.to_thread(
            _send_smtp_email,
            smtp_host,
            smtp_user,
            smtp_pass,
            to,
            msg.as_string(),
        )
        return f"邮件发送成功，收件人：{', '.join(to)}"

    except Exception as e:
        return f"邮件发送失败：{type(e).__name__} - {e}"


def _send_smtp_email(
    smtp_host: str,
    smtp_user: str,
    smtp_pass: str,
    recipients: list[str],
    message: str,
):
    """通过 QQ 邮箱 SMTP 发送邮件。"""
    with smtplib.SMTP_SSL(smtp_host, 465, timeout=10) as server:
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, recipients, message)


# ==================== 4. 创建邮件子 Agent ====================

class EmailSubAgent:
    """具有邮件撰写和发送功能的子 Agent。"""

    def __init__(self):
        self.agent = create_agent(
            model=llm,
            tools=[send_email],
            system_prompt=(
                "你是一个邮件助手。"
                "根据用户提供的信息生成合适的邮件主题和正文。"
                "发送邮件前，检查收件人、主题和正文是否完整。"
                "只有用户明确授权发送时，才调用发送邮件工具。"
                "不要声称发送成功，除非工具明确返回成功。"
            ),
        )

    async def __call__(self, input: str) -> str:
        result = await self.agent.ainvoke(
            {
                "messages": [
                    {"role": "user", "content": input}
                ]
            }
        )

        return result["messages"][-1].content


# ==================== 5. 创建子 Agent 实例 ====================

async def create_search_subagent():
    """异步获取 MCP 工具并创建搜索子 Agent。"""
    mcp_client = MultiServerMCPClient(
        {
            "WebSearch": {
                "transport": "sse",
                "url": (
                    "https://dashscope.aliyuncs.com/"
                    "api/v1/mcps/WebSearch/sse"
                ),
                "headers": {
                    "Authorization": (
                        f"Bearer {os.getenv('DASHSCOPE_API_KEY')}"
                    )
                },
            },
            "RailService": {
                "transport": "streamable_http",
                "url": (
                    "https://server.smithery.ai/"
                    "@DeniseLewis200081/rail/mcp"
                    f"?{urlencode({'api_key': os.getenv('SMITHERY_API_KEY')})}"
                ),
            },
        }
    )

    tools = await mcp_client.get_tools()

    print("已加载的搜索 MCP 工具：")
    for item in tools:
        print(f"- {item.name}: {item.description}")

    return SearchSubAgent(tools)


# ==================== 6. 将子 Agent 包装成工具 ====================

@tool
async def search(input: str) -> str:
    """
    调用搜索子 Agent。
    可以搜索网页、查询天气和查询火车票。
    请将用户的查询需求完整传递给子 Agent。
    """
    return await search_subagent(input)


@tool
async def email(input: str) -> str:
    """
    调用邮件子 Agent。
    可以根据用户提供的信息撰写邮件，并在获得明确授权后发送。
    """
    return await email_subagent(input)


# ==================== 7. 创建主管 Agent ====================

supervisor_agent = create_agent(
    model=llm,
    tools=[search, email],
    system_prompt=(
        "你是一个主管 Agent，负责协调搜索子 Agent 和邮件子 Agent。\n"
        "工作流程：\n"
        "1. 用户询问天气时，先调用搜索子 Agent 查询天气。\n"
        "2. 根据天气查询结果判断是否符合用户提出的条件。\n"
        "3. 如果用户要求且条件满足，再查询对应的火车票信息。\n"
        "4. 根据用户明确给出的邮件发送条件，决定是否调用邮件子 Agent。\n"
        "5. 只有天气和车票等必要信息查询完成后，才根据条件决定发送邮件。\n"
        "6. 如果查询失败、结果不明确或条件无法判断，不要编造信息，"
        "也不要擅自发送邮件。\n"
        "7. 最后向用户总结天气、车票查询结果及邮件发送状态。"
    ),
)


# ==================== 8. 主程序 ====================

async def main():
    global search_subagent, email_subagent

    # 在异步事件循环内初始化子 Agent。
    search_subagent = await create_search_subagent()
    email_subagent = EmailSubAgent()

    user_input = (
        "请查询北京明天的天气。如果天气不错，"
        "帮我查询明天上海到北京的车票；"
        "如果天气适合出行，发送邮件给 xxxxxx@qq.com，"
        "告诉他我明天去北京；如果天气不好，"
        "告诉他我明天不去北京。"
        "请根据真实查询结果决定，不要编造天气或车票信息。"
    )

    async for chunk in supervisor_agent.astream(
        {
            "messages": [
                {"role": "user", "content": user_input}
            ]
        },
        stream_mode="updates",
    ):
        print(chunk, end="\n\n")


if __name__ == "__main__":
    asyncio.run(main())

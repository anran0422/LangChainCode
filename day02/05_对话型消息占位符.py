"""
    在格式化过程中插入消息列表（感觉用处不大）
    使用场景：
        Agent 暂存中间步骤，使用 MessagePlaceHolder 负责在特定的位置插入消息列表

    插入消息列表，需要使用 format_messages，format 意思格式化，否则不完整
        看清楚两个方法，一个 from 一个 format
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

template = ChatPromptTemplate.from_messages( # 没有 from_messages 也可以！
    [
        ("system", "你是一个 AI 助手"),
        # ("placeholder", "{conversation}")
        MessagesPlaceholder(variable_name="conversation", optional=True)
        # 两种插入对话列表的方式
    ]
)

prompt = template.format_messages(
    conversation=[
        ("human", "你好"),
        ("ai", "你想让我帮你做些什么？"),
        ("human", "可以帮我画一副画吗，有...."),
        ("ai", "稍等")
    ]
)
print(prompt)
"""
    ChatPromptTemplate 是创建 对话/聊天类型的提示词模板类
    对于之前的 PromptTemplate 适合处理 多轮次、多对话场景
    支持 AI、System、Human 等不同角色的消息类型

    生成/调用 方式：
        format_messages 不带 ** 解包报错
            输出结果直接就是内容
        invoke 传入字典，默认内置**解包
            输出结果带有 messages=[...]
"""
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate(
    [
        ("system", "你是一个 AI 工程师，你的名字是 {name}"),
        ("human", "你好，你能为我做点什么？"),
        ("ai", "我是 AI 工程师，我能帮助你完成很多的事情，比如 {thing}"),
        ("human", "好，那么你开始吧。。。")
    ]
)


prompt = template.format_messages(name="小爱", thing="写代码、画画等")
print(prompt)

print("==============")
arguments = {"name": "小爱", "thing": "写代码、画画等"}
prompt = template.format_messages(**arguments)
print(prompt)

print("==============")

prompt = template.invoke(arguments)
print(prompt)
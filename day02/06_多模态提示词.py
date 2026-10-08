"""
    多模态提示词，
        1. 也是我们在与 AI 对话过程中的一种提示词,所以它属于 ChatPromptTemplate
        2. 多模态对话，要使用多模态的模型
"""
import os
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model(
    model="deepseek-v4-pro",
    model_provider=os.getenv('MODEL_PROVIDER'),
    base_url=os.getenv('DEEPSEEK_BASE_URL'),
    api_key=os.getenv('DEEPSEEK_API_KEY')
)

template = ChatPromptTemplate( # 构造函数
    # 元组类型消息 ("ai", "content")
    # OpenAI 字典聊天格式
    [
        {"role": "system", "content": "你是一个图画专家"},
        {"role": "user", "content": [
            {"type": "text", "text": "请描述一下这张图片"},
            {
                "type": "image_url",
                "image_url": {"url": "{img_url}"}
            }
        ]}
    ]
)

# template = ChatPromptTemplate([
#     ("system", "你是一个图画专家"),
#     (
#         "user",
#         [
#             {"type": "text", "text": "请描述一下这张图片"},
#             {
#                 "type": "image_url",
#                 "image_url": {"url": "{img_url}"}
#             }
#         ]
#     )
# ])



prompt = template.format_messages(
    img_url="xxxx" # 互联网可访问图片即可
)

resp = llm.invoke(prompt)
print(resp)

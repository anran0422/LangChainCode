import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

llm = init_chat_model(
    model=os.getenv('MODEL_NAME'),
    model_provider=os.getenv('MODEL_PROVIDER'),
    base_url=os.getenv('DEEPSEEK_BASE_URL'),
    api_key=os.getenv('DEEPSEEK_API_KEY')
)

messages = [
    {"role": "system", "content": "你是一个数学家"},
    {"role": "user", "content": "请给出勾股定理的公式"}
]

# 流式方法输出
for chunk in  llm.stream(messages):
    # 逐个打印内容，刷新缓冲区以即时显示内容
    print(chunk.content, end="", flush=True)
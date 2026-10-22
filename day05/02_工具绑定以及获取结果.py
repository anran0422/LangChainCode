"""
    工具绑定就是把工具给到 LLM 手中
    获取结果，并不是像之前 LLM 直接输出就能够得到的，而是需要进行手动获取
    解释：
        响应中 additional_kwargs 包含了工具调用的信息，但是还没有调用工具
        只是返回了要调用的工具及参数

    真正执行结果需要查看 tool_calls

    globals() 维护了名字-值的映射
"""
import os
from pydantic import BaseModel, Field
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
load_dotenv()


class DivideSchema(BaseModel):
    a: int = Field(description="被除数")
    b: int = Field(description="除数")


@tool(description="两个数相除2",
      args_schema=DivideSchema)
def divide_number(a, b):
    if b == 0:
        raise ValueError("除数不能为0")
    return a / b


print(f"{divide_number.name=}\n{divide_number.description=}\n{divide_number.args=}")
print("============================")


llm = init_chat_model(
    model=os.getenv('MODEL_NAME'),
    model_provider=os.getenv('MODEL_PROVIDER'),
    base_url=os.getenv('DEEPSEEK_BASE_URL'),
    api_key=os.getenv('DEEPSEEK_API_KEY')
)

# 为 LLM 提供工具
tools = [divide_number]
llm_with_tools = llm.bind_tools(tools)
res = llm_with_tools.invoke("8 除以 2 等于多少")
print(res)
# 下面结果说明使用了自己的工具
# additional_kwargs={'refusal': None, 'reasoning_content':
# 'The user asks: 8 divided by 2. Use the tool.'}

# 手动执行工具
for tool_call in res.tool_calls:
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]
    tool_res = globals()[tool_name].invoke(tool_args) # 执行工具
    print(tool_res)
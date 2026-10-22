"""
    创建工具一共只有两种方式
    1. @tool 装饰器
    2. 工具名 = tool(函数名)
        这里的 """""" 竟然变成了 description
        也可以使用 tool()函数传递 description
    
    创建工具的 入参结构：
    1. 使用 a:int 这种推断类型
    2. 使用 pydantic
    
    最后一个是融合 pydantic 和 tool 装饰器（JAVA中的注解）
"""

from langchain.tools import tool


# ====== 方式1 ======
@tool(
    description="两个整数相加"
)
def add_number(a:int, b:int) -> int:
    return a + b

print(f"{add_number.name=}\n{add_number.description=}\n{add_number.args=}")
print("============================")


# ====== 方式2 ======
def multi_number(a:int, b:int) -> int:
    """两个整数相乘"""
    return a*b

mutiply = tool(multi_number, description="两个整数相乘")

print(f"{mutiply.name=}\n{mutiply.description=}\n{mutiply.args=}")
print("============================")

# 定义函数的入参结构
from pydantic import BaseModel, Field
def divide_number(a, b):
    if b == 0:
        raise ValueError("除数不能为0")
    return a / b

class DivideSchema(BaseModel):
    a: int = Field(description="被除数")
    b: int = Field(description="除数")

divide = tool(divide_number, args_schema=DivideSchema, description="两个数相除")
print(f"{divide.name=}\n{divide.description=}\n{divide.args=}")
print("============================")

@tool(description="两个数相除2",
      args_schema=DivideSchema)
def divide_number2(a, b):
    if b == 0:
        raise ValueError("除数不能为0")
    return a / b
print(f"{divide_number2.name=}\n{divide_number2.description=}\n{divide_number2.args=}")
print("============================")

"""
    from_template 创建提示词模版
    + str.format()
    生成的时候 invoke 也能生成 提示词 prompt 输入是字典
"""
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template("请给我一个关于 "
                                        "{topic} 的 {type} 解释。")

# 第一种调用方式
prompt = template.format(topic="苹果笔记本", type="型号")
print(prompt)

# invoke 调用/ 生成prompt 方式需要 从 StringPromptValue 对象 -> toString
prompt = template.invoke({"topic": "苹果笔记本", "type": "型号"}) # text='请给我一个关于 苹果笔记本 的 型号 解释。'
print(type(prompt)) # <class 'langchain_core.prompt_values.StringPromptValue'>

print(prompt.to_string()) # 请给我一个关于 苹果笔记本 的 型号 解释。
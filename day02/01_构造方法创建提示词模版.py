"""
    这一章都是在去做关于输入输出的格式限制
    关于模型的建造
"""
from langchain_core.prompts import PromptTemplate

template = PromptTemplate(
    template="请评价 {product} 的优缺点，包含 {aspect1}和{aspect2} 两个方面",
    input_variables=["product", "aspect1", "aspect2"]
)

# 使用模版生成提示词
prompt1 = template.format(product="手机", aspect1="续航", aspect2="拍照效果")
prompt2 = template.format(product="笔记本电脑", aspect1="便携性", aspect2="美观")

print(prompt1)
print(prompt2)
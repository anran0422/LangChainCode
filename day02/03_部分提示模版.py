"""
    在生成提示词之前，可以给部分变量赋值
    方式1 ： 构造函数， 指定 partial_variables 参数
    方式2 ： from_template 方法， partial 方法指定默认值
"""

from langchain_core.prompts import PromptTemplate

# 方式1
template = PromptTemplate(
    template="请评价 {product} 的优缺点，包含 {aspect1}和{aspect2} 两个方面",
    input_variables=["product", "aspect1", "aspect2"],
    partial_variables={"product": "苹果"}
)

# 这里可以替换为 invoke
prompt = template.format(aspect1="便携性", aspect2="续航")

print(prompt)

print("===================")
# 方式2
template = PromptTemplate.from_template("请给我一个关于 "
                                        "{topic} 的 {type} 解释。")
partial_template = template.partial(topic="华为手机")

# 这里经过了 partial 方法，不是一步生成的，所以不能使用 invoke
prompt = partial_template.format(type="充电器型号")
print(prompt)

"""
    可以将 prompt 保存为 JSON 或者 yaml 文件，通过读取该文件，获取 prompt
        也方便对 prompt 进行维护和管理
"""
"""
    The function `load_prompt` was deprecated in LangChain 1.2.21 and will be removed in 2.0.0. 
    Use `Use `dumpd`/`dumps` from `langchain_core.load` to serialize prompts 
    and `load`/`loads` to deserialize them.`
    后面，下面的这种写法会被抛弃，写法变化直接给 AI 咨询即可
"""


from langchain_core.prompts import load_prompt

template = load_prompt("./prompt.json", encoding="utf-8")
prompt = template.format(name="小爱", thing="重庆")
print(prompt)


template = load_prompt("./prompt.yaml", encoding="utf-8")
prompt = template.format(name="雪王", thing="蜜雪冰城")
print(prompt)

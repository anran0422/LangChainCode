"""
    在 LangChain 中，直接使用原始 JSON Schema（而非仅依赖 Pydantic/TypedDict 自动转换）

    简而言之，‌Pydantic/TypedDict 提供了开发便利性‌，适合快速原型开发和 Python -centric 的项目；
    而‌原始 JSON Schema 提供了工程严谨性‌。
    在需要‌严格数据校验‌、‌多语言系统集成‌、‌复杂业务规则约束‌或‌长期维护的数据契约‌场景中，
    直接使用原始 JSON Schema 能够消除自动化转换带来的黑盒风险，确保大模型输出的数据不仅“看起来像”结构化数据，
    而且“严格符合”后端系统的硬性要求。
"""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

llm = init_chat_model(
    model=os.getenv("MODEL_NAME"),
    model_provider=os.getenv("MODEL_PROVIDER"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    extra_body={
            "thinking": {
                "type": "disabled"  # 强制关闭思考模式
            }
        }
)

# 【关键修正】
# 1. 根节点必须是 type: "object"
# 2. 你的数组数据应该放在 properties 的某个字段下（例如 "animals"）
# 3. 这样模型才会生成 {"animals": [...]} 这样的参数，而不是空参数
schema = {
    "title": "AnimalResponse",
    "description": "包含动物列表的响应对象",
    "type": "object",
    "properties": {
        "animals": {
            "type": "array",
            "description": "动物与表情列表",
            "items": {
                "type": "object",
                "properties": {
                    "animal": {
                        "type": "string",
                        "description": "动物名称"
                    },
                    "emoji": {
                        "type": "string",
                        "description": "动物的 emoji"
                    }
                },
                "required": ["animal", "emoji"],
                "additionalProperties": False
            }
        }
    },
    "required": ["animals"],
    "additionalProperties": False
}

messages = [
    {"role": "user", "content": "任意生成三种动物，以及他们的 emoji 表情"}
]

# 这个相当于是 system 预设，可以去比较 JsonOutputParser
llm_struct = llm.with_structured_output(schema, method="json_schema", include_raw=True)

res = llm_struct.invoke(messages)

print(res)
print(res["raw"])
print(res["parsed"])
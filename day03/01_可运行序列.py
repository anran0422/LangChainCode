"""
    LCEL
    可运行序列 RunnableSequence ,该类链接多个可运行对象，成链
    chain = RunnableSequence([runnable1, runnable2, runnable3])
"""

import os
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence

load_dotenv()

template = PromptTemplate(
    template="讲一个关于{topic}的笑话",
    input_variables=["topic"]
)

llm = init_chat_model(
    model=os.getenv("MODEL_NAME"),
    model_provider=os.getenv("MODEL_PROVIDER"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY")
)
parser = StrOutputParser()


chain = RunnableSequence(template, llm, parser)
# chain = template | llm | parser


res = chain.invoke({"topic": "人工智能"})

print(res)
"""
    代码的一切是没有任何问题的，只不过可能模型不是本地的出错了
    这里就不下载 HF 的模型了，就这样
"""

import os

from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymilvus import MilvusClient, DataType

load_dotenv()

# ==================== 1. 初始化 Milvus 客户端 ====================

client = MilvusClient(
    uri="./milvus_demo.db"
)

COLLECTION_NAME = "demo_collection"


# ==================== 2. 创建 Schema ====================

def build_schema():
    schema = MilvusClient.create_schema(
        auto_id=True,
        enable_dynamic_field=False
    )

    schema.add_field(
        field_name="id",
        datatype=DataType.INT64,
        is_primary=True
    )

    schema.add_field(
        field_name="vector",
        datatype=DataType.FLOAT_VECTOR,
        dim=768
    )

    schema.add_field(
        field_name="text",
        datatype=DataType.VARCHAR,
        max_length=8192
    )

    schema.add_field(
        field_name="metadata",
        datatype=DataType.JSON
    )

    return schema


# ==================== 3. 创建向量索引 ====================

def build_index():
    index_params = MilvusClient.prepare_index_params()

    index_params.add_index(
        field_name="vector",
        index_type="AUTOINDEX",
        metric_type="COSINE"
    )

    return index_params


# ==================== 4. 创建 Collection ====================

if client.has_collection(collection_name=COLLECTION_NAME):
    client.drop_collection(collection_name=COLLECTION_NAME)

client.create_collection(
    collection_name=COLLECTION_NAME,
    schema=build_schema(),
    index_params=build_index()
)


# ==================== 5. 加载 Markdown 文档 ====================

docs = UnstructuredMarkdownLoader(
    file_path="./导入数据规范.md",
    mode="single"
).load()


# ==================== 6. 文档切分 ====================

splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", "。", "，", "！", "？", ".....", ""],
    chunk_size=400,
    chunk_overlap=50
)

chunks = splitter.split_documents(docs)

if not chunks:
    raise ValueError("没有读取到有效文档内容，请检查 Markdown 文件路径和内容。")


# ==================== 7. 加载云端 Embedding 模型 ====================

hf_token = os.getenv("HF_TOKEN")

if not hf_token:
    raise ValueError("未找到 HF_TOKEN，请检查 .env 文件。")

embedding_model = HuggingFaceEndpointEmbeddings(
    model="BAAI/bge-base-zh-v1.5",
    task="feature-extraction",
    huggingfacehub_api_token=hf_token
)


# ==================== 8. 生成文档向量 ====================

texts = [chunk.page_content for chunk in chunks]

embeddings = embedding_model.embed_documents(texts)

# 检查实际输出维度，避免与 Milvus Schema 不匹配
if len(embeddings[0]) != 768:
    raise ValueError(
        f"Embedding 维度为 {len(embeddings[0])}，"
        "但 Milvus Schema 设置的是 768。"
    )


# ==================== 9. 整理并插入数据 ====================

data = [
    {
        "vector": vector,
        "text": chunk.page_content,
        "metadata": chunk.metadata
    }
    for chunk, vector in zip(chunks, embeddings)
]

insert_result = client.insert(
    collection_name=COLLECTION_NAME,
    data=data
)

print("文档数量：", len(chunks))
print("插入结果：", insert_result)


# ==================== 10. 向量检索 ====================

def retrieval(query, embedding_model, client):
    # BGE 中文检索模型的查询指令前缀
    query_with_instruction = (
        "为这个句子生成表示以用于检索相关文章：" + query
    )

    query_embedding = embedding_model.embed_query(
        query_with_instruction
    )

    results = client.search(
        collection_name=COLLECTION_NAME,
        data=[query_embedding],
        anns_field="vector",
        search_params={
            "metric_type": "COSINE",
            "params": {}
        },
        output_fields=["text", "metadata"],
        limit=3
    )

    return results


# ==================== 11. 执行检索 ====================

context = retrieval(
    "数据规范示例",
    embedding_model,
    client
)

for result_group in context:
    for item in result_group:
        print("相似度：", item["distance"])
        print("文本：", item["entity"]["text"])
        print("元数据：", item["entity"]["metadata"])
        print("-" * 50)

from openai import OpenAI

client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key="sk-xxxxx" # 模拟api-key 去看 .env 文件中
)

completion = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {"role": "user", "content": "将'你好'翻译成意大利语"}
    ],
)

print(completion.choices[0].message.content)
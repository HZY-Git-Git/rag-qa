import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
from dotenv import load_dotenv
from openai import OpenAI
from retrieve import retrieve

load_dotenv()

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com/v1"
)

def answers(question):
    docs,distances = retrieve(question)



    if distances[0]>0.9:
        print("不知道")
    else:
        context="\n\n".join(docs)
        messages=[
            {"role":"system","content":"你是一个客服助手。只根据下面提供的文档内容回答用户问题，不要编造。文档里没有答案就直接说不知道。"},
            {"role":"user","content":f"文档内容：\n{context}\n\n问题:{question}"}
        ]

        response = client.chat.completions.create(model="deepseek-chat",messages=messages)

        answer = response.choices[0].message.content

        return answer

if __name__ == "__main__":
    print(answers("咖啡机怎么清洗"))
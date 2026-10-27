import sys
import sqlite3
import ollama
import numpy as np
from openai import OpenAI

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")
con = sqlite3.connect("campus.db")

rows = con.execute(
    "SELECT id, name, area, category, popular_menu, description, embedding FROM restaurant"
).fetchall()
V = np.stack([np.frombuffer(r[-1], dtype=np.float32) for r in rows])
V = V / np.linalg.norm(V, axis=1, keepdims=True)


def search(question, k=3):
    q = np.array(ollama.embed(model="bge-m3", input=question).embeddings[0])
    q = q / np.linalg.norm(q)
    sims = V @ q
    return [(float(sims[i]), rows[i][:-1]) for i in np.argsort(-sims)[:k]]


def answer(question):
    found = search(question)
    context = "\n".join(
        f"- {name} ({area}, {category}): 대표 메뉴 {menu}. {desc}"
        for _, (id_, name, area, category, menu, desc) in found
    )
    prompt = f"""아래 식당 목록만 근거로 질문에 답한다. 목록에 없는 내용은 "자료에 없습니다"라고 답한다. 답은 두 문장 이내로 쓴다.

식당 목록:
{context}

질문: {question}"""
    r = client.chat.completions.create(model="gemma4", temperature=0,
                                       messages=[{"role": "user", "content": prompt}])
    return found, r.choices[0].message.content.strip()


questions = sys.argv[1:] or [
    "삼송동에서 들깨삼계탕 먹을 수 있는 곳은?",
    "행신동에 파스타나 브런치를 먹을 식당이 있어?",
    "행주산성에서 오리백숙 먹을 만한 곳은?",
    "원흥동에서 고기짬뽕 파는 식당은?",
    "덕양구에서 회를 먹을 수 있는 곳은?",
]
for q in questions:
    found, a = answer(q)
    print("Q:", q)
    for s, (id_, name, *_rest) in found:
        print(f"   {s:.3f} {name}")
    print("   답:", a)
    print()
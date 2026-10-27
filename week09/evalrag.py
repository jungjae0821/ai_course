import sqlite3
import ollama
import numpy as np

con = sqlite3.connect("campus.db")
rows = con.execute("SELECT id, name, embedding FROM restaurant").fetchall()
names = [r[1] for r in rows]
V = np.stack([np.frombuffer(r[2], dtype=np.float32) for r in rows])
V = V / np.linalg.norm(V, axis=1, keepdims=True)

# (질문, 정답 식당 이름)
TESTS = [
    ("삼송동에서 들깨삼계탕 먹고 싶어", "예담들깨삼계탕"),
    ("행신동에서 파스타 먹을 곳", "선식당"),
    ("행주산성 오리백숙", "장수촌"),
    ("원흥에서 고기짬뽕 파는 곳", "방울식당"),
    ("삼송역 근처 쌀국수 식당", "포메인 고양삼송점"),
    ("원흥역에서 삼겹살", "고반식당 원흥역점"),
    ("행주산성에서 메기매운탕", "유림식당"),
    ("스타필드 고양에서 중식", "JS가든 웍 스타필드 고양점"),
]

hit1 = hit3 = 0
for q, want in TESTS:
    qv = np.array(ollama.embed(model="bge-m3", input=q).embeddings[0])
    qv = qv / np.linalg.norm(qv)
    top = [names[i] for i in np.argsort(-(V @ qv))[:3]]
    ok1, ok3 = top[0] == want, want in top
    hit1 += ok1
    hit3 += ok3
    print("O" if ok1 else ("△" if ok3 else "X"), q, "->", top[0], "" if ok1 else f"(정답 {want}, 3위 안 {ok3})")
print(f"\n1위 적중 {hit1}/{len(TESTS)}, 3위 안 적중 {hit3}/{len(TESTS)}")
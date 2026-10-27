import sqlite3
import ollama
import numpy as np

con = sqlite3.connect("campus.db")
columns = [c[1] for c in con.execute("PRAGMA table_info(restaurant)")]
if "embedding" not in columns:
    con.execute("ALTER TABLE restaurant ADD COLUMN embedding BLOB")


def row_to_text(name, area, category, popular_menu, description):
    return f"{name}. {area}. {category}. 대표 메뉴: {popular_menu}. {description}"


rows = con.execute("SELECT id, name, area, category, popular_menu, description FROM restaurant").fetchall()
for i, (id_, *fields) in enumerate(rows):
    text = row_to_text(*fields)
    v = np.array(ollama.embed(model="bge-m3", input=text).embeddings[0], dtype=np.float32)
    con.execute("UPDATE restaurant SET embedding = ? WHERE id = ?", (v.tobytes(), id_))
    print(f"\r{i + 1}/{len(rows)} {text[:40]}", end="   ")
con.commit()
print("\n완료")
print("예:", row_to_text(*rows[0][1:]))
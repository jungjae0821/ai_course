import sqlite3

con = sqlite3.connect("campus.db")
for kw in ["쭈꾸미", "삼송", "행주산성", "한우"]:
    rows = con.execute(
        """SELECT name FROM restaurant
        WHERE name LIKE ? OR area LIKE ? OR category LIKE ?
        OR popular_menu LIKE ? OR description LIKE ?""",
        (f"%{kw}%",) * 5,
    ).fetchall()
    print(kw, [r[0] for r in rows])
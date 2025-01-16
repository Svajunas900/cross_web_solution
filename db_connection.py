import sqlite3

conn = sqlite3.connect("django_comp_db.sqlite3")
cursor = conn.cursor()
print(cursor.execute("SELECT * FROM app1_userprofile").fetchall())
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
import sqlite3

conn = sqlite3.connect('personal_data.db')
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS People (name TEXT, age INTEGER)')
cur.execute('INSERT INTO People (name, age) VALUES (?, ?)', ('Jose', 20))
conn.commit()

for row in cur.execute('SELECT * FROM People'):
    print(row)

conn.close()
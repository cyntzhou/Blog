import sqlite3

#create.py creates the tables. populate.py adds the stuff to the tables.

conn = sqlite3.connect("test.db")
c = conn.cursor()

q = "CREATE TABLE posts(title text UNIQUE, post text)"

result = c.execute(q)

q = "CREATE TABLE comments(title text, comment text, name text)"

c.execute(q)

conn.commit()

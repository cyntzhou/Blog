import sqlite3
import csv

#create.py creates the tables. populate.py adds the stuff to the tables.

conn = sqlite3.connect("test.db")

c = conn.cursor()

BASE="insert into posts values('%(title)s','%(post)s')"
for line in csv.DictReader(open("posts.csv")):
    q = BASE%line
    print q
    c.execute(q)

BASE="insert into comments values('%(title)s','%(comment)s','%(name)s')"
for line in csv.DictReader(open("comments.csv")):
    q = BASE%line
    print q
    c.execute(q)

conn.commit()

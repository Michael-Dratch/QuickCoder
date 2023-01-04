import sqlite3

conn = sqlite3.connect('quickcode.db')

c = conn.cursor()

# c.execute("""CREATE TABLE code (
#                 id integer,
#                 name text,
#                 color text
#                 ) """)

c.execute("""INSERT INTO code VALUES (2, 'Negative', '#FF0000')""")

c.execute("""SELECT * FROM code""")
print(c.fetchall())

conn.commit()
conn.close()

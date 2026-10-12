import sqlite3
connect = sqlite3.connect('anitracker/test.db')
cursor = connect.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS anime (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        rating INTEGER
    )
""")
## no lo se XD
cursor.execute(("INSERT INTO anime (title, rating) VALUES (?, ?)"), ("ONE PIECE", 2))
cursor.execute(("INSERT INTO anime (title, rating) VALUES (?, ?)"), ("NARUTO", 1))
cursor.execute(("INSERT INTO anime (title, rating) VALUES (?, ?)"), ("RE:ZERO", 10))
connect.commit()


def read():
    for row in cursor.execute("SELECT * FROM anime"):
        print(row)
def testidk():
    cursor.execute("SELECT * FROM anime WHERE rating > ?", (5,))
    print(cursor.fetchall())


def clear():
    cursor.execute("DELETE FROM anime")
    connect.commit()
def update_rating(anime_id, new_rating):
    cursor.execute("UPDATE anime SET rating = ? WHERE id = ?", (new_rating, anime_id))
    connect.commit()
update_rating(1, 0)
read()
def delete(anime_id):
    cursor.execute("DELETE FROM anime WHERE id = ?", (anime_id,))
    connect.commit()
def sorted_by_rating():
    cursor.execute("SELECT title, rating FROM anime WHERE rating IS NOT NULL ORDER BY rating DESC")
    for row in cursor.fetchall():
        print(row)
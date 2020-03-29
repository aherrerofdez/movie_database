import sqlite3


class Back(object):
    def __init__(self):
        db = sqlite3.connect("movies.db")
        cur = db.cursor()

        # Create Table
        cur.execute("create table if not exists movies (id integer primary key, title varchar(20), year integer, "
                    "director varchar(20), lead varchar(20))")

        db.commit()
        db.close()

    @staticmethod
    def add_to_db(title="", year=1890, director="", lead=""):
        db = sqlite3.connect("movies.db")
        cur = db.cursor()
        cur.execute("insert into movies values(NULL, ?, ?, ?, ?)", (title, year, director, lead))
        db.commit()
        db.close()

    @staticmethod
    def get_all():
        db = sqlite3.connect("movies.db")
        cur = db.cursor()
        cur.execute("select * from movies")
        rows = cur.fetchall()
        db.close()
        return rows


# Debug the BackEnd
if __name__ == "__main__":
    bk = Back()
    bk.add_to_db("Star Wars", 1977, "George Lucas", "Mark Hamill")

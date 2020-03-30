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

    def add_to_db(self, title="", year=1890, director="", lead=""):
        db = sqlite3.connect("movies.db")
        cur = db.cursor()
        cur.execute("insert into movies values(NULL, ?, ?, ?, ?)", (title, year, director, lead))
        db.commit()
        db.close()

    def del_from_db(self, index):
        db = sqlite3.connect("movies.db")
        cur = db.cursor()
        cur.execute("delete from movies where id=?", (index, ))
        db.commit()
        db.close()

    def update_db(self, title="", year=1890, director="", lead="", index=0):
        db = sqlite3.connect("movies.db")
        cur = db.cursor()
        cur.execute("update movies set title=?, year=?, director=?, lead=? where id=?",
                    (title, year, director, lead, index))
        db.commit()
        db.close()

    def get_all(self):
        db = sqlite3.connect("movies.db")
        cur = db.cursor()
        cur.execute("select * from movies")
        rows = cur.fetchall()
        db.close()
        return rows

    def search_db(self, title, year, director, lead):
        # Add wildcards
        title = "%" + title + "%"
        director = "%" + director + "%"
        lead = "%" + lead + "%"

        db = sqlite3.connect("movies.db")
        cur = db.cursor()

        if year != "":
            cur.execute("select * from movies where title like ? and year=? and director like ? and lead like ?",
                        (title, year, director, lead))
        else:
            cur.execute("select * from movies where title like ? and director like ? and lead like ?",
                        (title, director, lead))

        rows = cur.fetchall()
        db.close()
        return rows


# Debug the BackEnd
if __name__ == "__main__":
    bk = Back()
    bk.add_to_db("Star Wars", 1977, "George Lucas", "Mark Hamill")

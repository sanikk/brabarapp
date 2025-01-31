from sqlite3 import Row, connect


def get_connection():
    con = connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = Row
    return con


def execute(sql, params={}):
    with get_connection() as con:
        result = con.execute(sql, params)
        con.commit()
        return result.lastrowid


def executemany(sql, params={}):
    with get_connection() as con:
        con.executemany(sql, params)
        con.commit()


def query(sql, params={}):
    with get_connection() as con:
        result = con.execute(sql, params).fetchall()
        return result

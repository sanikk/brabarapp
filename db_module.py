from db_connection import execute, query


def get_last_buffets(amount: int = 5):
    sql = """SELECT b.id, b.name, r.name as restaurant_name FROM buffets b JOIN restaurants r ON b.restaurant_id = r.id WHERE b.active = 1 ORDER BY b.last_modified LIMIT :limit"""
    return query(sql, {"limit": amount}).fetchall()


def get_buffets_by_account_id(account_id: int):
    sql = """SELECT b.* FROM buffets b JOIN restaurants r ON b.restaurant_id = r.id WHERE b.active=1 AND r.account_id=:account_id"""
    return query(sql, {"account_id": account_id}).fetchall()


def get_single_buffet(buffet_id):
    sql = """SELECT
            b.*, r.name AS restaurant_name,

            json_group_array(
                json_object(
                    'weekday_number', oh.weekday_number,
                    'start_time', oh.buffet_open,
                    'end_time', oh.buffet_close
                )
            ) AS opening_hours
            FROM buffets b
            JOIN restaurants r ON b.restaurant_id = r.id
            LEFT JOIN buffet_opening_hours oh ON b.id = oh.buffet_id
            WHERE b.id = :buffet_id
            GROUP BY b.id;"""
    return query(sql, {"buffet_id": buffet_id}).fetchone()


def get_last_events(amount: int = 5):
    sql = """SELECT e.id, e.name, e.restaurant_id, e.start_time, r.name AS restaurant_name FROM events e JOIN restaurants r ON e.restaurant_id = r.id WHERE e.active = 1 ORDER BY e.last_modified LIMIT :limit"""
    return query(sql, {"limit": amount}).fetchall()


def get_events_by_account_id(account_id: int):
    sql = """SELECT e.* FROM events e WHERE active=1 AND account_id=:account_id"""
    return query(sql, {"account_id": account_id}).fetchall()


def get_last_ratings(amount: int = 5):
    sql = """SELECT ra.*, re.name as restaurant_name, a.firstname as account_name FROM ratings ra JOIN restaurants re ON ra.restaurant_id = re.id JOIN accounts a ON ra.account_id = a.id WHERE ra.active = 1 ORDER BY ra.last_modified LIMIT :limit"""
    return query(sql, {"limit": amount}).fetchall()


def get_ratings_by_account_id(account_id: int):
    sql = """SELECT r.* FROM ratings r WHERE active=1 AND account_id=:account_id"""
    return query(sql, {"account_id": account_id}).fetchall()


def get_buffet_opening_hours(buffet_id: int):
    sql = """SELECT * FROM buffet_opening_hours WHERE buffet_id = :buffet_id ORDER BY weekday_number"""
    return query(sql, {"buffet_id": buffet_id}).fetchall()

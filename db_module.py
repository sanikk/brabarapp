from db_connection import execute, query


def get_last_restaurants(amount: int = 5):
    sql = "SELECT id, name,address FROM restaurants WHERE active = 1 ORDER BY last_modified LIMIT :limit"
    return query(sql, {"limit": amount})


def get_single_restaurant(restaurant_id: int):
    sql = """SELECT * FROM restaurants WHERE id = :restaurant_id"""
    return query(sql, {"restaurant_id": restaurant_id})


def get_last_logged_in_accounts(amount: int = 5):
    sql = """SELECT id, firstname, lastname FROM accounts WHERE active = 1 ORDER BY last_logged_in LIMIT :limit"""
    return query(sql, {"limit": amount})


def get_last_buffets(amount: int = 5):
    sql = """SELECT b.id, b.name, r.name as restaurant_name FROM buffets b JOIN restaurants r ON b.restaurant_id = r.id WHERE b.active = 1 ORDER BY b.last_modified LIMIT :limit"""
    return query(sql, {"limit": amount})


def get_single_buffet(buffet_id):
    sql = """SELECT
            b.*,
            json_group_array(
                json_object(
                    'weekday_number', oh.weekday_number,
                    'start_time', oh.start_time,
                    'end_time', oh.end_time
                )
            ) AS opening_hours
            FROM buffets b
            LEFT JOIN buffet_opening_hours oh ON b.id = oh.buffet_id
            WHERE b.id = :buffet_id
            GROUP BY b.id;"""

    # sql = """SELECT * FROM buffets WHERE active = 1 AND id=:buffet_id"""
    #     sql = """SELECT b.id, b.name, b.price, b.description, b.restaurant_id, b.last_modified, r.name as restaurant_name, r.account_id
    #             FROM buffets b JOIN restaurants r ON b.restaurant_id = r.id
    #             WHERE b.id = :buffet_id"""
    return query(sql, {"buffet_id": buffet_id})


def get_last_events(amount: int = 5):
    sql = """SELECT e.id, e.name, e.restaurant_id, e.start_time, r.name AS restaurant_name FROM events e JOIN restaurants r ON e.restaurant_id = r.id WHERE e.active = 1 ORDER BY e.last_modified LIMIT :limit"""
    return query(sql, {"limit": amount})


def get_last_ratings(amount: int = 5):
    sql = """SELECT ra.*, re.name as restaurant_name, a.firstname as account_name FROM ratings ra JOIN restaurants re ON ra.restaurant_id = re.id JOIN accounts a ON ra.account_id = a.id WHERE ra.active = 1 ORDER BY ra.last_modified LIMIT :limit"""
    return query(sql, {"limit": amount})


def get_buffet_opening_hours(buffet_id: int):
    sql = """SELECT * FROM buffet_opening_hours WHERE buffet_id = :buffet_id ORDER BY weekday_number"""
    return query(sql, {"buffet_id": buffet_id})


def get_restaurant_opening_hours(restaurant_id: int):
    sql = """SELECT * FROM restaurant_opening_hours WHERE restaurant_id = :restaurant_id ORDER BY weekday_number"""
    return query(sql, {"restaurant_id": restaurant_id})


def create_user(
    username: str,
    password_hash: str,
    email: str,
    billing_info: str,
    firstname: str,
    lastname: str,
    description: str,
):
    if not (username and password_hash):
        return None
    sql = """INSERT INTO accounts (active, username, password, email, billing_info, firstname, lastname, description) \
            VALUES (1, :username, :password, :email, :billing_info, :firstname, :lastname, :description)"""
    execute(
        sql,
        {
            "username": username,
            "password": password_hash,
            "email": email,
            "billing_info": billing_info,
            "firstname": firstname,
            "lastname": lastname,
            "description": description,
        },
    )

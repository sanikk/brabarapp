from db_connection import execute, query


def get_last_restaurants(amount: int = 5):
    sql = "SELECT id, name,address FROM restaurants WHERE active = 1 ORDER BY last_modified LIMIT :limit"
    return query(sql, {"limit": amount})


def get_last_logged_in_accounts(amount: int = 5):
    sql = """SELECT id, firstname, lastname FROM accounts WHERE active = 1 ORDER BY last_logged_in LIMIT :limit"""
    return query(sql, {"limit": amount})


def get_last_buffets(amount: int = 5):
    sql = """SELECT id, name FROM buffets WHERE active = 1 ORDER BY last_modified LIMIT :limit"""
    return query(sql, {"limit": amount})


def get_last_events(amount: int = 5):
    sql = """SELECT id, name FROM events WHERE active = 1 ORDER BY last_modified LIMIT :limit"""
    return query(sql, {"limit": amount})


def get_last_ratings(amount: int = 5):
    sql = (
        """SELECT * FROM ratings WHERE active = 1 ORDER BY last_modified LIMIT :limit"""
    )
    return query(sql, {"limit": amount})


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

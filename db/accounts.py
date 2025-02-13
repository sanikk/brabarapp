from db_connection import execute, query
from werkzeug.security import check_password_hash


def get_last_logged_in_accounts(amount: int = 5):
    sql = """SELECT id, firstname, lastname FROM accounts WHERE active = 1 ORDER BY last_logged_in LIMIT :limit"""
    return query(sql, {"limit": amount}).fetchall()


def get_single_account_private(account_id: int):
    sql = """SELECT id, posted_on, last_logged_in, username, email, billing_info, firstname, lastname, description
            FROM accounts 
            WHERE active = 1 AND id=:account_id"""
    return query(sql, {"account_id": account_id}).fetchone()


def get_single_account_public(account_id: int):
    sql = """SELECT id, posted_on, last_logged_in, username, description
            FROM accounts 
            WHERE active = 1 AND id=:account_id"""
    return query(sql, {"account_id": account_id}).fetchone()


def check_username_and_password(username, password):
    sql = """SELECT id,username,password FROM accounts WHERE username=:username AND active = 1"""
    res = query(sql, {"username": username}).fetchone()
    if res:
        if check_password_hash(res["password"], password):
            return res["id"], res["username"]
    return None


def create_new_account(
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

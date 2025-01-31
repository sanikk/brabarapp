from flask import render_template
from app import app
from db_module import get_last_restaurants, get_last_logged_in_accounts


@app.route("/")
def index():
    accounts = get_last_logged_in_accounts()
    restaurants = get_last_restaurants()
    return render_template("index.html", restaurants=restaurants, accounts=accounts)


@app.route("/accounts")
def accounts_page():
    accounts = get_last_logged_in_accounts(20)
    return render_template("accounts_list.html", accounts=accounts)

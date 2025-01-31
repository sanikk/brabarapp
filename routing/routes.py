from flask import render_template
from app import app
from db_module import (
    get_last_restaurants,
    get_last_logged_in_accounts,
    get_last_events,
    get_last_buffets,
    get_last_ratings,
)


@app.route("/")
def index():
    accounts = get_last_logged_in_accounts()
    restaurants = get_last_restaurants()
    events = get_last_events()
    buffets = get_last_buffets()
    ratings = get_last_ratings()
    return render_template(
        "index.html",
        restaurants=restaurants,
        accounts=accounts,
        events=events,
        buffets=buffets,
        ratings=ratings,
    )


@app.route("/accounts")
def accounts_page():
    accounts = get_last_logged_in_accounts(20)
    return render_template("accounts_list.html", accounts=accounts)

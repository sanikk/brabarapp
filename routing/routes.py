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


@app.route("/events")
def events_page():
    events = get_last_events(20)
    return render_template("events_list.html", events=events)


@app.route("/restaurants")
def restaurants_page():
    restaurants = get_last_restaurants(20)
    return render_template("restaurants_list.html", restaurants=restaurants)


@app.route("/buffets")
def buffets_page():
    buffets = get_last_buffets(20)
    return render_template("buffets_list.html", buffets=buffets)


@app.route("/ratings")
def ratings_page():
    ratings = get_last_ratings(20)
    return render_template("ratings_list.html", ratings=ratings)

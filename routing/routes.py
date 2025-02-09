from flask import render_template, redirect
from app import app
from db_module import (
    get_last_restaurants,
    get_last_logged_in_accounts,
    get_last_events,
    get_last_buffets,
    get_single_buffet,
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


@app.route("/restaurants/new")
def new_restaurant_form():
    return render_template("restaurants_new.html", form_data={})


@app.route("/buffets")
def buffets_page():
    buffets = get_last_buffets(20)
    return render_template("buffets_list.html", buffets=buffets)


@app.route("/buffets/<int:buffet_id>")
def single_buffet_page(buffet_id: int):
    buffet = get_single_buffet(buffet_id)
    print(f"{buffet=}")
    if not buffet:
        return redirect("/buffets")
    return render_template("buffets_single.html", buffet=buffet[0])


@app.route("/ratings")
def ratings_page():
    ratings = get_last_ratings(20)
    return render_template("ratings_list.html", ratings=ratings)

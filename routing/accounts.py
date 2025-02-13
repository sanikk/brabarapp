from app import app
from db_module import (
    get_events_by_account_id,
    get_ratings_by_account_id,
    get_buffets_by_account_id,
)
from db.accounts import (
    get_last_logged_in_accounts,
    check_username_and_password,
    get_single_account_private,
    get_single_account_public,
)
from db.restaurants import get_restaurants_by_account_id
from flask import session, render_template, redirect, request, flash


@app.route("/accounts")
def accounts_page():
    accounts = get_last_logged_in_accounts(20)
    return render_template("accounts_list.html", accounts=accounts)


@app.route("/accounts/<int:account_id>")
def single_account_page(account_id: int):
    account = None
    if session["user_id"] == account_id:
        account = get_single_account_private(account_id)
    else:
        account = get_single_account_public(account_id)

    restaurants = get_restaurants_by_account_id(account_id)
    events = get_events_by_account_id(account_id)
    ratings = get_ratings_by_account_id(account_id)
    buffets = get_buffets_by_account_id(account_id)
    return render_template(
        "accounts_single.html",
        account=account,
        restaurants=restaurants,
        events=events,
        ratings=ratings,
        buffets=buffets,
    )


@app.route("/accounts/login", methods=["POST"])
def user_login():
    username = request.form["username"]
    password = request.form["password"]
    ret = check_username_and_password(username, password)
    if not ret:
        flash("Error: Login failed.")
        return redirect(request.referrer or "/")
    session["user_id"], session["screenname"] = ret
    flash("Success: Login was succesful.")
    return redirect(request.referrer or f"/accounts/{ret}")


@app.route("/accounts/register")
def user_registration():
    return render_template("accounts_new.html", form_data={})


@app.route("/accounts/logout")
def user_logout():
    session.clear()
    return redirect(request.referrer or "/")

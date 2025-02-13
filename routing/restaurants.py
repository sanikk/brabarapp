from app import app
from db.accounts import get_single_account_public
from db.restaurants import (
    get_last_restaurants,
    get_single_restaurant,
    get_restaurant_by_name,
    get_restaurant_opening_hours,
    create_new_restaurant,
    create_restaurant_opening_hours,
)

from flask import render_template, request, flash, redirect, session
from calendar import day_name


@app.route("/restaurants")
def restaurants_page():
    restaurants = get_last_restaurants(20)
    return render_template("restaurants_list.html", restaurants=restaurants)


@app.route("/restaurants/new")
def new_restaurant_form():
    return render_template("restaurants_new.html", form_data={})


@app.route("/restaurants/create", methods=["POST"])
def new_restaurant_endpoint():
    restaurant_data = {
        field: request.form[field] for field in ["name", "address", "description"]
    }
    if "user_id" in session:
        restaurant_data["account_id"] = session["user_id"]
        opening_hours = {
            day.lower() + suff: request.form[day.lower() + suff]
            for day in day_name
            for suff in ["start", "end"]
        }
        if validate_restaurant_data(restaurant_data):
            ret = create_new_restaurant(restaurant_data)
            if validate_opening_hours(opening_hours):
                create_restaurant_opening_hours(opening_hours)
            else:
                flash("Error: invalid opening hours")
            if ret:
                return redirect(f"/restaurants/{ret}")
    flash("Error: please login first.")
    return render_template("restaurants_new.html", form_data=request.form)


@app.route("/restaurants/<int:restaurant_id>")
def single_restaurant_page(restaurant_id: int):
    restaurant = get_single_restaurant(restaurant_id)
    if not restaurant:
        flash("Error: can't access restaurant with that id")
        return redirect("/restaurants")
    opening_hours = {
        key: (open, close)
        for key, open, close in get_restaurant_opening_hours(restaurant_id)
    }
    return render_template(
        "restaurants_single.html", restaurant=restaurant, opening_hours=opening_hours
    )


@app.route("/restaurants/edit/<int:restaurant_id>")
def edit_restaurant_form(restaurant_id: int):
    restaurant = get_single_restaurant(restaurant_id)
    if not restaurant:
        flash("Error: unknown restaurant_id")
        return redirect("/restaurants")
    opening_hours = {
        key: (open, close)
        for key, open, close in get_restaurant_opening_hours(restaurant_id)
    }
    print(opening_hours)
    return render_template(
        "restaurants_edit.html", restaurant=restaurant, oh=opening_hours, form_data={}
    )


@app.route("/restaurants/update", methods=["POST"])
def edit_restaurant_endpoint():
    restaurant_data = {
        field: request.form[field] for field in ["id", "name", "address", "description"]
    }
    opening_hours = {
        day.lower() + suff: request.form[day.lower() + suff]
        for day in day_name
        for suff in ["start", "end"]
    }
    if validate_restaurant_data(restaurant_data) and validate_opening_hours(
        opening_hours
    ):
        ret = create_new_restaurant(restaurant_data)
        create_restaurant_opening_hours(opening_hours)
        return redirect(f"/restaurants/{ret}")
    if "id" in restaurant_data:
        restaurant = get_single_restaurant(restaurant_data["id"])
        if (
            "account_id" in restaurant
            and restaurant["account_id"] == session["user_id"]
        ):

            return render_template(
                "restaurants_edit.html", form_data=request.form, restaurant=restaurant
            )
    flash("Error: there was a problem with edit access.")
    return redirect("/restaurants")


def validate_restaurant_data(restaurant_data):
    valid = True
    if "name" not in restaurant_data or not 3 <= len(restaurant_data["name"]) <= 24:
        flash("Error: restaurant name should be between 3 and 24 characters long.")
        valid = False
    if "name" in restaurant_data and get_restaurant_by_name(restaurant_data["name"]):
        flash(
            "Error: a restaurant with that name already exists. Name should be unique in the area."
        )
        valid = False
    if (
        "address" not in restaurant_data
        or not 3 <= len(restaurant_data["address"]) <= 36
    ):
        flash("Error: restaurant address should be between 3 and 36 characters long.")
        valid = False
    if (
        "description" not in restaurant_data
        or not 3 <= len(restaurant_data["description"]) < 501
    ):
        flash(
            "Error: restaurant description should be between 3 and 500 characters long."
        )
        valid = False
    if "account_id" not in restaurant_data or not get_single_account_public(
        restaurant_data["account_id"]
    ):
        flash("Error: please login with a valid user account")
        valid = False
    return valid


def validate_opening_hours(opening_hours):
    # validate opening_hours={'mondaystart': '', 'mondayend': '', 'tuesdaystart': '', 'tuesdayend': '', 'wednesdaystart': '', 'wednesdayend': '', 'thursdaystart': '14:01', 'thursdayend': '14:02', 'fridaystart': '', 'fridayend': '', 'saturdaystart': '', 'saturdayend': '', 'sundaystart': '', 'sundayend': ''}
    print(f"validate {opening_hours=}")
    return True

from flask import render_template
from app import app
from db_module import get_last_restaurants


@app.route("/")
def index():
    restaurants = get_last_restaurants()
    return render_template("index.html", restaurants=restaurants)

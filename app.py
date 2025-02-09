from config import FLASK_SECRET_KEY
from markupsafe import Markup

from flask import Flask
from calendar import day_name

app = Flask(__name__)
if not FLASK_SECRET_KEY:
    raise RuntimeError("Please check your config file and its FLASK_SECRET_KEY.")
app.secret_key = FLASK_SECRET_KEY


@app.context_processor
def inject_weekdays():
    return {"weekdays": day_name}


@app.template_filter("output_rating_stars")
def output_rating_stars(rating: int, size: int = 30):
    star_icon = f'<img src="/static/icons8-star-50.png" alt="Star" style="width:{size}px;height:{size}px;" />'
    return Markup(star_icon * rating)


@app.template_filter("zip")
def zip_filter(a, b):
    return zip(a, b)


import routing.routes

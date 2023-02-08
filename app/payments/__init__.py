from flask import Blueprint

from . import views

payment_blueprint = Blueprint("payment", __name__)

payment_blueprint.add_url_rule(
    "/payment/stkcallback",
    view_func=views.StkCallback.as_view("stkcallback")
)
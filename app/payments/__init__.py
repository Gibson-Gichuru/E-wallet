from flask import Blueprint

from . import views

payment_blueprint = Blueprint("payment", __name__)

payment_blueprint.add_url_rule(
    "/stkcallback",
    view_func=views.StkCallback.as_view("stkcallback")
)

payment_blueprint.add_url_rule(
    "b2c/validation",
    view_func=views.B2CValidate.as_view("b2c_validate")
)

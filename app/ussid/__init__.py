from flask import Blueprint

from . import views

ussid_blueprint = Blueprint("ussid", __name__)

ussid_blueprint.add_url_rule(
    "callback",
    view_func=views.UssidCallback.as_view("ussid")
)

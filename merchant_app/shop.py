from flask import Blueprint
from flask import render_template
from flask import url_for
from flask import current_app

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/')
def shop():
    template_data = dict(
        item_url=url_for(".shop", _external=True),
        item_thumbnail_url=url_for("static", filename='item.png', _external=True),
        user_confirmation_url=url_for(".user_confirm", _external=True),
        sku = "ACME-SLR-NG-01",
        display_name = "Acme SLR-NG",
        unit_price = "15.00"
    )

    if current_app.config["INJECT_CHECKOUT_NOTIFICATION"]:
        template_data['checkout_notification_url'] = url_for("webhooks.affirm_checkout_notification", _external=True)
    return render_template("index.html", **template_data)

@shop_bp.route("confirm")
def user_confirm():
    return "order confirmed"


import requests
import json
import flask
from flask import abort
from flask import url_for
import pprint
import urlparse
from uuid import uuid4


## Affirm Charges Rest API

def capture_charge(charge_id, amount):
    capture_charge_url = "/".join([
        app.config['AFFIRM']['API_URL'],
        "charges",
        charge_id,
        "capture"
    ])
    return requests.post(capture_charge_url,
                         data=json.dumps({
                             "amount": amount,
                         }),
                         headers={"Content-Type": "application/json"},
                         auth=(app.config["AFFIRM"]["PUBLIC_API_KEY"],
                               app.config["AFFIRM"]["SECRET_API_KEY"]))


def void_charge(charge_id):
    void_charge_url = "/".join([
        app.config['AFFIRM']['API_URL'],
        "charges",
        charge_id,
        "void"
    ])
    return requests.post(void_charge_url,
                         auth=(app.config["AFFIRM"]["PUBLIC_API_KEY"],
                               app.config["AFFIRM"]["SECRET_API_KEY"]))


def refund_charge(charge_id, amount):
    void_charge_url = "/".join([
        app.config['AFFIRM']['API_URL'],
        "charges",
        charge_id,
        "refund"
    ])
    return requests.post(void_charge_url,
                         data=json.dumps({
                             "amount": amount
                         }),
                         headers={"Content-Type": "application/json"},
                         auth=(app.config["AFFIRM"]["PUBLIC_API_KEY"],
                               app.config["AFFIRM"]["SECRET_API_KEY"]))


## Commerce App Example

app = flask.Flask(__name__)


@app.route("/")
def shopping_item_page():
    """
    The item page
    """

    # this gets turned into JSON and used to initialize the affirm checkout
    affirm_checkout_data = {

        "currency": "USD",

        "merchant": {
            "public_api_key": app.config['AFFIRM']['PUBLIC_API_KEY'],
            "user_cancel_url": url_for(".shopping_item_page", _external=True),
            "user_confirmation_url": url_for(".user_confirm_page", _external=True),
            "user_confirmation_url_action": "POST",
        },

        "items": [
            {
                "sku": "ACME-SLR-NG-01",
                "item_url": url_for(".shopping_item_page", _external=True),
                "item_image_url": url_for(".static", filename="item.png", _external=True),
                "display_name": "Acme SLR-NG",
                "unit_price": 1500,
                "qty": 1
            }
        ],
    }

    if app.config["INJECT_CHECKOUT_AMENDMENT_URL"]:
        affirm_checkout_data["merchant"]["checkout_amendment_url"] = url_for(
            ".affirm_checkout_amendment", _external=True)

    template_data = dict(
        affirm_checkout=affirm_checkout_data
    )

    return flask.render_template("index.html", **template_data)


@app.route("/user_confirm", methods=["POST"])
def user_confirm_page():
    """
    The page to render after the user completes checkout. Typically this will
    display a confirmation message to the user.
    """
    charge_id = flask.request.form['charge_id']
    return "Order confirmed: %s" % charge_id


@app.route("/checkout_amendment", methods=["POST"])
def affirm_checkout_amendment():
    """
    The webhook that is called by Affirm after the user begins checkout.
    This webhook should return information to Affirm about the order being
    placed.
    """
    print "Checkout Notification Callback:"
    pprint.pprint(flask.request.json)

    # item sku and unit_price should be checked to ensure consistency
    checkout_data = flask.request.json

    invalid = False

    if len(checkout_data.get('items', {})) != 1:
        invalid = True
    else:
        # checkout_data['items'] is a dictionary
        for item_sku, item in checkout_data["items"].iteritems():
            if item_sku != "ACME-SLR-NG-01":
                invalid = True
            elif item["unit_price"] != 1500:
                invalid = True

    if invalid:
        abort(400)

    return flask.jsonify({
        # Indicates the webhook that Affirm should call after approving payment
        # for the order.
        "charge_notification_url": url_for(".affirm_charge_notification", _external=True),

        # Shipping amount in cents
        "shipping_amount": 200,

        # tax amount in cents
        "tax_amount": 124,

        # User confirmation url can be replaced inside the checkout amendment
        "user_confirmation_url": url_for(".user_confirm_page", _external=True),

        # checkout_id can be replaced, this can be used for your own internal tracking
        "checkout_id": str(uuid4())
    })


@app.route("/charge_notification", methods=["POST"])
def affirm_charge_notification():
    """
    The webhook that is called by Affirm after charge is confirmed by Affirm
    """
    print "Charge Notification Callback:"
    pprint.pprint(flask.request.json)

    # if there are no errors return a 200 OK response
    return ""


# Example Admin Routes

# @app.route("/admin/fulfillment/", methods=["POST", "GET"])


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")


def create_app(settings):
    app.config.update(settings)

    # if SERVER_EXTERNAL_URL is configured then we force the app to use the hostname as the
    # SERVER_NAME.  This is used when generating external urls.
    if app.config['SERVER_EXTERNAL_URL']:
        url = urlparse.urlparse(app.config['SERVER_EXTERNAL_URL'])
        app.config['PREFERRED_URL_SCHEME'] = url.scheme
        app.config['SERVER_NAME'] = url.hostname
    return app

import requests
import json
import flask
from flask import abort
from flask import url_for
from uuid import uuid4


app = flask.Flask(__name__)


## Affirm Charges REST API

def create_charge(charge_token):
    create_charge_url = "{0}/charges".format(app.config["AFFIRM"]["API_URL"])
    print create_charge_url
    return requests.post(create_charge_url,
                         data=json.dumps({
                             "charge_token": charge_token
                         }),
                         headers={"Content-Type": "application/json"},
                         auth=(app.config["AFFIRM"]["PUBLIC_API_KEY"],
                               app.config["AFFIRM"]["SECRET_API_KEY"])).json()


def capture_charge(charge_id, amount=None):
    capture_charge_url = "{0}/charges/{1}/capture".format(app.config["AFFIRM"]["API_URL"], charge_id)
    print capture_charge_url
    return requests.post(capture_charge_url,
                         data=json.dumps({
                             "amount": amount,
                         }),
                         headers={"Content-Type": "application/json"},
                         auth=(app.config["AFFIRM"]["PUBLIC_API_KEY"],
                               app.config["AFFIRM"]["SECRET_API_KEY"])).json()


def void_charge(charge_id):
    void_charge_url = "{0}/charges/{1}/void".format(app.config["AFFIRM"]["API_URL"], charge_id)
    print void_charge_url
    return requests.post(void_charge_url,
                         auth=(app.config["AFFIRM"]["PUBLIC_API_KEY"],
                               app.config["AFFIRM"]["SECRET_API_KEY"])).json()


def refund_charge(charge_id, amount=None):
    refund_charge_url = "{0}/charges/{1}/refund".format(app.config["AFFIRM"]["API_URL"], charge_id)
    print refund_charge_url
    return requests.post(refund_charge_url,
                         data=json.dumps({
                             "amount": amount
                         }),
                         headers={"Content-Type": "application/json"},
                         auth=(app.config["AFFIRM"]["PUBLIC_API_KEY"],
                               app.config["AFFIRM"]["SECRET_API_KEY"])).json()


def read_charge(charge_id):
    get_charge_url = "{0}/charges/{1}".format(app.config["AFFIRM"]["API_URL"], charge_id)
    print get_charge_url
    return requests.get(get_charge_url,
                        auth=(app.config["AFFIRM"]["PUBLIC_API_KEY"],
                              app.config["AFFIRM"]["SECRET_API_KEY"])).json()


@app.route("/")
def shopping_item_page():
    """
    The item page
    """

    # this gets turned into JSON and used to initialize the affirm checkout
    affirm_checkout_data = {

        "currency": "USD",

        "merchant": {
            "public_api_key": app.config["AFFIRM"]["PUBLIC_API_KEY"],
            "user_cancel_url": url_for(".shopping_item_page", _external=True),
            "user_confirmation_url": url_for(".user_confirm_page", _external=True),
        },

        "config": {
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
        affirm_checkout=affirm_checkout_data,
        item_image_url=url_for(".static", filename="item.png"),
        display_name="Acme SLR-NG",
        unit_price_dollars="15.00",
    )

    return flask.render_template("index.html", **template_data)


@app.route("/user_confirm", methods=["POST"])
def user_confirm_page():
    """
    The page to render after the user completes checkout. Typically this will
    display a confirmation message to the user.
    """
    charge_token = flask.request.form["charge_token"]

    # Capture the charge with Affirm
    charge = create_charge(charge_token)

    template_data = {
        "charge_id": charge["id"],
    }

    for charge_action in {"read", "capture", "void", "refund"}:
        template_data["{0}_url".format(charge_action)] = url_for(".admin_do",
                                                                 charge_action=charge_action,
                                                                 charge_id=charge["id"])

    return flask.render_template("user_confirm.html", **template_data)


@app.route("/checkout_amendment", methods=["POST"])
def affirm_checkout_amendment():
    """
    The optional webhook that is called by Affirm after the user begins checkout.

    This webhook should contain any shipping, tax amount updates.
    """

    print "Checkout Amendment Webhook:"
    print json.dumps(flask.request.json, indent=2, sort_keys=True)

    # item sku and unit_price should be checked to ensure consistency
    checkout_data = flask.request.json

    invalid = False

    if len(checkout_data.get("items", {})) != 1:
        invalid = True
    else:
        for item_sku, item in checkout_data["items"].iteritems():
            if item_sku != "ACME-SLR-NG-01":
                invalid = True
            elif item["unit_price"] != 1500:
                invalid = True

    if invalid:
        abort(400)

    return flask.jsonify({
        "merchant": {

            # User confirmation url can be replaced inside the checkout amendment
            "user_confirmation_url": url_for(".user_confirm_page", _external=True),
        },

        # Shipping amount in cents
        "shipping_amount": 200,

        # tax amount in cents
        "tax_amount": 124,

        # checkout_id can be inserted, this can be used for your own internal tracking
        "checkout_id": str(uuid4())
    })


@app.route("/admin/do/<charge_action>/<charge_id>")
def admin_do(charge_action, charge_id):
    action_dispatch = {
        "capture": capture_charge,
        "read": read_charge,
        "refund": refund_charge,
        "void": void_charge,
    }
    if charge_action not in action_dispatch:
        return abort(404)
    response = action_dispatch[charge_action](charge_id)
    return "<pre>%s</pre>" % json.dumps(response, indent=2, sort_keys=True)


def create_app(settings):

    @app.route("/favicon.ico")
    def favicon():
        return app.send_static_file("favicon.ico")

    app.config.update(settings)
    return app

import requests
import json
import flask
from flask import abort
from flask import url_for
from uuid import uuid4
from datetime import datetime, timedelta


app = flask.Flask(__name__)


## Affirm Charges REST API
def _get_extra_request_args():
    if "extra_request_args" in app.config:
        return app.config["extra_request_args"]
    else:
        return {}

def get_checkout_from_token(checkout_token):
    read_checkout_url = "{0}/checkout/{1}".format(app.config["AFFIRM"]["API_URL"], checkout_token)
    print read_checkout_url
    return requests.get(read_checkout_url,
                        headers={"Content-Type": "application/json"},
                        auth=(app.config["AFFIRM"]["PUBLIC_API_KEY"],
                              app.config["AFFIRM"]["SECRET_API_KEY"]),
                              **_get_extra_request_args()).json()


def create_charge(checkout_token):
    create_charge_url = "{0}/charges".format(app.config["AFFIRM"]["API_URL"])
    print create_charge_url
    request_args = {}
    return requests.post(create_charge_url,
                         data=json.dumps({
                             "checkout_token": checkout_token
                         }),
                         headers={"Content-Type": "application/json"},
                         auth=(app.config["AFFIRM"]["PUBLIC_API_KEY"],
                               app.config["AFFIRM"]["SECRET_API_KEY"]),
                         **_get_extra_request_args()).json()


def capture_charge(charge_id, amount=None):
    capture_charge_url = "{0}/charges/{1}/capture".format(app.config["AFFIRM"]["API_URL"], charge_id)
    print capture_charge_url
    return requests.post(capture_charge_url,
                         data=json.dumps({
                             "amount": amount,
                         }),
                         headers={"Content-Type": "application/json"},
                         auth=(app.config["AFFIRM"]["PUBLIC_API_KEY"],
                               app.config["AFFIRM"]["SECRET_API_KEY"]),
                         **_get_extra_request_args()).json()


def void_charge(charge_id):
    void_charge_url = "{0}/charges/{1}/void".format(app.config["AFFIRM"]["API_URL"], charge_id)
    print void_charge_url
    return requests.post(void_charge_url,
                         auth=(app.config["AFFIRM"]["PUBLIC_API_KEY"],
                               app.config["AFFIRM"]["SECRET_API_KEY"]),
                         **_get_extra_request_args()).json()


def refund_charge(charge_id, amount=None):
    refund_charge_url = "{0}/charges/{1}/refund".format(app.config["AFFIRM"]["API_URL"], charge_id)
    print refund_charge_url
    return requests.post(refund_charge_url,
                         data=json.dumps({
                             "amount": amount
                         }),
                         headers={"Content-Type": "application/json"},
                         auth=(app.config["AFFIRM"]["PUBLIC_API_KEY"],
                               app.config["AFFIRM"]["SECRET_API_KEY"]),
                         **_get_extra_request_args()).json()


def read_charge(charge_id):
    get_charge_url = "{0}/charges/{1}".format(app.config["AFFIRM"]["API_URL"], charge_id)
    print get_charge_url
    return requests.get(get_charge_url,
                        auth=(app.config["AFFIRM"]["PUBLIC_API_KEY"],
                              app.config["AFFIRM"]["SECRET_API_KEY"]),
                        **_get_extra_request_args()).json()


@app.route("/")
def shopping_item_page():
    """
    The item page
    """
    kwargs = {'_external': True}
    if app.config['USE_HTTPS']:
        kwargs.update({'_scheme': 'https'})
    # this gets turned into JSON and used to initialize the affirm checkout
    checkout_expiration = (datetime.now() + timedelta(minutes=3)).replace(tzinfo=None).isoformat().rsplit('.', 1)[0] + 'Z'
    affirm_checkout_data = {

        "currency": "USD",

        # checkout_id can be inserted, this can be used for your own internal tracking
        "checkout_id": str(uuid4()),

        "merchant": {
            # "public_api_key": app.config["AFFIRM"]["PUBLIC_API_KEY"],
            "user_cancel_url": url_for(".shopping_item_page", **kwargs),
            "user_confirmation_url": url_for(".user_confirm_page", **kwargs),
        },

        "config": {
            "user_confirmation_url_action": "POST",
            "financial_product_key": app.config["AFFIRM"]["FINANCIAL_PRODUCT_KEY"],
        },

        "items": [
            {
                "sku": "ACME-SLR-NG-01",
                "item_url": url_for(".shopping_item_page", **kwargs),
                "item_image_url": url_for(".static", filename="item.png", **kwargs),
                "display_name": "Acme SLR-NG",
                "unit_price": 1500,
                "qty": 1
            }
        ],

        "shipping": {
            "name": {
                "full": "John Doe"
            },
            "address": {
                "line1": "325 Pacific Ave.",
                "city": "San Francisco",
                "state": "CA",
                "zipcode": "94111"
            }
        },
        "total": 1500,
        "checkout_expiration": checkout_expiration
    }


    if app.config["INJECT_CHECKOUT_AMENDMENT_URL"]:
        affirm_checkout_data["merchant"]["checkout_amendment_url"] = url_for(
            ".affirm_checkout_amendment", **kwargs)

    kwargs = {}
    if app.config['USE_HTTPS']:
        kwargs.update({'_external': True, '_scheme': 'https'})
    template_data = dict(
        affirm_checkout=affirm_checkout_data,
        item_image_url=url_for(".static", filename="item.png", **kwargs),
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
    checkout_token = flask.request.form["checkout_token"]

    checkout = get_checkout_from_token(checkout_token)
    import pprint
    pprint.pprint(checkout)

    # Capture the charge with Affirm
    charge = create_charge(checkout_token)

    import pprint
    pprint.pprint(charge)

    template_data = {
        "charge_id": charge["id"],
    }
    kwargs = {}
    if app.config['USE_HTTPS']:
        kwargs.update({'_external': True, '_scheme': 'https'})
    for charge_action in {"read", "capture", "void", "refund"}:
        template_data["{0}_url".format(charge_action)] = url_for(".admin_do",
                                                                 charge_action=charge_action,
                                                                 charge_id=charge["id"],
                                                                 **kwargs)

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

    for item_sku, item in checkout_data["items"].iteritems():
        if item_sku != "ACME-SLR-NG-01":
            abort(400)
        elif item["unit_price"] != 1500:
            abort(400)
    kwargs = {'_external': True}
    if app.config['USE_HTTPS']:
        kwargs.update({'_scheme': 'https'})
    return flask.jsonify({
        "merchant": {

            # User confirmation url can be replaced inside the checkout amendment
            "user_confirmation_url": url_for(".user_confirm_page", **kwargs),
        },

        # Shipping amount in cents
        "shipping_amount": 200,

        # tax amount in cents
        "tax_amount": 124,

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

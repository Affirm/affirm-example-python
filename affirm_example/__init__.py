import requests
import json
import flask
from flask import abort
from flask import url_for
from uuid import uuid4

app = flask.Flask(__name__)


# Affirm Charges REST API
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


def merchant_capture_charge(charge_id, amount=None):
    return _merchant_capture_charge(charge_id, amount)


def _merchant_capture_charge(charge_id, amount=None):
    capture_charge_url = "{0}/charges/{1}/capture".format(app.config["AFFIRM"]["API_URL"], charge_id)
    print capture_charge_url

    return requests.post(
        capture_charge_url,
        data=json.dumps({
            "amount": amount,
        }),
        headers={"Content-Type": "application/json"},
        auth=(app.config["AFFIRM"]["PUBLIC_API_KEY"],
              app.config["AFFIRM"]["SECRET_API_KEY"]),
        **_get_extra_request_args()).json()


def merchant_capture_and_originate_charge(charge_id):
    merchant_capture_result = _merchant_capture_charge(charge_id)
    originate_charge(charge_id)
    return merchant_capture_result


def originate_charge(charge_id):
    originate_charge_url = "{0}/originate/{1}".format(app.config["AFFIRM"]["FUNCTIONAL_TESTS_URL"], charge_id)

    print originate_charge_url
    requests.post(originate_charge_url)

    return read_charge(charge_id)


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

def display_charge_actions(template_data):
    kwargs = {}
    if app.config['USE_HTTPS']:
        kwargs.update({'_external': True, '_scheme': 'https'})
    for charge_action in {"read", "capture", "void", "refund", "merchant_capture", "originate"}:
        template_data["{0}_url".format(charge_action)] = url_for(".admin_do",
                                                                 charge_action=charge_action,
                                                                 charge_id=template_data["charge_id"],
                                                                 **kwargs)

    return flask.render_template("user_confirm.html", **template_data)

# Affirm Transactions REST API
def create_transaction(checkout_token):
    create_transaction_url = "{0}/transactions".format(app.config["AFFIRM"]["TRANSACTIONS_API_URL"])
    print create_transaction_url
    request_args = {}
    return requests.post(create_transaction_url,
                         data=json.dumps({
                             "transaction_id": checkout_token
                         }),
                         headers={"Content-Type": "application/json"},
                         auth=(app.config["AFFIRM"]["PUBLIC_API_KEY"],
                               app.config["AFFIRM"]["SECRET_API_KEY"]),
                         **_get_extra_request_args()).json()

def read_transaction(transaction_id):
    get_transaction_url = "{0}/transactions/{1}".format(app.config["AFFIRM"]["TRANSACTIONS_API_URL"], transaction_id)
    print get_transaction_url
    return requests.get(get_transaction_url,
                        auth=(app.config["AFFIRM"]["PUBLIC_API_KEY"],
                              app.config["AFFIRM"]["SECRET_API_KEY"]),
                        **_get_extra_request_args()).json()

def void_transaction(transaction_id):
    void_transaction_url = "{0}/transactions/{1}/void".format(app.config["AFFIRM"]["TRANSACTIONS_API_URL"], transaction_id)
    print void_transaction_url
    return requests.post(void_transaction_url,
                         auth=(app.config["AFFIRM"]["PUBLIC_API_KEY"],
                               app.config["AFFIRM"]["SECRET_API_KEY"]),
                         **_get_extra_request_args()).json()


def refund_transaction(transaction_id, amount=10):
    refund_transaction_url = "{0}/transactions/{1}/refund".format(app.config["AFFIRM"]["TRANSACTIONS_API_URL"], transaction_id)
    print refund_transaction_url
    return requests.post(refund_transaction_url,
                         data=json.dumps({
                             "amount": amount
                         }),
                         headers={"Content-Type": "application/json"},
                         auth=(app.config["AFFIRM"]["PUBLIC_API_KEY"],
                               app.config["AFFIRM"]["SECRET_API_KEY"]),
                         **_get_extra_request_args()).json()

def capture_transaction(transaction_id, amount=None):
    capture_transaction_url = "{0}/transactions/{1}/capture".format(app.config["AFFIRM"]["TRANSACTIONS_API_URL"], transaction_id)
    print capture_transaction_url

    return requests.post(
        capture_transaction_url,
        data=json.dumps({
            "amount": amount,
        }),
        headers={"Content-Type": "application/json"},
        auth=(app.config["AFFIRM"]["PUBLIC_API_KEY"],
              app.config["AFFIRM"]["SECRET_API_KEY"]),
        **_get_extra_request_args()).json()

def display_transaction_actions(template_data):
    kwargs = {}
    if app.config['USE_HTTPS']:
        kwargs.update({'_external': True, '_scheme': 'https'})
    for transaction_action in {"read", "update", "capture", "refund", "void"}:
        template_data["{0}_url".format(transaction_action)] = url_for(".transaction_admin_do",
                                                                 transaction_action=transaction_action,
                                                                 transaction_id=template_data["transaction_id"],
                                                                 **kwargs)

    return flask.render_template("lease_user_confirm.html", **template_data)

@app.route("/")
def shopping_item_page():
    """
    The item page
    """
    kwargs = {'_external': True}
    if app.config['USE_HTTPS']:
        kwargs.update({'_scheme': 'https'})

    default_currency = app.config.get('DEFAULT_CURRENCY', 'USD')

    # this gets turned into JSON and used to initialize the affirm checkout
    affirm_checkout_data = {

        # checkout_id can be inserted, this can be used for your own internal tracking
        "checkout_id": str(uuid4()),

        "merchant": {
            # "public_api_key": app.config["AFFIRM"]["PUBLIC_API_KEY"],
            "user_cancel_url": url_for(".shopping_item_page", **kwargs),
            "user_confirmation_url": url_for(".user_confirm_page", **kwargs),
        },

        "config": {
            "user_confirmation_url_action": "POST",
        },

        "items": [
            {
                "sku": "ACME-SLR-NG-01",
                "item_url": url_for(".shopping_item_page", **kwargs),
                "item_image_url": url_for(".static", filename="item.png", **kwargs),
                "display_name": "Acme SLR-NG",
                "unit_price": 10000,
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

        "billing": {
            "name": {
                "first": None,
                "last": None,
            },
            "address": {
                "line1": "325 Pacific Ave.",
                "line2": None,
                "city": "San Francisco",
                "state": "CA",
                "zipcode": "94111"
            }
        },
        "metadata": {
            "shipping_type": "Standard Shipping",
            "__affirm_tracking_uuid": None,
        },
        "order_id": None,
        "total": 10000
    }

    # This data is used to initialize the Affirm Prequal
    affirm_prequal_data = {
        "page_type": "product",
        "items": [
            {
                "sku": "ACME-SLR-NG-01",
                "item_url": url_for(".shopping_item_page", **kwargs),
                "display_name": "Acme SLR-NG",
                "unit_price": 10000,
                "qty": 1
            }
        ],
    }

    ca_address = {
        'street1': '745 Thurlow Street',
        'street2': 'Suite 2400',
        'city': 'Vancouver',
        'region1_code': 'BC',
        'postal_code': 'V6E 0C5',
        'country_code': 'CA',
    }

    if app.config["INJECT_CHECKOUT_AMENDMENT_URL"]:
        affirm_checkout_data["merchant"]["checkout_amendment_url"] = url_for(
            ".affirm_checkout_amendment", **kwargs)

    kwargs = {}
    if app.config['USE_HTTPS']:
        kwargs.update({'_external': True, '_scheme': 'https'})
    template_data = dict(
        affirm_checkout=affirm_checkout_data,
        affirm_prequal=affirm_prequal_data,
        default_currency=default_currency,
        item_image_url=url_for(".static", filename="item.png", **kwargs),
        display_name="Acme SLR-NG",
        unit_price_dollars="100.00",
        ca_address=ca_address,
    )

    return flask.render_template("index.html", **template_data)


@app.route("/user_confirm", methods=["GET", "POST"])
def user_confirm_page():
    """
    The page to render after the user completes checkout. Typically this will
    display a confirmation message to the user.
    """

    if flask.request.method == 'GET':
        checkout_token = flask.request.args.get("checkout_token")
    else:
        checkout_token = flask.request.form["checkout_token"]

    import pprint

    for i in range(3):
        try:
            checkout = get_checkout_from_token(checkout_token)
            pprint.pprint(checkout)
        except Exception:
            # retry for timeouts
            continue
        else:
            break
    else:
        print("Error: unable to fetch checkout")

    if checkout_token.startswith('LS-'):
        transaction = create_transaction(checkout_token)
        pprint.pprint(transaction)

        return display_transaction_actions({"transaction_id": transaction["id"]})
    else:
        # Capture the charge with Affirm
        charge = create_charge(checkout_token)
        pprint.pprint(charge)

        return display_charge_actions({"charge_id": charge["id"]})


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
        "read": read_charge,
        "capture": merchant_capture_and_originate_charge,
        "refund": refund_charge,
        "void": void_charge,
        "merchant_capture": merchant_capture_charge,
        "originate": originate_charge,
    }
    if charge_action not in action_dispatch:
        return abort(404)
    response = action_dispatch[charge_action](charge_id)
    return "<pre>%s</pre>" % json.dumps(response, indent=2, sort_keys=True)

@app.route("/admin/do/transaction/<transaction_action>/<transaction_id>")
def transaction_admin_do(transaction_action, transaction_id):
    action_dispatch = {
        "read": read_transaction,
        "capture": capture_transaction,
        "refund": refund_transaction,
        "void": void_transaction,
    }
    if transaction_action not in action_dispatch:
        return abort(404)
    response = action_dispatch[transaction_action](transaction_id)
    return "<pre>%s</pre>" % json.dumps(response, indent=2, sort_keys=True)


@app.route("/main.js")
def main_js():
    return flask.render_template("main.js")


def create_app(settings):
    @app.route("/favicon.ico")
    def favicon():
        return app.send_static_file("favicon.ico")

    app.config.update(settings)
    return app

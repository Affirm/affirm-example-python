import pprint
import requests
import flask
import json

def create_app(settings):
    app = flask.Flask(__name__)
    app.config.from_object(settings)

    # Externally visible name of our server.
    OUR_SERVER_NAME = app.config["OUR_SERVER_NAME"]
    assert OUR_SERVER_NAME[-1] != "/", "Don't include trailing slash in OUR_SERVER_NAME"

    AFFIRM_SERVER_NAME = app.config["AFFIRM"]["SERVER_NAME"]
    assert AFFIRM_SERVER_NAME[-1] != "/", "Don't include trailing slash in SERVER_NAME"

    AFFIRM_API_URL_BASE = AFFIRM_SERVER_NAME + "/api/" + app.config["AFFIRM"]["API_VERSION"]

    # URLs relative to OUR_SERVER_NAME
    SHOPPING_ITEM_PAGE = "/" # Page showing the item to be ordered.
    USER_CONFIRM_PAGE = "/user_confirm" # Page to show the user that there order is confirmed.
    CHECKOUT_NOTIFICATION = "/checkout_hook" # webhook called when a user begins checkout.
    ORDER_NOTIFICATION = "/confirmation_hook" # webhook called when an order has been approved.


    #####
    # Define webpages and webhooks. The parameter to app.route defines the URL
    # served relative to the server name.
    #####

    @app.route("/favicon.ico")
    def favicon():
        return flask.send_from_directory(app.static_folder, "favicon.ico",
                                         mimetype="image/vnd.microsoft.icon")

    @app.route(SHOPPING_ITEM_PAGE)
    def shopping_item_page():
        """
        The shopping page
        """
        template_data = dict(
            item_url=OUR_SERVER_NAME + SHOPPING_ITEM_PAGE,
            item_thumbnail_url=OUR_SERVER_NAME + "/static/item.png",
            user_confirmation_url=OUR_SERVER_NAME + USER_CONFIRM_PAGE,
            sku = "ACME-SLR-NG-01",
            display_name = "Acme SLR-NG",
            unit_price = "15.00"
        )
    
        if app.config["INJECT_CHECKOUT_NOTIFICATION"]:
            template_data["checkout_notification_url"] = OUR_SERVER_NAME + CHECKOUT_NOTIFICATION
        return flask.render_template("index.html", **template_data)
    
    @app.route(USER_CONFIRM_PAGE)
    def user_confirm_page():
        """
        The page to render after the user completes checkout. Typically this will
        display a confirmation message to the user.
        """
        return "Order confirmed."
    
    @app.route(CHECKOUT_NOTIFICATION, methods=["POST"])
    def affirm_checkout_notification():
        """
        The webhook that is called by Affirm after the user begins checkout.
        This webhook should return information to Affirm about the order being
        placed.
        """
        print "Checkout Notification Callback:"
        pprint.pprint(flask.request.json)

        return flask.jsonify({
            # Indicates the webhook that Affirm should call after approving payment
            # for the order.
            "order_notification_url": OUR_SERVER_NAME + ORDER_NOTIFICATION,
    
            # Indicates shipping/taxes for each item in the order
            "items": {
                "ACME-SLR-NG-01": {
                    "shipping_amount": "2.00",
                    "tax_amount": "1.24"
                }
            }
        })
    
    @app.route(ORDER_NOTIFICATION, methods=["POST"])
    def affirm_order_notification():
        """
        The webhook that is called by Affirm after Affirm confirms the the
        purchase is approved. This webhook should capture or cancel the order.
        """
        print "Order Notification Callback:"
        pprint.pprint(flask.request.json)
    
        # The CVT is posted as the data of the request
        assert "token" in flask.request.json
        assert "sig" in flask.request.json
    
        token = flask.request.json["token"]
        sig = flask.request.json["sig"]
        conf_code = token["conf_code"]

        order_is_valid = True
        for sku, sku_details in token["items"].items():
            # Check sku, sku_details["unit_price"],
            # sku_details["shipping_amount"], etc. to verify that this is a
            # valid order.
            # order_is_valid = False
            pass
    
        if order_is_valid:
            # Capture the order.
            response = requests.post(AFFIRM_API_URL_BASE + "/order/" + conf_code + "/capture",
                                     data=json.dumps(dict(cvt=dict(sig=sig, token=token))),
                                     headers={"Content-Type": "application/json"},
                                     auth=(app.config["AFFIRM"]["PUBLIC_API_KEY"],
                                           app.config["AFFIRM"]["SECRET_API_KEY"]))
        
            if not response.ok:
                print "Attempted to capture. Server response was %s" % response
                print response.content
            else:
                print "Captured successfully."
        else:
            # Cancel the order.
            response = requests.post(AFFIRM_API_URL_BASE + "/order/" + conf_code + "/cancel",
                                     data=json.dumps(dict(cvt=dict(sig=sig, token=token))),
                                     headers={"Content-Type": "application/json"},
                                     auth=(app.config["AFFIRM"]["PUBLIC_API_KEY"],
                                           app.config["AFFIRM"]["SECRET_API_KEY"]))
        
            if not response.ok:
                # Even if we don't successfully cancel, the order will eventually expire.
                print "Attempted to cancel. Server response was %s" % response
                print response.content
            else:
                print "Canceled successfully."
    
        return ""

    #####
    # End of webpages and webhooks definitions
    #####

    return app

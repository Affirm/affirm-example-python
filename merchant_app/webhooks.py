import pprint
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import url_for

webhooks_bp = Blueprint("webhooks", __name__)

@webhooks_bp.route("/checkout", methods=['POST'])
def affirm_checkout_notification():
    print "Checkout Notification Callback:"
    pprint.pprint(request.json)
    return jsonify({
        'order_notification_url': url_for(".affirm_order_notification", _external=True),
        'items': {
            'ACME-SLR-NG-01': {
                'shipping_amount': "2.00",
                'tax_amount': '1.24'
            }
        }
    })

@webhooks_bp.route("/confirmation", methods=['POST'])
def affirm_order_notification():
    print "Order Notification Callback:"
    pprint.pprint(request.json)
    return ""


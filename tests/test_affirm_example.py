from __future__ import absolute_import
from __future__ import print_function
from flask_testing import TestCase as FlaskTestCase
from mock import patch
from affirm_example import app
from affirm_example import capture_charge
from affirm_example import void_charge
from affirm_example import refund_charge
import urlparse
import json


class TestAffirmExample(FlaskTestCase):

    def create_app(self):
        app.config.update({
            "AFFIRM": {
                "API_URL": "https://test.affirm.com/api/v2",
                "PUBLIC_API_KEY": "my_public_key",
                "SECRET_API_KEY": "my_secret_key"
            },
            "INJECT_CHECKOUT_AMENDMENT_URL": False,
        })
        return app

    def test_shopping_item_page(self):
        self.client.get("/")
        self.assert_template_used("index.html")
        affirm_checkout = self.get_context_variable("affirm_checkout")
        self.assertEqual(affirm_checkout["merchant"]["public_api_key"], "my_public_key")

    def test_shopping_item_page_inject_checkout_amendment(self):
        self.app.config['INJECT_CHECKOUT_AMENDMENT_URL'] = True
        self.client.get("/")
        self.assert_template_used("index.html")
        affirm_checkout = self.get_context_variable("affirm_checkout")
        self.assertEqual(affirm_checkout["merchant"]["checkout_amendment_url"],
                         "http://localhost/checkout_amendment")

    def test_user_confirm(self):
        response = self.client.post("/user_confirm", data={"charge_id": "CHARGE"})
        self.assert200(response)
        self.assertEqual(response.data, "Order confirmed: CHARGE")

    @patch("affirm_example.uuid4")
    def test_checkout_amendment(self, uuid4):
        uuid4.return_value = "734d73c0-a40e-11e3-a5e2-0800200c9a66"
        response = self.client.post("/checkout_amendment",
                                    content_type="application/json",
                                    data=json.dumps({
                                        "items": {
                                            "ACME-SLR-NG-01": {
                                                "unit_price": 1500
                                            }
                                        }
                                    }))
        self.assert200(response)
        self.assertEqual(response.json['checkout_id'], uuid4.return_value)
        self.assertEqual(response.json['shipping_amount'], 200)
        self.assertEqual(response.json['tax_amount'], 124)
        self.assertEqual(response.json['charge_notification_url'],
                         "http://localhost/charge_notification")

    @patch("affirm_example.pprint")
    def test_charge_notification(self, pprint):
        response = self.client.post("/charge_notification",
                                    content_type="application/json",
                                    data=json.dumps({
                                        "id": "CHARGE"
                                    }))
        self.assert200(response)
        pprint.pprint.assert_called_once_with(
            {
                "id": "CHARGE"
            }
        )

    @patch("affirm_example.requests", autospec=True)
    def test_capture_charge(self, requests):
        with self.app.test_request_context():
            capture_charge("CHARGE", 100)

        requests.post.assert_called_once_with(
            "https://test.affirm.com/api/v2/charges/CHARGE/capture",
            data=json.dumps({"amount": 100}),
            headers={"Content-Type": "application/json"},
            auth=(
                "my_public_key",
                "my_secret_key"
            )
        )

    @patch("affirm_example.requests", autospec=True)
    def test_void_charge(self, requests):
        with app.test_request_context():
            void_charge("CHARGE")

        requests.post.assert_called_once_with(
            "https://test.affirm.com/api/v2/charges/CHARGE/void",
            auth=(
                "my_public_key",
                "my_secret_key"
            )
        )

    @patch("affirm_example.requests", autospec=True)
    def test_refund_charge(self, requests):
        with self.app.test_request_context():
            refund_charge("CHARGE", 100)

        requests.post.assert_called_once_with(
            "https://test.affirm.com/api/v2/charges/CHARGE/refund",
            data=json.dumps({"amount": 100}),
            headers={"Content-Type": "application/json"},
            auth=(
                "my_public_key",
                "my_secret_key"
            )
        )



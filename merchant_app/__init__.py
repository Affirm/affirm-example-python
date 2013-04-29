from flask import Flask
from flask import redirect
from flask import send_from_directory
from flask import url_for
from .shop import shop_bp
from .webhooks import webhooks_bp

def register_blue_prints(app):
    app.register_blueprint(shop_bp, url_prefix="/")
    app.register_blueprint(webhooks_bp, url_prefix="/affirm")

def create_app(settings):
    app = Flask(__name__)
    app.config.from_object(settings)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(app.static_folder, 'favicon.ico',
                                   mimetype='image/vnd.microsoft.icon')

    # @app.route('/')
    # def root():
    #     return redirect(url_for("shop.shop"))

    register_blue_prints(app)
    return app


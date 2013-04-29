from flask.ext.script import Server, Manager, Shell
from merchant_app import create_app

try:
    from merchant_app import config
    if (config.AFFIRM["PUBLIC_API_KEY"] == "<Your public API key from Affirm>"
            or config.AFFIRM["SECRET_API_KEY"] == "<Your secret API key from Affirm>"):
        raise Exception("Need to fill out template.")
except:
    import sys
    print "Problem importing config."
    print "Please run:"
    print "  cp merchant_app/config.py.txt merchant_app/config.py"
    print "Then fill in your public/secret API keys in merchant_app/config.py"
    sys.exit(1)

app = create_app(config)

manager = Manager(app)
manager.add_command("runserver", Server(**config.FLASK_SERVER_ARGS))

if __name__ == "__main__":
    manager.run()


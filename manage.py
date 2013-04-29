from flask.ext.script import Server, Manager, Shell
from merchant_app import create_app
from merchant_app import config

app = create_app(config)

manager = Manager(app)
manager.add_command("runserver", Server(host=app.config['HOST']))

if __name__ == "__main__":
    manager.run()


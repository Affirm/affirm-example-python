import sys
import os
import os.path
from flask.ext.script import Server, Manager
from affirm_example import create_app
import yaml

settings_file = os.path.join(os.path.dirname(__file__), "config", "app.yml")

if not os.path.exists(settings_file):
    print >>sys.stderr, "The file %s does not exist."
    print >>sys.stderr, "Please copy %s.tmpl to %s. Then fill in your public/secret API key." % (
        settings_file, settings_file
    )
    sys.exit(1)

settings = yaml.load(file(settings_file))

if not settings['AFFIRM']['PUBLIC_API_KEY'] or not settings['AFFIRM']['SECRET_API_KEY']:
    print >>sys.stderr, "Please configure your Affirm public and secret API keys in %s" % settings_file
    sys.exit(1)


app = create_app(settings)

manager = Manager(app)
manager.add_command("runserver", Server())

def main():
    manager.run()

if __name__ == "__main__":
    main()



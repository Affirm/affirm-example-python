affirm-example-python
=====================

Example Affirm merchant integration with a python-flask web app

Quickstart guide:

1. Clone template and fill-in public/secret API keys (Affirm will give you
   these)
```
cp merchant_app/config.py.txt merchant_app/config.py
```

2. Configure virtualenv environment
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

3. Run the server and configure to listen on a publicly addressable interface.
   It is important that sandbox.affirm.com can access this interface so that
   checkout and order notifications can reach this demo app.
```
python manage.py runserver --host <public-ip-address> --port <public-port>
```

4. Point your browser to <pre>http://&lt;public-ip-address&gt;:&lt;public-port&gt;</pre>

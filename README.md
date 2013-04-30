affirm-example-python
=====================

Example Affirm merchant integration with a python-flask web app, talking to the Affirm sandbox.

Quickstart guide:

1. Clone template and fill-in public/secret API keys (Affirm will give you
   these):
```
cp merchant_app/config.py.txt merchant_app/config.py
```

2. Configure virtualenv environment:
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

3. Run the server:
```
python manage.py runserver --host 127.0.0.1 --port 8080
```
You may set host and port to whatever makes sense for your system.

4. Point your browser to ```http://127.0.0.1:8080```
(or whatever you set host/port to in step 3)

Notes: A full integration requires ```sandbox.affirm.com``` to call
webhooks defined by this server, so eventually you'll need to listen
on a publicly addressable interface. Replace ```127.0.0.1``` and
```8080``` with the correct values when you are ready.

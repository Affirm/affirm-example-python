affirm-example-python
=====================

example Affirm merchant integration with a python-flask web app

Configure virtualenv environment

virtualenv env
source env/bin/activate
pip install -r requirements.txt

Run the server and configure to listen on a publicly addressable interface. It
is important that sanbox.affirm.com can access this interface so that
checkout and order notifications can reach this demo app.

python manage.py runserver --host <public_ip_address> --port <public_port>

Point your browser to http://<public_ip_address>:<public_port>



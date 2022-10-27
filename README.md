affirm-example-python
=====================

Example Affirm merchant integration with a python flask web app, integrated with the Affirm sandbox.

Quickstart guide:

1. Configure virtualenv environment:

    ```
    virtualenv env
    source env/bin/activate
    ```

2. Install the requirements and package in development mode

    ```
    pip install -r requirements.txt
    python setup.py develop
    ```

3. Edit the file `config/app.yml` and fill in public/secret API keys (Affirm will give you these). There is one default merchant on the Thor. More can
be added as needed.

    ```
    PUBLIC_API_KEY: PreSeededApiKeyDirect
    SECRET_API_KEY: PreSeededSecretKeyDirect
    ```

4. Replace the <thor_id> in `config/app.yml` with the Thor subdomain (hostname -s)

5. Optionally, configure the app to recieve checkout amendments and charge notifications.  In `config/app.yml` set `INJECT_CHECKOUT_AMENDMENT` to `true` in order to recieve the checkout amendment hook.

    ```
    INJECT_CHECKOUT_AMENDMENT_URL: true
    ```

6. Run the server.

    ```
    affirm_example_manage runserver --host 127.0.0.1 --port 7777
    ```

6. Point your browser to ```http://127.0.0.1:7777```
(or whatever you set host/port to in step 5)

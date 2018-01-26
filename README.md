affirm-example-python
=====================

Example Affirm merchant integration with a python flask web app, integrated with the Affirm sandbox.

Quickstart guide:

1. Configure virtualenv environment:

    ```
    virtualenv env
    source env/bin/activate
    ```

2. Install the package in development mode

    ```
    python setup.py develop
    ```

3. Edit the file `config/app.yml` and fill in public/secret API keys (Affirm will give you these)

    ```
     # Set the public API key from Affirm
     PUBLIC_API_KEY:

     # Set the secret API key from Affirm
     SECRET_API_KEY:
    ```

4. Optionally, configure the app to recieve checkout amendments and charge notifications.  In `config/app.yml` set `INJECT_CHECKOUT_AMENDMENT` to `true` in order to recieve the checkout amendment hook.  

    ```
    INJECT_CHECKOUT_AMENDMENT_URL: true
    ```

5. Run the server.  If you have followed step 3 and configured the app to recieve amendment webhooks then the `host` and `port` parameters should allow external access from `sandbox.affirm.com`

    ```
    affirm_example_manage runserver --host 127.0.0.1 --port 8080
    ```

6. Point your browser to ```http://127.0.0.1:8080```
(or whatever you set host/port to in step 5)

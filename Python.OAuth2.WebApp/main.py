from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import os

app = Flask(__name__)


CLIENT_ID = "db045219-98ac-491e-804b-0cb09221cde7" 
CLIENT_SECRET = "fT4uG5qQ4gJ7eM5cJ3jL4xS6iP6qW4hM0jQ8lX2gW7bB6eS3nJ"
REDIRECT_URI = "https://localhost:5000/home/finishauth"
AUTH_ENDPOINT = "https://sso.digikey.com/as/authorization.oauth2"
TOKEN_ENDPOINT = "https://sso.digikey.com/as/token.oauth2"


@app.route("/")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. digikey)
    using an URL with a few key OAuth parameters.
    """
    digikey = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope="")
    authorization_url, state = digikey.authorization_url(AUTH_ENDPOINT)

    # State is used to prevent CSRF, keep this for later.
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.

@app.route("/home/finishauth", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """
    code = request.args.get('code')
    digikey = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI,)
    token = digikey.fetch_token(TOKEN_ENDPOINT, 
                                client_secret=CLIENT_SECRET,
                                authorization_response=request.url, 
                                code=code)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.

    return  jsonify(token)


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

    app.secret_key = os.urandom(24)
    app.run(ssl_context='adhoc', debug=True)

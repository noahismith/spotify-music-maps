import json
from flask import Flask, request, redirect, g, render_template, make_response, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import base64
import urllib
from urlparse import urlparse

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://noahismith:spotify-mmaps@spotify-mmaps.cnfthxsaxcoe.us-east-2.rds.amazonaws.com/spotifymmaps'
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True

db = SQLAlchemy(app)

#  Client Keys
CLIENT_ID = "113d03ef95bd4e29889577312ec0817d"
CLIENT_SECRET = "4fd53ac1a0554655b3b9f12d3c2c8421"

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)


# Server-side Parameters
CLIENT_SIDE_URL = "http://52.15.141.175"
REDIRECT_URI = CLIENT_SIDE_URL + "/profile"
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()


auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}

@app.route("/")
def index():
	return render_template('index.html') 	

from models import User

@app.route("/login")
def login():
	# Auth Step 1: Authorization
	url_args = "&".join(["{}={}".format(key,urllib.quote(val)) for key,val in auth_query_parameters.iteritems()])
	auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
	return redirect(auth_url)

@app.route("/profile")
def profile():
	if ("error" in request.query_string):
		return make_response(redirect(url_for("index")))
	else: 
		return make_response(redirect(url_for("index")))


@app.route("/geo")
def geo():
	send_url = 'http://ip-api.com/json/' + request.remote_addr
	resp = requests.get(send_url)
	json_data = json.loads(resp.text)
	lat = json_data['lat']
	lng = json_data['lon']
	return render_template('geo.html', lat=lat, lng=lng)

def create_user():
    new_user = User(0, 0, 0.1, 0.2)
    new_user.save()
    return new_user.__repr__()


if __name__ == "__main__":
    app.run(ssl_context="adhoc")

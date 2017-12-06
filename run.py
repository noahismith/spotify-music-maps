import json
from flask import Flask, request, redirect, g, render_template, make_response, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import base64
import urllib
from spotifyapi import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://noahismith:spotify-mmaps@spotify-mmaps.cnfthxsaxcoe.us-east-2.rds.amazonaws.com/spotifymmaps'
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True

db = SQLAlchemy(app)

from models import User


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login")
def login():
    # Auth Step 1: Authorization
    url_args = "&".join(["{}={}".format(key, urllib.quote(val)) for key, val in auth_query_parameters.iteritems()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)

@app.route("/callback")
def callback():
    if ("error" in request.query_string):
        return make_response(redirect(url_for("index")))

    code = request.args.get('code')
    tokens = get_tokens(code)

    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    token_type = tokens["token_type"]
    expires_in = tokens["expires_in"]

    profile_data = get_profile_me(access_token)

    # TODO: check for profile error

    user_id = profile_data['id']

    new_user = db.session.query(User).filter_by(user_id=id).first()
    if new_user is not None:
        # TODO: handle error user already exists
        return False

    track_id = get_current_track_id(access_token)
    ip = request.remote_addr
    new_user = User(user_id, track_id, ip, access_token)
    new_user.save()

    return make_response(redirect(url_for("dashboard") + user_id))


@app.route("/profile")
def profile():
    payload = json.loads(requests.data.decode())
    user_id = payload['id']
    user = db.session.query(User).filter_by(user_id=user_id).first()
    if user is None:
        # TODO: return error
        return False
    # TODO: populate html profile page
    return render_template('profile.html')


@app.route("/dashboard")
def dashboard():
    payload = json.loads(requests.data.decode())
    user_id = payload['id']
    user = db.session.query(User).filter_by(user_id=user_id).first()
    if user is None:
        # TODO: return error
        return False
        # TODO: populate html profile page
    return render_template('dashboard.html')


@app.route("/follow")
def follow():
    return


@app.route("/unfollow")
def unfollow():
    return


@app.route("/geo")
def geo():
    send_url = 'http://ip-api.com/json/' + request.remote_addr
    resp = requests.get(send_url)
    json_data = json.loads(resp.text)
    lat = json_data['lat']
    lng = json_data['lon']
    return render_template('geo.html', lat=lat, lng=lng)


def get_location(ip):
    send_url = 'http://ip-api.com/json/' + ip
    resp = requests.get(send_url)
    return json.loads(resp.text)


if __name__ == "__main__":
    app.run()

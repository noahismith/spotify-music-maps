from flask import  Blueprint
import os
import urllib
from flask import Flask, request, redirect, render_template, make_response, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from spotifyapi import *
from app import create_app, db

views_blueprint = Blueprint('views', __name__)

from .models import User

@views_blueprint.route("/")
def index():
    # TODO: populate dashboard with public feed
    all_users = User.get_all()
    markers = []
    for user in all_users:
        location = get_location(user.ip)
        lat = location['lat']
        lng = location['lon']
        obj = {
            "user_id": user.user_id,
            "track_id": user.track_id,
            "lat": lat,
            "lng": lng
        }
        markers.append(obj)


    print(markers)
    return render_template('index.html', auth_url=get_auth_url(), markers=markers)


@views_blueprint.route("/login")
def login():
    url_args = "&".join(["{}={}".format(key, urllib.quote(val)) for key, val in auth_query_parameters.iteritems()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


@views_blueprint.route("/callback")
def callback():
    if "error" in request.query_string:
        return render_template("error.html", error=request.query_string['error'], url=request.url_root)

    code = request.args.get('code')
    tokens = get_tokens(code)

    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    token_type = tokens["token_type"]
    expires_in = tokens["expires_in"]

    # Get spotify user id
    profile_data = get_profile_me(access_token)

    if "error" in profile_data:
        return render_template("error.html", error=profile_data['error'], url=request.url_root)

    user_id = profile_data['id']

    # Check if user already exists, update, and redirect to dashboard
    new_user = db.session.query(User).filter_by(user_id=user_id).first()
    if new_user is not None:
        new_user.update(remote_addr=request.remote_addr, token=access_token)
        return make_response(redirect(url_for("views.dashboard") + "?id=" + user_id), 303)

    new_user = User(user_id, 0, 0, access_token)
    new_user.update(remote_addr=request.remote_addr, token=access_token)

    return make_response(redirect(url_for("views.dashboard") + "?id=" + user_id), 303)


@views_blueprint.route("/profile")
def profile():
    user_id = request.args['id']
    user = db.session.query(User).filter_by(user_id=user_id).first()
    if user is None:
        # TODO: error handling
        return False
    profile_data = get_profile(user.token, user_id)
    return render_template('profile.html', profile=profile_data)


@views_blueprint.route("/dashboard")
def dashboard():
    user_id = request.args['id']
    user = db.session.query(User).filter_by(user_id=user_id).first()
    if user is None:
        # TODO: error handling
        return False
    # TODO: add markers table and endpoints


    # Get private_markers endpoint
    # pass markers endpoint to render_template, center on last listen otherwise any user

    user.track_id = get_current_track_me(user.token)['id']
    user.ip = request.remote_addr
    location = get_location(user.ip)

    if "error" in location:
        return render_template("error.html", error="Unable to find location based on ip address", url=request.url_root)


    center_lat = location['lat']
    center_lng = location['lon']
    db.session.commit()

    all_users = User.get_all()
    markers = []
    for user in all_users:
        location = get_location(user.ip)
        lat = location['lat']
        lng = location['lon']
        obj = {
            "user_id": user.user_id,
            "track_id": user.track_id,
            "lat": lat,
            "lng": lng
        }
        markers.append(obj)

    return render_template('dashboard.html', center_lat=center_lat, center_lng=center_lng, user_id=user_id, markers=markers)

# TODO: edits for local tests
def get_location(ip):
    send_url = 'http://ip-api.com/json/' + ip
    try:
        resp = requests.get(send_url)
    except requests.exeptions.RequestException as e:
        print(e)
        #return {"error": e}
        return {"lat": 0, "lon": 0}
    resp_json = json.loads(resp.text)
    if resp_json['status'] == 'fail':
        #return {"error": "fail"}
        return {"lat": 0, "lon": 0}
    return resp_json


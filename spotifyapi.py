import json
from flask import Flask, request, redirect, g, render_template
from flask_sqlalchemy import SQLAlchemy
import requests
import base64
import urllib

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
REDIRECT_URI = CLIENT_SIDE_URL + "/callback"
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


def get_tokens(auth_token):
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    base64encoded = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET))
    headers = {"Authorization": "Basic {}".format(base64encoded)}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)
    return json.loads(post_request.text)


def get_profile_me(access_token):
    authorization_header = {"Authorization":"Bearer {}".format(access_token)}
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_data = requests.get(user_profile_api_endpoint, headers=authorization_header)
    print(profile_data.text)
    return json.loads(profile_data.text)


def get_profile(access_token, user_id):
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}
    user_profile_api_endpoint = "{}/users/{}".format(SPOTIFY_API_URL, user_id)
    profile_data = requests.get(user_profile_api_endpoint, headers=authorization_header)
    print(profile_data.text)
    return json.loads(profile_data.text)


def get_track_info(auth_token):

    return


def get_recent_track_id(auth_token):

    return

# me
def get_current_track_id(access_token):
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}
    current_playing_api_endpoint = "{}/me/player/currently-playing".format(SPOTIFY_API_URL)
    current_playing_object = requests.get(current_playing_api_endpoint, headers=authorization_header)
    print(current_playing_object.text)
    return

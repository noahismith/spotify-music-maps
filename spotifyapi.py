import json
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
CLIENT_SIDE_URL = "http://127.0.0.1:5000"
REDIRECT_URI = CLIENT_SIDE_URL + "/callback"
SCOPE = "playlist-modify-public playlist-modify-private user-read-currently-playing user-read-recently-played user-modify-playback-state"
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


def get_auth_url():
    url_args = "&".join(["{}={}".format(key, urllib.quote(val)) for key, val in auth_query_parameters.iteritems()])
    return "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)


def post_request(url, data, headers):
    try:
        resp = requests.post(url, data=data, headers=headers)
    except requests.exeptions.RequestException as e:
        print(e)
        return {"error": e}
    return json.loads(resp.text)


def get_request(url, headers):
    try:
        resp = requests.get(url, headers=headers)
    except requests.exeptions.RequestException as e:
        print("Exception ERROR: ", e)
        return {"error": e}
    print(resp)
    return json.loads(resp.text)


def get_tokens(auth_token):
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    base64encoded = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET))
    headers = {"Authorization": "Basic {}".format(base64encoded)}
    return post_request(SPOTIFY_TOKEN_URL, code_payload, headers)


def get_profile_me(access_token):
    authorization_header = {"Authorization":"Bearer {}".format(access_token)}
    api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    print(api_endpoint)
    return get_request(api_endpoint, authorization_header)


def get_profile(access_token, user_id):
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}
    api_endpoint = "{}/users/{}".format(SPOTIFY_API_URL, user_id)
    return get_request(api_endpoint, authorization_header)


def get_track(access_token, track_id):
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}
    api_endpoint = "{}/tracks/{}".format(SPOTIFY_API_URL, track_id)
    return get_request(api_endpoint, authorization_header)


def get_recent_track_me(access_token):
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}
    api_endpoint = "{}/me/player/recently-played".format(SPOTIFY_API_URL)
    return get_request(api_endpoint, authorization_header)['items'][0]['track']


def get_current_track_me(access_token):
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}
    api_endpoint = "{}/me/player/currently-playing".format(SPOTIFY_API_URL)
    return get_request(api_endpoint, authorization_header)['item']


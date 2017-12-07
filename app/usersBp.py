from flask import Blueprint, json, request, jsonify, render_template

users_blueprint = Blueprint('users', __name__)

from .models import *


def get_user(user_id):
    return db.session.query(User).filter_by(user_id=user_id).first()


def update(user_id, remote_addr, token):
    user = get_user(user_id)
    if user is None:
        return {"error": "User does not exist"}

    user.ip = remote_addr
    user.token = token
    track = get_current_track_me(token)
    if "error" in track:
        track = get_recent_track_me(token)
        if "error" in track:
            user.track_id = None
        else:
            # TODO: get the time within the object
            user.track = track['id']
            location = get_location(user.ip)
            print(track['timestamp'])
            new_marker = Marker(user_id, user.track, location['lat'], location['lng'], datetime.utcnow)
    else:
        user.track = track['id']
        location = get_location(user.ip)
        new_marker = Marker(user_id, user.track, location['lat'], location['lng'], datetime.utcnow)




    return


# TODO: edits for local tests
def get_location(ip):
    send_url = 'http://ip-api.com/json/' + ip
    try:
        resp = requests.get(send_url)
    except requests.exeptions.RequestException as e:
        print(e)
        #return {"error": e}
        return {"lat": 0, "lng": 0}
    resp_json = json.loads(resp.text)
    if resp_json['status'] == 'fail':
        #return {"error": "fail"}
        return {"lat": 0, "lng": 0}
    return resp_json

from app import db
from datetime import datetime
from spotifyapi import *


class User(db.Model):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), unique=True, nullable=False)
    track_id = db.Column(db.String(255), nullable=True)
    ip = db.Column(db.String(255), nullable=True)
    token = db.Column(db.String(255), nullable=False)

    def __init__(self, user_id, track_id, ip, token):
        self.user_id = user_id
        self.track_id = track_id
        self.ip = ip
        self.token = token

    def __repr__(self):
        return 'id: {}, user_id: {}, track_id: {}, ip: {}, token: {}'.format(self.id, self.user_id, self.track_id, self.ip, self.token)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, remote_addr, token):
        track = get_current_track_me(token)
        if "error" in track:
            track = get_recent_track_me(token)
            if "error" in track:
                self.track_id = self.track_id
            else:
                self.track_id = track['id']
        else:
            self.track_id = track['id']
            db.session.commit()

        self.ip = remote_addr
        self.token = token
        self.save()



    @staticmethod
    def get_all():
        return User.query.all()


class Follower(db.Model):

    __tablename__ = 'Followers'

    id = db.Column(db.Integer, primary_key=True)
    user_from = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete='CASCADE'), nullable=False)
    user_to = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete='CASCADE'), nullable=False)

    user_from_rel = db.relationship('User', backref=db.backref('user_from', passive_deletes=True), foreign_keys=user_from)
    user_to_rel = db.relationship('User', backref=db.backref('user_to', passive_deletes=True), foreign_keys=user_to)

    def __init__(self, user_from, user_to):
        self.user_from = user_from
        self.user_to = user_to

    def __repr__(self):
        return 'id: {}, user_from: {}, user_to: {}'.format(self.id, self.user_from, self.user_to)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_followers(self):
        followers = db.session.query_property(Follower).filter_by(user_to=self.user_to).all()
        return followers

    def get_following(self):
        following = db.session.query_property(Follower).filter_by(user_from=self.user_from).all()
        return following


class Marker(db.Model):

    __tablename__ = 'Markers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('Users.id', ondelete='CASCADE'), nullable=False)
    track_id = db.Column(db.String(255), nullable=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_rel = db.relationship('User', backref=db.backref('user_marker', passive_deletes=True), foreign_keys=user_id)

    def __init__(self, user_id, track_id, lat, lng):
        self.user_id = user_id
        self.track_id = track_id
        self.lat = lat
        self.lng = lng

    def __repr__(self):
        return 'id: {}, user_id: {},  track_id: {}, lat: {}, lng {}'.format(self.id, self.user_id, self.track_id, self.lat, self.lng)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Marker.query.all()

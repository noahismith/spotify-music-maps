from run import db

class User(db.Model):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.Integer, unique=True, nullable=False)
    track_id = db.Column(db.Integer, nullable=True)
    lat = db.Column(db.Float, nullable=True)
    lon = db.Column(db.Float, nullable=True)

    def __init__(self, spotify_id, track_id, lat, lon):
        self.spotify_id = spotify_id
        self.track_id = track_id
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return 'id: {}, spotify_id: {}, track_id: {}, lat: {}, lon: {}'.format(self.id, self.spotify_id, self.track_id,
                                                                               self.lat, self.lon)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        # TODO: get recent track_id, lat, and lon
        self.track_id = 0
        self.lat = 0
        self.lon = 0
        self.save()

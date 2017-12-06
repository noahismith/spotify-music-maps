from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://noahismith:spotify-mmaps@spotify-mmaps.cnfthxsaxcoe.us-east-2.rds.amazonaws.com/spotifymmaps'
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True
db = SQLAlchemy(app)

from models import User

@app.route("/")
def hello():
    return "Welcome to Spotify Music Maps!"

@app.route("/test")
def create_user():
    new_user = User(0, 0, 0.1, 0.2)
    new_user.save()
    return new_user.__repr__()


if __name__ == "__main__":
    app.run()

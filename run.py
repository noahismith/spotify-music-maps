from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():
    return "Welcome to Spotify Music Maps!"
if __name__ == "__main__":
    app.run()

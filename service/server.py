from flask import Flask


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Welcome to Flask!'


@app.route("/ping")
def ping():
    return "Cats Service. Version 0.1"


if __name__ == "__main__":
    app.run(host="localhost", port=8080)

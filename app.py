from flask import Flask

app = Flask(__name__)

@app.route("/apod")
def apod():
    return "OK"
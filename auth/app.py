from flask import Flask


application = Flask(__name__)


@application.route("/", methods=["GET"])
def home():
    return "<h1>Bem-vindo(a)</h>"
from backendAPI import API
from config import engine
from json import dumps
from flask import Flask, request


api = API(engine)
app = Flask("debugServer")


@app.route("/user", methods=["GET", "POST"])
def queryUser():
    if request.method == "GET":
        uuid = request.args.get("uuid")
        return dumps(api.getUser(uuid))
    elif request.method == "POST":
        return dumps(api.addUser(**request.form.to_dict()))

@app.route("/echo", methods=["GET"])
def echo():
    return request.args.get("echo")


app.run(host="0.0.0.0", port=24135)

from backendAPI import API
from createTables import tables
from config import engine, DEBUG, PORT, Config
from json import dumps
from flask import Flask, request, render_template
#from flask import Blueprint
#from cos import sign 
from cam.auth.cam_url import CamUrl
import urllib.request


import os

__all__ = ["app"]

api = API(engine)

# turn the template folder and static folder to absolute path
# so that you can start the server in any working folder
curdir = os.path.abspath(os.path.dirname(__file__))
template_folder = os.path.join(curdir, "templates")
static_folder = os.path.join(curdir, "static")

app = Flask("create404", template_folder=template_folder, static_folder=static_folder)

# the sign and upload file blueprint
#app.register_blueprint(sign, url_prefix='/sign', template_folder=template_folder, static_folder=static_folder)


@app.errorhandler(404)
def page_not_found(_):
    return "Page not found."

@app.route("/", methods=["GET"])
def getIndex():
    return '<script>s="It works! ";for(i=0;i<11;i++) s+=s;document.write(s);</script>'


@app.route('/sign', methods=["GET"])
def signcos():
    policy = Config.POLICY
    secret_id = Config.SECRET_ID
    secret_key = Config.SECRET_KEY
    duration = Config.DURATION_SECOND
    url_generator = CamUrl(policy, duration, secret_id, secret_key)
    real_url = url_generator.url()
    print(real_url)
    proxy_handler = urllib.request.ProxyHandler({'https': '10.14.87.100:8080'})
    opener = urllib.request.build_opener()
    r = opener.open(real_url)
    response = r.read()
    #print(response)
    return response


@app.route("/api", methods=["GET", "POST"])
def dealRequests():
    if request.method == "GET":
        form = request.args.to_dict()
    elif request.method == "POST":
        form = request.form.to_dict()
    else:
        return "supported method: get, post."
    result = api.postCallAPI(form)
    return dumps(result)

if DEBUG:
    # all debug interface
    @app.route("/debugapi/", methods=["GET", "POST"])
    def queryAPIWithoutTable():
        return "Page not found. Url format: /debugapi/tablename"

    @app.route("/debugapi/<table>", methods=["GET", "POST"])
    def queryAPI(table):
        tableName = table.lower()
        if request.method == "GET":
            getArgs = request.args.to_dict()
            result = api.commonGetAPI(tableName, **getArgs)
            return dumps(result)

        elif request.method == "POST":
            postForm = request.form.to_dict()
            result = api.commonAddAPI(tableName, **postForm)
            return dumps(result)

    @app.route("/echo", methods=["GET"])
    def echo():
        return request.args.get("echo")

    @app.route("/debug/", methods=["GET", "POST"])
    def debugPageWithoutTable():
        return "Page not found. Url format: /debug/tablename"

    @app.route("/debug/<table>")
    def debugPage(table):
        tableName = table.lower()
        if tableName not in tables:
            return "Table %s not found." % tableName
        fields = tables[tableName].__requiredFields__
        return render_template("debugPage.html", fields=fields, tableName=tableName)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

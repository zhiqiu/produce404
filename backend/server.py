from backendAPI import API
from createTables import Tables
from config import engine, DEBUG, PORT
from json import dumps
from flask import Flask, request, render_template

__all__ = ["app"]

api = API(engine)
app = Flask("create404", template_folder='backend/templates')

@app.errorhandler(404)
def page_not_found(_):
    return "Page not found."

@app.route("/", methods=["GET"])
def getIndex():
    return '<script>s="It works! ";for(i=0;i<11;i++) s+=s;document.write(s);</script>'

@app.route("/api", methods=["POST"])
def dealRequests():
    form = request.form.to_dict()
    action = form["action"]
    result = getattr(api, API.allAPI[action])(form)
    return dumps(result)

if DEBUG:
    # all debug interface
    @app.route("/debugapi/", methods=["GET", "POST"])
    def queryAPIWithoutTable():
        return "Page not found. Url format: /api/tableName"

    @app.route("/debugapi/<table>", methods=["GET", "POST"])
    def queryAPI(table):
        tableName = table[0].upper() + table[1::].lower()

        if request.method == "GET":
            getArgs = request.args.to_dict()
            print(getArgs)
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
        return "Page not found. Url format: /debug/tableName"

    @app.route("/debug/<table>")
    def debugPage(table):
        tableName = table[0].upper() + table[1::].lower()
        if tableName not in dir(Tables):
            return "Table %s not found." % tableName
        fields = getattr(Tables,tableName).requiredFields
        return render_template("debugPage.html", fields=fields, tableName=tableName)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

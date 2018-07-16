from databaseAPI.backendAPI import API
from databaseAPI.defineTables import tables
from databaseAPI.config import Config
from databaseAPI.utils import jsonDumps, logger
from flask import Flask, request, render_template
import os

from flask import send_file, send_from_directory

__all__ = ["app"]

# flask port for debugging
DEBUG = True
PORT = 24135

api = API(Config.engine)

# turn the template folder and static folder to absolute path
# so that you can start the server in any working folder
curdir = os.path.abspath(os.path.dirname(__file__))
template_folder = os.path.join(curdir, "templates")
static_folder = os.path.join(curdir, "static")

app = Flask("create404", template_folder=template_folder, static_folder=static_folder)

@app.errorhandler(404)
def page_not_found(_):
    return "Page not found.", 404

@app.route("/", methods=["GET"])
def getIndex():
    logger.info("Request: %s /" % (request.method,))
    return '<script>s="It works! ";for(i=0;i<11;i++) s+=s;document.write(s);</script>'


@app.route('/<filename>')
def send_file(filename):
    logger.info("Request: %s /%s" % (request.method, filename))
    directory = os.getcwd()
    return send_from_directory(directory, filename, as_attachment=True)


@app.route("/api", methods=["GET", "POST"])
def dealRequests():
    logger.info("Request: %s /api" % (request.method,))
    if request.method == "GET":
        form = request.args.to_dict()
    elif request.method == "POST":
        form = request.form.to_dict()
    else:
        logger.warning("supported method: get, post.")
        return "supported method: get, post."
    logger.info("Request form: %s" % jsonDumps(form))
    result = api.postCallAPI(form)
    return jsonDumps(result)

if DEBUG:
    # all debug interface
    @app.route("/debugapi/", methods=["GET", "POST"])
    def queryAPIWithoutTable():
        logger.info("Request: %s /debugapi" % (request.method,))
        return "Table not found. Url format: /debugapi/tablename"

    @app.route("/debugapi/<table>", methods=["GET", "POST"])
    def queryAPI(table):
        logger.info("Request: %s /debugapi/%s" % (request.method,table))
        tableName = table.lower()
        if request.method == "GET":
            getArgs = request.args.to_dict()
            logger.info("Request form: %s" % jsonDumps(getArgs))
            result = api.commonGetAPI(tableName, **getArgs)
            return jsonDumps(result)

        elif request.method == "POST":
            postForm = request.form.to_dict()
            logger.info("Request form: %s" % jsonDumps(postForm))
            result = api.commonAddAPI(tableName, **postForm)
            return jsonDumps(result)

    @app.route("/echo", methods=["GET"])
    def echo():
        return request.args.get("echo")

    @app.route("/debug/", methods=["GET", "POST"])
    def debugPageWithoutTable():
        logger.info("Request: %s /debug" % (request.method,))
        return "Table not found. Url format: /debug/tablename"

    @app.route("/debug/<table>")
    def debugPage(table):
        logger.info("Request: %s /debug/%s" % (request.method,table))
        tableName = table.lower()
        if tableName not in tables:
            logger.warning("Table %s not found." % tableName)
            return "Table %s not found." % tableName
        fields = tables[tableName].__requiredFields__
        return render_template("debugPage.html", fields=fields, tableName=tableName)

    @app.route('/testcos')
    def testcos():
        logger.info("Request: %s /testcos" % (request.method,))
        return render_template("test.html")

if __name__ == "__main__":

    logger.info("Debug API %sabled." % "en" if DEBUG else "dis")
    logger.info("Flask server: %s:%d" % ("0.0.0.0", PORT))

    app.run(host="0.0.0.0", port=PORT)

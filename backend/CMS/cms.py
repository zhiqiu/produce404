from flask import Flask, request, render_template, flash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from flask_admin.model.template import macro
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, TIMESTAMP, BOOLEAN, ForeignKey, and_
import hashlib
import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)

from databaseAPI.backendAPI import API
from databaseAPI.defineTables import Creatable
from databaseAPI.defineTables import *
from databaseAPI.config import Config
from databaseAPI.utils import jsonDumps

__all__ = ["app"]

DEBUG = True
PORT = 8080

api = API(Config.engine)



# turn the template folder and static folder to absolute path
# so that you can start the server in any working folder
curdir = os.path.abspath(os.path.dirname(__file__))
template_folder = os.path.join(curdir, "template")

static_folder = os.path.join(curdir, "static")

app = Flask("create404", template_folder=template_folder, static_folder=static_folder)
app.secret_key = '123456'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
session = sessionmaker(bind=Config.engine)()

class AdminModelView(ModelView):
    column_display_pk = True
    can_export                  = True
    can_view_details            = True
    export_types                = ['xls']
    column_formatters           = dict(user=lambda v, c, m, p: m.email)

    def is_accessible(self):
        return True
        #return current_user.is_authenticated and (current_user.superuser or current_user.email in U.superuser_set)

    def inaccessible_callback(self, name, **kwargs):
        return 'logout'


class AdminAudioModelView(ModelView):
    edit_template = "test.html"
    can_export = True
    can_view_details = True
    export_types = ['xls']
    column_display_pk = True
    # column_display_all_relations               = True
    column_formatters = dict(url=macro('render_audio'))
    def is_accessible(self):
        return True
        return current_user.is_authenticated and (current_user.superuser or current_user.email in U.superuser_set)



class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return U.redirect('../../login')

admin = Admin(app, url = '/admin', name = 'create404', template_mode = 'bootstrap3')


admin.add_view(AdminModelView(User, api.session))
admin.add_view(AdminModelView(Audio, api.session))
admin.add_view(AdminModelView(AudioTag, api.session))
admin.add_view(AdminModelView(Medal, api.session))
admin.add_view(AdminModelView(Comment, api.session))
admin.add_view(AdminModelView(Collection, api.session))
admin.add_view(AdminModelView(R_User_Create_Audio, api.session))
admin.add_view(AdminModelView(R_Audio_Has_AudioTag, api.session))
admin.add_view(AdminModelView(R_User_Has_Medal, api.session))
admin.add_view(AdminModelView(R_User1_Follow_User2, api.session))
admin.add_view(AdminModelView(R_Audio_In_Collection, api.session))
admin.add_view(AdminModelView(R_User_Like_Audio, api.session))
admin.add_view(AdminModelView(R_User_Like_Comment, api.session))
admin.add_view(AdminModelView(Message, api.session))
admin.add_view(LogoutView(name = 'Logout', endpoint = 'logout'))


@login_manager.user_loader
def load_user(userid):
    return session.query(CMSUser).filter_by(id=int(userid)).first()


class U:
    @staticmethod
    def redirect(uri):
        return render_template('redirect.html', uri = uri)


@app.route('/')
def index_default():
    return U.redirect('login')






@app.route('/login', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        logout_user()
        return render_template('login.html')

    if request.method == 'GET':
        return render_template('login.html')
    else:
        login = request.form.to_dict()

        md5 = hashlib.md5()
        md5.update(login['password'].encode('utf-8'))
        md5password = md5.hexdigest()

        # check user existence
        user = session.query(CMSUser).filter(and_(
            CMSUser.email == login['email'],
            CMSUser.password == md5password
        )).first()
        if not user:
            flash('no user', 'error')
            return U.redirect('login')
        # autologin
        login_user(user, 'off')

        return U.redirect('admin')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return render_template('login.html')

#adminuser = User.create('admin@admin', 'admin')


@app.errorhandler(404)
def page_not_found(_):
    return "Page not found.", 404


@app.route("/", methods=["GET"])
def getIndex():
    return '<script>s="It works! ";for(i=0;i<11;i++) s+=s;document.write(s);</script>'


@app.route("/myaudio", methods=["GET"])
def getaudio():
    return render_template('audio.html')


@app.route("/api", methods=["GET", "POST"])
def dealRequests():
    if request.method == "GET":
        form = request.args.to_dict()
    elif request.method == "POST":
        form = request.form.to_dict()
    else:
        return "supported method: get, post."
    result = api.postCallAPI(form)
    return jsonDumps(result)


if DEBUG:
    # all debug interface
    @app.route("/debugapi/", methods=["GET", "POST"])
    def queryAPIWithoutTable():
        return "Table not found. Url format: /debugapi/tablename"


    @app.route("/debugapi/<table>", methods=["GET", "POST"])
    def queryAPI(table):
        tableName = table.lower()
        if request.method == "GET":
            getArgs = request.args.to_dict()
            result = api.commonGetAPI(tableName, **getArgs)
            return jsonDumps(result)

        elif request.method == "POST":
            postForm = request.form.to_dict()
            result = api.commonAddAPI(tableName, **postForm)
            return jsonDumps(result)


    @app.route("/echo", methods=["GET"])
    def echo():
        return request.args.get("echo")


    @app.route("/debug/", methods=["GET", "POST"])
    def debugPageWithoutTable():
        return "Table not found. Url format: /debug/tablename"


    @app.route("/debug/<table>")
    def debugPage(table):
        tableName = table.lower()
        if tableName not in tables:
            return "Table %s not found." % tableName
        fields = tables[tableName].__requiredFields__
        return render_template("debugPage.html", fields=fields, tableName=tableName)


    @app.route('/testcos')
    def testcos():
        return render_template("test.html")

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=PORT)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_admin import Admin
from flask_ckeditor import CKEditor


app  = Flask(__name__)



'''@app.route("/")
def hello():
    return jsonify({"about": "HelloWorld!"})

if __name__=='__main__':
    app.run(debug=True)'''

app.config['SECRET_KEY'] = 'Thisisasecret!'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


import myblog.forms as views
admin = Admin(app)
#admin.add_view(views.HelloView(name='Hello'))

from flask_admin.contrib.sqla import ModelView

#admin.add_view(ModelView(views.User, db.session))
admin.add_view(views.UserAdminView(views.User, db.session))
ckeditor = CKEditor(app)

def blog_formating(content):
    return (content[:50] + '...') if len(content) > 50 else content

app.jinja_env.globals.update(blog_formating=blog_formating)

from myblog import routes


from flask_sqlalchemy import SQLALCHEMY
from flask import  FLask



app  = Flask(__name__)



basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir , 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON _TEARDOWN'] = True



db = SQLALCHEMY(app)

class Roles(db.model) :
    __tablename_ = 'roles'
    id = db.column(db.Integer , Primary_key = True)
    name = db.column(db.String(20) , Unique  = True)
    users  = db.relationship('Users' , backref = 'role')
    def __repr__(self):
        return 'roles %r' %self.name


class Users(db.model):
    __tablename_ = 'users'
    id = db.column(db.Integer, Primary_key=True)
    username = db.column(db.String(20), Unique=True)
    role_id = db.column(db.Integer , db.ForiegnKey('roles.id'))
    def __repr__(self):
        return 'users %r' % self.username


if __name__ == __main__ :
    app.run(debug = True)


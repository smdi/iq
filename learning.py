from flask import Flask , render_template , redirect ,  url_for , flash , session
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import  datetime
from flask_wtf import Form
from wtforms import StringField , SubmitField
from wtforms.validators import Required , Email
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate ,MigrateCommand
import os.path




app = Flask(__name__)
bootstrap = Bootstrap(app)
moment  = Moment(app)
app.config['SECRET_KEY'] = 'immuhamziza'




basedir  = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate  = Migrate(app , db)

manager = Manager(app)
manager.add_command('db' , MigrateCommand)

def make_shell_context() :
    return dict(app = app ,db = db , Users = Users , Roles  = Roles)
manager.add_command('shell' , Shell(make_context = make_shell_context))


class Roles(db.Model):
  __tablename__  = 'roles'
  id  = db.Column(db.Integer , primary_key = True)
  name  = db.Column(db.String(64) , unique = True)
  users = db.relationship('Users',backref = 'role' , lazy = 'dynamic')
  def __repr__(self):
      return  'role %r' %self.name



class Users(db.Model):
    __tablename__  = 'users'
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String , unique = True , index = True)
    roles_id = db.Column(db.Integer ,db.ForeignKey('roles.id'))
    def __repr__(self):
        return 'user %r' %self.username


class NameForm(Form):
    question    = StringField('Whats your question ? Whats on your mind' , validators=[Required()])
    name        = StringField('Enter your name',validators= [Required()])
    submit      = SubmitField('Request Question')


@app.route('/',methods = ['GET','POST'])
def index() :
    form  = NameForm()
    if form.validate_on_submit() :
        user = Users.query.filter_by(username = form.name.data).first()
        if user is None :
            user = Users(username = form.name.data)
            db.session.add(user)
            db.session.commit()
            session['question'] = form.question.data
            session['known'] = False
        else:
            session['known'] = True
        session['question']  = form.question.data
        session['name']      = form.name.data
        return redirect(url_for('index'))
    return  render_template('index.html',current_time = datetime.utcnow() , question = session.get('question') , name = session.get('name') , form  = form , known = session.get('known',False))


@app.route('/user/<name>')
def user(name) :
    return  render_template('user.html' , name=name)


@app.errorhandler(404)
def page_not_found(e):
    return  render_template('404.html') , 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html') , 500


#
# if __name__ == '__main__':
#
#     app.run(debug=True)



if __name__ == '__main__':
    manager.run()

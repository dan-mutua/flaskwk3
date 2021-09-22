from flask import Flask,render_template,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_user,login_required,LoginManager,logout_user,current_user
from flask_wtf import FlaskForm
from flask_wtf.form import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.form import Form
from wtforms.validators import InputRequired,Length,ValidationError
from flask_bcrypt import Bcrypt
from ..email import mail_message
from ..models import User,loginForm,RegisterForm



app = Flask(__name__)
db=SQLAlchemy(app)
bcrypt= Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] =''
app.config['SECRET_KEY'] = 'lion22'

Login_Manager= LoginManager()
Login_Manager.init_app(app)
Login_Manager.login_view = "login"

@app.route('/login',methods=['GET','POST'])
def login():
  Form=loginForm()
  if Form.validate_on_submit():
    user = User.query.filter_by(username=Form.username.data).first()
    if user:
      if bcrypt.check_password_hash(user.password,Form.password.data):
        login_user(user)
        return redirect(url_for('pitches'))
  return render_template("login.html", form=Form)
    

@app.route('/pitches',methods=['GET','POST'] )
@login_required
def pitches():
  return render_template('pitches.html')


@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
  login_user()
  return redirect(url_for('login'))

@app.route('/signup',methods=['GET','POST'])
def signup():
  Form= RegisterForm()

  if Form.validate_on_submit():
     hashed_password= bcrypt.generate_password_hash(Form.password.data)
     new_user = User(username=Form.username.data, password= hashed_password)
     db.session.add(new_user)
     db.session.commit()

     
     return url_for(login)
  return render_template("signup.html", form=Form)
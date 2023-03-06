"""
moodule docstring
"""

from datetime import timedelta
from functools import wraps
import os
import re
import datetime

from flask import Flask
from flask import flash, redirect, session, url_for
from flask import request, render_template
from flask import jsonify

from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap

from flask_login import LoginManager, login_required
from flask_login import UserMixin, login_user, login_required
from flask_login import logout_user, current_user

from flask_migrate import Migrate
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, EmailField

from wtforms.validators import DataRequired, Length, Email, EqualTo,Regexp
from wtforms.validators import InputRequired

import psycopg2

from model import db
from flask_change_password import ChangePassword, ChangePasswordForm, SetPasswordForm


app = Flask(__name__)
"""
P_HOST0 = 'postgres://ldqtkymuvcsnlr:'

P_HOST1 = 'd8a8cbb1f77ae9f99769c29a85a42f7df830e670aacfa'
P_HOST2 = '0afd6a5476d85743200@ec2-3-209-39-2.compute-1.'
P_HOST3 = 'amazonaws.com:5432/dipeglem2kl7d'

P_HOST = P_HOST0 + P_HOST1 + P_HOST2 + P_HOST3

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', P_HOST)
app.config['SECRET_KEY'] = '9f4b5227ab07794dc2b3b390c7951793'
"""
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres@benso7130@panasonic"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY'] = '9f4b5227ab07794dc2b3b390c7951793'

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'

bootstrap = Bootstrap(app)

bcrypt = Bcrypt()
gen_pass = bcrypt.generate_password_hash



@login_manager.user_loader
def load_user(email):
    """Function's docstring"""

    if email not in account:  # pylint: disable=unsupported-membership-test
        return None

    return account.query.get(email)


@app.before_request
def session_handler():
    """Function's docstring"""
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)


def is_logged_in(function):
    """Function's docstring"""
    @wraps(function)
    def wrap(*args, **kwargs):
        """Function's docstring"""
        if 'logged_in' in session:
            return function(*args, **kwargs)
        flash('Unauthorized, please login', 'danger')
        return redirect(url_for('login'))
    return wrap


@app.route("/")
def home():
    """Function's docstring"""
    return render_template('home.html')


# @get_services_id
@app.route("/services")
def service():
    """
    Services router
    """

    # if not session.get("email"):
    #     return redirect("/login")

    return render_template("services.html")


@app.route("/services/pharmaceuticals")
def pharmaceuticals():
    """
    Pharmaceuticals router
    if not session.get("email"):
        return redirect("/login")

    id = get_services_id()
    print(session["email"], id)
    """

    return render_template("Pharmaceuticals.html")


@app.route("/services/medical-supplies")
def medical_supplies():
    """
    Medical supplies...
    if not session.get("email"):
        return redirect("/login")

    id = get_services_id()
    print(session["email"], id)
    """

    return render_template("medical-supplies.html")


@app.route("/why-us")
def why():
    """
    About us router
    """
    return render_template("why-us.html")


@app.route("/why-us/about")
def about():
    """
    About us router
    """
    return render_template("about.html")


@app.route("/contact")
def contact():
    """
    Contact us router
    """

    return render_template("contact.html")


class RegistrationForm(FlaskForm):
    """Class docstring"""

    firstname = StringField('firstname', validators=[
        InputRequired(), Length(min=2, max=30)])
    lastname = StringField('lastname', validators=[
        InputRequired(), Length(min=2, max=30)])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),Length(min=8,message='Password should be at least %(min)d characters long')])

    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', "Passwords must match")])

    submit = SubmitField('Sign up')
    
def validate_password(password: str) -> bool:
    special_chars = ['$', '!', '@', '#', '%', '&']
    return all([
        any(list(map(str.isupper, password), message="Password should have at least one uppercase letter")),
        any(list(map(str.isdigit, password),message="Password should have at least one number")),
        any(list(map(str.islower, password),message="Password should have at least one lowercase letter")),
        any(list(map(str.isalpha, password))),
        any(list(map(str.isprintable, password))),
        len([char for char in special_chars if char in password]) > 0,
        len(password) > 8 and len(password) < 18,
    ])


@app.route('/signup', methods=['GET', 'POST'])
def register():
    """Function's docstring"""

    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        password = form.password.data
        
        # conn = mysql.connect
        # cursor = conn.cursor()

        #conn = psycopg2.connect(P_HOST, sslmode='require')

        #cursor = conn.cursor()
        conn = psycopg2.connect (user = "postgres", password = "@benso7130", host = "localhost", database = "panasonic")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM account WHERE email = %s", (email,))
        result = cursor.fetchone()
        
        password = gen_pass(form.password.data,10).decode('utf-8')
        
        if not result:
            try:
                # Execute Query
                cursor.execute("""INSERT INTO account
                    (firstname, lastname, email, password)
                    VALUES(%s, %s, %s, %s)""",
                    (firstname, lastname, email,  password))
                
                print((firstname, lastname, email,  password))
                # Commit to DB
                conn.commit()           
            except:     
                return redirect(url_for('register'))
            else:
                # Close cursor
                cursor.close()
                flash("Successful registration", "success")
            return redirect(url_for('new_delivery',email=None))
        else:
            flash("Already Registered! Please Login", 'danger')
            cursor.close()   
    #Get request
    return render_template('signup.html', form=form, title="Register")


@app.route('/new-delivery', methods=['POST', 'GET'])
def new_delivery():
    """Function's docstring"""

    #conn = psycopg2.connect(P_HOST, sslmode='require')

    #cursor = conn.cursor()
    conn = psycopg2.connect (user = "postgres", password = "@benso7130", host = "localhost", database = "panasonic")
    cursor = conn.cursor()

    if request.method == 'POST':

        first_name = request.form.get("fname")
        last_name = request.form.get("lname")
        email = request.form.get("email")
        address = request.form.get("address")
        phone_no = request.form.get("phone_no")
        product = request.form.get("value_select")
        dtime = request.form.get("pickup_time")
        special_instructions = request.form.get("instructions")

        data = (first_name, last_name, email, address, phone_no,
                product, dtime, special_instructions,)

        query = """INSERT INTO delivery (first_name, last_name,
        email, address, phone_no, product, dtime, special_instructions)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""

        # conn = mysql.connect
        # cursor = conn.cursor()

        cursor.execute(query, data)
        conn.commit()

        query1 = f"""SELECT order_id FROM delivery WHERE email='{email}'"""

        cursor.execute(query1)
        order_id = cursor.fetchone()

        cursor.close()
        conn.close()

        if order_id:
            return render_template('order-success.html',
                                   order_id=order_id[0])

    return render_template('delivery.html')


class LoginForm(FlaskForm):
    """Class docstring"""

    email = EmailField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password',validators=[InputRequired()])
    submit = SubmitField('Login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Function's docstring"""

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password_candidate = form.password.data
        
        #conn = psycopg2.connect(P_HOST, sslmode='require')
        #cursor = conn.cursor()
        conn = psycopg2.connect (user = "postgres", password = "@benso7130", host = "localhost", database = "panasonic")
        cursor = conn.cursor()

        try:
            # Get User by email
            cursor.execute("SELECT * FROM account WHERE email=%s", [email])
            result = cursor.fetchone()
            password = result[-1]
            #password = cursor.execute("SELECT password fROM account WHERE email=%s", [email])
            print(result)
        except:
            flash("Please Register! ", "danger")
        else:
            if result:
                # Compare Passwords
                if bcrypt.check_password_hash(password, password_candidate):
                    session['logged_in']= True
                    session['email'] = email
                    print(session['email'])
                    #flash("Log-in successfully", "success")             
                    return redirect(url_for('new_delivery'))
                else:
                    flash('Incorrect password', 'danger')
                    return render_template('login.html',form=form)
            else:
                # User email doesn't exist
                flash("Email not found! Register", "danger")
                return render_template('signup.html', form=form)
    return render_template('login.html', form=form)


@login_required
@app.route('/logout')
def logout():
    """Function's docstring"""
    #session.clear()
    logout_user()
    flash("You are now logged out", "success")
    return redirect(url_for('home'))


class UpdateAccountForm(FlaskForm):
    """Class docstring"""

    email = EmailField('Email', validators=[InputRequired(), Email()])
    submit = SubmitField('update')


class RequestResetForm(FlaskForm):
    """Class docstring"""

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Forgot Password')


class ResetPasswordForm(FlaskForm):
    """Class docstring"""

    email = EmailField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Reset Password')


@app.route('/change', methods=['GET', 'POST'])
def change():
    """Function's docstring"""

    form = ResetPasswordForm(request.form)
    #msg = ''
    if request.method == "POST":
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        
        # and \'email' in request.form and \
        #'password' in request.form and \
            #'confirm_password' in request.form:
            
        # Create Cursor
        #conn = psycopg2.connect(P_HOST, sslmode='require')
        #cursor = conn.cursor()
        conn = psycopg2.connect (user = "postgres", password = "@benso7130", host = "localhost", database = "panasonic")
        cursor = conn.cursor()

        # Get User by email
        cursor.execute("SELECT * FROM account WHERE email=%s", [email])
        acc = cursor.fetchone()
        if acc:
            if password == confirm_password:
                hashed_pass = gen_pass(password).decode('utf-8')
                cursor.execute("""UPDATE account SET password = %s where email = %s """,(hashed_pass, acc[3]))
        
                #Commit to DB
                conn.commit()
                flash("Password changed successfully", "success")
                return redirect(url_for('login'))
            else:
                cursor.close()
                flash("New password and confirm password are not matched")
                return redirect(url_for('change'))         
        else:
            flash("Invalid email, Please SIGN UP","danger")
            cursor.close()
            return render_template('signup.html', form=RegistrationForm())
    return render_template('change.html', title='Reset Password',form=form)


@app.context_processor
def inject_current_user():
    """
    Inject the current logged-in user as a variable
    into the context of the application templates
    """

    return dict(current_user=current_user)

@login_required
@app.route('/show-orders')
def show():
       
    #conn = psycopg2.connect(P_HOST, sslmode='require')
    conn = psycopg2.connect (user = "postgres", password = "@benso7130", host = "localhost", database = "panasonic")

    cursor = conn.cursor()
    email = dict(session)['email']
    cursor.execute("SELECT * FROM delivery WHERE email = %s",(email,))
    result = cursor.fetchall()
    date = datetime.date.today()
    print(date)
    cursor.close()
    #print(result)
    if result:
        return render_template('show.html', result=result)
    else:
        flash("You have NO Delivery order","danger")
        return render_template('delivery.html')


@app.route('/account')
@login_required
def account():
    """Function's docstring"""

    #conn = psycopg2.connect(P_HOST, sslmode='require')

    #cursor = conn.cursor()
"""
    form = UpdateAccountForm(request.form)
    if request.method == "POST" and 'email' in request.form:
        current_user.email = form.email.data
        conn.commit()
        flash('Your account has been updated!', 'success')
        cursor.close()

        conn.close()
        return redirect(url_for('service'))

    # elif request.method == 'GET':
    #     form.email.data = current_user.email

    cursor.close()
    conn.close()
    return render_template('account.html', title='Account', form=form)"""

@app.route('/new-delivery', methods=['GET', 'POST'])
def orders_insertion():
    """Function's docstring"""

    #conn = psycopg2.connect(P_HOST, sslmode='require')
    conn = psycopg2.connect (user = "postgres", password = "@benso7130", host = "localhost", database = "panasonic")

    cursor = conn.cursor()

    if request.method == 'POST':
        first_name = request.form.get("fname")
        last_name = request.form.get("fname")
        email = request.form.get("email")
        address = request.form.get("address")
        phone_no = request.form.get("phone_no")
        product = request.form.get("value_select")
        dtime = request.form.get("pickup_time")
        special_instructions = request.form.get("instructions")

        data = (first_name, last_name, email, address, phone_no,
                product, dtime, special_instructions,)

        query = "INSERT INTO delivery (%s,%s,%s,%s,%s,%s,%s,%s)"

        cursor.execute(query, data)
        conn.commit()

        cursor.close()
        conn.close()

        return render_template('index.html')

    return render_template('index.html')


port = int(os.environ.get("PORT", 5500))


if __name__ == '__main__':
    app.run(debug=True, port=port, host='0.0.0.0',use_reloader=False)

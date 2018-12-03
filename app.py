#!/usr/bin/python
# -*- coding: utf-8 -*-

# DESCRIPTION
"""
FLASK APPLICATION: SHOCKWAVE (SHK)
Cryptocurrency in python.
app.py is main program.
"""

__author__ = "Will Assad"
__copyright__ = "Copyright 2018, Shockwave"
__credits__ = ["Will Assad"]
__developers__ = ["willassad"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Will Assad"
__email__ = "willassadcode@gmail.com"
__status__ = "Production"

#IMPORTS
from flask import (Flask, render_template,
    flash, redirect, url_for,
    session, request, logging)
from cryptography.passwordtools import get_pass
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from functools import wraps
from appfuncs import *
from forms import *
import time
import os

#initialize app instance
app = Flask(__name__)

#use mysql to store datasets
# Configure MySQL settings
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = """YOUR MYSQL PASSWORD"""
app.config['MYSQL_DB'] = 'shockwave'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# initialize MySQL
mysql = MySQL(app)

"""WRAPS: verify if user is logged in,
   is a manager, or is a developer
"""

def sflash(message): flash(message, 'success')
def dflash(message): flash(message, 'danger')

#Check if user is logged in using wraps
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login.', 'danger')
            return redirect(url_for('login'))
    return wrap

#Check if user is logged in using wraps
def is_logged_out(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            flash('You are already logged in.', 'danger')
            return redirect(url_for('dashboard'))
        else:
            return f(*args, **kwargs)
    return wrap

#Check if user is developer using wraps
def is_developer(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session.get('username') in __developers__:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('dashboard'))
    return wrap


"""BASIC PAGES: /, /home
   ONLY HTML, BOOTSTRAP, CSS
"""
@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html")


@app.route("/blank")
@is_developer
def blank_page():
    return render_template("blank.html")


"""REGISTER AND LOGIN PAGES
"""

#Register page for students
@app.route("/register", methods = ['GET','POST'])
@is_logged_out
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        name = form.name.data

        if isnewuser(username) and isnewtable(username):
            password = sha256_crypt.encrypt(form.password.data)

            sql_raw(
                "INSERT INTO users(name,email,username,password)" +
                "VALUES(\"%s\", \"%s\", \"%s\", \"%s\")" %(
                    name,email,username,password
                )
            )

            send_money(username,0,True); log_in_user(username)
            sflash('Welcome to your dashboard %s.' %username)
            return redirect(url_for('dashboard'))

        else:
            dflash('User already exists.')
            return redirect(url_for('register'))

    return render_template('register.html', form=form)


def log_in_user(username):
    users = Table("users")
    user = users.getone("username", username)
    accpass = user.get('password')
    balances = getbalances()

    session['logged_in'] = True
    session['username'] = username
    session['name'] = user.get('name')
    session['email'] = user.get('email')
    session['balance'] = balances.get(username)

#Login page for students
@app.route("/login", methods=['GET','POST'])
@is_logged_out
def login():
    if request.method == 'POST':
        username = request.form['username']
        candidate = request.form['password']

        users = Table("users")
        user = users.getone("username", username)
        accpass = user.get('password')

        if accpass is None:
            dflash('Username "%s" not found.' %username)
            return redirect(url_for('login'))
        else:

            if sha256_crypt.verify(candidate, accpass):
                log_in_user(username)
                sflash('You are now logged in.')
                return redirect(url_for('dashboard'))
            else:
                dflash('Invalid username and/or password.')
                return redirect(url_for('login'))

    return render_template('login.html')


#Logout, ends current session
@app.route("/logout")
@is_logged_in
def logout():
    session.clear()
    sflash('You have now logged out.')
    return redirect(url_for('login'))

#Dashboard
@app.route("/dashboard", methods=['GET','POST'])
@is_logged_in
def dashboard():
    current_time = time.strftime("%I:%M %p")
    blockchain = getLastBlockchain()
    if not verifyBlockchain():
        dflash("Corrupt blockchain.")
        return redirect(url_for('index'))

    return render_template(
        'dashboard.html',
        page='dashboard',
        ct=current_time,
        blockchain=blockchain,
        session=session
    )

@app.route("/transaction", methods=['GET','POST'])
@is_logged_in
def transaction():
    form = SendMoneyForm(request.form)

    if request.method == 'POST' and form.validate():
        username = form.username.data
        amount = form.amount.data

        if not amount.isdigit():
            dflash('Must enter number value for amount.')
        elif int(amount) > session.get('balance'):
            dflash('Amount exceeds current balance.')
        elif username == session.get('username'):
            dflash('Cannot send money to yourself.')
        elif isnewuser(username):
            dflash('User does not exist, cannot send.')
        else:
            send_money(username,int(amount))
            sflash('%s SHK successfully sent to %s.' %(amount,username))

        return redirect(url_for('transaction'))

    return render_template(
        'transaction.html',
        page='transaction',
        form=form,
        session=session
    )


#Buy SHK
@app.route("/buy", methods=['GET','POST'])
@is_logged_in
def buy():
    form = BuyShockwave(request.form)

    if request.method == 'POST' and form.validate():
        amount = form.amount.data
        key = form.key.data

        if key == 'password':
            send_money(session.get('username'),int(amount),True)
            sflash('Transaction successful.')
        else:
            dflash('Transaction failed, incorrect key.')

        return redirect(url_for('buy'))

    return render_template(
        'buy.html',
        page='buy',
        form=form,
        session=session
    )


"""ERROR HANDLERS 404"""
#Handle 404 error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('handlers/404.html'), 404

#Run as main, not module
if __name__ == "__main__":
    if not internet_connected():
        print("CHECK CONNECTION.")
    else:
        app.secret_key = """YOUR APP SECRET KEY"""
        app.run(debug = True, port = 65013)

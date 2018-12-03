#!/usr/bin/python
# -*- coding: utf-8 -*-
# Project File: Python 2.x or 3.x

# DESCRIPTION
"""
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
from wtforms import (
    Form, StringField, DecimalField,
    IntegerField, TextAreaField, PasswordField,
    validators
)

"""FORMS: registration, login, messaging
   setup class for each
"""

#User registration form
class RegisterForm(Form):
    name = StringField('Full Name', [validators.Length(min=1,max=50)])
    username = StringField('Username', [validators.Length(min=4,max=25)])
    email = StringField('Email',[validators.Length(min=6,max=50)])
    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm',message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


#Send money form
class SendMoneyForm(Form):
    username = StringField('Username', [validators.Length(min=4,max=25)])
    amount = StringField('Amount',[validators.Length(min=1,max=50)])


#Buy SHK form
class BuyShockwave(Form):
    amount = StringField('Amount',[validators.Length(min=1,max=50)])
    key = StringField('Key', [validators.Length(min=4,max=25)])

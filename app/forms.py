#!/usr/bin/env python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, TextAreaField, DateField, HiddenField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import Conversations, Message

class SelectMessageForm(FlaskForm):
    message = QuerySelectField(query_factory=lambda: Message.query.all())

class ArbitraryMessageForm(FlaskForm):
    message = StringField('Message')

class AddMessageForm(FlaskForm):
    message = StringField('Message', validators=[DataRequired()])

class AddConversationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])


class BotForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    year_of_birth = IntegerField('Year of Birth')
    sex = SelectField('Sex', choices=[('M','Male'), ('F', 'Female')])


class RandomBotForm(FlaskForm):
    # conversation = QuerySelectField(query_factory=lambda: Conversations.query.all())
    hidden = HiddenField()
    amount = IntegerField('Number of bots to generate')
    date_range_start = IntegerField('Year of birth start', default=1950)
    date_range_end = IntegerField('Year of birth end', default=1990)
    sex = SelectField('Sex', choices=[('M','Male'), ('F', 'Female')])
    options = BooleanField('Filter ?', default=False)
    participant_id = BooleanField('Generate random participant ids ?', default=True)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
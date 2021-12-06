#!/usr/bin/env python
from threading import Lock
from flask import (render_template,
                   render_template_string,
                   session,
                   request,
                   copy_current_request_context,
                   flash,
                   redirect,
                   url_for,
                   jsonify)

from app import app, db
from app.utils import randomize_bot_names, token_generator
from app.forms import BotForm, RandomBotForm, AddMessageForm, LoginForm, AddConversationForm
from app.models import Bot, Message, Conversations, User
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import func
import datetime
import functools
from flask_login import current_user, login_user, logout_user, login_required

async_mode = None
thread = None
thread_lock = Lock()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    form = AddConversationForm()
    conversations = Conversations.query.order_by('name').all()
    return render_template('index.html', conversations=conversations, conversationform=form)


@app.route('/jitsi/<id>')
@login_required
def jitsi(id):
    messages = Message.query.all()
    conversation = Conversations.query.filter_by(id=id).first()
    botlist = []
    for bot in conversation.bot:
        botlist.append(f'api_{bot.id}')

    return render_template('jitsi.html', conversation=conversation, messages=messages, botlist=botlist)


@app.route('/conversation/<id>')
@login_required
def conversation_detail(id):
    conversation = Conversations.query.filter_by(id=id).first()
    return render_template('conversation_detail.html', conversation=conversation,
                           randombotform=RandomBotForm(hidden=id))


@app.route('/add_conversation', methods=['POST'])
@login_required
def add_conversation():
    form = AddConversationForm()
    if form.validate_on_submit():
        try:
            conversation = Conversations(name=form.name.data, domain=form.domain.data, token=token_generator())
            db.session.add(conversation)
            db.session.commit()
        except IntegrityError:
            flash('Conversation already exists')
    return redirect(url_for('index'))


@app.route('/delete_conversation/<id>', methods=['GET', 'POST'])
@login_required
def delete_conversation(id):
    conversation = Conversations.query.filter_by(id=id).first()
    db.session.delete(conversation)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/bots')
@login_required
def bots():
    bots = Bot.query.all()
    messages = Message.query.all()
    return render_template("bots.html", botform=BotForm(),
                           messageform=AddMessageForm(), bots=bots, messages=messages)


@app.route('/add(<data>', methods=['POST'])
@login_required
def add(data):
    form = BotForm()
    if form.validate_on_submit():
        try:
            bot = Bot(name=form.name.data, year_of_birth=form.year_of_birth.data, sex=form.sex.data)
            db.session.add(bot)
            db.session.commit()
        except IntegrityError:
            flash('Bot already exists')
    return redirect(url_for('bots'))


@app.route('/add_message(<data>', methods=['POST'])
@login_required
def add_message(data):
    form = AddMessageForm()
    if form.validate_on_submit():
        try:
            message = Message(text=form.message.data)
            db.session.add(message)
            db.session.commit()
        except IntegrityError:
            flash('Message already exists')
    return redirect(url_for('bots'))


@app.route('/delete_message(<id>', methods=['POST'])
@login_required
def _delete_message(id):
    m = Message.query.filter_by(id=id).first()
    db.session.delete(m)
    db.session.commit()
    messages = Message.query.all()
    tmpl = """
                    <table class="table table-striped" id="messages">
                    <thead>
                    <th>Message</th>
                    <th>Delete</th>
                    </thead>
                    <tbody>
                    {% for message in messages %}
                    <tr>
                        <td>{{message.text}}</td>
                        <td><button class="btn btn-sm btn-danger" hx-post="{{ url_for('_delete_message', id=message.id) }} "hx-target="#messages" hx-swap="outerHTML">
                            <span class="glyphicon glyphicon-trash" aria-hidden="true"></span>
                        </button>
                        </td>
                    </tr>
                    {% endfor %}
                    </tbody>
                </table>         
            
           """
    return render_template_string(tmpl, messages=messages)


@app.route('/_assign_bots(<data>', methods=['POST'])
@login_required
def _assign_bots(data):
    form = RandomBotForm()
    print(form.hidden.data)
    conversation = Conversations.query.filter_by(id=form.hidden.data).first()
    if form.validate_on_submit():
        if form.options.data:
            bots = Bot.query.filter_by(sex=form.sex.data, default=True).filter(
                Bot.year_of_birth >= int(form.date_range_start.data),
                Bot.year_of_birth <= int(form.date_range_end.data)).order_by(func.random()).limit(
                int(form.amount.data)).all()
        else:
            bots = Bot.query.filter_by(default=True).order_by(func.random()).limit(
                int(form.amount.data)).all()

        for bot in bots:
            if form.participant_id.data:
                new_bot = Bot(name=randomize_bot_names(bot.name), year_of_birth=bot.year_of_birth, sex=bot.sex,
                              default=False)
                conversation.bot.append(new_bot)
            else:
                conversation.bot.append(bot)
            db.session.add(conversation)
            db.session.commit()

    return redirect(request.referrer)


@app.route('/_delete_bot_from_conversation(<conversation>/<id>', methods=['GET', 'POST'])
@login_required
def _delete_bot_from_conversation(conversation, id):
    print(conversation, id)
    bot = Bot.query.filter_by(id=id).first()
    if bot.default:
        conversation = Conversations.query.filter_by(id=conversation).first()
        conversation.bot.remove(bot)
    else:
        db.session.delete(bot)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/_delete_bot_from_settings(<id>', methods=['POST'])
@login_required
def _delete_bot_from_settings(id):
    bot = Bot.query.filter_by(id=id).first()
    db.session.delete(bot)
    db.session.commit()
    return ''

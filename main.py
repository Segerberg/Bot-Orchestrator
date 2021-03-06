#!/usr/bin/env python
from app import app, db
from app.models import Bot, Message

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'bot': Bot, 'message': Message}

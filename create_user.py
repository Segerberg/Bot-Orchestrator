from app import app, db
import os
from app.models import User
from sqlalchemy.exc import IntegrityError

USERNAME = input("USERNAME: ")
PASSWORD = input("PASSWORD: ")
users = User.query.all()

try:
    u = User(username=USERNAME)
    u.set_password(PASSWORD)
    db.session.add(u)
    db.session.commit()
    print(f"User {USERNAME} created")
except IntegrityError:
    print(f"{USERNAME}  already exists")


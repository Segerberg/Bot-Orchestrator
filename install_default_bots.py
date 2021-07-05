import csv
from app import app, db
from app.models import Bot
from sqlalchemy.exc import IntegrityError

with open('bot_names.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',')
    next(reader)

    for name, year_of_birth, sex in reader:
        try:
            bot = Bot(name=name, year_of_birth=year_of_birth, sex=sex, default=True)
            db.session.add(bot)
            db.session.commit()
        except IntegrityError:
            print(f'{name} already exists')
            db.session.rollback()
            continue


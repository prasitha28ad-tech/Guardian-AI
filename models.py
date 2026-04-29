from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.BigInteger, unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    anti_spam = db.Column(db.Boolean, default=True)
    anti_toxicity = db.Column(db.Boolean, default=True)
    max_warnings = db.Column(db.Integer, default=3)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    group_id = db.Column(db.BigInteger, nullable=False)
    username = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    warnings = db.Column(db.Integer, default=0)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.BigInteger, nullable=False)
    action = db.Column(db.String(50), nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    target_user_id = db.Column(db.BigInteger, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

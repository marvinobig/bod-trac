from datetime import timezone
from . import db
from flask_login import UserMixin 
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150))
    startingBw = db.Column(db.Numeric)
    recordedBws = db.relationship('BodyWeight')

class BodyWeight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currentDate = db.Column(db.DateTime(timezone=True), default=func.now())
    bW = db.Column(db.Numeric)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



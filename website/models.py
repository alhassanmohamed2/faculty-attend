from . import db
from sqlalchemy.sql import func


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    departement = db.Column(db.String(255))
    date = db.Column(db.Date(), default=func.date())
    subject = db.Column(db.String(255))


class NAMES(db.Model):
    __bind_key__ = 'student_names'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    departement = db.Column(db.String(255))
    subject = db.Column(db.String(255))
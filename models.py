# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(10), unique=True, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    start_point = db.Column(db.String(10), nullable=False, default="A")
    end_point = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return f'<Car {self.license_plate}>'

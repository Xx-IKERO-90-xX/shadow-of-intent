from sqlalchemy import Column, Numeric, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, declarative_base
from extensions import db

class User(db.Model):
    __tablename__ = 'Usuario'

    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(400), unique=True)
    passwd = db.Column(String(100), unique=True)
    role = db.Column(String(50))

    def __init__ (self, username, passwd, role):
        self.username = username
        self.passwd = passwd
        self.role = role

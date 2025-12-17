from sqlalchemy import Column, Numeric, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, declarative_base
from extensions import db

class Repository(db.Model):
    __tablename__ = 'Repository'

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(400), unique=True)
    url = db.Column(String(500), unique=True)
    description = db.Column(String(400))
    type = db.Column(String(100))

    def __init__(self, name, url, description, type):
        self.name = name
        self.url = url
        self.description = description
        self.type = type
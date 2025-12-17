from sqlalchemy import Column, Numeric, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, declarative_base
from extensions import db

class EvilDomain(db.Model):
    __tablename__ = 'EvilDomain'

    id = db.Column(Integer, primary_key=True)
    domain = db.Column(String(400), unique=True)

    def __init__ (self, domain, ):
        self.domain = domain
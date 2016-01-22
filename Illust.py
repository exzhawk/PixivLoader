# -*- encoding: utf-8 -*-
# Author: Epix

from sqlalchemy import Column, String
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Illust(Base):
    __tablename__ = 'illusts'
    id = Column(Integer(), primary_key=True)
    data = Column(String())

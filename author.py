import config

from sqlalchemy import Column, Integer, String

class Author(config.BASE):
  __tablename__ = 'authors'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  email = Column(String, index=True, unique=True)

  def __init__(self, name, email):
    self.name = name
    self.email = email

  def __repr__(self):
    return '<Author(%s, %s)>' % (self.name, self.email)

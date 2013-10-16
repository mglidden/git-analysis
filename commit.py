import common

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref

class Commit(common.Base):
  __tablename__ = 'commits'

  id = Column(Integer, primary_key=True)
  message = Column(String)
  time = Column(Integer)
  committer_email = Column(String, ForeignKey('authors.email'))
  author_email = Column(String, ForeignKey('authors.email'))

  def __init__(self, message, time, committer_email, author_email):
    self.message = message
    self.time = time
    self.committer_email = committer_email
    self.author_email = author_email

  def __repr__(self):
    return '<Commit(%s, %s, %s, %s)>' % (self.message, self.time, self.committer_email, self.author_email)

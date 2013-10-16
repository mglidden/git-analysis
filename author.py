from commit import Commit
import config

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref

class Author(config.BASE):
  __tablename__ = 'authors'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  email = Column(String, index=True, unique=True)
  commits = relationship('Commit', foreign_keys=[Commit.committer_email], backref='committer')
  authored_commits = relationship('Commit', foreign_keys=[Commit.author_email], backref='author')

  def __init__(self, name, email):
    self.name = name
    self.email = email

  def __repr__(self):
    return '<Author(%s, %s)>' % (self.name, self.email)

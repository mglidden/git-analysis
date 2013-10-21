import common

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref

class Patch(common.Base):
  __tablename__ = 'patches'

  id = Column(Integer, primary_key=True)
  diff = Column(String)
  lines_added = Column(Integer)
  lines_removed = Column(Integer)

  def __init__(self, diff):
    self.diff = diff
    self.lines_added = -1 #todo
    self.lines_removed = -1 #todo

  def __repr__(self):
    return '<Patch(%s)>' % (self.id)

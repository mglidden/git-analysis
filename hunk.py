import common

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref

class Hunk(common.Base):
  __tablename__ = 'hunks'

  id = Column(Integer, primary_key=True)
  lines_added = Column(Integer)
  lines_removed = Column(Integer)
  file_diff_id = Column(Integer, ForeignKey('file_diffs.id'))
  file_diff = relationship('FileDiff', backref='hunks')

  def __init__(self, lines_added=-1, lines_removed=-1):
    self.lines_added = lines_added
    self.lines_removed = lines_removed

  def __repr__(self):
    return '<Hunk(%s, %s, %s)>' % (self.id, self.lines_added, self.lines_removed)

import common

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref

class Patch(common.Base):
  __tablename__ = 'patches'

  id = Column(Integer, primary_key=True)
  diff = Column(String)
  lines_added = Column(Integer)
  lines_removed = Column(Integer)
  files_changed = Column(Integer)

  def __init__(self, diff, lines_added, lines_removed, files_changed):
    self.diff = diff
    self.lines_added = lines_added
    self.lines_removed = lines_removed
    self.files_changed = files_changed

  def __repr__(self):
    return '<Patch(%s)>' % (self.id)

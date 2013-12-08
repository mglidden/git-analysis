import common

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref

class Patch(common.Base):
  __tablename__ = 'patches'

  id = Column(Integer, primary_key=True)
  diff = Column(String)
  files_changed = Column(Integer)
  _lines_added = None
  _lines_removed = None

  def __init__(self, diff='', files_changed=-1):
    self.diff = diff
    self.files_changed = files_changed

  def lines_added(self):
    if self._lines_added == None:
      self._lines_added = sum([diff.lines_added() for diff in self.file_diffs])
    return self._lines_added

  def lines_removed(self):
    if self._lines_removed == None:
      self._lines_removed = sum([diff.lines_removed() for diff in self.file_diffs])
    return self._lines_removed

  def __repr__(self):
    return '<Patch(%s)>' % (self.id)

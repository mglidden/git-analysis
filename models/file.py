import common

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref

class File(common.Base):
  __tablename__ = 'files'

  id = Column(Integer, primary_key=True)
  name = Column(String, index=True)
  file_diff_id = Column(Integer, ForeignKey('file_diffs.id'), index=True)
  file_diff = relationship('FileDiff')

  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return '<File(%s, %s, %s, %s)>' % (self.id, self.name, self.file_diff_id)

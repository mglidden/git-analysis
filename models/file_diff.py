import fix_paths

import common

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref

class FileDiff(common.Base):
  __tablename__ = 'file_diffs'

  id = Column(Integer, primary_key=True)
  new_file_path = Column(String)
  old_file_path = Column(String)
  patch_id = Column(Integer, ForeignKey('patches.id'), index=True)
  patch = relationship('Patch', backref='file_diffs')

  def __init__(self, old_file_path, new_file_path):
    # filepaths can have utf-8 characters, which cause sqlalchemy to break
    self.old_file_path = unicode(old_file_path, 'utf-8')
    self.new_file_path = unicode(new_file_path, 'utf-8')

  def lines_added(self):
    return sum([hunk.lines_added for hunk in self.hunks])

  def lines_removed(self):
    return sum([hunk.lines_removed for hunk in self.hunks])

  def __repr__(self):
    return '<FileDiff(%s, %s, %s)>' % (self.id, self.old_file_path, self.new_file_path)

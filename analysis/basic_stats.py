import fix_paths

from models.commit import Commit
import common

from collections import defaultdict
from sqlalchemy import func

# Given a field and an optional session, this function groups by that field, then returns a dictionary mapping the size of the groups to a list of fields for those groups.
def histogram_for_field(field, session=None):
  # Given a list of (key, value) items, returns a dictionary mapping key to all values with that key.
  def _group_items(items):
    grouped_items = defaultdict(list)
    for key, value in items:
      grouped_items[key].append(value)
    return grouped_items

  if not session:
    session = common.Session()

  return _group_items(session.query(func.count(field), field).group_by(field).all())

# Returns a dictionary mapping the number of changes committed by an author to a list of all authors.
def committer_frequency_histogram(session=None):
  return histogram_for_field(Commit.committer_email, session)

# Returns a dictionary mapping the number of changes authored by an author to a list of all authors.
def author_frequency_histogram(session=None):
  return histogram_for_field(Commit.author_email, session)

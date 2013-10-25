from author import Author
import basic_stats
from commit import Commit
import common
from patch import Patch

from collections import Counter
import pylab
import sqlalchemy

session = common.Session()

print 'Number of authors: %s' % (session.query(Author).count())
print 'Number of commits: %s' % (session.query(Commit).count())

def _print_histogram(histogram):
  histogram_counts = [(count, len(values)) for count, values in histogram.iteritems()]
  histogram_counts.sort(key=lambda key: key[0])
  print histogram_counts

commit_counts = [count[0] for count in session.query(sqlalchemy.func.count(Commit.committer_email)).group_by(Commit.committer_email).all()]
author_counts = [count[0] for count in session.query(sqlalchemy.func.count(Commit.author_email)).group_by(Commit.author_email).all()]

pylab.figure()
pylab.hist([author_counts], 50, histtype='bar', color=['yellow'], label=['Authorship Counts'])
#pylab.hist([commit_counts, author_counts], 50, histtype='bar', color=['blue', 'yellow'], label=['Commit Counts', 'Authorship Counts'])
pylab.xlabel('Number of changes')
pylab.ylabel('Number of authors')
pylab.legend()

def remove_max(list):
  list.remove(max(list))
  return list

def detuple(list):
  return [val[0] for val in list]

lines_added = remove_max(detuple(session.query(Patch.lines_added).all()))
lines_removed = remove_max(detuple(session.query(Patch.lines_removed).all()))
files_touched = remove_max(detuple(session.query(Patch.files_changed).all()))

pylab.figure()
pylab.hist([lines_added, lines_removed, files_touched], 50, histtype='bar', color=['blue', 'green', 'red'], label=['Lines Added', 'Lines Removed', 'Files Changed'], log=True)
pylab.legend()

lines_added_capped = filter(lambda x: x < 5000, lines_added)
lines_removed_capped = filter(lambda x: x < 5000, lines_removed)
files_touched_capped = filter(lambda x: x < 5000, files_touched)

pylab.figure()
pylab.hist([lines_added_capped , lines_removed_capped, files_touched_capped], 50, histtype='bar', color=['blue', 'green', 'red'], label=['Lines Added', 'Lines Removed', 'Files Changed'], log=True)
pylab.legend()

pylab.show()

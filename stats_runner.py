from author import Author
import basic_stats
from commit import Commit
import common

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

pylab.hist([author_counts], 50, histtype='bar', color=['yellow'], label=['Authorship Counts'])
#pylab.hist([commit_counts, author_counts], 50, histtype='bar', color=['blue', 'yellow'], label=['Commit Counts', 'Authorship Counts'])
pylab.xlabel('Number of changes')
pylab.ylabel('Number of authors')
pylab.legend()
pylab.show()

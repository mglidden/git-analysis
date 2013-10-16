from author import Author
import basic_stats
from commit import Commit
import common

import sqlalchemy

session = common.Session()

print 'Number of authors: %s' % (session.query(Author).count())
print 'Number of commits: %s' % (session.query(Commit).count())

def _print_histogram(histogram):
  histogram_counts = [(count, len(values)) for count, values in histogram.iteritems()]
  histogram_counts.sort(key=lambda key: key[0])
  print histogram_counts

print 'Map of number->number of authors with that many committed changes:'
_print_histogram(basic_stats.committer_frequency_histogram(session))
print 'Map of number->number of authors with that many authored changes:'
_print_histogram(basic_stats.author_frequency_histogram(session))

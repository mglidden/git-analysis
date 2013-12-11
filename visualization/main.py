import fix_paths

from models.author import Author
from models.commit import Commit
import common

from collections import defaultdict
from datetime import datetime
from flask import Flask, render_template
import json
from sqlalchemy import func

app = Flask('GitAnalysis')
session = common.Session()

@app.route('/')
def main_page():
  authors = session.query(Author).join(Author.authored_commits).group_by(Author.email).order_by(func.count(Author.commits).desc())

  return render_template('repo.html', authors=authors)

def _name_for_classification(classification):
  if classification == 2:
    return 'Bugfix'
  elif classification == 3:
    return 'Cleanup / Refactor'
  elif classification == 5:
    return 'Merge'
  elif classification == 6:
    return 'Feature'

def _format_commits_for_stacked_graph(commit_classifications):
  data_by_week = defaultdict(lambda: {2:0, 3:0, 5:0, 6:0})
  seconds_in_week = 7 * 24 * 60 * 60
  for classification, time in commit_classifications:
    weeknum = time / seconds_in_week
    data_by_week[weeknum][classification] += 1

  layers = defaultdict(list)
  for week, data in sorted(data_by_week.iteritems(), key=lambda val: val[0]):
    date = week * seconds_in_week * 1000;
    for classification, count in data.iteritems():
      layers[classification].append((date, count))

  out = []
  for classification, data in layers.iteritems():
    out.append({
      'key': _name_for_classification(classification),
      'values': data
    })
  return json.dumps(out)

@app.route('/repo_classification.json')
def repo_classification():
  commit_classifications = session.query(Commit.classification, Commit.time)
  return _format_commits_for_stacked_graph(commit_classifications)

@app.route('/author_classification.json/<author_id>')
def author_classification(author_id):
  author_email = str(session.query(Author.email).filter(Author.id == int(author_id)).first()[0])
  print author_email
  authors_commits = session.query(Commit.classification, Commit.time).filter(Commit.author_email == author_email)
  return _format_commits_for_stacked_graph(authors_commits)

if __name__ == '__main__':
  app.run(host='0.0.0.0')

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
app.debug = True
session = common.Session()

@app.route('/')
def main_page():
  authors = session.query(Author).join(Author.commits).group_by(Author.email).order_by(func.count(Author.commits).desc())

  commit_classifications = session.query(Commit.classification, Commit.time).order_by(Commit.time)
  data_by_week = []
  current_week = -1
  for classification, time in commit_classifications:
    calendar = datetime.fromtimestamp(time).isocalendar()
    weeknum = calendar[0]*52 + calendar[1]
    if weeknum != current_week:
      data_by_week.append({2:0, 3:0, 5:0, 6:0})
      current_week = weeknum
    data_by_week[-1][classification] += 1

  layers = defaultdict(list)
  for week, data in zip(range(0, len(data_by_week)), data_by_week):
    for classification, count in data.iteritems():
      layers[classification].append({'x': week, 'y': count})

  return render_template('repo.html', authors=authors, layers=json.dumps(layers.values()))

if __name__ == '__main__':
  app.run()

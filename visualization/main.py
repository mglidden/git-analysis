import fix_paths

from models.author import Author
from models.commit import Commit
import common

from flask import Flask, render_template
from sqlalchemy import func

app = Flask('GitAnalysis')
app.debug = True
session = common.Session()

@app.route('/')
def main_page():
  authors = session.query(Author).join(Author.commits).group_by(Author.email).order_by(func.count(Author.commits).desc())
  return render_template('repo.html', authors=authors)

if __name__ == '__main__':
  app.run()

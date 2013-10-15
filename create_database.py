from author import Author
from commit import Commit
import config

import os
import pygit2
import sqlalchemy

# If it exists and we want to reset the DB, remove the file
if config.RESET_DB and os.path.exists(config.DB_PATH):
  os.remove(config.DB_PATH)

engine = sqlalchemy.create_engine(config.DB_URL, echo=False)
config.BASE.metadata.create_all(engine)

Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

repo = pygit2.Repository(config.REPO_PATH)
for commit in repo.walk(repo.head.target, pygit2.GIT_SORT_TIME):
  author = session.query(Author).filter(Author.email == commit.author.email).first()
  if not author:
    author = Author(commit.author.name, commit.author.email)
    session.add(author)

  committer = session.query(Author).filter(Author.email == commit.committer.email).first()
  if not committer:
    committer = Author(commit.committer.name, commit.committer.email)
    session.add(committer)

  session.add(Commit(commit.message, commit.commit_time, committer.email, author.email))

session.commit()

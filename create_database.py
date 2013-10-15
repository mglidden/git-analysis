import author
import commit
import config

import os
import pygit2
import sqlalchemy

repo = pygit2.Repository(config.REPO_PATH)

# Probably want to completly reset the DB
if config.RESET_DB and os.path.exists(config.DB_PATH):
  os.remove(config.DB_PATH)

engine = sqlalchemy.create_engine(config.DB_URL, echo=True)
config.BASE.metadata.create_all(engine)



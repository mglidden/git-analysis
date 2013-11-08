from author import Author
from commit import Commit
from parent_relationship import parent_relationship_table
from patch import Patch
import common
import config

import os
import pygit2
import sqlalchemy

# If it exists and we want to reset the DB, remove the file
if config.RESET_DB and os.path.exists(config.DB_PATH):
  os.remove(config.DB_PATH)

common.Base.metadata.create_all(common.engine)

session = common.Session()

parents = []
count = 0
repo = pygit2.Repository(config.REPO_PATH)
for commit in repo.walk(repo.head.target, pygit2.GIT_SORT_REVERSE):
  author = session.query(Author).filter(Author.email == commit.author.email).first()
  if not author:
    author = Author(commit.author.name, commit.author.email)
    session.add(author)

  committer = session.query(Author).filter(Author.email == commit.committer.email).first()
  if not committer:
    committer = Author(commit.committer.name, commit.committer.email)
    session.add(committer)

  patch = None
  if len(commit.parents) > 0:
    try:
      # If a commit has multiple parents, it's a merge commit. pygit2 appears to put the merged commit last, so we'll take that. TODO: find a commit with > 2 parents and make sure everything works out
      # TODO: This sometimes throws a GitError - "Object not found - no matching loose object"
      diff = commit.tree.diff_to_tree(commit.parents[-1].tree)

      lines_added = 0
      lines_removed = 0
      files_changed = 0
      for patch in diff:
        files_changed += 1
        for hunk in patch.hunks:
          for line in hunk.lines:
            if line[0] == '-':
              lines_removed += 1
            elif line[0] == '+':
              lines_added += 1

      patch = Patch(diff.patch, lines_added, lines_removed, files_changed)
    except pygit2.GitError as e:
      print e
  else:
    print 'no parents'
  # TODO: are merge commits the only commits with > 1 parent?
  session.add(Commit(commit.message, commit.commit_time, commit.hex, len(commit.parents) > 1, patch, committer.email, author.email))
  for parent_commit in commit.parents:
    session.execute(parent_relationship_table.insert().values(child_hash=commit.hex, parent_hash=parent_commit.hex))

  count += 1
  if count % 100 == 0:
    print count

session.commit()

import fix_paths

from models.author import Author
from models.commit import Commit
import common
import config
from models.file_diff import FileDiff
from models.hunk import Hunk
import word_frequencies

def _is_merge(commit):
  return int(commit.is_merge)

def _files_modified(commit):
  if not commit.patch:
    return 0
  return min(1.0, commit.patch.files_changed / 25.0)

def _lines_added(commit):
  if not commit.patch:
    return 0
  return min(1.0, commit.patch.lines_added() / 500.0)

def _lines_removed(commit):
  if not commit.patch:
    return 0
  return min(1.0, commit.patch.lines_removed() / 500.0)

def _lines_ratio(commit):
  if not commit.patch or commit.patch.lines_added() + commit.patch.lines_removed() == 0:
    return 0.5
  return commit.patch.lines_added() / float(commit.patch.lines_added() + commit.patch.lines_removed())

def _clean_or_refactor_in_message(commit):
  return 'clean' in commit.message.lower() or 'refactor' in commit.message.lower()

all_words = word_frequencies.load_word_frequencies()
def _word_features(commit):
  words = word_frequencies.get_words_from_message(commit.message)
  return [int(word in words) for word in all_words]


def create_features(commit):
  feature_creators = [_is_merge, _files_modified, _lines_added, _lines_removed, _lines_ratio, _clean_or_refactor_in_message]
  return [feature_creator(commit) for feature_creator in feature_creators] + _word_features(commit)

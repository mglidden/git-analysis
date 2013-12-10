import fix_paths

import common
import config
from load_samples import load_samples_from_file
from models.commit import Commit

from collections import Counter
import json
import string

def get_words_from_message(commit_message):
  #TODO: clean up this method
  cleaned_message = str(commit_message.encode('ascii', 'ignore').replace('\n', ' ')).translate(string.maketrans('', ''), string.punctuation + '\t').lower()
  return set(cleaned_message.split(' '))

def create_word_frequencies():
  session = common.Session()
  training_samples = load_samples_from_file(config.TRAINING_DATA_PATH)
  word_frequencies = Counter()
  for _, commit_id in training_samples:
    commit = session.query(Commit).filter(Commit.id == commit_id).first()
    for word in get_words_from_message(commit.message):
      word_frequencies[word] += 1
  all_words = [word for word, _ in word_frequencies.most_common(800)]

  word_frequency_file = open(config.WORD_FREQUENCY_PATH, 'w')
  word_frequency_file.write(json.dumps(all_words))
  word_frequency_file.close()

def load_word_frequencies():
  # TODO: Cache this file
  word_frequency_file = open(config.WORD_FREQUENCY_PATH, 'r')
  word_frequency = json.loads(word_frequency_file.read())
  word_frequency_file.close()
  return word_frequency

if __name__ == '__main__':
  create_word_frequencies()

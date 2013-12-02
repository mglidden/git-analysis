from commit import Commit
import common
import config
from file_diff import FileDiff
from hunk import Hunk

from collections import Counter
import csv
from sklearn import svm
import string

session = common.Session()

training_file = open(config.TRAINING_DATA_PATH, 'r')
training_samples = list(csv.reader(training_file))
training_file.close()

def is_merge(commit):
  return int(commit.is_merge)

def files_modified(commit):
  if not commit.patch:
    return 0
  return min(1.0, commit.patch.files_changed / 25.0)

# TODO: when I fix the lines removed / added bug, change these to be correct
def lines_added(commit):
  if not commit.patch:
    return 0
  return min(1.0, commit.patch.lines_removed() / 1000.0)

def lines_removed(commit):
  if not commit.patch:
    return 0
  return min(1.0, commit.patch.lines_added() / 1000.0)

def get_words_from_message(commit_message):
  cleaned_message = str(commit_message.replace('\n', ' ')).translate(string.maketrans('', ''), string.punctuation + '\t')
  return set(cleaned_message.split(' '))

word_frequencies = Counter()
for _, commit_id in training_samples:
  commit = session.query(Commit).filter(Commit.id == commit_id).first()
  for word in get_words_from_message(commit.message):
    word_frequencies[word] += 1
all_words = [word for word, _ in word_frequencies.most_common(20)]

def word_features(commit):
  words = get_words_from_message(commit.message)
  return [int(word in words) for word in all_words]

training_features = []
training_classifications = []

feature_creators = [is_merge, files_modified, lines_added, lines_removed]
def create_features(commit):
  return [feature_creator(commit) for feature_creator in feature_creators] + word_features(commit)

print 'Creating training features'
for classification, commit_id in training_samples:
  training_features.append(create_features(session.query(Commit).filter(Commit.id == commit_id).first()))
  training_classifications.append(classification)

print training_features


print 'Training SVC'
clf = svm.SVC()
clf.fit(training_features, training_classifications)


print 'Creating testing features'
testing_file = open(config.TESTING_DATA_PATH, 'r')
testing_reader = csv.reader(testing_file)
testing_features = []
testing_truth_classifications = []
for classification, commit_id in testing_reader:
  testing_features.append(create_features(session.query(Commit).filter(Commit.id == commit_id).first()))
  testing_truth_classifications.append(classification)

print 'Classifying the testing features.'
correct = 0
incorrect = 0
testing_guess_classifications = clf.predict(testing_features)
for truth, guess in zip(testing_truth_classifications, testing_guess_classifications):
  if truth == guess:
    correct += 1
  else:
    incorrect += 1

print correct
print incorrect

from commit import Commit
import common
import config
from file_diff import FileDiff
from hunk import Hunk

from collections import Counter, defaultdict
import csv
import numpy as np
from sklearn import svm
from sklearn.cross_validation import StratifiedKFold
from sklearn.grid_search import GridSearchCV
import string

session = common.Session()


should_remove_tweaks = True
def remove_tweaks(samples):
  return map(lambda (feature, commit_id): (min(6, int(feature)), commit_id), samples)

should_remove_unknowns = True
def remove_unknowns(samples):
  return filter(lambda (feature, commit_id): feature != 1, samples)

def load_samples_from_file(filename):
  samples_file = open(filename, 'r')
  samples = list(csv.reader(samples_file))
  samples_file.close()
  samples = map(lambda (feature, commit_id): (int(feature), int(commit_id)), samples)
  if should_remove_tweaks:
    samples = remove_tweaks(samples)
  if should_remove_unknowns:
    samples = remove_unknowns(samples)
  return samples

training_samples = load_samples_from_file(config.TRAINING_DATA_PATH)

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

def lines_ratio(commit):
  if not commit.patch or commit.patch.lines_added() + commit.patch.lines_removed() == 0:
    return 0.5
  return commit.patch.lines_added() / float(commit.patch.lines_added() + commit.patch.lines_removed())

def clean_or_refactor_in_message(commit):
  return 'clean' in commit.message.lower() or 'refactor' in commit.message.lower()

def get_words_from_message(commit_message):
  cleaned_message = str(commit_message.replace('\n', ' ')).translate(string.maketrans('', ''), string.punctuation + '\t').lower()
  return set(cleaned_message.split(' '))

word_frequencies = Counter()
for _, commit_id in training_samples:
  commit = session.query(Commit).filter(Commit.id == commit_id).first()
  for word in get_words_from_message(commit.message):
    word_frequencies[word] += 1
all_words = [word for word, _ in word_frequencies.most_common(800)]

def word_features(commit):
  words = get_words_from_message(commit.message)
  return [int(word in words) for word in all_words]

training_features = []
training_classifications = []

feature_creators = [is_merge, files_modified, lines_added, lines_removed, lines_ratio, clean_or_refactor_in_message]
def create_features(commit):
  return [feature_creator(commit) for feature_creator in feature_creators] + word_features(commit)


print 'Creating training features'
for classification, commit_id in training_samples:
  training_features.append(create_features(session.query(Commit).filter(Commit.id == commit_id).first()))
  training_classifications.append(classification)


print 'Training SVC'
do_grid_search = False
if do_grid_search:
  C_range = np.arange(1, 4000, 250)
  gamma_range = 10 ** np.arange(-5, 4)
  param_grid = dict(gamma=gamma_range, C=C_range)
  cv = StratifiedKFold(y=training_classifications, n_folds=3)
  grid = GridSearchCV(svm.SVC(class_weight='auto'), param_grid=param_grid, cv=cv)
  grid.fit(training_features, training_classifications)
  clf = grid.best_estimator_
  print clf
else:
  clf = svm.SVC(class_weight='auto', C=250, gamma=0.0)
  clf.fit(training_features, training_classifications)


print 'Creating testing features'
testing_samples = load_samples_from_file(config.TESTING_DATA_PATH)
testing_features = []
testing_truth_classifications = []
for classification, commit_id in testing_samples:
  testing_features.append(create_features(session.query(Commit).filter(Commit.id == commit_id).first()))
  testing_truth_classifications.append(classification)

def classify_and_grade(features, truth, classifier):
  correct = 0
  incorrect = 0
  predictions = classifier.predict(features)
  score_per_class = defaultdict(lambda: {True: 0, False: 0, 'distribution': defaultdict(int)});

  for truth, guess in zip(truth, predictions):
    if truth == guess:
      correct += 1
    else:
      incorrect += 1
    score_per_class[truth][truth == guess] += 1
    score_per_class[truth]['distribution'][guess] += 1
  return (correct, incorrect, score_per_class)

def pretty_print_results(results):
  correct, incorrect, score_per_class = results
  print 'Correct: %s\nIncorrect: %s\nPrecent: %s' % (correct, incorrect, correct / float(correct + incorrect))
  for classname in sorted(score_per_class.keys()):
    class_results = score_per_class[classname]
    print '%s: %s/%s %s' % (classname, class_results[True], class_results[True] + class_results[False], dict(class_results['distribution']))
  print ''


print 'Classifying the testing features.'
pretty_print_results(classify_and_grade(testing_features, testing_truth_classifications, clf))


print 'Classifying the training features.'
pretty_print_results(classify_and_grade(training_features, training_classifications, clf))

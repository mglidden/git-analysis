import fix_paths

from models.author import Author
from models.commit import Commit
import common
import config
import features
from load_samples import load_samples_from_file
from models.file_diff import FileDiff
from models.hunk import Hunk

from collections import Counter, defaultdict
import csv
import numpy as np
import pickle
from sklearn import svm
from sklearn.cross_validation import StratifiedKFold
from sklearn.grid_search import GridSearchCV
import string

session = common.Session()

training_samples = load_samples_from_file(config.TRAINING_DATA_PATH)
training_features = []
training_classifications = []

print 'Creating training features'
for classification, commit_id in training_samples:
  training_features.append(features.create_features(session.query(Commit).filter(Commit.id == commit_id).first()))
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
  testing_features.append(features.create_features(session.query(Commit).filter(Commit.id == commit_id).first()))
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


should_serialize_svc = True
if should_serialize_svc:
  clf_str = pickle.dumps(clf)

  clf_file = open(config.SERIALIZED_SVC_LOCATION, 'w')
  clf_file.write(clf_str)
  clf_file.close()

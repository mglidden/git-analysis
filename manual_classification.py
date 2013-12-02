from commit import Commit
import common
import config
from file_diff import FileDiff
from hunk import Hunk

import csv
import random

num_train = raw_input("Enter number of samples for the training set [100]:")
num_test = raw_input("Enter number of samples for the testing set [100]:")

try:
  num_train = int(num_train)
except ValueError:
  num_train = 100

try:
  num_test = int(num_test)
except:
  num_test = 100

session = common.Session()

assert num_train + num_test <= session.query(Commit.id).count(), 'Train and test size is larger than  the number of commits.'

iteration_order = list(range(session.query(Commit.id).count()))
random.shuffle(iteration_order)

training_data = []
testing_data = []

training_file = open(config.TRAINING_DATA_PATH, 'a')
training_writer = csv.writer(training_file)
testing_file = open(config.TESTING_DATA_PATH, 'a')
testing_writer = csv.writer(testing_file)

def classifyCommit(session, commit_id):
  commit = session.query(Commit).filter(Commit.id == commit_id).first()
  print 'ID:\t\t%s' % commit.id
  print 'Hash:\t\t%s' % commit.hash
  print 'Is merge:\t%s' % commit.is_merge
  print 'Message:\t%s' % commit.message.replace('\n', '  ')
  if commit.patch:
    print 'Lines added:\t%s' % commit.patch.lines_removed()
    print 'Lines removed:\t%s' % commit.patch.lines_added()
    print 'Files changed:'
    for file_diff in commit.patch.file_diffs:
      print '\t%s, +%s, -%s' % (file_diff.new_file_path, file_diff.lines_removed(), file_diff.lines_added())

  classification_number = None
  while not classification_number:
    try:
      classification_number = int(raw_input('Enter classification number for commit %s: ' % (commit_id)))
    except:
      print 'Enter an int for the classification number.'
  print
  return (classification_number, commit_id)

i = 1
for index in iteration_order:
  if i <= num_train:
    training_writer.writerow(classifyCommit(session, index))
    training_file.flush()
  elif i <= num_train + num_test:
    testing_writer.writerow(classifyCommit(session, index))
    testing_file.flush()
  else:
    break

  i += 1

training_file.close()

testing_file.close()

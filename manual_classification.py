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

def classifyCommit(session, commit_id):
  commit = session.query(Commit).filter(Commit.id == commit_id).first()
  print commit.id
  print commit.hash
  print commit.is_merge
  print commit.message
  print commit.patch.files_changed
  print commit.patch.lines_added()
  print commit.patch.lines_removed()


  classification_number = None
  while not classification_number:
    try:
      classification_number = int(raw_input('Enter classification number for commit %s: ' % (commit_id)))
    except:
      print 'Enter an int for the classification number.'
  return (classification_number, commit_id)

i = 1
for index in iteration_order:
  if i <= num_train:
    training_data.append(classifyCommit(session, index))
  elif i <= num_train + num_test:
    testing_data.append(classifyCommit(session, index))
  else:
    break

  i += 1

training_file = open(config.TRAINING_DATA_PATH, 'w')
training_writer = csv.writer(training_file)
training_writer.writerows(training_data)
training_file.close()

testing_file = open(config.TESTING_DATA_PATH, 'w')
testing_writer = csv.writer(testing_file)
testing_writer.writerows(testing_data)
testing_file.close()

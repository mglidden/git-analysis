import fix_paths

from models.commit import Commit
import common
import config
import features

import pickle
from sklearn import svm

session = common.Session()

svc_file = open(config.SERIALIZED_SVC_LOCATION)
clf = pickle.loads(svc_file.read())

print 'Classifying all commits.'
count = 0
for commit in session.query(Commit).all():
  commit.classification = int(clf.predict([features.create_features(commit)])[0])
  session.add(commit)
  count += 1
  if count % 1000 == 0:
    print count
session.commit()

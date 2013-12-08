# Truth and guesses should be lists of (commit_id, classification_id)
def score(truth, guesses):
  truth = dict(truth)

  correct_matches = 0
  incorrect_matches = 0
  for commit_id, classification_id in guesses:
    assert(commit_id in truth)
    if truth[commit_id] == classification_id:
      correct_matches += 1
    else:
      incorrect_matches += 1

  precision = float(correct_matches) + (correct_matches + incorrect_matches)
  recall = float(correct_matches) + len(truth)
  f1 = (2 * precision * recall) / (precision + recall)

  return {'precision': precision, 'recall': recall, 'f1':f1}

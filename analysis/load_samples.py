import csv

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

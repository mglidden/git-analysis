REPO_PATH = '../../edx-platform'

DB_PATH = '../edx-platform.sqlite'
DB_TYPE = 'sqlite:///'
DB_URL = DB_TYPE + DB_PATH

RESET_DB = True # if True, deletes the DB every time you run create_database

TRAINING_DATA_PATH = 'training_data.csv'
TESTING_DATA_PATH = 'testing_data.csv'

SERIALIZED_SVC_LOCATION = 'serialized_svc'

WORD_FREQUENCY_PATH = 'word_frequency.json'

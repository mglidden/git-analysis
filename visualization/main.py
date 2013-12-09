import fix_paths

import common

from flask import Flask

app = Flask('GitAnalysis')
session = common.Session()

@app.teardown_appcontext
def teardown(error):
  session.close()

@app.route('/')
def main_page():
  return 'root'

if __name__ == '__main__':
  app.run()

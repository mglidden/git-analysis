import fix_paths

import common

from flask import Flask, render_template

app = Flask('GitAnalysis')
app.debug = True
session = common.Session()

@app.route('/')
def main_page():
  return render_template('layout.html')

if __name__ == '__main__':
  app.run()

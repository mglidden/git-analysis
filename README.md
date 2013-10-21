edX-analysis
============

A collection of scripts that I'm using to do an ethnography of the community forming around the development of edX.


To run these scripts, you'll need to install pygit2, sqlalchemy, and matplotlib. 

Configure the desired git repo in config.py. Running create_database.py will store all commits from the repo into a DB (default is sqlite). Running stats_runner.py will generate some basic stats about the repository.

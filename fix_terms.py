# This is one time use script to remove old terms and create a new term
# related to issue #52 ==> CDM
# after the script is ran, this file should be deleted. 

import os, sys
import importlib

# Don't forget to import your own models!
from app.models import *

conf = load_config('app/config.yaml')

sqlite_dbs  = [ conf['databases']['dev']
                # add more here if multiple DBs
              ]

def class_from_name (module_name, class_name):
  # load the module, will raise ImportError if module cannot be loaded
  # m = __import__(module_name, globals(), locals(), class_name)
  # get the class, will raise AttributeError if class cannot be found
  c = getattr(module_name, class_name)
  return c
    
"""This file creates the database and fills it with some dummy run it after you have made changes to the models pages."""
def get_classes (db):
  classes = []
  for str in conf['models'][db]:
    print ("\tCreating model for '{0}'".format(str))
    c = class_from_name(sys.modules[__name__], str)
    classes.append(c)
  return classes

bad_semesters = ['201615', '201614', '201613', '201714']

for semester in bad_semesters:
    delete_query = "DELETE FROM semesters WHERE SEID = " + semester + ";"
    mainDB.execute_sql(delete_query)
    
insert_query = "INSERT INTO semesters (SEID, year, term) VALUES ('201713', '2018', 'Summer')"
mainDB.execute_sql(insert_query)

insert_instructor = "INSERT INTO users (username, firstName, lastName, email, isAdmin) VALUES ('brooksjam', 'Jamiella', 'Brooks', 'brooksjam@berea.edu', 0)"
mainDB.execute_sql(insert_instructor)
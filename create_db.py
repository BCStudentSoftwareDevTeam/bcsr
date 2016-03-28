# WARNING: NOT FOR USE IN PRODUCTION AFTER REAL DATA EXISTS!!!!!!!!!!!!!!!!!!!!!!
'''
This script creates the database tables in the SQLite file. 
Update this file as you update your database.
'''
import os, sys
import importlib

# Don't forget to import your own models!
from app.models import *

conf = load_config('app/config.yaml')

sqlite_dbs  = [ conf['databases']['dev']
                # add more here if multiple DBs
              ]

# Remove DBs
for fname in sqlite_dbs:
  try:
    print ("Removing {0}.".format(fname))
    os.remove(fname)
  except OSError:
    pass

# Creates DBs
for fname in sqlite_dbs:
  if os.path.isfile(fname):
    print ("Database {0} should not exist at this point!".format(fname))
  print ("Creating empty SQLite file: {0}.".format(fname))
  open(fname, 'a').close()
  

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

  
mainDB.create_tables(get_classes('mainDB'))

# When adding dummy data the varialbes should be in Mixed case and should be the name of the class

semesters = Semesters(  year      = 2016,
                        term      = "Spring",
                        current   = True
                      ).save()
                      
divisions = Divisions(  name      = "Division 1"
                      ).save()
                      
programs  = Programs(   name      = "Computer Science",
                        DID       = 1
                     ).save()
                     
users     = Users(      firstName = "Scott",
                        lastName  = "Heggen",
                        userName  = "heggens",
                        email     = "heggens@berea.edu",
                        admin     = True
                  ).save()

users     = Users(      firstName = "Matt",
                        lastName  = "Jadud",
                        userName  = "jadudm",
                        email     = "jadudm@berea.edu",
                        PID       = 1
                  ).save()  
             
courses   = Courses(  prefix = "BIO",
                      number = "101",
                      section = "A1",
                      PID     = 1,
                      SEID    = 1
                  ).save()

userscourses  = UsersCourses ( userName = 'heggens',
                               CID      = 1
                              ).save()

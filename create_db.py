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

courses = Courses(  prefix = "BIO",
                    number = "101",
                    section = "A1",
                    PID     = 1
                  ).save()
                  
currentSemester = CurrentSemester( SEID = 1 
                                  ).save()
                         
divisions = Divisions( name = "division1"
                     ).save()
                     
divisionChair = DivisionChair(  DID  = 1,
                                UID  = 1,
                              ).save()
                               
divisionToProgram = DivisionToProgram(  DID  = 1,
                                        PID  = 1
                                      ).save()
programs = Programs(  name  = "Biology"
                   ).save()
                   
programChair = ProgramChair(  PID  = 1,
                              UID  = 2,
                             ).save()
                             
role = Role(  name   = "Administrator"
           ).save()

role = Role(  name   = "Program Chair"
           ).save()
           
role = Role(  name   = "Division Chair"
           ).save()

role = Role(  name   = "Professor"
           ).save()
           
semester = Semester(  year  = 2016,
                      term  = "Spring"
                   ).save()
            
syllabusCourseSemester = SyllabusCourseSemester(     SID  = 1,
                                                     CID  = 1,
                                                     SEID = 1
                                                   ).save()
                        
UsersToSCS =  UsersToSCS( SCSID = 1,
              UID   = 1
             ).save()
                      
users = Users(  firstName = "Scott",
                lastName  = "Heggen",
                userName  = "heggens",
                email     = "heggens@berea.edu",
                RID       = 1
             ).save()

users = Users(  firstName = "Matt",
                lastName  = "Jadud",
                userName  = "jadudm",
                email     = "jadudm@berea.edu",
                RID       = 2
             ).save()           
             

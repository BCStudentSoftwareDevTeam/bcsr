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

# Adding dummy data

courses = Courses(  cprefix = "BIO",
                    cnumber = "101",
                    section = "A1",
                    PID     = 1
                  ).save()
                  
currentSEID = CurrentSEID( SEID = 201512 
                         ).save()
                         
divisions = Divisions( name = "division1"
                     ).save()
                     
division_chair = Division_chair(  DID  = 1,
                                  UID  = 1,
                               ).save()
                               
division_to_program = Division_to_program(  DID  = 1,
                                            PID  = 1
                                         ).save()
programs = Programs(  name  = "Biology"
                   ).save()
                   
program_chair = Program_chair(  PID  = 1,
                                UID  = 2,
                             ).save()
                             
role = Role(  access_level  = "Full_Access",
              access_name   = "Administrator"
           ).save()

role = Role(  access_level  = "Program_Access",
              access_name   = "Program Chair"
           ).save()
           
role = Role(  access_level  = "Division_Access",
              access_name   = "Division Chair"
           ).save()

role = Role(  access_level  = "Prof_Access",
              access_name   = "Professor"
           ).save()
           
semester = Semester(  year  = 2016,
                      term  = "Spring"
                   ).save()
            
syllabus_course_semester = Syllabus_course_semester( SID  = 1,
                                                     CID  = 1,
                                                     SEID = 1
                                                   ).save()
                        
uscs =  Uscs( XID = 1,
              UID = 1
             ).save()
                      
users = Users(  firstname = "Scott",
                lastname  = "Heggen",
                username  = "heggens",
                email     = "heggens@berea.edu"
             ).save()

users = Users(  firstname = "Matt",
                lastname  = "Jadud",
                username  = "jadudm",
                email     = "jadudm@berea.edu"
             ).save()           
             
user_role = User_role(  RID = 1,
                        UID = 1,
                     ).save()
                    
user_role = User_role(  RID = 3,
                        UID = 2
                     ).save()
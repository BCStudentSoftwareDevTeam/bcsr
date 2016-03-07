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

courses = courses(  CID     = 1,
                    cprefix = "BIO",
                    cnumber = "101",
                    section = "A1",
                    PID     = 1
                  ).save()
                  
currentSEID = currentSEID( SEID = 201512 
                         ).save()
                         
divisions = divisions(  DID = 1,
                        name = "division1"
                     ).save()
                     
division_chair = division_chair(  DCID = 1,
                                  DID  = 1,
                                  UID  = 1,
                               ).save()
                               
division_to_program = division_to_program(  DPID = 1,
                                            DID  = 1,
                                            PID  = 1
                                         ).save()
programs = programs(  PID   = 1,
                      name  = "Biology"
                   ).save()
                   
program_chair = program_chair(  PCID = 1,
                                PID  = 1,
                                UID  = 2,
                             ).save()
                             
role = role(  RID           = 1,
              access_level  = "Full_Access",
              access_name   = "Administrator"
           ).save()

role = role(  RID           = 2,
              access_level  = "Program_Access",
              access_name   = "Program Chair"
           ).save()
           
role = role(  RID           = 3,
              access_level  = "Division_Access",
              access_name   = "Division Chair"
           ).save()

role = role(  RID           = 4,
              access_level  = "Prof_Access",
              access_name   = "Professor"
           ).save()
           
semester = semester(  SEID  = 201512,
                      year  = 2016,
                      term  = "Spring"
                   ).save()
            
syllabus_course_semester = syllabus_course_semester( XID  = 1,
                                                     SID  = NULL,
                                                     CID  = 1,
                                                     SEID = 201512
                                                   ).save()
                        
uscs =  uscs( QID = 1,
              XID = 1,
              UID = 1
             ).save()
                      
users = users(  UID       = 1,
                firstname = "Scott",
                lastName  = "Heggen",
                username  = "heggens",
                email     = "heggens@berea.edu"
             ).save()

users = users(  UID       = 2,
                firstName = "Matt",
                lastName  = "Jadud",
                username  = "jadudm",
                email     = "jadudm@berea.edu"
             ).save()           
             
user_role = user_role(  RID = 1,
                        UID = 1,
                     ).save()
                    
user_role = user_role(  RID = 3,
                        UID = 2
                     ).save()
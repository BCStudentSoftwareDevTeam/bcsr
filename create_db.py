# WARNING: NOT FOR USE IN PRODUCTION AFTER REAL DATA EXISTS!!!!!!!!!!!!!!!!!!!!!!
'''
This script creates the database tables in the SQLite file. 
Update this file as you update your database.
'''
import os, sys
import importlib
import pymysql
from app.models import * # Don't forget to import your own models!

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="root"
)

cursor = connection.cursor()
cursor.execute("DROP DATABASE IF EXISTS bcsr")
cursor.execute("CREATE DATABASE bcsr")
cursor.close()
connection.close()
conf = load_config('app/config.yaml')

os.makedirs("data", exist_ok=True)
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
###########
#SEMESTERS#
###########
semesters = Semesters(  SEID      = 201612,
                        year      = 2017,
                        term      = "Spring",
                      ).save(force_insert = True)
###########
#DIVISIONS#
###########            
divisions = Divisions(  name      = "Division 1"
                      ).save()

divisions = Divisions(  name      = "Division 2"
                      ).save()
##########
#PROGRAMS#
##########
programs  = Programs(   name      = "Computer Science",
                        DID       = 2
                     ).save()
                     
programs  = Programs(   name      = "Biology",
                        DID       = 1
                    ).save()
#######
#USERS#
#######
users     = Users(      firstName = "Scott",
                        lastName  = "Heggen",
                        username  = "heggens",
                        email     = "heggens@berea.edu",
                        isAdmin     = True
                  ).save(force_insert=True)
            
users     = Users(      firstName  = "Jan",
                        lastName   = "Pearce",
                        username   = "pearcej",
                        email      = "pearcej@berea.edu",
                        DID        = 2
                  ).save(force_insert=True)
                        
users     = Users(      firstName = "Mario",
                        lastName  = "Nakazawa",
                        username  = "nakazawam",
                        PID       = 1,
                        email     = "nakazawam@berea.edu"
                  ).save(force_insert=True)
                  
users     = Users(      firstName = "Matt",
                        lastName  = "Jadud",
                        username  = "jadudm",
                        email     = "jadudm@berea.edu",
                  ).save(force_insert=True)  
#########                  
#COURSES#  
#########             
courses   = Courses(  prefix  = "BIO",
                      number  = "101",
                      section = "A1",
                      PID     = 2,
                      SEID    = 201612
                  ).save()
                  
courses   = Courses(  prefix  = "CSC",
                      number  = "415",
                      section = "SH",
                      PID     = 1,
                      SEID    = 201612
                  ).save()
##############
#USERSCOURSES#
##############
userscourses  = UsersCourses ( username = 'heggens',
                               CID      = 1
                              ).save()
                              
userscourses  = UsersCourses ( username = 'heggens',
                               CID      = 2
                              ).save()
##############################
#COURSE LIST UPLOAD TEST DATA#
##############################
# The course list upload maps each subject to a program through a course that
# already uses that subject. These programs, each with one placeholder course
# in Spring 2017, let Courses.for.BCSR.xlsx import on a fresh database.
# LES is left out on purpose, so its one row fails and the error display can
# still be seen.
testPrograms = {
  "AFR":  "African and African American Studies",
  "ANR":  "Agriculture and Natural Resources",
  "APS":  "Appalachian Studies",
  "ARH":  "Art History",
  "ART":  "Art",
  "AST":  "Asian Studies",
  "BUS":  "Business",
  "CFS":  "Child and Family Studies",
  "CHI":  "Chinese",
  "CHM":  "Chemistry",
  "CLS":  "Classics",
  "COM":  "Communication",
  "ECO":  "Economics",
  "EDS":  "Education Studies",
  "ENG":  "English",
  "ETAD": "Engineering Technologies and Applied Design",
  "FRN":  "French",
  "GEO":  "Geology",
  "GST":  "General Studies",
  "GSTR": "General Studies Seminars",
  "HHP":  "Health and Human Performance",
  "HIS":  "History",
  "HLT":  "Health",
  "JPN":  "Japanese",
  "L&I":  "Learning and Inquiry",
  "LAT":  "Latin",
  "MAT":  "Mathematics",
  "MUA":  "Applied Music",
  "MUS":  "Music",
  "NUR":  "Nursing",
  "PHI":  "Philosophy",
  "PHY":  "Physics",
  "PSC":  "Political Science",
  "PSJ":  "Peace and Social Justice Studies",
  "PSY":  "Psychology",
  "REL":  "Religion",
  "SENS": "Sustainability and Environmental Studies",
  "SOC":  "Sociology",
  "SPN":  "Spanish",
  "THR":  "Theatre",
  "WELL": "Wellness",
  "WGS":  "Women's and Gender Studies",
}
for prefix, name in testPrograms.items():
  program = Programs.create(name = name, DID = 1)
  Courses.create( prefix  = prefix,
                  number  = "000",
                  section = "A1",
                  PID     = program.PID,
                  SEID    = 201612
                )

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

fall_term = '201811'

#remove fall courses and instructors
fall_courses = Courses.select().where(Courses.SEID == fall_term)
for course in fall_courses:
  remove_course     = "DELETE FROM courses WHERE CID = {0};".format(course.CID)
  remove_instructor = "DELETE FROM userscourses WHERE CID_id = {0};".format(course.CID) 
  print 'Removing course: ({0}) from database'.format(course.CID)
  mainDB.execute_sql(remove_course)
  mainDB.execute_sql(remove_instructor)
  print 'Removing instructor & course pairing'

print '\nRemoving fall 2017 semester'
delete_query = "DELETE FROM semesters WHERE SEID = {};".format(fall_term)
mainDB.execute_sql(delete_query)
    
print '\nRemoving Summer 2018 Internships'
internships = {'495':63,'395':108}
'''the key is the course number, and the value is how rows there are in the database'''
for course_num in internships.keys():
  delete_query = "DELETE FROM courses WHERE number = {0} AND SEID_id = 201713;".format(course_num) 
  mainDB.execute_sql(delete_query)
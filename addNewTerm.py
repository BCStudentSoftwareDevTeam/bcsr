''' 
Author: Cody Myers Date: 20161206
File Purpose: 
The purpose of this file is to add courses to a new semester given a csv, while
also running debug checks to ensure that no problems occur.  

Instructions:
 - A portion of the data required for this script to run properly directly 
 depends on the format and content of the csv file. Therefore any data that is 
 dependent on csv is located in the Global Variables Section. The intent is to 
 have the server admin edit the global variables to the accomodate the csv and then
 the script should run prperly form there.

 - It is also currently the server admin's responsiblity to filter out all of the courses
 that do not have an instructor assigned to them. You can go ahead and add the course to 
 the database, but without an instructor the software will not hold anyone responsible for
 uploading that syllabi. Therefore, it may be best to seperate those courses into a serperate
 excel file and them to the registrar's office.    
'''
from app.models import *
import csv
import re
import sys
import os

##Global Variables##
csvFileName = 'terms_csv/201812.csv'
SEID        = 201812


#Create Index Map
'''TODO:
  - Record the csv column index for the table column names below
  - If the csv doesn't include some the data column then set the values to None'''
#Courses Table
CRN      = 2	#NOTE: start at zero 
prefix   = 3
number   = 4
section  = 5
#UsersCourses Table
'''There may be more than one instructor per course, the max instructors a course
can have is 3, but they rarely have more than 2. Therefore, we need get the index
for the potential teachers here. '''
firstName1 = 19
lastName1 = 18
username1  = 20
firstName2 = 22
lastName2 = 21
username2  = 23
firstName3 = 25
lastName3 = 24
username3  = 26

def createPrefixMapping():
  """ Creates a dictionary of all prefixes (e.g., CSC, TAD) """
  prefixDict = dict()
  pids = Programs.select(Programs.PID)
  for pid in pids:
    prefixs = Courses.select(Courses.prefix).distinct().where(Courses.PID == pid)
    for pre in prefixs:
      prefixDict[str(pre.prefix)] = pid.PID
  # print(prefixDict)
  return prefixDict

def addCourse(course,prefixDict):
    try:
      pid = prefixDict[course[prefix].strip()]  # Strip off white space because dirty data
      addCourse = Courses.create(prefix  = course[prefix],
                     number  = course[number],
                     section = course[section],
                     PID     = pid,
                     SEID    = SEID)
#      print ("added", course[CRN])
#      print (addCourse.prefix + " " + addCourse.number)
      return addCourse.CID
    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      print (e, 
            'CRN: {} '.format(course[CRN]),
	    'Course: {}'.format(course[prefix] + " " + course[number] + " - " + course[section]),
            "Line ({})".format(exc_tb.tb_lineno))
      return False
            
def findInstructors(course):
  ''' 
	Gets all of the instructors for a course, or creates them if they do not already exist
  '''
  instructors = []
  usernames=[username1,username2,username3]
  firstNames = [firstName1, firstName2, firstName3]
  lastNames = [lastName1, lastName2, lastName3]
  index = 0
  for username in usernames:
    if username != None:
      if course[username] != "":
        try:
          check = Users.get(Users.username == course[username])
        except Exception as e:
          check = Users.get_or_create(username=course[username], 
				      firstName = course[firstNames[index]], 
				      lastName = course[lastNames[index]], 
				      email = course[username] + "@berea.edu")	# Find the user in the db; all these fields are required
	  # print e
          # pass
        instructors.append(course[username])                  # Adds to instructor list
    index += 1  
  if instructors == []:
    return False
  else:
    return instructors

def addInstructor(instructor,cid):
  try:
    addInstr = UsersCourses.create(username=instructor,CID=cid)
    return addInstr.UCID
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print (e, 
           'CID: {} '.format(cid),
           'Username: {}'.format(instructor),
           "Line ({})".format(exc_tb.tb_lineno))
    print "TODO: Add relationship manually."
    return False
    
def main():
  try:
    # Make sure that the semester is in the database
    Semesters.get(Semesters.SEID == SEID)
    # Create a prefixDict so that we can map a course prefix to a program id
    prefixDict = createPrefixMapping()
    with open(csvFileName, 'rb') as csvfile: #Open CSV file
      courses = csv.reader(csvfile)
      next(courses) #Disregard the first line because it is the header
      print "Adding Courses & Instructors, this may take a moment."
      for course in courses:
        CID = addCourse(course,prefixDict)
        if CID:
          instructors = findInstructors(course)
          if instructors:
            for instructor in instructors:
              addInstructor(instructor,CID)
                
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    if "SemestersDoesNotExist" in str(exc_type):
      print "ERROR: Semester is not in database"
      print "TODO: Use BCSR database to add semester then run script again"
    else:
      print (e, "Line ({})".format(exc_tb.tb_lineno))

main()


# This script needs to get the data from the existing sqlite database and save it into mysql
from peewee import *
import mysql.connector
import app.models as old
import time
from datetime import datetime
import sys
import os
reload(sys)
sys.setdefaultencoding("utf-8")
from app.loadConfig import load_config

print("Hello")
dir_name  = os.path.dirname(__file__) # Return the directory name of pathname _file_
cfg       = load_config(os.path.join(dir_name, 'app/config.yaml')) #load config file
db_name   = cfg['db']['db_name']
print(db_name)
host      = cfg['db']['host']
username  = cfg['db']['username']
password  = cfg['db']['password']
# Create a connection to the mysql database
cnx = mysql.connector.connect(database=db_name, host = host, password = password, user = username)
print("Hello2")

# *******************************
# A cursor is a temporary work area created in the system memory when a SQL statement is executed.
# A cursor contains information in a mysql statement and the rows of data accessed by it.
# This temporary work area is used to store the data retrieved from the database, and manipulate this data.
# *******************************

cursor = cnx.cursor()
##############
add_semesters = ("INSERT INTO semesters (SEID, year, term) VALUES (%s, %s, %s)")

semesters = old.Semesters()
semesters = semesters.select()
for i in semesters:
    SEID = int(i.SEID)
    year = int(i.year)
    term = str(i.term)

    data_semesters = (SEID, year, term)

    cursor.execute(add_semesters, data_semesters)
##############
add_divisions = (" INSERT INTO divisions (DID, name) VALUES (%s, %s)")

divisions = old.Divisions()
divisions = divisions.select()
for i in divisions:
    DID = int(i.DID)
    name = str(i.name)

    data_divisions = (DID, name)

    cursor.execute(add_divisions, data_divisions)
#################
add_programs = ("INSERT INTO programs (PID, name, DID_id) VALUES (%s, %s, %s)")

programs = old.Programs()
programs = programs.select()
for i in programs:
    PID = int(i.PID)
    name = str(i.name) #Foerign key to User table, username
    DID = int(i.DID.DID)

    data_programs = (PID, name, DID)

    cursor.execute(add_programs, data_programs)
#################
add_users = ("INSERT INTO users (username, firstname, lastname, email, isAdmin, PID_id, DID_id) VALUES (%s, %s, %s, %s, %s, %s, %s)")
users = old.Users()
users = users.select()
for i in users:
    username = str(i.username)
    firstName = str(i.firstName)
    lastName = str(i.lastName)
    email = str(i.email)
    isAdmin = bool(i.isAdmin)
    PID = int(i.PID.PID) if i.PID else None
    DID = int(i.DID.DID) if i.DID else None

    data_users = (username, firstName, lastName, email, isAdmin, PID, DID)

    cursor.execute(add_users, data_users)
#################
add_courses = ("INSERT INTO courses (CID, prefix, number, section, PID_id, SEID_id, filePath, lastModified) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

courses = old.Courses()
courses = courses.select()
for i in courses:
    CID = int(i.CID)
    prefix = str(i.prefix)
    number = str(i.number)
    section = str(i.section)
    PID = int(i.PID.PID)
    SEID = int(i.SEID.SEID)
    filePath = str(i.filePath)
    lastModified = str(i.lastModified)

    data_courses = (CID, prefix, number, section, PID, SEID, filePath, lastModified)

    cursor.execute(add_courses, data_courses)
#################
add_userscourses = ("INSERT INTO userscourses (UCID, username_id, CID_id) VALUES (%s, %s, %s)")

userscourses = old.UsersCourses()
userscourses = userscourses.select()
for i in userscourses:
    UCID = int(i.UCID)
    username = str(i.username.username)
    CID = int(i.CID.CID)

    data_userscourses = (UCID, username, CID)

    cursor.execute(add_userscourses, data_userscourses)
#################
add_deadline = ("INSERT INTO deadline (description, date) VALUES (%s, %s)")

deadline = old.Deadline()
deadline = deadline.select()
for i in deadline:
    descriptiion = str(i.description)
    date = str(i.date)

    data_deadline = (description, date)

    cursor.execute(add_deadline, data_deadline)

cnx.commit()
cursor.close()
cnx.close()

print("Last")

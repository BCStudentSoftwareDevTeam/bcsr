# This script needs to get the data from the existing sqlite database and save it into mysql
from peewee import *
import mysql.connector
import app.models as old
import time
from datetime import datetime
import sys
import os
# reload(sys)
# sys.setdefaultencoding("utf-8")
from app.loadConfig import load_config

dir_name  = os.path.dirname(__file__) # Return the directory name of pathname _file_
cfg       = load_config('app/secret_config.yaml') #load config file
db_name   = cfg['db']['db_name']
host      = cfg['db']['host']
username  = cfg['db']['username']
password  = cfg['db']['password']
# Create a connection to the mysql database
cnx = mysql.connector.connect(database=db_name, host = host, password = password, user = username, auth_plugin='mysql_native_password')

# *******************************
# A cursor is a temporary work area created in the system memory when a SQL statement is executed.
# A cursor contains information in a mysql statement and the rows of data accessed by it.
# This temporary work area is used to store the data retrieved from the database, and manipulate this data.
# *******************************

cursor = cnx.cursor()
##############
add_semesters = ("INSERT INTO semesters (SEID, year, term) VALUES (%s, %s, %s)")
# x = old.Semesters.create(SEID = 201615, year = 2016, term = "Fake")
semesters = old.Semesters()
semesters = semesters.select()
for i in semesters:
    try:
        SEID = int(i.SEID)
        year = int(i.year)
        term = str(i.term)
        print (i)

        data_semesters = (SEID, year, term)
        print (data_semesters)

        cursor.execute(add_semesters, data_semesters)
    except Exception as e:
        print("Could not create semester: ", SEID, e)

##############
add_divisions = (" INSERT INTO divisions (DID, name) VALUES (%s, %s)")

divisions = old.Divisions()
divisions = divisions.select()
for i in divisions:
    try:
        DID = int(i.DID)
        name = str(i.name)

        data_divisions = (DID, name)

        cursor.execute(add_divisions, data_divisions)
    except Exception as e:
        print("Could not create Division: ", i.DID, e)
#################
add_programs = ("INSERT INTO programs (PID, name, DID_id) VALUES (%s, %s, %s)")

programs = old.Programs()
programs = programs.select()
for i in programs:
    try:
        PID = int(i.PID)
        name = str(i.name) #Foerign key to User table, username
        DID = int(i.DID.DID)

        data_programs = (PID, name, DID)

        cursor.execute(add_programs, data_programs)
    except Exception as e:
        print("Could not create Program: ", e)
#################
add_users = ("INSERT INTO users (username, firstname, lastname, email, isAdmin, PID_id, DID_id) VALUES (%s, %s, %s, %s, %s, %s, %s)")
users = old.Users()
users = users.select()
for i in users:
    try:
        username = str(i.username)
        firstName = str(i.firstName)
        lastName = str(i.lastName)
        email = str(i.email)
        isAdmin = bool(i.isAdmin)
        PID = int(i.PID.PID) if i.PID else None
        DID = int(i.DID.DID) if i.DID else None

        data_users = (username, firstName, lastName, email, isAdmin, PID, DID)

        cursor.execute(add_users, data_users)
    except Exception as e:
        print("Could not create user: ", e)
#################
add_courses = ("INSERT INTO courses (CID, prefix, number, section, PID_id, SEID_id, filePath, lastModified) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
# 11716,12072,12149,12234,12238,12241,12290,
# badcourses = [12352,12788,13282,13283,13284,13285,13286,13287,13288,13289,13290,13291,13292,13295,13296,13297,13298,13299,13300,13301,13302,13303,13304,13305,13306,13307,13308,13309,13310,13311,13312,13313,13314,13315,13316,13321,13322,13323,13324,13325,13326,13327,13328,13329,13330,13331,13332,13333,13334,13335,13336,13337,13338,13340,13341,13342,13343,13344,13345,13346,13347,13348,13349,13350,13351,13352,13353,13354,13355,13356,13357,13358,13359,13360,13361,13362,13363,13364,13365,13366,13367,13368,13369,13370,13371,13372,13373,13374,13375,13376,13380,13381,13382,13383,13384,13385,13386,13387,13388,13389,13390,13391,13392,13393,13394,13395,13396,13397,13398,13399,13400,13401,13402,13403,13404,13405,13406,13407,13408,13409,13412,13413,13414,13415,13416,13417,13418,13419,13420,13421,13422,13423,13424,13425,13426,13427,13428,13429]
# for c in badcourses:
#     print(c)
#     try:
#         x = old.Courses.create(CID= c, prefix = "CSC", number = "999", section="A", PID = 17, SEID = 201615)
#     except Exception as e:
#         print(e)
courses = old.Courses()
courses = courses.select()
for i in courses:
    try:
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
    except Exception as e:
        print("Could not create course: ", e)
#################
add_userscourses = ("INSERT INTO userscourses (UCID, username_id, CID_id) VALUES (%s, %s, %s)")

userscourses = old.UsersCourses()
userscourses = userscourses.select()
for i in userscourses:
    try:
        UCID = int(i.UCID)
        username = str(i.username.username)
        print(i.CID.CID)
        if i.CID:
            CID = int(i.CID.CID)
        else:
            continue

        data_userscourses = (UCID, username, CID)

        cursor.execute(add_userscourses, data_userscourses)
    except Exception as e:
        print("Could not add user to course: ", e)
#################
add_deadline = ("INSERT INTO deadline (description, date) VALUES (%s, %s)")

deadline = old.Deadline()
deadline = deadline.select()
for i in deadline:
    try:
        description = str(i.description)
        date = str(i.date)

        data_deadline = (description, date)

        cursor.execute(add_deadline, data_deadline)
    except Exception as e:
        print("Could not create deadline: ", e)

cnx.commit()
cursor.close()
cnx.close()

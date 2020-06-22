from app.loadConfig import *
from peewee import *

import os
import datetime
 ################################################################################################
 # This file is for migrating from SQLite to MySql. This is the file that creates the structure

def getDB():
    dir_name  = os.path.dirname(__file__) # Return the directory name of pathname _file_
    cfg       = load_config(os.path.join(dir_name, 'app/secret_config.yaml'))
    db_name   = cfg['db']['db_name']
    host      = cfg['db']['host']
    username  = cfg['db']['username']
    password  = cfg['db']['password']
    theDB     = MySQLDatabase ( db_name, host = host, user = username, passwd = password)

    return theDB


mainDB = getDB()


class baseModel(Model):
  class Meta:
    database = mainDB

# CLASSES WITH NO FOREIGN KEY FIELD
class Semesters (baseModel):
  SEID          = PrimaryKeyField()
  year          = IntegerField()
  term          = CharField()

  def __str__(self):
    return str(self.SEID)

class Divisions (baseModel):
  DID           = PrimaryKeyField()
  name          = CharField()
  def __str__(self):
    return str(self.DID)

  # CLASSES WITH FOREIGN KEY FIELDS
class Programs (baseModel):
  PID           = PrimaryKeyField()
  name          = CharField()
  DID           = ForeignKeyField(Divisions)

  def __str__(self):
    return str(self.PID)

class Users (baseModel):
  username      = CharField(primary_key=True)
  firstName     = CharField()
  lastName      = CharField()
  email         = CharField()
  isAdmin       = BooleanField(default = False)
  PID           = ForeignKeyField(Programs,  null = True)
  DID           = ForeignKeyField(Divisions, null = True)

  def __str__(self):
    return self.username

class Courses (baseModel):
  CID           = PrimaryKeyField()
  prefix        = CharField()
  number        = CharField()
  section       = CharField()
  PID           = ForeignKeyField(Programs)
  SEID          = ForeignKeyField(Semesters)
  filePath      = TextField(null = True)
  lastModified  = TextField(null = True)

  def __str__(self):
    return str(self.CID)

class UsersCourses (baseModel):
  UCID          = PrimaryKeyField()
  username      = ForeignKeyField(Users)
  CID           = ForeignKeyField(Courses)

class Deadline(baseModel):
  description  = TextField()
  date         = DateField()

# Enter all the tables here

mainDB.create_tables([Semesters, Divisions, Programs, Users, Courses, UsersCourses, Deadline])

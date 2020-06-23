from peewee import *
import os
from app.loadConfig import load_config


secret_cfg = load_config('app/secret_config.yaml')
mainDB = MySQLDatabase(secret_cfg['db']['db_name'],
                       host = secret_cfg['db']['host'],
                       user = secret_cfg['db']['username'],
                       passwd = secret_cfg['db']['password'])

# FOR USE IN MIGRATING FROM SQLITE TO SQL ONLY!
#mainDB = SqliteDatabase("data/bcsr.sqlite", pragmas = (('busy_timeout', 100), ('journal_mode', 'WAL')))

# Creates the class that will be used by Peewee to store the database
class dbModel (Model):
  class Meta:
    database = mainDB

'''
When adding a new table to the DB, add a new class here (also add
it to the config.yaml file)
Class Style Structure
--------------------------------------------------------------------------------
Data               | Style                       | Example
--------------------------------------------------------------------------------
Class Names        | CAP Case                     |  Ex. Semester
Primary Keys       | All Caps                     |  Ex. SEID
ForeignKeyField    | All Caps (Same as other key) |  Ex. Divisions.DID = Programs.DID
Variables in Class | Mixed Case                   |  Ex. filePath
--------------------------------------------------------------------------------
'''

# CLASSES WITH NO FOREIGN KEY FIELD
class Semesters (dbModel):
  SEID          = PrimaryKeyField()
  year          = IntegerField()
  term          = CharField()

  def __str__(self):
    return str(self.SEID)

class Divisions (dbModel):
  DID           = PrimaryKeyField()
  name          = CharField()
  def __str__(self):
    return str(self.DID)

# CLASSES WITH FOREIGN KEY FIELDS
class Programs (dbModel):
  PID           = PrimaryKeyField()
  name          = CharField()
  DID           = ForeignKeyField(Divisions)

  def __str__(self):
    return str(self.PID)

class Users (dbModel):
  username      = CharField(primary_key=True)
  firstName     = CharField()
  lastName      = CharField()
  email         = CharField()
  isAdmin       = BooleanField(default = False)
  PID           = ForeignKeyField(Programs,  null = True)   # indicates I'm a Program Chair
  DID           = ForeignKeyField(Divisions, null = True)   # indicates I'm a Division Chair

  def __str__(self):
    return self.username

class Courses (dbModel):
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

class UsersCourses (dbModel):
  UCID          = PrimaryKeyField()
  username      = ForeignKeyField(Users)
  CID           = ForeignKeyField(Courses)

class Deadline(dbModel):
  description  = TextField()
  date         = DateField()

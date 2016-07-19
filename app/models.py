from peewee import *
import os
from app.loadConfig import *

cfg       = load_config('app/config.yaml')
mainDB    = SqliteDatabase(cfg['databases']['dev'])

# Creates the class that will be used by Peewee to store the database
class dbModel (Model):
  class Meta: 
    database = mainDB
    
'''
When adding a new table to the DB, add a new class here (also add
it to the config.yaml file)
Class Style Structure
--------------------------------------------------------------------------------
Data Structure      | Style                       | Example      
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
 
class Divisions (dbModel):
  DID           = PrimaryKeyField()
  name          = CharField()
  
# CLASSES WITH FOREIGN KEY FIELDS 
class Programs (dbModel):
  PID           = PrimaryKeyField()
  name          = CharField()
  DID           = ForeignKeyField(Divisions)
  
class Users (dbModel):
  username      = CharField(primary_key=True)
  firstName     = CharField()
  lastName      = CharField()
  email         = CharField()
  isAdmin       = BooleanField(default = False)
  PID           = ForeignKeyField(Programs,  null = True)
  DID           = ForeignKeyField(Divisions, null = True)
  
class Courses (dbModel):
  CID           = PrimaryKeyField()
  prefix        = CharField()
  number        = CharField()
  section       = CharField()
  PID           = ForeignKeyField(Programs)
  SEID          = ForeignKeyField(Semesters)
  filePath      = TextField(null = True)
  lastModified  = TextField(null = True)
  
class UsersCourses (dbModel):
  UCID          = PrimaryKeyField()
  username      = ForeignKeyField(Users)
  CID           = ForeignKeyField(Courses)
from peewee import *
import os
#from allImports import *   #Don't believe this import is needed for this file
# Create a database
from app.loadConfig import *

cfg       = load_config('app/config.yaml')
mainDB    = SqliteDatabase(cfg['databases']['dev'])

# Creates the class that will be used by Peewee to store the database
class dbModel (Model):
  class Meta: 
    database = mainDB

# When adding new tables to the DB, add a new class here (also add 
# to the config.yaml file)

######## CLASSES WITH NO FOREIGN KEY FIELD ########
class Syllabus (dbModel):
  SID           = PrimaryKeyField()
  location      = CharField()
  
class Semester (dbModel):
  SEID          = PrimaryKeyField()
  year          = IntegerField()
  term          = CharField()

class Role (dbModel):
  RID           = PrimaryKeyField()
  access_level  = CharField()
  access_name   = CharField()
  
class Programs (dbModel):
  PID           = PrimaryKeyField()
  name          = CharField()
  
class Divisions (dbModel):
  DID           = PrimaryKeyField()
  name          = CharField()
  
class Users (dbModel):
  UID           = PrimaryKeyField()
  firstname     = CharField()
  lastname      = CharField()
  username      = CharField()
  email         = CharField()



######## CLASSES WITH FOREIGN KEY FIELDS ########
class Division_to_program (dbModel):
  DPID          = PrimaryKeyField()
  DID           = ForeignKeyField(Divisions)
  PID           = ForeignKeyField(Programs)
  
class Courses (dbModel):
  CID           = PrimaryKeyField()
  cprefix       = CharField()
  cnumber       = CharField()
  PID           = ForeignKeyField(Programs)  

class CurrentSEID (dbModel):
  CSEID         = PrimaryKeyField()
  SEID          = ForeignKeyField(Semester)
  
class Syllabus_course_semester (dbModel):
  XID           = PrimaryKeyField()
  SID           = ForeignKeyField(Syllabus)
  CID           = ForeignKeyField(Courses)
  SEID          = ForeignKeyField(Semester)
  
class Program_chair (dbModel):
  PCID          = PrimaryKeyField()
  PID           = ForeignKeyField(Programs)
  UID           = ForeignKeyField(Users)

class User_role (dbModel):
  URID          = PrimaryKeyField()
  RID           = ForeignKeyField(Role)
  UID           = ForeignKeyField(Users)
  
class Division_chair (dbModel):
  DCID          = PrimaryKeyField()
  DID           = ForeignKeyField(Divisions)
  UID           = ForeignKeyField(Users)
  
class Uscs (dbModel):
  QID           = PrimaryKeyField()
  XID           = ForeignKeyField(Syllabus_course_semester)
  UID           = ForeignKeyField(Users)
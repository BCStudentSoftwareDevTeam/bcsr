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
###########################CLASSES#############################
#Class Names        -> Camel Case                                         Ex. SyllCourseSemester
#Primary Keys       -> All Caps                                           Ex. SID
#ForeignKeyField    -> All Caps and Named After Key being related to      Ex. RID
#Variables in Class -> Mixed Case                                         Ex. firstName


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
  name          = CharField()
  
class Programs (dbModel):
  PID           = PrimaryKeyField()
  name          = CharField()
  
class Divisions (dbModel):
  DID           = PrimaryKeyField()
  name          = CharField()
  

######## CLASSES WITH FOREIGN KEY FIELDS ########
class Users (dbModel):
  UID           = PrimaryKeyField()
  firstName     = CharField()
  lastName      = CharField()
  userName      = CharField()
  email         = CharField()
  RID           = ForeignKeyField(Role)

class DivisionToProgram (dbModel):
  DPID          = PrimaryKeyField()
  DID           = ForeignKeyField(Divisions)
  PID           = ForeignKeyField(Programs)
  
class Courses (dbModel):
  CID           = PrimaryKeyField()
  prefix        = CharField()
  number        = CharField()
  section       = CharField()
  PID           = ForeignKeyField(Programs)  

class CurrentSemester (dbModel):
  CSEID         = PrimaryKeyField()
  SEID          = ForeignKeyField(Semester)
  
class SyllabusCourseSemester (dbModel):
  SCSID         = PrimaryKeyField()
  SID           = ForeignKeyField(Syllabus)
  CID           = ForeignKeyField(Courses)
  SEID          = ForeignKeyField(Semester)
  
class ProgramChair (dbModel):
  PCID          = PrimaryKeyField()
  PID           = ForeignKeyField(Programs)
  UID           = ForeignKeyField(Users)
  
class DivisionChair (dbModel):
  DCID          = PrimaryKeyField()
  DID           = ForeignKeyField(Divisions)
  UID           = ForeignKeyField(Users)
  
class UsersToSCS (dbModel): #SCS stands for SyllabusCourseSemester
  QID           = PrimaryKeyField()
  SCSID         = ForeignKeyField(SyllabusCourseSemester)
  UID           = ForeignKeyField(Users)